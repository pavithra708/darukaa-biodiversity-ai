"""Soil health knowledge chunks for RAG indexing."""

DOCUMENTS = [
    {
        "id": "soil_soc_thresholds",
        "domain": "soil_health",
        "title": "Soil organic carbon thresholds and biodiversity linkage",
        "content": (
            "Soil organic carbon (SOC) below 0.5% in cultivated soils indicates severe "
            "degradation with reduced microbial biomass, weak aggregate stability, and "
            "low habitat quality for soil fauna. FAO and IPCC soil guidelines treat "
            "SOC as a master variable: raising SOC improves water-holding capacity, "
            "nutrient cycling, and below-ground biodiversity. Semi-arid monocultures "
            "often fall to 0.2–0.5% SOC. Cover crops, residues, and agroforestry can "
            "raise SOC by roughly 15–40% over 2–5 years depending on climate and clay content."
        ),
        "metrics": ["soil_organic_carbon", "microbial_diversity", "water_holding"],
        "source": "FAO",
        "citation": "FAO Status of the World's Soil Resources (2015); IPCC AFOLU guidance on SOC",
        "year": 2015,
        "url": "https://www.fao.org/soils-portal/",
    },
    {
        "id": "soil_ph_biodiversity",
        "domain": "soil_health",
        "title": "Soil pH effects on nutrient availability and biota",
        "content": (
            "Most soil microbes and many crop-associated invertebrates perform best near "
            "pH 6.0–7.5. Acidic soils (pH < 5.5) limit phosphorus availability and "
            "suppress earthworm activity; alkaline soils (pH > 8.0) can lock micronutrients. "
            "Biodiversity interventions fail if pH extremes block microbial recovery. "
            "Lime or organic amendments should be paired with habitat measures when pH is "
            "outside the biological window."
        ),
        "metrics": ["soil_ph", "nutrient_availability", "earthworm_abundance"],
        "source": "USDA NRCS",
        "citation": "USDA NRCS Soil Health Technical Note – pH and biological activity",
        "year": 2018,
        "url": "https://www.nrcs.usda.gov/",
    },
    {
        "id": "soil_moisture_fauna",
        "domain": "soil_health",
        "title": "Soil moisture, drought, and soil fauna survival",
        "content": (
            "Chronic low soil moisture reduces microbial respiration and collapses "
            "mesofauna populations. Mulching, contour bunds, and deep-rooted perennials "
            "increase infiltration and buffer dry spells. In low-rainfall zones, water "
            "harvesting multiplies the benefit of organic amendments because SOC gains "
            "require sufficient moisture for decomposition and root growth."
        ),
        "metrics": ["soil_moisture", "rainfall", "soil_fauna"],
        "source": "CGIAR",
        "citation": "CGIAR / ICRISAT dryland soil moisture management syntheses",
        "year": 2020,
        "url": "https://www.icrisat.org/",
    },
    {
        "id": "legume_cover_crops",
        "domain": "soil_health",
        "title": "Legume-based cover crops and SOC gains",
        "content": (
            "Legume cover crops (e.g., cowpea, clover, pigeon pea) fix atmospheric nitrogen, "
            "increase root exudates, and build SOC. Meta-analyses and FAO case studies "
            "report SOC increases of about 15–25% over 2–3 years under continuous cover, "
            "with concurrent rises in microbial diversity and pollinator forage when "
            "flowering legumes are used. Benefits are strongest where baseline SOC is low "
            "and nitrogen is limiting."
        ),
        "metrics": ["soil_organic_carbon", "nitrogen", "pollinator_support", "microbial_diversity"],
        "source": "FAO",
        "citation": "FAO Cover Crops and Soil Health practice briefs; Poore & Nemecek related SOC literature",
        "year": 2019,
        "url": "https://www.fao.org/",
    },
]
