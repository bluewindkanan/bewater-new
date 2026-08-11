from __future__ import annotations

from pathlib import Path

import pytest

from skill_helpers import (
    SkillCheckError,
    skill_dir,
    validate_skill,
    validate_skill_evals,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


GOOD_FM = "---\nname: bw-x\ndescription: Use when the user wants to x.\n---\n# bw-x\nbody\n"


def _good_skill(repo: Path) -> None:
    _write(skill_dir(repo, "bw-x") / "SKILL.md", GOOD_FM)
    _write(repo / "evals" / "bw-x" / "scenarios" / "s1.yaml",
           "scenario_id: S-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    _write(repo / "evals" / "bw-x" / "red" / "r1.yaml",
           "scenario_id: R-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 1\n")


def test_validate_skill_passes_well_formed_skill(tmp_path: Path):
    repo = tmp_path / "repo"
    _good_skill(repo)
    validate_skill(skill_dir(repo, "bw-x"))          # no raise
    validate_skill_evals(repo / "evals", "bw-x")      # no raise


def test_skill_dir_path():
    assert skill_dir(Path("/r"), "bw-start") == Path("/r/src/skills/bw-start")


@pytest.mark.parametrize("bad_fm", [
    "---\nname: bw-x\n---\n# x\n",                       # missing description
    "---\nname: bw-x\ndescription: Trigger here.\n---\n",  # not "Use when"
    "---\nname: bw-x\ndescription: Use when x.\nallowed-tools: Bash\n---\n",  # extra key
])
def test_validate_skill_rejects_bad_frontmatter(tmp_path: Path, bad_fm):
    repo = tmp_path / "repo"
    _write(skill_dir(repo, "bw-x") / "SKILL.md", bad_fm)
    with pytest.raises(SkillCheckError):
        validate_skill(skill_dir(repo, "bw-x"))


def test_validate_skill_rejects_escaping_reference(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM)
    _write(sd / "references" / "escape.md", "see ../outside/other.md")
    with pytest.raises(SkillCheckError):
        validate_skill(sd)


def test_validate_skill_allows_shared_reference_citation(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM + "cite ../_bw-shared/ledger-schema.md\n")
    validate_skill(sd)  # no raise: sanctioned shared citation


def test_validate_skill_rejects_placeholders(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(skill_dir(repo, "bw-x") / "SKILL.md", GOOD_FM.replace("body", "TODO fill"))
    with pytest.raises(SkillCheckError):
        validate_skill(skill_dir(repo, "bw-x"))


def test_validate_skill_requires_contract_metadata_on_contract_refs(tmp_path: Path):
    repo = tmp_path / "repo"
    sd = skill_dir(repo, "bw-x")
    _write(sd / "SKILL.md", GOOD_FM)
    _write(sd / "references" / "local-ledger.md",
           "---\ncontract_id: bw-ledger\n---\n# x\n")  # version missing
    with pytest.raises(SkillCheckError):
        validate_skill(sd)


def test_validate_skill_evals_requires_scenarios_and_red(tmp_path: Path):
    repo = tmp_path / "repo"
    _write(repo / "evals" / "bw-x" / "scenarios" / "s1.yaml",
           "scenario_id: S-1\ntarget_skill: bw-x\nprompt: hi\n"
           "required_assertions: [a]\nforbidden_behaviors: []\nrepetition_count: 3\n")
    # red/ missing
    with pytest.raises(SkillCheckError):
        validate_skill_evals(repo / "evals", "bw-x")
