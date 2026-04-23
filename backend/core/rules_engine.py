from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


RULES_PATH = Path(__file__).resolve().parents[1] / "rules" / "default_rules.yaml"


@dataclass(slots=True)
class DetectionRule:
    name: str
    pattern: str
    severity: str
    title: str
    description: str
    source_contains: str | None = None
    mitre_tag: str | None = None
    cooldown_seconds: int = 60
    compiled_pattern: re.Pattern | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.compiled_pattern = re.compile(self.pattern, flags=re.IGNORECASE)

    def matches(self, event: dict[str, Any]) -> bool:
        haystack = " ".join(
            str(value)
            for value in [
                event.get("title", ""),
                event.get("message", ""),
                event.get("event_type", ""),
                event.get("source", ""),
                event.get("raw_payload", ""),
            ]
        )
        if self.source_contains and self.source_contains.lower() not in str(event.get("source", "")).lower():
            return False
        return bool(self.compiled_pattern.search(haystack) if self.compiled_pattern else False)


@lru_cache(maxsize=1)
def load_rules() -> list[DetectionRule]:
    with RULES_PATH.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or []
    return [DetectionRule(**item) for item in raw]
