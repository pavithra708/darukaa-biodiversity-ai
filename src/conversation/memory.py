from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from src.models.schemas import StructuredSiteInput


@dataclass
class Turn:
    role: str
    content: str
    site_snapshot: dict[str, Any] | None = None


@dataclass
class Session:
    session_id: str
    turns: list[Turn] = field(default_factory=list)
    site: StructuredSiteInput = field(default_factory=StructuredSiteInput)

    def add_turn(self, role: str, content: str) -> None:
        self.turns.append(
            Turn(
                role=role,
                content=content,
                site_snapshot=self.site.model_dump(exclude_none=True),
            )
        )


class ConversationMemory:
    """In-memory multi-turn session store with cumulative site context."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._lock = Lock()

    def get_or_create(self, session_id: str | None = None) -> Session:
        with self._lock:
            sid = session_id or str(uuid.uuid4())
            if sid not in self._sessions:
                self._sessions[sid] = Session(session_id=sid)
            return self._sessions[sid]

    def merge_site(self, session: Session, incoming: StructuredSiteInput | None) -> StructuredSiteInput:
        if incoming is None:
            return session.site
        current = session.site.model_dump()
        for key, value in incoming.model_dump(exclude_none=True).items():
            current[key] = value
        session.site = StructuredSiteInput(**current)
        return session.site

    def extract_from_text(self, session: Session, message: str) -> StructuredSiteInput:
        """Lightweight NLP extraction to accumulate structured metrics from free text."""
        text = message.lower()
        updates: dict[str, Any] = {}

        soc = re.search(r"(?:soc|soil organic carbon|organic carbon)\D{0,12}(\d+(?:\.\d+)?)\s*%?", text)
        if soc:
            updates["soil_organic_carbon_pct"] = float(soc.group(1))

        ph = re.search(r"(?:ph|pH)\D{0,8}(\d+(?:\.\d+)?)", message)
        if ph:
            updates["soil_ph"] = float(ph.group(1))

        if re.search(r"\b(low rainfall|rainfall\s*[:=]?\s*low|arid|semi[-\s]?arid)\b", text):
            updates["rainfall"] = "low"
            if "semi" in text or "arid" in text:
                updates["region"] = updates.get("region") or "semi-arid"
        elif re.search(r"\b(erratic rainfall|rainfall\s*[:=]?\s*erratic)\b", text):
            updates["rainfall"] = "erratic"
        elif re.search(r"\b(high rainfall|rainfall\s*[:=]?\s*high)\b", text):
            updates["rainfall"] = "high"
        elif re.search(r"\b(moderate rainfall|rainfall\s*[:=]?\s*moderate)\b", text):
            updates["rainfall"] = "moderate"

        if re.search(r"\bmonoculture\b", text):
            updates["land_use"] = "monoculture"
        elif re.search(r"\bagroforestry\b", text):
            updates["land_use"] = "agroforestry"
        elif re.search(r"\bmixed cropping|intercrop", text):
            updates["land_use"] = "mixed_cropping"
        elif re.search(r"\bdegraded\b", text):
            updates["land_use"] = "degraded"

        crop = re.search(r"\b(wheat|rice|maize|corn|soy|cotton|millet|sorghum)\b", text)
        if crop:
            updates["crop"] = crop.group(1)

        if re.search(r"\bdry soil|soil moisture\s*[:=]?\s*dry\b", text):
            updates["soil_moisture"] = "dry"
        if re.search(r"\bhigh pollution|pollution\s*[:=]?\s*high\b", text):
            updates["pollution_level"] = "high"

        latlon = re.search(
            r"(?:lat(?:itude)?\s*[:=]?\s*)(-?\d+(?:\.\d+)?).*?(?:lon(?:gitude)?\s*[:=]?\s*)(-?\d+(?:\.\d+)?)",
            text,
        )
        if latlon:
            updates["latitude"] = float(latlon.group(1))
            updates["longitude"] = float(latlon.group(2))

        if updates:
            return self.merge_site(session, StructuredSiteInput(**updates))
        return session.site


memory = ConversationMemory()
