from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class CheckResult:
    name: str
    status: str
    summary: str
    severity: str = "info"
    data: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
