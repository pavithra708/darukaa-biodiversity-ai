"""Intervention playbook: actionable, evidence-linked recommendations."""

DOCUMENTS = [
    {
        "id": "intervention_legume_cover",
        "domain": "intervention",
        "title": "Introduce legume-based cover crops",
        "content": (
            "ACTION: Plant legume cover crops (cowpea, clover, sunn hemp, or locally "
            "adapted species) in fallows or as inter-row cover. WHY: Biological N "
            "fixation and root carbon inputs raise SOC ~15–25% over 2–3 years (FAO), "
            "boost microbial diversity, and provide pollinator forage if allowed to "
            "flower. METRICS: SOC, microbial diversity, pollinator support, nitrogen. "
            "BEST WHEN: SOC < 1.0%, monoculture systems, moderate-to-low rainfall with "
            "moisture conservation."
        ),
        "metrics": ["soil_organic_carbon", "microbial_diversity", "pollinator_support"],
        "source": "FAO",
        "citation": "FAO cover crop and soil organic matter practice evidence",
        "year": 2019,
        "url": "https://www.fao.org/",
        "time_horizon": "medium_term",
        "triggers": ["low_soc", "monoculture", "low_biodiversity"],
    },
    {
        "id": "intervention_agroforestry",
        "domain": "intervention",
        "title": "Establish drought-tolerant agroforestry / intercropping",
        "content": (
            "ACTION: Integrate spaced native or proven nitrogen-fixing trees with "
            "intercrops (legume–cereal mixtures) rather than continuous wheat monoculture. "
            "WHY: Multi-strata systems buffer temperature, raise SOC, reduce wind "
            "erosion, and create habitat niches—linking climate, soil, and biodiversity. "
            "Dryland FAO programs document woody cover and avian richness gains over "
            "3–7 years. METRICS: SOC, habitat diversity, microclimate, species richness. "
            "BEST WHEN: semi-arid, low rainfall, monoculture, SOC critically low."
        ),
        "metrics": ["soil_organic_carbon", "habitat_diversity", "species_richness", "microclimate"],
        "source": "FAO",
        "citation": "FAO dryland agroforestry / climate-smart agriculture guidance",
        "year": 2020,
        "url": "https://www.fao.org/",
        "time_horizon": "long_term",
        "triggers": ["semiarid", "low_rainfall", "monoculture", "low_soc"],
    },
    {
        "id": "intervention_water_harvesting",
        "domain": "intervention",
        "title": "Micro-catchments and mulched water harvesting",
        "content": (
            "ACTION: Install contour bunds, zai pits, or micro-catchments; apply organic "
            "mulch to reduce evaporation. WHY: Water availability gates species survival "
            "and SOC sequestration—organic amendments fail without moisture. ICRISAT/"
            "CGIAR dryland trials show infiltration and biomass gains within 1–2 seasons. "
            "METRICS: soil_moisture, water_availability, plant_cover, SOC trajectory. "
            "BEST WHEN: low/erratic rainfall, dry soil moisture, semi-arid regions."
        ),
        "metrics": ["soil_moisture", "water_availability", "soil_organic_carbon"],
        "source": "CGIAR/ICRISAT",
        "citation": "ICRISAT water harvesting and dryland productivity studies",
        "year": 2020,
        "url": "https://www.icrisat.org/",
        "time_horizon": "short_term",
        "triggers": ["low_rainfall", "dry_moisture", "semiarid"],
    },
    {
        "id": "intervention_habitat_margins",
        "domain": "intervention",
        "title": "Native field margins and pollinator strips",
        "content": (
            "ACTION: Convert 5–10% of field edges to native flowering strips and "
            "undisturbed nesting habitat. WHY: Habitat diversity—not fertilizer—drives "
            "pollinator and natural-enemy recovery (IPBES/FAO). Short-term insect "
            "response often appears within one flowering season; bird benefits grow "
            "over 2–4 years. METRICS: habitat_diversity, pollinator_abundance, "
            "species_richness. BEST WHEN: monoculture, low habitat diversity, "
            "biodiversity decline reports."
        ),
        "metrics": ["habitat_diversity", "pollinator_abundance", "species_richness"],
        "source": "IPBES / FAO",
        "citation": "IPBES Global Assessment; FAO Pollinators Initiative",
        "year": 2019,
        "url": "https://ipbes.net/",
        "time_horizon": "short_term",
        "triggers": ["monoculture", "low_habitat", "biodiversity_decline"],
    },
    {
        "id": "intervention_reduce_agrochemicals",
        "domain": "intervention",
        "title": "IPM and nutrient-precision pollution control",
        "content": (
            "ACTION: Shift to integrated pest management, threshold-based spraying, and "
            "precision nitrogen; add vegetative filter strips near water. WHY: Toxicity "
            "can negate habitat restoration; UNEP/IPBES link pesticide load to insect "
            "biomass collapse. METRICS: pollution, insect_biomass, water_quality. "
            "BEST WHEN: high pollution, intensive monoculture."
        ),
        "metrics": ["pollution", "insect_biomass", "water_quality"],
        "source": "UNEP",
        "citation": "UNEP pollution assessments; IPBES pesticide-related evidence",
        "year": 2019,
        "url": "https://www.unep.org/",
        "time_horizon": "medium_term",
        "triggers": ["high_pollution", "monoculture"],
    },
    {
        "id": "intervention_ph_correction",
        "domain": "intervention",
        "title": "Correct soil pH before biodiversity planting",
        "content": (
            "ACTION: Apply lime (acidic soils) or organic sulfur/acidifying organics "
            "(alkaline) based on soil test; combine with organic matter. WHY: Microbial "
            "and earthworm recovery stalls outside pH ~6.0–7.5 (USDA NRCS). pH "
            "correction unlocks nutrient cycling that SOC-building practices need. "
            "METRICS: soil_ph, nutrient_availability, microbial_diversity. "
            "BEST WHEN: pH < 5.5 or pH > 8.0."
        ),
        "metrics": ["soil_ph", "microbial_diversity", "nutrient_availability"],
        "source": "USDA NRCS",
        "citation": "USDA NRCS soil pH and biological activity guidance",
        "year": 2018,
        "url": "https://www.nrcs.usda.gov/",
        "time_horizon": "short_term",
        "triggers": ["ph_extreme"],
    },
]
