from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    with open(FIXTURE_DIR / name, "r", encoding="utf-8") as f:
        return f.read()
