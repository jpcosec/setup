"""Isolated runtime regressions; no real credentials or network calls."""
import base64
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1] / 'pi/scion'


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def launcher(tmp_path, monkeypatch):
    module = load('scion_launch_test', 'launch.py')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('PI_CODING_AGENT_DIR', str(tmp_path / 'agent'))
    calls = []
    monkeypatch.setattr(module.os, 'execvp', lambda executable, args: calls.append((executable, args)))
    return module, tmp_path / 'agent/scion/session.jsonl', calls


def invoke(monkeypatch, module, args):
    monkeypatch.setattr(sys, 'argv', ['launch.py', *args])
    module.main()


def persist(session, content):
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_text(content)


def test_first_launch_forwards_task_and_pins_session(launcher, monkeypatch):
    module, session, calls = launcher
    args = ['--provider', 'deepseek', '--model', 'dummy-model', '--tools', 'read', 'Original task']
    invoke(monkeypatch, module, args)
    assert calls == [('pi', ['pi', '--offline', '--session', str(session), *args])]
    assert module.os.environ['PI_OFFLINE'] == '1'
    assert module.os.environ['PI_SKIP_VERSION_CHECK'] == '1'


def test_resume_keeps_options_and_session_without_replaying_task(launcher, monkeypatch):
    module, session, calls = launcher
    persist(session, json.dumps({'type': 'session', 'id': 'dummy-id', 'cwd': str(Path.cwd())}) + '\n')
    invoke(monkeypatch, module, ['--provider', 'deepseek', '--model', 'dummy-model', '--tools', 'read', '--no-context-files', '--resume', 'Original task', 'second positional'])
    assert calls == [('pi', ['pi', '--offline', '--session', str(session), '--provider', 'deepseek', '--model', 'dummy-model', '--tools', 'read', '--no-context-files'])]


@pytest.mark.parametrize('content', ['invalid json', '', '[]', json.dumps({'type': 'message', 'id': 'x', 'cwd': '/workspace'}), json.dumps({'type': 'session', 'id': '', 'cwd': '/workspace'}), json.dumps({'type': 'session', 'id': 'x'}), json.dumps({'type': 'session', 'id': 'x', 'cwd': 'relative'}), json.dumps({'type': 'session', 'id': 'x', 'cwd': '/clearly-different-workspace'})])
def test_invalid_or_mismatched_session_rejected(launcher, monkeypatch, content):
    module, session, calls = launcher
    persist(session, content)
    with pytest.raises(ValueError):
        invoke(monkeypatch, module, ['Original task'])
    assert not calls
    assert session.read_text() == content


@pytest.mark.parametrize('args', [['--session', '/dummy'], ['--session=/dummy'], ['--session-dir=/dummy'], ['--no-session'], ['--fork']])
def test_session_overrides_rejected(launcher, monkeypatch, args):
    module, session, calls = launcher
    with pytest.raises(ValueError):
        invoke(monkeypatch, module, args)
    assert not calls


@pytest.mark.parametrize('failure', [None, 400, 503, 'exception', 'interrupt'])
def test_secret_sync_scope_encoding_and_sanitized_failures(tmp_path, monkeypatch, capsys, failure):
    module = load('scion_secret_test', 'sync-deepseek-secret.py')
    secret, token = 'dummy-secret-DO-NOT-PRINT', 'dummy-token-DO-NOT-PRINT'
    source, token_file = tmp_path / 'dummy.env', tmp_path / 'dummy.token'
    source.write_text('UNRELATED_KEY=ignored\nexport DEEPSEEK_API_KEY="' + secret + '"\n')
    token_file.write_text(token)
    monkeypatch.setattr(sys, 'argv', ['sync', '--source', str(source), '--token-file', str(token_file), '--project-id', 'dummy-project'])
    requests = []

    class Response:
        status = failure if isinstance(failure, int) else 200
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    class Opener:
        def open(self, request, timeout):
            requests.append(request)
            assert timeout == 30
            if failure == 'exception':
                raise RuntimeError(secret + token)
            if failure == 'interrupt':
                raise KeyboardInterrupt(secret + token)
            return Response()

    monkeypatch.setattr(module, 'build_opener', lambda *handlers: Opener())
    assert module.main() == (0 if failure is None else 1)
    request, = requests
    assert request.method == 'PUT'
    assert request.get_header('Authorization') == 'Bearer ' + token
    assert json.loads(request.data) == {'value': base64.b64encode(secret.encode()).decode(), 'scope': 'project', 'scopeId': 'dummy-project', 'type': 'environment', 'target': 'DEEPSEEK_API_KEY', 'injectionMode': 'as_needed'}
    captured = capsys.readouterr()
    for credential in (secret, token, base64.b64encode(secret.encode()).decode()):
        assert credential not in captured.out + captured.err
