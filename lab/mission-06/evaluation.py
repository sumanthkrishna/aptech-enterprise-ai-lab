"""Mission 06: deterministic RAG evaluation without model calls."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_source: str | None
    expected_answer_fragment: str | None = None

def evaluate_case(case: EvalCase, answer: str, sources: list[dict],
                  http_status: int = 200) -> dict:
    ids = [str(s.get("source_id", "")) for s in sources]
    source_ok = case.expected_source in ids if case.expected_source else not ids
    # This is an exact-substring proxy, not a semantic or citation-support verifier.
    answer_ok = (case.expected_answer_fragment.lower() in answer.lower()
                 if case.expected_answer_fragment is not None else True)
    transport_ok = 200 <= http_status < 300
    return {
        "http_success": transport_ok,
        "source_match": source_ok,
        "answer_fragment_match": answer_ok,
        "passed": transport_ok and source_ok and answer_ok,
        "answer_support_verified": False,
    }

def evaluate_dataset(cases: list[EvalCase], runner: Callable[[str], dict]) -> dict:
    if not cases:
        raise ValueError("Evaluation dataset must not be empty")
    results = []
    for case in cases:
        response = runner(case.question)
        results.append(evaluate_case(case, str(response.get("answer", "")),
            response.get("sources", []), int(response.get("http_status", 200))))
    return {"cases": len(results), "passed": sum(r["passed"] for r in results),
            "pass_rate": round(sum(r["passed"] for r in results) / len(results), 3),
            "results": results}
