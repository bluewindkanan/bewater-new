import subprocess, sys

def test_bw_help_exits_zero_and_lists_command_groups():
    result = subprocess.run([sys.executable, "-m", "bw", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    out = result.stdout
    for grp in ["init", "ledger", "validate", "hash", "gate-scan"]:
        assert grp in out
