"""
Defect Detection Rules (v1)

Maps PageFeatures + RuntimeSignals → Defects.

NO navigation
NO LangGraph logic
NO LLMs
"""

from typing import List
from crawlergraph.state import PageFeatures, RuntimeSignals
from crawlergraph.defects.models import Defect, DefectCategory


def detect_defects(
    features: PageFeatures,
    signals: RuntimeSignals
) -> List[Defect]:
    defects: List[Defect] = []

    defects.extend(_functional_defects(signals))
    defects.extend(_ui_defects(signals))
    defects.extend(_performance_defects(signals))

    return defects

# Functional defects
def _functional_defects(signals: RuntimeSignals) -> List[Defect]:
    defects = []

    if signals.status_code >= 500:
        defects.append(
            Defect(
                category=DefectCategory.FUNCTIONAL,
                subtype="ServerError",
                severity=9,
                confidence=0.95,
                description="Server returned 5xx error",
                evidence={"status_code": signals.status_code},
            )
        )

    if 400 <= signals.status_code < 500:
        defects.append(
            Defect(
                category=DefectCategory.FUNCTIONAL,
                subtype="ClientError",
                severity=7,
                confidence=0.9,
                description="Client-side HTTP error",
                evidence={"status_code": signals.status_code},
            )
        )

    if signals.console_errors:
        defects.append(
            Defect(
                category=DefectCategory.FUNCTIONAL,
                subtype="ConsoleError",
                severity=6,
                confidence=0.85,
                description="JavaScript console errors detected",
                evidence={"errors": signals.console_errors},
            )
        )

    if signals.failed_requests > 0:
        defects.append(
            Defect(
                category=DefectCategory.FUNCTIONAL,
                subtype="NetworkFailure",
                severity=6,
                confidence=0.8,
                description="Failed network requests detected",
                evidence={"failed_requests": signals.failed_requests},
            )
        )

    return defects

# UI defects
def _ui_defects(signals: RuntimeSignals) -> List[Defect]:
    defects = []

    if signals.layout_overlaps:
        defects.append(
            Defect(
                category=DefectCategory.UI,
                subtype="LayoutOverlap",
                severity=5,
                confidence=0.75,
                description="Overlapping UI elements detected",
                evidence={},
            )
        )

    return defects

# Performance defects
def _performance_defects(signals: RuntimeSignals) -> List[Defect]:
    defects = []

    if signals.page_load_time_ms and signals.page_load_time_ms > 3000:
        defects.append(
            Defect(
                category=DefectCategory.PERFORMANCE,
                subtype="SlowPageLoad",
                severity=6,
                confidence=0.8,
                description="Page load time exceeded threshold",
                evidence={"page_load_time_ms": signals.page_load_time_ms},
            )
        )

    if signals.long_tasks_ms and signals.long_tasks_ms > 200:
        defects.append(
            Defect(
                category=DefectCategory.PERFORMANCE,
                subtype="LongMainThreadTasks",
                severity=5,
                confidence=0.75,
                description="Long main-thread tasks detected",
                evidence={"long_tasks_ms": signals.long_tasks_ms},
            )
        )

    return defects
