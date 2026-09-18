"""Human impact knowledge chunks."""

DOCUMENTS = [
    {
        "id": "deforestation_cascade",
        "domain": "human_impact",
        "title": "Deforestation cascades to soil, climate, and species loss",
        "content": (
            "Deforestation removes canopy regulation of microclimate, accelerates SOC "
            "oxidation, and fragments wildlife habitat. Even selective clearing can "
            "collapse understory biodiversity. Restoration pathways prioritize native "
            "regeneration, assisted natural regeneration, and agroforestry rather than "
            "exotic monoculture plantations that provide limited habitat value."
        ),
        "metrics": ["deforestation", "soil_organic_carbon", "habitat_connectivity", "microclimate"],
        "source": "IPCC / IPBES",
        "citation": "IPCC SRCCL; IPBES land degradation assessment",
        "year": 2019,
        "url": "https://www.ipcc.ch/",
    },
    {
        "id": "pollution_biodiversity",
        "domain": "human_impact",
        "title": "Agrochemical pollution and aquatic–terrestrial biodiversity",
        "content": (
            "Excess nitrogen and pesticide drift reduce insect biomass and contaminate "
            "aquatic food webs. Integrated pest management, precision nutrient "
            "application, and vegetative filter strips cut pollution loads while "
            "preserving beneficials. Pollution control is a biodiversity intervention "
            "because toxicity thresholds often override habitat gains."
        ),
        "metrics": ["pollution", "insect_biomass", "water_quality"],
        "source": "UNEP",
        "citation": "UNEP Towards a Pollution-Free Planet; IPBES pesticide-related findings",
        "year": 2019,
        "url": "https://www.unep.org/",
    },
    {
        "id": "grazing_pressure",
        "domain": "human_impact",
        "title": "Overgrazing, compaction, and grassland biodiversity",
        "content": (
            "Chronic overgrazing compacts soils, reduces infiltration, and shifts plant "
            "communities toward unpalatable species. Rotational grazing and rest "
            "periods restore plant diversity and SOC in grasslands. Coupling grazing "
            "management with woody enrichment in drylands addresses soil, water, and "
            "biodiversity together."
        ),
        "metrics": ["grazing_pressure", "soil_compaction", "plant_diversity", "infiltration"],
        "source": "FAO",
        "citation": "FAO grassland and pastoral systems sustainability guidance",
        "year": 2020,
        "url": "https://www.fao.org/",
    },
]
