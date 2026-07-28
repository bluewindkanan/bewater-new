from bw import cli, init as init_mod
from bw import io, schema, paths
from pathlib import Path


def test_init_creates_scaffold(tmp_path):
    rc = cli.main(["init", str(tmp_path / "proj")])
    assert rc == 0
    root = tmp_path / "proj"
    assert (root / "_bewater" / "state" / "assumption-ledger.yaml").exists()
    for stage in ["immersion", "discover", "define", "ideate", "shape", "handoff"]:
        assert (root / "_bewater" / "artifacts" / stage).is_dir()
    assert (root / "_bewater" / "state" / "gates").is_dir()
    assert (root / "_bewater" / "knowledge-base").is_dir()


def test_init_is_idempotent(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    rc = cli.main(["init", str(root)])  # second run
    assert rc == 0


def test_init_writes_empty_ledger_with_project_name(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    ledger = io.load_ledger(root)
    assert ledger.project == "proj"
    assert ledger.assumptions == []
    assert ledger.last_baselined_at is None
    assert ledger.baseline is None


def test_init_preserves_existing_ledger_unless_force(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    # mutate the ledger to simulate real use
    ledger = io.load_ledger(root)
    ledger.project = "renamed"
    ledger.assumptions.append(
        schema.Assumption(
            id="A1",
            statement="x",
            layer="root",
            category="consumer",
            impact="high",
            uncertainty="high",
            evidence_level="L1",
            validation_status="open",
            status="active",
            evidence_ref="",
        )
    )
    io.save_ledger(root, ledger)

    # second init without force: ledger untouched
    cli.main(["init", str(root)])
    again = io.load_ledger(root)
    assert again.project == "renamed"
    assert len(again.assumptions) == 1

    # force rewrites a fresh empty ledger
    cli.main(["init", str(root), "--force"])
    wiped = io.load_ledger(root)
    assert wiped.project == "proj"
    assert wiped.assumptions == []


def test_scaffold_returns_existing_ledger_path_compat(tmp_path):
    # scaffold works on a plain Path and is callable directly
    root = tmp_path / "proj"
    rc = init_mod.scaffold(root)
    assert rc is None or rc == 0
    assert paths.ledger_path(root).exists()
