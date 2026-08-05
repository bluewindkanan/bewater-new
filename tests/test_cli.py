import subprocess
import sys


def test_bw_help_exits_zero_and_lists_command_groups():
    result = subprocess.run(
        [sys.executable, "-m", "bw", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    out = result.stdout
    assert "{ledger,validate,hash,gate-scan}" in out
    for grp in ["ledger", "validate", "hash", "gate-scan"]:
        assert grp in out
    assert "init" not in out
