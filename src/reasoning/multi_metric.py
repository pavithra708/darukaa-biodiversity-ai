from __future__ import annotations

from typing import Any

from src.models.schemas import MetricAssessment, StructuredSiteInput


def _norm_str(value: Any) -> str:
    return str(value or "").strip().lower()


def assess_site(site: StructuredSiteInput | None) -> list[MetricAssessment]:
    """Score individual environmental metrics from structured (or partial) input."""
    if site is None:
        return []

    assessments: list[MetricAssessment] = []
    soc = site.soil_organic_carbon_pct
    if soc is not None:
        if soc < 0.5:
            status, note = "critical", "SOC critically low; soil biology and structure likely collapsed."
        elif soc < 1.0:
            status, note = "low", "SOC below healthy cultivated range; limited microbial habitat."
        elif soc < 2.0:
            status, note = "moderate", "SOC improving but still room for biodiversity co-benefits."
        else:
            status, note = "good", "SOC supports stronger below-ground biodiversity."
        assessments.append(
            MetricAssessment(metric="soil_organic_carbon", value=soc, status=status, note=note)
        )

    if site.soil_ph is not None:
        ph = site.soil_ph
        if ph < 5.5 or ph > 8.0:
            status, note = "critical", "pH outside biological window; microbial recovery blocked."
        elif ph < 6.0 or ph > 7.5:
            status, note = "low", "pH suboptimal for many soil biota and nutrient cycles."
        else:
            status, note = "good", "pH near optimal for soil biota."
        assessments.append(
            MetricAssessment(metric="soil_ph", value=ph, status=status, note=note)
        )

    moisture = _norm_str(site.soil_moisture)
    if moisture:
        if moisture in {"dry", "arid", "low"}:
            status, note = "critical", "Low moisture limits fauna survival and SOC sequestration."
        elif moisture in {"moderate", "medium"}:
            status, note = "moderate", "Moisture adequate but sensitive to dry spells."
        elif moisture in {"wet", "high"}:
            status, note = "good", "Moisture supports biological activity if drainage is ok."
        else:
            status, note = "unknown", "Moisture reported but not classified."
        assessments.append(
            MetricAssessment(metric="soil_moisture", value=moisture, status=status, note=note)
        )

    rainfall = _norm_str(site.rainfall)
    if rainfall:
        if rainfall in {"low", "erratic"}:
            status, note = "critical", "Water stress elevates species mortality risk."
        elif rainfall == "moderate":
            status, note = "moderate", "Rainfall usable with conservation practices."
        elif rainfall == "high":
            status, note = "good", "Rainfall supports vegetation if erosion is controlled."
        else:
            status, note = "unknown", "Rainfall pattern unclear."
        assessments.append(
            MetricAssessment(metric="rainfall", value=rainfall, status=status, note=note)
        )

    land_use = _norm_str(site.land_use)
    if land_use:
        if land_use in {"monoculture", "degraded"}:
            status, note = "critical", "Simplified land use drives habitat homogenization."
        elif land_use in {"mixed_cropping", "pasture", "urban_edge"}:
            status, note = "moderate", "Some structure present; connectivity likely limited."
        elif land_use in {"agroforestry", "forest", "wetland"}:
            status, note = "good", "Land use supports higher habitat complexity."
        else:
            status, note = "unknown", "Land use needs clarification."
        assessments.append(
            MetricAssessment(metric="land_use", value=land_use, status=status, note=note)
        )

    if site.habitat_diversity_index is not None:
        h = site.habitat_diversity_index
        if h < 0.3:
            status, note = "critical", "Habitat diversity too low for resilient species assemblages."
        elif h < 0.5:
            status, note = "low", "Limited niche diversity."
        elif h < 0.7:
            status, note = "moderate", "Habitat structure improving."
        else:
            status, note = "good", "Strong habitat heterogeneity."
        assessments.append(
            MetricAssessment(
                metric="habitat_diversity", value=h, status=status, note=note
            )
        )

    if site.species_richness is not None:
        # Relative heuristic without regional baseline: treat very low counts as warning
        s = site.species_richness
        if s < 10:
            status, note = "low", "Species richness appears constrained for the site class."
        elif s < 30:
            status, note = "moderate", "Moderate richness; gains possible via habitat complexity."
        else:
            status, note = "good", "Relatively high observed richness."
        assessments.append(
            MetricAssessment(
                metric="species_richness", value=s, status=status, note=note
            )
        )

    pollution = _norm_str(site.pollution_level)
    if pollution:
        if pollution in {"high", "severe"}:
            status, note = "critical", "Pollution may override habitat gains."
        elif pollution in {"moderate", "medium"}:
            status, note = "low", "Pollution stress present."
        else:
            status, note = "good", "Pollution pressure appears limited."
        assessments.append(
            MetricAssessment(metric="pollution", value=pollution, status=status, note=note)
        )

    deforestation = _norm_str(site.deforestation_pressure)
    if deforestation:
        if deforestation in {"high", "severe", "active"}:
            status, note = "critical", "Deforestation fragments habitat and oxidizes SOC."
        elif deforestation in {"moderate", "medium"}:
            status, note = "low", "Clearing pressure threatens connectivity."
        else:
            status, note = "good", "Deforestation pressure limited."
        assessments.append(
            MetricAssessment(
                metric="deforestation", value=deforestation, status=status, note=note
            )
        )

    region = _norm_str(site.region)
    if region and any(k in region for k in ("semi-arid", "semiarid", "arid", "dryland")):
        assessments.append(
            MetricAssessment(
                metric="climate_context",
                value=site.region,
                status="low",
                note="Semi-arid/dryland context amplifies water–biodiversity coupling.",
            )
        )

    return assessments


