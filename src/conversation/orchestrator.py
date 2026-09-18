from __future__ import annotations

from src.conversation.memory import memory
from src.knowledge.retriever import KnowledgeRetriever
from src.llm.client import LLMClient
from src.models.schemas import ChatRequest, ChatResponse, StructuredSiteInput
from src.reasoning.clarifying import build_clarifying_questions, needs_more_info
from src.reasoning.multi_metric import assess_site, multi_metric_links, synthesize_reasoning
from src.reasoning.recommender import generate_recommendations


class BiodiversityOrchestrator:
    """End-to-end pipeline: memory → assess → retrieve → recommend → respond."""

    def __init__(self) -> None:
        self.retriever = KnowledgeRetriever()
        self.llm = LLMClient()

    def handle(self, request: ChatRequest) -> ChatResponse:
        session = memory.get_or_create(request.session_id)

        site = memory.merge_site(session, request.site)
        if request.geo:
            site = memory.merge_site(
                session,
                StructuredSiteInput(
                    latitude=request.geo.get("lat", request.geo.get("latitude")),
                    longitude=request.geo.get("lon", request.geo.get("longitude")),
                ),
            )
        if request.message:
            site = memory.extract_from_text(session, request.message)
            session.add_turn("user", request.message)

        assessments = assess_site(site)
        links = multi_metric_links(assessments, site)
        synthesis = synthesize_reasoning(assessments, links)
        clarifying = build_clarifying_questions(request.message, site, assessments)
        insufficient = needs_more_info(site, assessments)

        retrieved = self.retriever.retrieve(
            message=request.message,
            site=site,
            assessments=[a.model_dump() for a in assessments],
        )

        recommendations = []
        if not insufficient or len(assessments) >= 2:
            recommendations = generate_recommendations(site, assessments, retrieved)

        answer = self._format_answer(
            assessments=assessments,
            links=links,
            synthesis=synthesis,
            recommendations=recommendations,
            clarifying=clarifying,
            retrieved=retrieved,
            insufficient=insufficient,
        )

        response = ChatResponse(
            session_id=session.session_id,
            clarifying_questions=clarifying if insufficient else clarifying[:1],
            assessments=assessments,
            recommendations=recommendations,
            multi_metric_synthesis=synthesis,
            retrieved_knowledge=[
                {
                    "id": h["id"],
                    "title": h.get("title"),
                    "source": h.get("source"),
                    "citation": h.get("citation"),
                    "score": round(float(h.get("score", 0)), 3),
                    "domain": h.get("domain"),
                }
                for h in retrieved
            ],
            answer=answer,
            needs_more_info=insufficient and len(recommendations) == 0,
        )

        response.answer = self.llm.polish(response, request.message)
        session.add_turn("assistant", response.answer)
        return response

    def _format_answer(
        self,
        assessments,
        links,
        synthesis,
        recommendations,
        clarifying,
        retrieved,
        insufficient,
    ) -> str:
        lines: list[str] = []
        lines.append("## Biodiversity Intelligence Assessment")
        lines.append("")
        lines.append("### Multi-metric synthesis")
        lines.append(synthesis)
        lines.append("")

        if assessments:
            lines.append("### Metric status")
            for a in assessments:
                lines.append(f"- **{a.metric}**: {a.value} — {a.status} — {a.note}")
            lines.append("")

        if links:
            lines.append("### Cross-variable couplings")
            for link in links:
                lines.append(f"- {link}")
            lines.append("")

        if recommendations:
            lines.append("### Evidence-backed recommendations")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"**{i}. {rec.action}**")
                lines.append(f"- Why it works: {rec.scientific_reasoning}")
                lines.append(f"- Impacted metrics: {', '.join(rec.impacted_metrics)}")
                lines.append(f"- Expected impact: {rec.expected_impact}")
                lines.append(f"- Time horizon: {rec.time_horizon.value}")
                lines.append(f"- Confidence: {rec.confidence:.2f}")
                if rec.linked_variables:
                    lines.append(f"- Linked variables: {'; '.join(rec.linked_variables)}")
                for ev in rec.evidence:
                    cite = f"{ev.source}: {ev.citation}"
                    if ev.year:
                        cite += f" ({ev.year})"
                    if ev.url:
                        cite += f" — {ev.url}"
                    lines.append(f"- Evidence: {cite}")
                lines.append("")
        elif insufficient:
            lines.append("### Need a bit more context")
            lines.append(
                "I can reason across soil × water × land-use, but key inputs are incomplete."
            )
            lines.append("")

        if clarifying and (insufficient or not recommendations):
            lines.append("### Clarifying questions")
            for q in clarifying:
                lines.append(f"- {q}")
            lines.append("")

        if retrieved:
            lines.append("### Knowledge retrieved (RAG)")
            for h in retrieved[:5]:
                lines.append(
                    f"- [{h.get('domain')}] {h.get('title')} "
                    f"(score={float(h.get('score', 0)):.2f}, source={h.get('source')})"
                )

        return "\n".join(lines)
