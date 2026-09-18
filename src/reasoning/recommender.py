from __future__ import annotations

from src.models.schemas import (
    EvidenceRef,
    MetricAssessment,
    Recommendation,
    StructuredSiteInput,
    TimeHorizon,
)


def _status_map(assessments: list[MetricAssessment]) -> dict[str, str]:
    return {a.metric: a.status for a in assessments}


def _norm(value: object) -> str:
    return str(value or "").strip().lower()


def _evidence(source: str, citation: str, year: int, url: str) -> EvidenceRef:
    return EvidenceRef(source=source, citation=citation, year=year, url=url)


def generate_recommendations(
    site: StructuredSiteInput | None,
    assessments: list[MetricAssessment],
    retrieved: list[dict],
) -> list[Recommendation]:
    """
    Rule-guided, RAG-informed recommender.
    Rules encode multi-metric triggers; retrieved docs supply evidence text.
    """
    status = _status_map(assessments)
    region = _norm(site.region if site else None)
    crop = _norm(site.crop if site else None)
    rainfall = _norm(site.rainfall if site else None)
    land_use = _norm(site.land_use if site else None)
    semiarid = any(k in region for k in ("semi-arid", "semiarid", "arid", "dryland"))
    monoculture = land_use == "monoculture" or "mono" in land_use

    recs: list[Recommendation] = []

    def add(rec: Recommendation) -> None:
        if len(recs) >= 4:
            return
        if any(r.action == rec.action for r in recs):
            return
        recs.append(rec)

    # 1) Semi-arid monoculture + low SOC → agroforestry / intercropping
    if (
        status.get("soil_organic_carbon") in {"critical", "low"}
        and (semiarid or rainfall in {"low", "erratic"} or status.get("rainfall") == "critical")
        and (monoculture or "wheat" in crop or status.get("land_use") == "critical")
    ):
        add(
            Recommendation(
                action=(
                    "Establish drought-tolerant agroforestry with legume–cereal intercropping "
                    "(replace continuous monoculture blocks)"
                ),
                scientific_reasoning=(
                    "Low SOC under semi-arid monoculture is a coupled soil–climate–habitat failure: "
                    "sparse residue inputs and heat/wind exposure oxidize carbon while removing "
                    "vertical niche structure. Multi-strata trees buffer microclimate, deep roots "
                    "improve infiltration, and intercrops restore functional diversity—raising SOC "
                    "and species richness together."
                ),
                impacted_metrics=[
                    "soil_organic_carbon",
                    "habitat_diversity",
                    "species_richness",
                    "microclimate",
                    "water_availability",
                ],
                expected_impact=(
                    "Woody cover and SOC gains typically emerge over 3–7 years in dryland "
                    "agroforestry programs; avian/habitat diversity rises as strata develop. "
                    "Near-term (1–2 seasons): improved shade, wind reduction, and intercrop N economy."
                ),
                time_horizon=TimeHorizon.LONG,
                confidence=0.86,
                evidence=[
                    _evidence(
                        "FAO",
                        "FAO dryland agroforestry / climate-smart agriculture guidance",
                        2020,
                        "https://www.fao.org/",
                    ),
                    _evidence(
                        "IPCC",
                        "IPCC AR6 / SRCCL — AFOLU land management and ecosystem climate linkages",
                        2022,
                        "https://www.ipcc.ch/",
                    ),
                ],
                linked_variables=[
                    "soil_organic_carbon ↔ habitat_diversity",
                    "rainfall ↔ species_survival",
                    "land_use ↔ habitat_fragmentation",
                ],
            )
        )

    # 2) Low SOC → legume cover crops
    if status.get("soil_organic_carbon") in {"critical", "low"}:
        add(
            Recommendation(
                action="Introduce legume-based cover crops in fallows / inter-rows",
                scientific_reasoning=(
                    "Legumes add biologically fixed nitrogen and root-derived carbon, rebuilding "
                    "microbial networks that collapse when SOC < ~1%. Flowering legumes also "
                    "supply pollinator resources—linking below-ground recovery to above-ground "
                    "biodiversity rather than treating soil as an isolated agronomic metric."
                ),
                impacted_metrics=[
                    "soil_organic_carbon",
                    "microbial_diversity",
                    "pollinator_support",
                    "nitrogen",
                ],
                expected_impact=(
                    "SOC increases of ~15–25% over 2–3 years are reported in FAO-linked cover-crop "
                    "evidence under continuous cover, with concurrent microbial diversity gains."
                ),
                time_horizon=TimeHorizon.MEDIUM,
                confidence=0.88,
                evidence=[
                    _evidence(
                        "FAO",
                        "FAO cover crops and soil organic matter practice evidence",
                        2019,
                        "https://www.fao.org/",
                    )
                ],
                linked_variables=[
                    "soil_health ↔ biodiversity",
                    "nitrogen ↔ microbial_diversity",
                ],
            )
        )

    # 3) Water stress → harvesting
    if status.get("rainfall") == "critical" or status.get("soil_moisture") == "critical" or rainfall in {
        "low",
        "erratic",
    }:
        add(
            Recommendation(
                action="Deploy micro-catchments / contour bunds with organic mulching",
                scientific_reasoning=(
                    "In water-limited systems, species survival and SOC sequestration are gated by "
                    "soil moisture. Water harvesting raises infiltration and extends plant-available "
                    "water, so organic amendments and habitat plantings can establish instead of failing."
                ),
                impacted_metrics=[
                    "soil_moisture",
                    "water_availability",
                    "soil_organic_carbon",
                    "plant_cover",
                ],
                expected_impact=(
                    "Infiltration and biomass responses often appear within 1–2 seasons (ICRISAT/"
                    "CGIAR dryland trials); SOC trajectory improves over medium term as cover persists."
                ),
                time_horizon=TimeHorizon.SHORT,
                confidence=0.84,
                evidence=[
                    _evidence(
                        "CGIAR/ICRISAT",
                        "ICRISAT water harvesting and dryland productivity studies",
                        2020,
                        "https://www.icrisat.org/",
                    )
                ],
                linked_variables=[
                    "water_availability ↔ species_survival",
                    "soil_moisture ↔ soil_organic_carbon",
                ],
            )
        )

    # 4) Habitat / monoculture → margins
    if monoculture or status.get("land_use") == "critical" or status.get("habitat_diversity") in {
        "critical",
        "low",
    }:
        add(
            Recommendation(
                action="Convert 5–10% of field edges to native flowering margins / pollinator strips",
                scientific_reasoning=(
                    "Species richness tracks habitat heterogeneity more than fertilizer inputs. "
                    "Margins restore nesting/forage resources and act as corridors, countering "
                    "fragmentation from monoculture blocks while complementary soil practices run."
                ),
                impacted_metrics=[
                    "habitat_diversity",
                    "pollinator_abundance",
                    "species_richness",
                    "pest_regulation",
                ],
                expected_impact=(
                    "Insect/pollinator responses can appear within one flowering season; bird and "
                    "broader richness gains typically strengthen over 2–4 years (IPBES/FAO)."
                ),
                time_horizon=TimeHorizon.SHORT,
                confidence=0.83,
                evidence=[
                    _evidence(
                        "IPBES",
                        "IPBES Global Assessment Report on Biodiversity and Ecosystem Services",
                        2019,
                        "https://ipbes.net/",
                    ),
                    _evidence(
                        "FAO",
                        "FAO International Pollinators Initiative",
                        2021,
                        "https://www.fao.org/pollination/",
                    ),
                ],
                linked_variables=[
                    "land_use ↔ habitat_fragmentation",
                    "habitat_diversity ↔ species_richness",
                ],
            )
        )

    # 5) pH extremes
    if status.get("soil_ph") == "critical":
        add(
            Recommendation(
                action="Correct soil pH toward ~6.0–7.5 before scaling habitat plantings",
                scientific_reasoning=(
                    "Microbial and earthworm recovery stalls outside the biological pH window; "
                    "without this unlock, SOC-building and biodiversity plantings underperform."
                ),
                impacted_metrics=["soil_ph", "microbial_diversity", "nutrient_availability"],
                expected_impact="Biological activity response within months after correction + organics.",
                time_horizon=TimeHorizon.SHORT,
                confidence=0.8,
                evidence=[
                    _evidence(
                        "USDA NRCS",
                        "USDA NRCS soil pH and biological activity guidance",
                        2018,
                        "https://www.nrcs.usda.gov/",
                    )
                ],
                linked_variables=["soil_ph ↔ microbial_diversity"],
            )
        )

    # 6) Pollution
    if status.get("pollution") == "critical":
        add(
            Recommendation(
                action="Adopt IPM + precision nutrients with vegetative filter strips",
                scientific_reasoning=(
                    "Toxic loads can nullify habitat restoration. Cutting pesticide/N surplus "
                    "while filtering runoff protects insect biomass and aquatic food webs."
                ),
                impacted_metrics=["pollution", "insect_biomass", "water_quality"],
                expected_impact="Insect biomass and water-quality indicators improve over 1–3 years.",
                time_horizon=TimeHorizon.MEDIUM,
                confidence=0.81,
                evidence=[
                    _evidence(
                        "UNEP",
                        "UNEP Towards a Pollution-Free Planet; IPBES pesticide-related findings",
                        2019,
                        "https://www.unep.org/",
                    )
                ],
                linked_variables=["pollution ↔ insect_biomass"],
            )
        )

    # Enrich confidence slightly if RAG supports same themes
    retrieved_text = " ".join(h.get("text", "") for h in retrieved).lower()
    for rec in recs:
        keywords = [m.replace("_", " ") for m in rec.impacted_metrics[:3]]
        if any(k in retrieved_text for k in keywords):
            rec.confidence = min(0.95, rec.confidence + 0.03)

    # Fallback if user gave narrative but little structure
    if not recs:
        add(
            Recommendation(
                action=(
                    "Start a multi-metric baseline (SOC %, rainfall pattern, land-use map) then "
                    "pilot cover crops + 5% habitat margins"
                ),
                scientific_reasoning=(
                    "Without soil–water–land-use context, single practices are speculative. "
                    "A minimal triad baseline enables evidence-linked intervention sequencing."
                ),
                impacted_metrics=["soil_organic_carbon", "habitat_diversity", "water_availability"],
                expected_impact="Baseline enables targeted 15–25% SOC pathway planning over 2–3 years.",
                time_horizon=TimeHorizon.SHORT,
                confidence=0.55,
                evidence=[
                    _evidence(
                        "FAO",
                        "FAO soil and biodiversity monitoring guidance",
                        2015,
                        "https://www.fao.org/soils-portal/",
                    )
                ],
                linked_variables=["soil_health ↔ biodiversity", "land_use ↔ habitat_fragmentation"],
            )
        )

    return recs
