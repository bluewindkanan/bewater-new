import pytest, yaml
from pathlib import Path

@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    (tmp_path / "_bewater").mkdir(parents=True)
    (tmp_path / "_bewater" / "records").mkdir()
    (tmp_path / "_bewater-output").mkdir()
    (tmp_path / "_bewater" / "ledger.yaml").write_text(
        yaml.safe_dump({"schema_version": 1, "revision": 1, "next_id": 1,
                        "updated_at": None, "updated_by": "bw-init", "assumptions": {}})
    )
    return tmp_path


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    return home


@pytest.fixture
def tmp_dest(tmp_path):
    dest = tmp_path / "dest"
    dest.mkdir()
    return dest
