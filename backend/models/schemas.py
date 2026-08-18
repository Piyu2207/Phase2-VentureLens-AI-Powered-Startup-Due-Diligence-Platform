from dataclasses import dataclass, asdict

@dataclass
class RetrievalResult:
    engine: str
    context: str
    latency_ms: float
    ok: bool
    error: str | None = None
    raw: object = None
    def to_dict(self):
        return asdict(self)
