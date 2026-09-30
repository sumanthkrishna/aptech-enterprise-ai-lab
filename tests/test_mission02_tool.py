"""Regression checks for Mission 02's local weather tool.

These tests intentionally validate the Python source of truth without requiring
Azure authentication or a model call.
"""

import importlib.util
import re
from pathlib import Path

MISSION_FILE = Path(__file__).resolve().parents[1] / "lab" / "mission-02" / "02_add_tools.py"


def load_mission_module():
    spec = importlib.util.spec_from_file_location("mission02_add_tools", MISSION_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {MISSION_FILE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_mission_module()

    for _ in range(25):
        result = module.generate_weather_result("Seattle")
        assert "Seattle" in result, f"Location missing from tool result: {result}"
        match = re.search(r"high of (\d+)°C", result)
        assert match, f"Temperature missing from tool result: {result}"
        high_c = int(match.group(1))
        assert 10 <= high_c <= 30, f"Tool returned out-of-contract temperature: {high_c}°C"

    print("[PASS] Mission 02 tool regression: 25 results stayed within the 10–30°C sample contract.")


if __name__ == "__main__":
    main()
