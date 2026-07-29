from __future__ import annotations

from installer_helpers import has_managed_marker, write_managed_marker


def test_tmp_home_is_isolated(tmp_home):
    assert tmp_home.is_dir()
    # a fresh HOME has no installed bewater skills
    assert not (tmp_home / ".claude" / "skills" / "bw-start").exists()


def test_tmp_dest_is_writable(tmp_dest):
    (tmp_dest / "probe").write_text("x")
    assert (tmp_dest / "probe").read_text() == "x"


def test_managed_marker_roundtrip(tmp_dest):
    target = tmp_dest / "bw-start"
    target.mkdir()
    write_managed_marker(target, version="0.1.0")
    assert has_managed_marker(target) is True

    stranger = tmp_dest / "stranger"
    stranger.mkdir()
    assert has_managed_marker(stranger) is False
