"""Aggregate all knowledge documents for ingestion."""

from data.knowledge_base.biodiversity import DOCUMENTS as BIODIVERSITY
from data.knowledge_base.climate import DOCUMENTS as CLIMATE
from data.knowledge_base.human_impact import DOCUMENTS as HUMAN_IMPACT
from data.knowledge_base.interventions import DOCUMENTS as INTERVENTIONS
from data.knowledge_base.land_use import DOCUMENTS as LAND_USE
from data.knowledge_base.soil_health import DOCUMENTS as SOIL_HEALTH

ALL_DOCUMENTS = (
    SOIL_HEALTH + BIODIVERSITY + CLIMATE + LAND_USE + HUMAN_IMPACT + INTERVENTIONS
)


def iter_documents():
    for doc in ALL_DOCUMENTS:
        yield doc
