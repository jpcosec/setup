"""Tests for the fork-from-base path of the Scion Pi launcher (DSP-1)."""
import json
from pathlib import Path

import launch


def _base(tmp_path: Path) -> Path:
    d = tmp_path / "fork-from"
    d.mkdir()
    entries = [{"type": "session", "version": 3, "id": "base-id", "cwd": "/elsewhere"},
               {"type": "message", "message": {"role": "user", "content": "contexto común"}}]
    (d / "ejecutor-1.jsonl").write_text("\n".join(json.dumps(e) for e in entries) + "\n")
    return d


def test_first_start_forks_the_base_with_a_new_header(tmp_path):
    base_dir = _base(tmp_path)
    session = tmp_path / "session.jsonl"
    assert launch.fork_base(session, Path("/workspace"), base_dir, "ejecutor-1")
    header, *rest = [json.loads(line) for line in session.read_text().splitlines()]
    assert header["type"] == "session" and header["id"] != "base-id"
    assert header["cwd"] == "/workspace" and header["parentSession"].endswith("ejecutor-1.jsonl")
    assert rest == [{"type": "message", "message": {"role": "user", "content": "contexto común"}}]


def test_existing_session_or_missing_base_is_left_alone(tmp_path):
    base_dir = _base(tmp_path)
    session = tmp_path / "session.jsonl"
    session.write_text('{"type": "session", "id": "propia", "cwd": "/workspace"}\n')
    assert not launch.fork_base(session, Path("/workspace"), base_dir, "ejecutor-1")
    assert json.loads(session.read_text())["id"] == "propia"
    assert not launch.fork_base(tmp_path / "otra.jsonl", Path("/workspace"), base_dir, "sin-base")
