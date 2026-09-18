"""Land use / land cover knowledge chunks."""

DOCUMENTS = [
    {
        "id": "monoculture_risks",
        "domain": "land_use",
        "title": "Monoculture wheat and biodiversity collapse pathways",
        "content": (
            "Monoculture wheat systems simplify canopy structure, increase pesticide "
            "dependence, and deplete SOC through residue removal and intensive tillage. "
            "The land-use signal couples to habitat fragmentation at landscape scale: "
            "large contiguous cereal blocks reduce edge habitats. Diversifying with "
            "intercropping, rotations including legumes, and field-margin habitats "
            "simultaneously improves soil metrics and species richness."
        ),
        "metrics": ["land_use", "soil_organic_carbon", "species_richness", "habitat_diversity"],
        "source": "IPBES",
        "citation": "IPBES Global Assessment – agriculture and land-use change drivers",
        "year": 2019,
        "url": "https://ipbes.net/",
    },
    {
        "id": "intercropping_benefits",
        "domain": "land_use",
        "title": "Intercropping and polyculture biodiversity benefits",
        "content": (
            "Intercropping cereals with legumes or oilseeds increases functional "
            "diversity, suppresses pests via associational resistance, and improves "
            "nitrogen economy. Meta-analyses show yield stability gains and higher "
            "arthropod diversity versus monocultures. When paired with reduced tillage, "
            "intercropping accelerates SOC recovery in degraded plots."
        ),
        "metrics": ["land_use", "arthropod_diversity", "soil_organic_carbon", "yield_stability"],
        "source": "Nature Plants / FAO",
        "citation": "FAO Save and Grow; intercropping meta-analyses on biodiversity and yield",
        "year": 2018,
        "url": "https://www.fao.org/",
    },
    {
        "id": "riparian_buffers",
        "domain": "land_use",
        "title": "Riparian and field-margin habitat buffers",
        "content": (
            "Native vegetative buffers along watercourses filter nutrients, reduce "
            "erosion, and serve as biodiversity corridors. Even 3–10 m margins "
            "measurably increase bird and beneficial insect abundance. Buffers link "
            "water quality, habitat connectivity, and on-farm biodiversity—classic "
            "multi-metric synergy."
        ),
        "metrics": ["habitat_connectivity", "water_quality", "avian_abundance"],
        "source": "USDA / UNEP",
        "citation": "USDA NRCS buffer practice standards; UNEP ecosystem restoration briefs",
        "year": 2017,
        "url": "https://www.unep.org/",
    },
]
