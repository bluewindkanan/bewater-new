from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_old_runtime_plan_has_superseded_banner():
    plan = REPO / "docs" / "superpowers" / "plans" / "2026-07-28-bw-runtime-phase1.md"
    text = plan.read_text()
    assert "SUPERSEDED" in text
    assert "2026-07-27-bewater-decision-phase-skills-design.md" in text
    assert "do not execute" in text.lower()


def test_coverage_source_includes_bwkit():
    text = (REPO / "pyproject.toml").read_text()
    assert 'source = ["bw", "bwkit"]' in text


def test_pytest_pythonpath_includes_root():
    # evals/_harness lives at repo root; it must be importable from tests
    text = (REPO / "pyproject.toml").read_text()
    assert 'pythonpath = ["src", "."]' in text
