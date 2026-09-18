"""Biodiversity indicator knowledge chunks."""

DOCUMENTS = [
    {
        "id": "species_richness_habitat",
        "domain": "biodiversity",
        "title": "Species richness depends on habitat heterogeneity",
        "content": (
            "Species richness scales with habitat diversity and connectivity more than with "
            "any single soil nutrient. Monocultures create simplified vegetation structure, "
            "reducing niche availability for birds, insects, and soil invertebrates. "
            "Introducing structural complexity—hedgerows, native strips, multi-strata "
            "planting—raises habitat diversity indices and supports pollinators and "
            "natural enemies. IPBES assessments link land-use homogenization to accelerating "
            "species loss."
        ),
        "metrics": ["species_richness", "habitat_diversity", "land_use"],
        "source": "IPBES",
        "citation": "IPBES Global Assessment Report on Biodiversity and Ecosystem Services (2019)",
        "year": 2019,
        "url": "https://ipbes.net/",
    },
    {
        "id": "pollinator_landscape",
        "domain": "biodiversity",
        "title": "Pollinator recovery via floral resources and nesting habitat",
        "content": (
            "Pollinator abundance declines where continuous flowering resources and nesting "
            "sites are absent. Semi-natural habitat patches of 5–10% of farm area can "
            "substantially increase wild bee visitation. Combining flowering cover crops "
            "with undisturbed margins links soil management to above-ground biodiversity. "
            "Evidence from EU agri-environment schemes and FAO pollinator initiatives "
            "supports multi-year floral continuity."
        ),
        "metrics": ["pollinator_abundance", "habitat_diversity", "crop_yield_stability"],
        "source": "FAO",
        "citation": "FAO International Pollinators Initiative; EU agri-environment evaluations",
        "year": 2021,
        "url": "https://www.fao.org/pollination/",
    },
    {
        "id": "soil_microbiome_diversity",
        "domain": "biodiversity",
        "title": "Below-ground biodiversity and plant community resilience",
        "content": (
            "Soil microbial diversity underpins nutrient cycling and plant disease "
            "suppression. Low SOC and tillage intensity correlate with reduced fungal "
            "hyphal networks and bacterial richness. Restoring organic inputs and "
            "reducing disturbance rebuilds microbial networks that support plant "
            "diversity and drought resilience—connecting soil health metrics directly "
            "to ecosystem stability."
        ),
        "metrics": ["microbial_diversity", "soil_organic_carbon", "plant_diversity"],
        "source": "Nature Sustainability / IPCC",
        "citation": "IPCC AR6 WGII/WGIII AFOLU; soil microbiome–plant diversity reviews",
        "year": 2022,
        "url": "https://www.ipcc.ch/",
    },
    {
        "id": "habitat_fragmentation",
        "domain": "biodiversity",
        "title": "Habitat fragmentation and edge effects",
        "content": (
            "Fragmented landscapes increase edge effects, isolate populations, and reduce "
            "gene flow. Corridor planting, riparian buffers, and stepping-stone habitats "
            "mitigate fragmentation. Land-use conversion to continuous monoculture is a "
            "primary driver of fragmentation; reversing it requires spatial planning, not "
            "only plot-level agronomy."
        ),
        "metrics": ["habitat_connectivity", "land_use", "species_persistence"],
        "source": "IPBES",
        "citation": "IPBES land degradation and restoration assessment",
        "year": 2018,
        "url": "https://ipbes.net/",
    },
]
