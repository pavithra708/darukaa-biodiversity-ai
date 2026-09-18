"""Climate and hydrology knowledge chunks."""

DOCUMENTS = [
    {
        "id": "rainfall_species_survival",
        "domain": "climate",
        "title": "Rainfall, water stress, and species survival",
        "content": (
            "Low or erratic rainfall reduces primary productivity and intensifies "
            "competition for water, lowering survival of drought-sensitive species. "
            "Water availability couples to biodiversity through plant cover, flowering "
            "duration, and soil moisture for fauna. In semi-arid systems, interventions "
            "that ignore hydrology underperform: agroforestry with deep-rooted natives "
            "and micro-catchments jointly raise moisture retention and habitat value."
        ),
        "metrics": ["rainfall", "water_availability", "species_survival", "soil_moisture"],
        "source": "IPCC",
        "citation": "IPCC AR6 WGII – drought impacts on ecosystems",
        "year": 2022,
        "url": "https://www.ipcc.ch/",
    },
    {
        "id": "temperature_phenology",
        "domain": "climate",
        "title": "Temperature extremes and phenological mismatch",
        "content": (
            "Rising mean temperatures and heat extremes shift flowering and insect "
            "emergence timing, causing phenological mismatches that reduce pollination "
            "success. Shade from multi-strata agroforestry buffers microclimate "
            "extremes by several degrees, protecting understory biodiversity and "
            "soil moisture. Climate-smart biodiversity planning must co-optimize "
            "temperature buffers with habitat structure."
        ),
        "metrics": ["temperature", "microclimate", "pollination_success"],
        "source": "IPCC",
        "citation": "IPCC AR6 WGII – terrestrial ecosystem climate impacts",
        "year": 2022,
        "url": "https://www.ipcc.ch/",
    },
    {
        "id": "semiarid_agroforestry",
        "domain": "climate",
        "title": "Semi-arid agroforestry for carbon and biodiversity",
        "content": (
            "In semi-arid regions with low rainfall and wheat monoculture, introducing "
            "drought-tolerant trees (e.g., Faidherbia, Prosopis managed carefully, or "
            "native nitrogen-fixing trees) with intercrops increases SOC, reduces "
            "wind erosion, and creates vertical habitat niches. FAO and World Bank "
            "dryland projects report measurable gains in woody cover, soil carbon, and "
            "avian richness over 3–7 years when grazing pressure is controlled."
        ),
        "metrics": ["soil_organic_carbon", "woody_cover", "avian_richness", "rainfall"],
        "source": "FAO",
        "citation": "FAO Dryland agroforestry and climate-smart agriculture guidance",
        "year": 2020,
        "url": "https://www.fao.org/",
    },
]
