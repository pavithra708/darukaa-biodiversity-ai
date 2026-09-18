from __future__ import annotations

from src.models.schemas import MetricAssessment, StructuredSiteInput


CRITICAL_FIELDS = [
    ("soil_organic_carbon_pct", "soil organic carbon %"),
    ("rainfall", "rainfall pattern (low / moderate / high / erratic)"),
    ("land_use", "land use type (e.g., monoculture, mixed cropping, agroforestry)"),
]

USEFUL_FIELDS = [
    ("soil_ph", "soil pH"),
    ("soil_moisture", "soil moisture (dry / moderate / wet)"),
    ("crop", "main crop or vegetation"),
    ("region", "region / climate zone (e.g., semi-arid)"),
    ("habitat_diversity_index", "habitat diversity index (0–1)"),
    ("pollution_level", "pollution level (low / moderate / high)"),
]


def missing_critical(site: StructuredSiteInput | None) -> list[str]:
    if site is None:
        return [label for _, label in CRITICAL_FIELDS]
    missing = []
    data = site.model_dump()
    for field, label in CRITICAL_FIELDS:
        if data.get(field) in (None, "", "unknown"):
            missing.append(label)
    return missing


def build_clarifying_questions(
    message: str | None,
    site: StructuredSiteInput | None,
    assessments: list[MetricAssessment],
) -> list[str]:
    questions: list[str] = []
    for label in missing_critical(site):
        questions.append(f"Can you provide {label}?")

    data = site.model_dump() if site else {}
    # Ask useful follow-ups if critical mostly present
    if len(questions) <= 1:
        for field, label in USEFUL_FIELDS:
            if data.get(field) in (None, "", "unknown"):
                questions.append(f"Do you have data on {label}?")
            if len(questions) >= 3:
                break

    text = (message or "").lower()
    if "biodiversity" in text and "declin" in text and not questions:
        questions.append(
            "Can you provide soil organic carbon %, rainfall pattern, and land use type?"
        )

    # Geo bonus prompt
    if site and site.latitude is None and site.longitude is None:
        if len(questions) < 3:
            questions.append(
                "Optional: can you share latitude/longitude for spatial climate context?"
            )

    return questions[:4]


def needs_more_info(site: StructuredSiteInput | None, assessments: list[MetricAssessment]) -> bool:
    """True when fewer than 3 environmental variables are available for multi-metric reasoning."""
    if len(assessments) >= 3:
        return False
    return len(missing_critical(site)) > 0