def multi_metric_links(assessments: list[MetricAssessment], site: StructuredSiteInput | None) -> list[str]:
    """Explicit cross-variable couplings — core evaluation differentiator."""
    status = {a.metric: a.status for a in assessments}
    links: list[str] = []

    if status.get("soil_organic_carbon") in {"critical", "low"} and status.get("land_use") == "critical":
        links.append(
            "soil_organic_carbon ↔ land_use: monoculture residue removal and tillage keep SOC suppressed, "
            "starving microbial and invertebrate food webs."
        )
    if status.get("rainfall") in {"critical", "low"} and status.get("soil_organic_carbon") in {"critical", "low"}:
        links.append(
            "water_availability ↔ soil_carbon: low rainfall limits biomass inputs and slows SOC accrual; "
            "moisture conservation must accompany organic amendments."
        )
    if status.get("rainfall") in {"critical", "low"} or status.get("soil_moisture") == "critical":
        links.append(
            "water_availability ↔ species_survival: drought stress shortens flowering windows and "
            "collapses soil fauna activity."
        )
    if status.get("land_use") == "critical":
        links.append(
            "land_use ↔ habitat_fragmentation: continuous monoculture reduces edge habitats and "
            "connectivity, lowering species persistence."
        )
    if status.get("soil_organic_carbon") in {"critical", "low"}:
        links.append(
            "soil_health ↔ biodiversity: low SOC reduces microbial diversity and plant disease "
            "suppression, weakening above-ground community resilience."
        )
    if status.get("pollution") == "critical":
        links.append(
            "pollution ↔ insect_biomass: chemical stress can erase gains from habitat strips unless "
            "toxicity load is reduced in parallel."
        )
    if status.get("deforestation") in {"critical", "low"}:
        links.append(
            "deforestation ↔ microclimate ↔ SOC: canopy loss raises temperature extremes and "
            "accelerates carbon oxidation while fragmenting habitat."
        )
    if status.get("soil_ph") == "critical":
        links.append(
            "soil_ph ↔ microbial_diversity: extreme pH blocks nutrient cycling required for "
            "cover-crop and habitat restoration success."
        )

    # Crop-specific coupling
    crop = _norm_str(site.crop if site else None)
    if "wheat" in crop and status.get("land_use") in {"critical", "low", None}:
        links.append(
            "cropping_system ↔ biodiversity: wheat monoculture simplifies canopy architecture "
            "and typically increases agrochemical dependence."
        )

    # Ensure at least a generic triad when enough signals exist
    if len(assessments) >= 3 and len(links) < 2:
        links.append(
            "integrated_system: soil × water × land-use jointly determine habitat quality; "
            "single-variable fixes underperform."
        )
    return links


def synthesize_reasoning(assessments: list[MetricAssessment], links: list[str]) -> str:
    if not assessments and not links:
        return (
            "Insufficient multi-metric context. Collect soil organic carbon, rainfall pattern, "
            "and land-use type to enable cross-variable ecological reasoning."
        )
    degraded = [a for a in assessments if a.status in {"critical", "low"}]
    parts = []
    if degraded:
        parts.append(
            "Priority degradation signals: "
            + "; ".join(f"{a.metric}={a.value} ({a.status})" for a in degraded[:5])
            + "."
        )
    if links:
        parts.append("Cross-metric couplings: " + " ".join(links[:4]))
    parts.append(
        "Recommendations therefore jointly target soil recovery, water retention, and habitat "
        "structure rather than a single practice slogan."
    )
    return " ".join(parts)
