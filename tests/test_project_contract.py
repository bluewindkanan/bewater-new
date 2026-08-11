from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def test_claude_declares_decision_phase_scope():
    text = (REPO / "CLAUDE.md").read_text()
    assert "## Scope" in text
    assert "decision segment (Immersion -> G2)" in text
    assert "Design/Build/Launch/Grow" in text
    assert "G3/G4" in text


def test_backtrack_is_recovery_capability_not_router():
    text = (REPO / "CLAUDE.md").read_text()
    routing = text.split("## Skill Routing", 1)[1].split("##", 1)[0]
    assert "backtrack        ->" not in routing
    assert "## Recovery Capabilities" in text
    assert "bw-backtrack" in text.split("## Recovery Capabilities", 1)[1]
