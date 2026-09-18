from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TimeHorizon(str, Enum):
    SHORT = "short_term"  # 0–12 months
    MEDIUM = "medium_term"  # 1–3 years
    LONG = "long_term"  # 3+ years


class LandUseType(str, Enum):
    MONOCULTURE = "monoculture"
    MIXED_CROPPING = "mixed_cropping"
    AGROFORESTRY = "agroforestry"
    PASTURE = "pasture"
    FOREST = "forest"
    DEGRADED = "degraded"
    URBAN_EDGE = "urban_edge"
    WETLAND = "wetland"
    UNKNOWN = "unknown"


class RainfallPattern(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    ERRATIC = "erratic"
    UNKNOWN = "unknown"


class StructuredSiteInput(BaseModel):
    """Structured environmental snapshot for a site/parcel."""

    soil_organic_carbon_pct: float | None = Field(
        default=None, description="Soil organic carbon %, typically 0.1–6.0"
    )
    soil_ph: float | None = Field(default=None, ge=3.0, le=10.0)
    soil_moisture: str | None = Field(
        default=None, description="dry | moderate | wet | unknown"
    )
    rainfall: RainfallPattern | str | None = None
    temperature_c: float | None = None
    land_use: LandUseType | str | None = None
    crop: str | None = None
    region: str | None = None
    species_richness: float | None = Field(
        default=None, description="Observed or estimated species count / index"
    )
    habitat_diversity_index: float | None = Field(
        default=None, ge=0.0, le=1.0, description="0–1 habitat diversity score"
    )
    deforestation_pressure: str | None = None
    pollution_level: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    notes: str | None = None


class ChatRequest(BaseModel):
    message: str | None = None
    site: StructuredSiteInput | None = None
    session_id: str | None = None
    geo: dict[str, float] | None = Field(
        default=None, description="Optional {lat, lon} spatial context"
    )


class EvidenceRef(BaseModel):
    source: str
    citation: str
    year: int | None = None
    url: str | None = None


class Recommendation(BaseModel):
    action: str
    scientific_reasoning: str
    impacted_metrics: list[str]
    expected_impact: str
    time_horizon: TimeHorizon
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[EvidenceRef]
    linked_variables: list[str] = Field(
        default_factory=list,
        description="Multi-metric links, e.g. soil_carbon ↔ microbial_diversity",
    )


class MetricAssessment(BaseModel):
    metric: str
    value: Any
    status: str  # critical | low | moderate | good | unknown
    note: str


class ChatResponse(BaseModel):
    session_id: str
    clarifying_questions: list[str] = Field(default_factory=list)
    assessments: list[MetricAssessment] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    multi_metric_synthesis: str = ""
    retrieved_knowledge: list[dict[str, Any]] = Field(default_factory=list)
    answer: str = ""
    needs_more_info: bool = False


class IngestStats(BaseModel):
    documents_indexed: int
    collection: str
    persist_dir: str
