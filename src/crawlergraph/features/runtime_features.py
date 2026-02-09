"""
Runtime Feature Extraction

Normalizes raw runtime / browser telemetry into a structured,
deterministic RuntimeSignals object.

Input is assumed to come from an external browser abstraction
(e.g. Playwright instrumentation).

NO browser orchestration
NO retries
NO LangGraph logic
"""

from typing import Dict, Any, List
from crawler_graph.state import RuntimeSignals

# Public API
def extract_runtime_features(raw_signals: Dict[str, Any]) -> RuntimeSignals:
    """
    Entry point for runtime feature extraction.

    Args:
        raw_signals: Arbitrary telemetry from browser layer

    Returns:
        RuntimeSignals
    """

    return RuntimeSignals(
        status_code=_extract_status_code(raw_signals),
        redirect_detected=_detect_redirect(raw_signals),

        console_errors=_extract_console_errors(raw_signals),
        console_warnings=_extract_console_warnings(raw_signals),

        network_errors=_extract_network_errors(raw_signals),
        failed_requests=_count_failed_requests(raw_signals),

        layout_overlaps=_detect_layout_overlaps(raw_signals),

        long_tasks_ms=_extract_long_tasks(raw_signals),
        page_load_time_ms=_extract_page_load_time(raw_signals),
    )

# Signal Extractors
def _extract_status_code(raw: Dict[str, Any]) -> int:
    """
    Extract primary HTTP status code for the page.
    """
    return int(raw.get("status_code", 200))

def _detect_redirect(raw: Dict[str, Any]) -> bool:
    """
    Detect redirect via:
    - HTTP 3xx
    - Explicit redirect flags
    """
    status = raw.get("status_code")
    return bool(
        raw.get("redirect_detected", False)
        or (status and 300 <= int(status) < 400)
    )

def _extract_console_errors(raw: Dict[str, Any]) -> List[str]:
    logs = raw.get("console", {}).get("errors", [])
    return [str(e) for e in logs]

def _extract_console_warnings(raw: Dict[str, Any]) -> List[str]:
    logs = raw.get("console", {}).get("warnings", [])
    return [str(w) for w in logs]

def _extract_network_errors(raw: Dict[str, Any]) -> List[str]:
    return [
        str(err)
        for err in raw.get("network", {}).get("errors", [])
    ]

def _count_failed_requests(raw: Dict[str, Any]) -> int:
    return int(raw.get("network", {}).get("failed_requests", 0))

def _detect_layout_overlaps(raw: Dict[str, Any]) -> bool:
    """
    Assumes browser layer did layout analysis.
    """
    return bool(raw.get("layout", {}).get("overlaps", False))

def _extract_long_tasks(raw: Dict[str, Any]) -> int | None:
    """
    Long tasks indicate main-thread blocking (ms).
    """
    tasks = raw.get("performance", {}).get("long_tasks_ms")
    if tasks is None:
        return None
    return int(tasks)

def _extract_page_load_time(raw: Dict[str, Any]) -> int | None:
    timing = raw.get("performance", {}).get("page_load_time_ms")
    if timing is None:
        return None
    return int(timing)
