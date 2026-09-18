from src.models.schemas import StructuredSiteInput
from src.reasoning.clarifying import build_clarifying_questions, missing_critical
from src.reasoning.multi_metric import assess_site, multi_metric_links
from src.reasoning.recommender import generate_recommendations


def test_example_use_case_multi_metric():
    site = StructuredSiteInput(
        soil_organic_carbon_pct=0.3,
        rainfall="low",
        land_use="monoculture",
        crop="wheat",
        region="semi-arid",
    )
    assessments = assess_site(site)
    assert len(assessments) >= 3
    links = multi_metric_links(assessments, site)
    assert len(links) >= 2
    recs = generate_recommendations(site, assessments, retrieved=[])
    assert len(recs) >= 2
    actions = " ".join(r.action.lower() for r in recs)
    assert "agroforestry" in actions or "intercrop" in actions
    assert all(r.evidence for r in recs)
    assert all(r.impacted_metrics for r in recs)
    assert all(r.scientific_reasoning for r in recs)


def test_clarifying_questions_on_incomplete_input():
    qs = build_clarifying_questions(
        "Biodiversity is declining on my land",
        None,
        [],
    )
    assert any("soil organic carbon" in q.lower() for q in qs)
    assert missing_critical(None) == [
        "soil organic carbon %",
        "rainfall pattern (low / moderate / high / erratic)",
        "land use type (e.g., monoculture, mixed cropping, agroforestry)",
    ]


def test_recommendation_has_time_horizon_and_confidence():
    site = StructuredSiteInput(
        soil_organic_carbon_pct=0.4,
        rainfall="low",
        land_use="monoculture",
        region="semi-arid",
    )
    assessments = assess_site(site)
    recs = generate_recommendations(site, assessments, [])
    assert recs
    assert 0 < recs[0].confidence <= 1
    assert recs[0].time_horizon.value in {"short_term", "medium_term", "long_term"}
