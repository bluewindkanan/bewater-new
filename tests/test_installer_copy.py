"""install.sh copy-mode behaviors (spec §9). Drives the script via subprocess against
isolated tmp_home / tmp_dest from Plan 1's conftest."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from installer_helpers import has_managed_marker, write_managed_marker

REPO = Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.sh"


def _run(project_root: Path, *extra) -> subprocess.CompletedProcess:
    env = {**os.environ}
    return subprocess.run(
        ["bash", str(INSTALL), "--project-root", str(project_root), "--src", str(REPO), *extra],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_copy_deploys_all_skills_and_shared_with_markers(tmp_dest):
    r = _run(tmp_dest, "--copy")
    assert r.returncode == 0, r.stderr
    skills_dest = tmp_dest / ".claude" / "skills"
    skills = sorted(p.name for p in (REPO / "src" / "skills").glob("bw-*"))
    installed = sorted(p.name for p in skills_dest.glob("bw-*"))
    assert installed == skills
    for s in installed:
        assert has_managed_marker(skills_dest / s), f"{s} missing marker"
    shared = skills_dest / "_bw-shared"
    assert shared.is_dir() and has_managed_marker(shared)


def test_copy_deploys_frozen_concept_skills_and_prunes_superseded_managed_names(tmp_dest):
    skills = tmp_dest / ".claude" / "skills"
    superseded = ["bw-concept-card", "bw-idea-seed", "bw-notion-development"]
    for name in superseded:
        obsolete = skills / name
        obsolete.mkdir(parents=True)
        (obsolete / "SKILL.md").write_text("managed obsolete skill\n")
        write_managed_marker(obsolete, version="0.1.0")

    r = _run(tmp_dest, "--copy")

    assert r.returncode == 0, r.stderr
    assert (skills / "bw-concept-seed" / "SKILL.md").is_file()
    assert (skills / "bw-concept-development" / "SKILL.md").is_file()
    assert all(not (skills / name).exists() for name in superseded)


def test_copy_deploys_runnable_bwkit(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    bwkit = tmp_dest / "_bewater" / "bwkit"
    assert (bwkit / "__main__.py").exists()
    env = {**os.environ, "PYTHONPATH": str(tmp_dest / "_bewater")}
    r = subprocess.run(
        [sys.executable, "-m", "bwkit", "--help"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "lock" in r.stdout and "cas" in r.stdout


def test_copy_fresh_install_initializes_complete_project_state(tmp_dest):
    r = _run(tmp_dest, "--copy")

    assert r.returncode == 0, r.stderr
    bewater = tmp_dest / "_bewater"
    assert (bewater / "config.yaml").is_file()
    assert (bewater / "ledger.yaml").is_file()
    assert (bewater / "conditions.yaml").is_file()
    assert (bewater / "records").is_dir()
    assert (tmp_dest / "_bewater-output").is_dir()
    assert sorted(path.name for path in (tmp_dest / "_bewater-output").iterdir()) == [
        "artifacts",
        "knowledge",
        "sources",
    ]
    assert "current_stage: immersion" in (bewater / "config.yaml").read_text()


def test_copy_is_idempotent(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    bewater = tmp_dest / "_bewater"
    yaml_sentinels = {
        bewater / "config.yaml": b"\ncustom_config_sentinel: true\n",
        bewater / "ledger.yaml": b"\ncustom_ledger_sentinel: true\n",
        bewater / "conditions.yaml": b"\ncustom_conditions_sentinel: true\n",
    }
    sentinels = {
        bewater / "records" / "custom.bin": b"record sentinel\x00\xff",
        tmp_dest / "_bewater-output" / "custom.bin": b"output sentinel\x00\xff",
    }
    for path, suffix in yaml_sentinels.items():
        path.write_bytes(path.read_bytes() + suffix)
    for path, content in sentinels.items():
        path.write_bytes(content)
    before = {
        path: path.read_bytes()
        for path in (*yaml_sentinels, *sentinels)
    }

    r2 = _run(tmp_dest, "--copy")

    assert r2.returncode == 0, r2.stderr
    assert (tmp_dest / ".claude" / "skills" / "bw-immersion" / "SKILL.md").exists()
    assert {path: path.read_bytes() for path in before} == before


def test_managed_skills_do_not_publish_legacy_flat_artifact_writer_paths():
    legacy = re.compile(r"_bewater-output/(?:ART|EXP)-", re.IGNORECASE)
    offenders = []
    for path in sorted((REPO / "src" / "skills").rglob("*.md")):
        if "_bw-shared" in path.parts:
            continue
        if legacy.search(path.read_text()):
            offenders.append(str(path.relative_to(REPO)))
    assert offenders == []


def test_copy_invalid_state_fails_before_updating_managed_payload(tmp_dest):
    assert _run(tmp_dest, "--copy").returncode == 0
    skill = tmp_dest / ".claude" / "skills" / "bw-immersion" / "SKILL.md"
    bwkit = tmp_dest / "_bewater" / "bwkit" / "__main__.py"
    skill.write_bytes(b"installed skill sentinel\n")
    bwkit.write_bytes(b"installed bwkit sentinel\n")
    (tmp_dest / "_bewater" / "config.yaml").write_bytes(b"partial invalid state\n")

    r = _run(tmp_dest, "--copy")

    assert r.returncode != 0
    assert "invalid" in r.stderr.lower()
    assert skill.read_bytes() == b"installed skill sentinel\n"
    assert bwkit.read_bytes() == b"installed bwkit sentinel\n"


def test_copy_prunes_managed_skill_missing_from_source(tmp_dest, tmp_path):
    assert _run(tmp_dest, "--copy").returncode == 0
    alternate_source = tmp_path / "alternate-source"
    shutil.copytree(REPO / "src", alternate_source / "src")
    removed_skill = alternate_source / "src" / "skills" / "bw-immersion"
    shutil.rmtree(removed_skill)
    unmanaged = tmp_dest / ".claude" / "skills" / "bw-personal"
    unmanaged.mkdir()
    (unmanaged / "SKILL.md").write_bytes(b"personal skill\n")

    r = subprocess.run(
        [
            "bash",
            str(INSTALL),
            "--copy",
            "--project-root",
            str(tmp_dest),
            "--src",
            str(alternate_source),
        ],
        capture_output=True,
        text=True,
        env={**os.environ},
        check=False,
    )

    assert r.returncode == 0, r.stderr
    assert not (tmp_dest / ".claude" / "skills" / "bw-immersion").exists()
    assert (unmanaged / "SKILL.md").read_bytes() == b"personal skill\n"


def test_copy_migrates_managed_4c_research_to_discovery_research(tmp_dest, tmp_path):
    alternate_source = tmp_path / "alternate-source"
    shutil.copytree(REPO / "src", alternate_source / "src")
    source_skills = alternate_source / "src" / "skills"
    legacy_source = source_skills / "bw-4c-research"
    replacement_source = source_skills / "bw-discovery-research"
    if legacy_source.exists():
        if replacement_source.exists():
            shutil.rmtree(legacy_source)
        else:
            legacy_source.rename(replacement_source)
    assert replacement_source.is_dir()

    skills_dest = tmp_dest / ".claude" / "skills"
    legacy_installed = skills_dest / "bw-4c-research"
    legacy_installed.mkdir(parents=True)
    (legacy_installed / "SKILL.md").write_bytes(b"managed legacy skill\n")
    write_managed_marker(legacy_installed, version="0.1.0")
    unmanaged = skills_dest / "bw-personal"
    unmanaged.mkdir()
    (unmanaged / "SKILL.md").write_bytes(b"personal skill\n")

    r = subprocess.run(
        [
            "bash",
            str(INSTALL),
            "--copy",
            "--project-root",
            str(tmp_dest),
            "--src",
            str(alternate_source),
        ],
        capture_output=True,
        text=True,
        env={**os.environ},
        check=False,
    )

    replacement_installed = skills_dest / "bw-discovery-research"
    assert r.returncode == 0, r.stderr
    assert not legacy_installed.exists()
    assert (replacement_installed / "SKILL.md").is_file()
    assert has_managed_marker(replacement_installed)
    assert (unmanaged / "SKILL.md").read_bytes() == b"personal skill\n"


def test_copy_fails_closed_for_unmanaged_obsolete_bw_start(tmp_dest, tmp_path):
    alternate_source = tmp_path / "alternate-source"
    shutil.copytree(REPO / "src", alternate_source / "src")
    obsolete_source = alternate_source / "src" / "skills" / "bw-start"
    if obsolete_source.exists():
        shutil.rmtree(obsolete_source)
    obsolete = tmp_dest / ".claude" / "skills" / "bw-start"
    obsolete.mkdir(parents=True)
    sentinel = obsolete / "SKILL.md"
    sentinel.write_bytes(b"unmanaged obsolete sentinel\n")

    r = subprocess.run(
        [
            "bash",
            str(INSTALL),
            "--copy",
            "--project-root",
            str(tmp_dest),
            "--src",
            str(alternate_source),
        ],
        capture_output=True,
        text=True,
        env={**os.environ},
        check=False,
    )

    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr
    assert sentinel.read_bytes() == b"unmanaged obsolete sentinel\n"


def test_copy_fails_closed_on_unrelated_target(tmp_dest):
    stranger = tmp_dest / ".claude" / "skills" / "bw-immersion"
    stranger.parent.mkdir(parents=True)
    stranger.mkdir()
    (stranger / "SKILL.md").write_text("someone else's skill")
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr


def test_copy_fails_closed_on_foreign_marker(tmp_dest):
    # a foreign .bewater-managed (not bewater) must NOT authorize overwrite
    foreign = tmp_dest / ".claude" / "skills" / "bw-immersion"
    foreign.parent.mkdir(parents=True)
    foreign.mkdir()
    (foreign / "SKILL.md").write_text("someone else's skill")
    (foreign / ".bewater-managed").write_text('{"managed_by":"other-tool","version":"9.9"}')
    r = _run(tmp_dest, "--copy")
    assert r.returncode != 0
    assert "not bewater-managed" in r.stderr
    assert (foreign / "SKILL.md").read_text() == "someone else's skill"  # survives


def test_copy_honors_skill_destination_override(tmp_dest):
    skills_dest = tmp_dest / "custom-skills"
    r = _run(tmp_dest, "--copy", "--dest", str(skills_dest))
    assert r.returncode == 0, r.stderr
    assert (skills_dest / "bw-immersion" / "SKILL.md").exists()
    assert (tmp_dest / "_bewater" / "bwkit" / "__main__.py").exists()


def test_skills_only_copy_deploys_skills_without_touching_bewater_state(tmp_dest):
    bewater = tmp_dest / "_bewater"
    bwkit = bewater / "bwkit"
    bwkit.mkdir(parents=True)
    state = bewater / "config.yaml"
    state.write_bytes(b"user state sentinel\n")
    runtime = bwkit / "runtime-sentinel.py"
    runtime.write_bytes(b"user runtime sentinel\n")

    result = _run(tmp_dest, "--copy", "--skills-only")

    assert result.returncode == 0, result.stderr
    assert (tmp_dest / ".claude" / "skills" / "bw-immersion" / "SKILL.md").exists()
    assert has_managed_marker(tmp_dest / ".claude" / "skills" / "_bw-shared")
    assert state.read_bytes() == b"user state sentinel\n"
    assert runtime.read_bytes() == b"user runtime sentinel\n"


def test_skills_only_can_deploy_one_named_skill_without_replacing_others(tmp_dest):
    result = _run(tmp_dest, "--copy", "--skills-only", "--skill", "bw-immersion")

    assert result.returncode == 0, result.stderr
    skills = tmp_dest / ".claude" / "skills"
    assert (skills / "bw-immersion" / "SKILL.md").exists()
    assert not (skills / "bw-discover").exists()
    assert has_managed_marker(skills / "_bw-shared")
