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
