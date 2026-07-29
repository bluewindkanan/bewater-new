import pytest, yaml
from pathlib import Path

@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    (tmp_path / "_bewater" / "state").mkdir(parents=True)
    (tmp_path / "_bewater" / "artifacts").mkdir()
    (tmp_path / "_bewater" / "knowledge-base").mkdir()
    (tmp_path / "_bewater" / "state" / "assumption-ledger.yaml").write_text(
        yaml.safe_dump({"project": "t", "last_baselined_at": None, "baseline": None, "assumptions": []})
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
