"""Mission 06: offline, standard-library observability primitives.

Do not log prompts, answers, identities or retrieved document bodies.
This is in-process tracing, not OpenTelemetry or Azure Monitor.
"""
from dataclasses import dataclass, asdict
from time import perf_counter
from typing import Callable, Any
import uuid

@dataclass(frozen=True)
class TraceEvent:
    trace_id: str
    stage: str
    duration_ms: float
    success: bool
    error_type: str | None = None

class TraceRecorder:
    def __init__(self):
        self.events: list[TraceEvent] = []

    def run_stage(self, trace_id: str, stage: str, action: Callable[[], Any]) -> Any:
        start = perf_counter()
        try:
            result = action()
        except Exception as exc:
            self.events.append(TraceEvent(trace_id, stage,
                round((perf_counter() - start) * 1000, 3), False, type(exc).__name__))
            raise
        self.events.append(TraceEvent(trace_id, stage,
            round((perf_counter() - start) * 1000, 3), True))
        return result

    def new_trace_id(self) -> str:
        return uuid.uuid4().hex

    def summary(self) -> dict:
        count = len(self.events)
        return {"events": count, "errors": sum(not e.success for e in self.events),
                "average_stage_ms": round(sum(e.duration_ms for e in self.events) / count, 3) if count else 0}

    def export(self) -> list[dict]:
        return [asdict(e) for e in self.events]
