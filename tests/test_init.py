from bw import cli, init as init_mod
from bw import io, schema, paths
from pathlib import Path


def test_init_creates_scaffold(tmp_path):
    rc = cli.main(["init", str(tmp_path / "proj")])
    assert rc == 0
    root = tmp_path / "proj"
    assert (root / "_bewater" / "ledger.yaml").exists()
    assert (root / "_bewater" / "config.yaml").exists()
    assert (root / "_bewater" / "records").is_dir()
    assert (root / "_bewater-output").is_dir()


def test_init_is_idempotent(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    rc = cli.main(["init", str(root)])
    assert rc == 0


def test_init_writes_empty_ledger(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    ledger = io.load_ledger(root)
    assert ledger.schema_version == 1
    assert ledger.revision == 1
    assert ledger.assumptions == {}
    assert ledger.updated_by == "bw-init"


def test_init_preserves_existing_ledger_unless_force(tmp_path):
    root = tmp_path / "proj"
    cli.main(["init", str(root)])
    ledger = io.load_ledger(root)
    ledger.revision = 99
    ledger.assumptions["A1"] = schema.Assumption(
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
    io.save_ledger(root, ledger)

    # second init without force: ledger untouched
    cli.main(["init", str(root)])
    again = io.load_ledger(root)
    assert again.revision == 99
    assert len(again.assumptions) == 1

    # force rewrites a fresh empty ledger
    cli.main(["init", str(root), "--force"])
    wiped = io.load_ledger(root)
    assert wiped.revision == 1
    assert wiped.assumptions == {}


def test_scaffold_returns_existing_ledger_path_compat(tmp_path):
    root = tmp_path / "proj"
    rc = init_mod.scaffold(root)
    assert rc is None or rc == 0
    assert paths.ledger_path(root).exists()
