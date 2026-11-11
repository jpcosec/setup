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
    (tmp_path / 'agent').mkdir()
    (tmp_path / 'agent/settings.json').write_text(json.dumps({
        'defaultProvider': 'deepseek', 'defaultModel': 'deepseek-flash'}))
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


def test_resume_pins_provisioned_provider_instead_of_implicit_fallback(launcher, monkeypatch):
    module, session, calls = launcher
    persist(session, json.dumps({'type': 'session', 'id': 'same-session', 'cwd': str(Path.cwd())}) + '\n')
    invoke(monkeypatch, module, ['--continue', 'Original task'])
    assert calls == [('pi', ['pi', '--offline', '--session', str(session),
                            '--provider', 'deepseek', '--model', 'deepseek-flash'])]
    assert json.loads(session.read_text())['id'] == 'same-session'


def test_native_resume_alias_is_not_a_pi_catalogue_search(launcher, monkeypatch):
    module, session, calls = launcher
    monkeypatch.setenv('SCION_MODEL', 'small')
    persist(session, json.dumps({'type': 'session', 'id': 'same-session', 'cwd': str(Path.cwd())}) + '\n')
    invoke(monkeypatch, module, ['--model', 'small', '--continue', 'Original task'])
    argv = calls[0][1]
    assert argv[argv.index('--provider') + 1] == 'deepseek'
    assert argv[argv.index('--model') + 1] == 'deepseek-flash'
    assert 'small' not in argv
    assert 'Original task' not in argv


def test_explicit_provider_model_pair_survives_matching_scion_model(launcher, monkeypatch):
    module, session, calls = launcher
    monkeypatch.setenv('SCION_MODEL', 'deepseek-flash')
    args = ['--provider', 'deepseek', '--model', 'deepseek-flash', 'Task']
    invoke(monkeypatch, module, args)
    assert calls[0][1][-len(args):] == args


@pytest.mark.parametrize('settings', [None, [], {}, {'defaultProvider': 'deepseek'},
                                    {'defaultProvider': 'deepseek', 'defaultModel': ''}])
def test_missing_model_binding_fails_before_launch(launcher, monkeypatch, settings):
    module, session, calls = launcher
    config = session.parent.parent / 'settings.json'
    if settings is None:
        config.unlink()
    else:
        config.write_text(json.dumps(settings))
    with pytest.raises((ValueError, OSError)):
        invoke(monkeypatch, module, ['Original task'])
    assert not calls


@pytest.mark.parametrize('project', [None, 'test-project'])
def test_claude_sync_uses_native_file_reference_not_credential_argv(tmp_path, monkeypatch, capsys, project):
    module = load('claude_sync_test', 'sync-claude-secret.py')
    credential = 'dummy-private-credential-DO-NOT-PRINT'
    source = tmp_path / 'credentials.json'
    source.write_text(json.dumps({'claudeAiOauth': {'accessToken': credential}}))
    args = ['sync', '--source', str(source)]
    if project:
        args += ['--project-id', project]
    monkeypatch.setattr(sys, 'argv', args)
    calls = []
    def native(argv, **kwargs):
        calls.append(argv)
        return type('Result', (), {'returncode': 0})()
    monkeypatch.setattr(module.subprocess, 'run', native)
    assert module.main() == 0
    assert calls[0][-2:] == ['CLAUDE_AUTH', '@' + str(source)]
    assert credential not in repr(calls)
    assert ('--project=' + project in calls[0]) if project else ('user' in calls[0])
    assert credential not in capsys.readouterr().out


def test_claude_sync_suppresses_native_credential_diagnostics(tmp_path, monkeypatch, capsys):
    module = load('claude_sync_failure_test', 'sync-claude-secret.py')
    secret = 'dummy-sensitive-diagnostic'
    source = tmp_path / 'credentials.json'
    source.write_text(json.dumps({'claudeAiOauth': {'accessToken': secret}}))
    monkeypatch.setattr(sys, 'argv', ['sync', '--source', str(source)])
    def native(*args, **kwargs):
        raise module.subprocess.TimeoutExpired(secret, 45, output=secret)
    monkeypatch.setattr(module.subprocess, 'run', native)
    assert module.main() == 1
    assert secret not in repr(capsys.readouterr())


@pytest.mark.parametrize('document', [[], {}, {'claudeAiOauth': 'invalid'}])
def test_claude_sync_rejects_invalid_login_before_upload(tmp_path, monkeypatch, document):
    module = load('claude_sync_invalid_test', 'sync-claude-secret.py')
    source = tmp_path / 'credentials.json'
    source.write_text(json.dumps(document))
    monkeypatch.setattr(sys, 'argv', ['sync', '--source', str(source)])
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid credentials must not be uploaded')
    monkeypatch.setattr(module.subprocess, 'run', forbidden)
    assert module.main() == 1


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


def test_autonomous_resume_recovers_once_without_initial_task(launcher, monkeypatch):
    module, session, calls = launcher
    persist(session, json.dumps({'type': 'session', 'id': 'dummy-id', 'cwd': str(Path.cwd())}) + '\n')
    monkeypatch.setenv('DESKOPS_AUTONOMOUS', '1')
    invoke(monkeypatch, module, ['--tools', 'read,bash', 'Original task'])
    args = calls[0][1]
    assert args[-1] == module.RECOVERY_PROMPT
    assert 'Original task' not in args
    assert str(session) in args


def test_bridge_loading_respects_no_extensions(launcher, monkeypatch, tmp_path):
    module, session, calls = launcher
    bridge = tmp_path / 'scion-events.ts'
    bridge.write_text('dummy extension')
    monkeypatch.setattr(module, 'BRIDGE', bridge)
    invoke(monkeypatch, module, ['Original task'])
    argv = calls[-1][1]
    assert argv[argv.index('--extension') + 1] == str(bridge)
    assert argv[-1] == 'Original task'
    invoke(monkeypatch, module, ['--no-extensions', 'Review only'])
    assert '--extension' not in calls[-1][1]
