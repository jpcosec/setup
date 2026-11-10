"""Dummy-only bootstrap/extension regressions: no real Hub or task dispatch."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

import pytest

from test_scion_pi_runtime import load, ROOT


def call_git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / 'original'
    root.mkdir()
    call_git(root, 'init')
    (root / 'tracked').write_text('original')
    call_git(root, 'add', '.')
    call_git(root, '-c', 'user.name=Dummy', '-c', 'user.email=dummy@example.invalid', 'commit', '-m', 'fixture')
    return root


def test_owned_worktree_preserves_dirty_original_and_rejects_changed_copy(repo, tmp_path):
    m = load('bootstrap', 'start-desk.py')
    commit = call_git(repo, 'rev-parse', 'HEAD')
    (repo / 'tracked').write_text('dirty original')
    desk, directory = m.owned_worktree(repo, tmp_path, commit)
    assert (desk / 'tracked').read_text() == 'original'
    assert (repo / 'tracked').read_text() == 'dirty original'
    assert m.owned_worktree(repo, tmp_path, commit) == (desk, directory)
    (desk / 'tracked').write_text('changed worktree')
    with pytest.raises(ValueError, match='changed'):
        m.owned_worktree(repo, tmp_path, commit)
    assert (desk / 'tracked').read_text() == 'changed worktree'


def test_unknown_worktree_never_adopted(repo, tmp_path):
    m = load('bootstrap_unknown', 'start-desk.py')
    commit = call_git(repo, 'rev-parse', 'HEAD')
    desk, directory = m.owned_worktree(repo, tmp_path, commit)
    (directory / 'ownership.json').unlink()
    with pytest.raises(ValueError, match='ownership'):
        m.owned_worktree(repo, tmp_path, commit)


def args_for(tmp_path, repo):
    source, sldb = tmp_path / 'source', tmp_path / 'sldb-src'
    (source / 'deskops').mkdir(parents=True)
    (sldb / 'sldb').mkdir(parents=True)
    return argparse.Namespace(root=str(repo), workspace_root=str(tmp_path), source_root=str(source),
                              sldb_root=str(sldb), ref='DOES-NOT-EXIST', project='dummy', agent='dummy-coordinator',
                              templates_dir=str(tmp_path / 'project-config' / '.scion' / 'templates'), hub='http://127.0.0.1:1')


def test_bad_ref_fails_before_any_mutation(repo, tmp_path):
    m = load('bootstrap_bad_ref', 'start-desk.py')
    with pytest.raises(ValueError):
        m.bootstrap(args_for(tmp_path, repo))
    assert not (tmp_path / '.tmp').exists()
    assert call_git(repo, 'worktree', 'list', '--porcelain').count('worktree ') == 1


@pytest.mark.parametrize('field,value', [('root', 'relative'), ('source_root', '/tmp'), ('sldb_root', '/tmp'), ('templates_dir', 'relative')])
def test_invalid_context_paths_fail_before_worktree(repo, tmp_path, field, value):
    m = load('bootstrap_bad_context', 'start-desk.py')
    args = args_for(tmp_path, repo)
    setattr(args, field, value)
    with pytest.raises(ValueError):
        m.bootstrap(args)
    assert not (tmp_path / '.tmp').exists()


def test_reconcile_refuses_foreign_or_duplicate_identity():
    m = load('bootstrap_reconcile', 'start-desk.py')
    labels = {'deskops.desk': 'dummy', 'deskops.role': 'coordinator'}
    agent = {'name': 'dummy-coordinator', 'labels': labels, 'phase': 'running'}
    assert m.reconcile([], 'dummy-coordinator', labels) == 'start'
    assert m.reconcile([agent], 'dummy-coordinator', labels) == 'existing'
    assert m.reconcile([{**agent, 'phase': 'stopped'}], 'dummy-coordinator', labels) == 'resume'
    for agents in [[agent, agent], [{**agent, 'labels': {}}], [{**agent, 'name': 'other'}], [{**agent, 'phase': 'error'}], [None]]:
        with pytest.raises(ValueError):
            m.reconcile(agents, 'dummy-coordinator', labels)


def test_bridge_native_callbacks_and_payload_redaction(tmp_path):
    node = shutil.which('node')
    if not node or int(subprocess.check_output([node, '--version'], text=True).split('.')[0][1:]) < 22:
        pytest.skip('Node22 required to execute pinned runtime extension source')
    bridge = (ROOT / 'scion-events.ts').as_uri()
    script = f'''
import assert from 'node:assert/strict';
import {{EventEmitter}} from 'node:events';
import extension, {{emit, payload}} from {json.dumps(bridge)};
const callbacks = new Map();
extension({{on:(name, callback)=>callbacks.set(name, callback)}});
assert.deepEqual([...callbacks.keys()], ['session_start','input','agent_start','agent_end','tool_execution_start','tool_execution_end']);
for (const [type, expected] of Object.entries({{session_start:'SessionStart',input:'UserPromptSubmit',agent_start:'agent-start',agent_end:'Stop',tool_execution_start:'PreToolUse',tool_execution_end:'PostToolUse'}})) {{
  const event = {{type, text:'SECRET',args:{{secret:'SECRET'}},result:'SECRET',messages:['SECRET'],toolName:'bash',toolCallId:'dummy:1'}};
  assert.equal(payload(event).hook_event_name, expected);
  assert.ok(!JSON.stringify(payload(event)).includes('SECRET'));
}}
assert.equal(payload({{type:'message_end',message:'SECRET'}}),undefined);
assert.deepEqual(payload({{type:'tool_execution_start',toolName:'SECRET arbitrary text',toolCallId:'SECRET arbitrary text'}}),{{hook_event_name:'PreToolUse'}});
let sent;
const run = (binary,args,opts)=>{{
 assert.equal(binary,'sciontool'); assert.deepEqual(args,['hook','--dialect=claude']);
 assert.deepEqual(opts.stdio,['pipe','ignore','ignore']);
 const child = new EventEmitter(); child.stdin = new EventEmitter();
 child.stdin.end=(data)=>{{sent=JSON.parse(data); queueMicrotask(()=>child.emit('close',0));}};
 return child;
}};
assert.equal(await emit({{type:'agent_end',messages:['SECRET']}},run),true);
assert.deepEqual(sent,{{hook_event_name:'Stop'}});
assert.equal(await emit({{type:'input'}},()=>{{throw Error('SECRET')}}),false);
let killed = false;
assert.equal(await emit({{type:'input'}},()=>{{
 const child = new EventEmitter(); child.stdin = new EventEmitter();
 child.stdin.end=()=>{{}}; child.kill=(signal)=>{{assert.equal(signal,'SIGKILL'); killed=true;}};
 return child;
}}),false);
assert.equal(killed,true);
// Execute all registered handlers with a fake sciontool from the test's PATH.
for(const [type, callback] of callbacks) await callback({{type,toolName:'bash',toolCallId:'dummy-1',args:'SECRET',result:'SECRET',text:'SECRET'}});
'''
    tool = tmp_path / 'sciontool'
    output = tmp_path / 'events.jsonl'
    tool.write_text('#!/usr/bin/env python3\nimport sys\nwith open(' + repr(str(output)) + ', "a") as f: f.write(sys.stdin.read()+"\\n")\n')
    tool.chmod(0o755)
    import os
    result = subprocess.run([node, '--experimental-strip-types', '--input-type=module', '-e', script],
                            env={**os.environ, 'PATH': str(tmp_path) + os.pathsep + os.environ['PATH']},
                            text=True, capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    events = [json.loads(line) for line in output.read_text().splitlines()]
    assert len(events) == 6
    assert 'SECRET' not in output.read_text()


def test_bootstrap_dummy_commands_bind_context_and_reconcile_once(repo, tmp_path, monkeypatch):
    m = load('bootstrap_dummy', 'start-desk.py')
    args = args_for(tmp_path, repo)
    args.ref = 'HEAD'
    source, sldb = Path(args.source_root), Path(args.sldb_root)
    env = {'PYTHONPATH': str(source) + ':' + str(sldb)}
    commit = call_git(repo, 'rev-parse', 'HEAD')
    source_revision = ['dummy-source-revision']
    monkeypatch.setattr(m, 'validate', lambda a: (tmp_path, repo, source, sldb, commit, source_revision[0], env))
    commands = []
    sync_roots = []
    state = []

    def fake_run(command, *, cwd, env):
        command = list(map(str, command))
        commands.append(command)
        if command[:2] in (['scion', 'start'], ['scion', 'resume']):
            # Start also resolves a local same-named template before Hub lookup.
            assert Path(cwd) / '.scion' / 'templates' == Path(args.templates_dir)
        if command[:3] == ['scion', 'templates', 'sync']:
            # Native CLI selects the local source from cwd, not --project.
            assert Path(cwd) / '.scion' / 'templates' == Path(args.templates_dir)
            sync_roots.append(str(cwd))
        if command[:2] == ['scion', 'list']:
            return json.dumps(state)
        if command[:2] == ['scion', 'start']:
            labels = dict(command[i + 1].split('=', 1) for i, v in enumerate(command) if v == '--label')
            state.append({'name': args.agent, 'labels': labels, 'phase': 'running'})
        return ''

    original_run = m.run
    # Keep actual Git operations confined to this disposable fixture.
    monkeypatch.setattr(m, 'run', lambda command, **kwargs: original_run(command, **kwargs)
                        if command[0] == 'git' else fake_run(command, **kwargs))
    first = m.bootstrap(args)
    assert first['action'] == 'start'
    provenance = json.loads(Path(first['provenance']).read_text())
    context = json.loads((Path(first['provenance']).parent / 'context.json').read_text())
    assert set(context) == {'project', 'workspace_root', 'desk_root', 'source_root', 'sldb_root'}
    assert provenance['source_commit'] == 'dummy-source-revision'
    assert context['sldb_root'] == str(sldb)
    template_commands = [c for c in commands if 'template' in c]
    assert len(template_commands) == 3
    assert len(sync_roots) == 3
    assert {c[c.index('--mode') + 1] for c in template_commands} == {'coordinator', 'executor', 'tester'}
    assert all('--context-file' in c for c in template_commands)
    # Generic initialized desks have no implementation RoleDocs/profiles.
    # Materialize from tested source; context still targets the data worktree.
    assert not (Path(context['desk_root']) / 'desk' / 'roles').exists()
    assert all(c[c.index('--root') + 1] == str(source) for c in template_commands)
    assert all(c[c.index('--task-repo') + 1] == repo.name for c in template_commands)
    assert context['desk_root'] != str(source)
    start = next(c for c in commands if c[:2] == ['scion', 'start'])
    assert json.loads(Path(start[start.index('--config') + 1]).read_text()) == {'env': {'DESKOPS_AUTONOMOUS': '1'}}
    assert start[start.index('--workspace') + 1] == str(tmp_path)
    source_revision[0] = 'new-doc-only-commit'
    (source / 'docs').mkdir()
    (source / 'docs' / 'notes.md').write_text('metadata outside runtime')
    assert m.bootstrap(args)['action'] == 'existing'
    for package in (source / 'deskops', sldb / 'sldb'):
        changed = package / 'uncommitted-runtime.py'
        changed.write_text('changed runtime source')
        with pytest.raises(ValueError, match='provenance'):
            m.bootstrap(args)
        assert changed.read_text() == 'changed runtime source'
        changed.unlink()
    assert len([c for c in commands if c[:2] == ['scion', 'start']]) == 1
    owned = Path(context['desk_root'])
    (owned / 'tracked').write_text('completed first task')
    call_git(owned, 'add', 'tracked')
    call_git(owned, '-c', 'user.name=Dummy', '-c', 'user.email=dummy@example.invalid', 'commit', '-m', 'own closeout')
    (owned / 'in-progress-evidence').write_text('paused child evidence')
    state[0]['phase'] = 'stopped'
    args.ref = 'origin/main-vanished'
    assert m.bootstrap(args)['action'] == 'resume'
    assert (owned / 'in-progress-evidence').read_text() == 'paused child evidence'
    assert (owned / 'tracked').read_text() == 'completed first task'
    assert call_git(repo, 'worktree', 'list', '--porcelain').count('worktree ') == 2
    args.project = 'mismatched-project'
    with pytest.raises(ValueError):
        m.bootstrap(args)
    args.project = 'dummy'
    context_file = Path(first['provenance'])
    bad = json.loads(context_file.read_text())
    bad['source_content'] = {'deskops': 'mismatch', 'sldb': 'mismatch'}
    context_file.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match='provenance'):
        m.bootstrap(args)
    assert (owned / 'in-progress-evidence').read_text() == 'paused child evidence'
    resume = next(c for c in commands if c[:2] == ['scion', 'resume'])
    assert '--config' in resume
    assert len([c for c in commands if c[:2] == ['scion', 'start']]) == 1


def test_import_verification_failure_prevents_runtime_mutation(repo, tmp_path, monkeypatch):
    m = load('bootstrap_import_failure', 'start-desk.py')
    args = args_for(tmp_path, repo)
    args.ref = 'HEAD'
    args.source_root = str(repo)
    (repo / 'deskops').mkdir()
    original_run = m.run

    def fail_import(command, **kwargs):
        if command[0] != 'git':
            raise ValueError('dummy import mismatch')
        return original_run(command, **kwargs)

    monkeypatch.setattr(m, 'run', fail_import)
    with pytest.raises(ValueError, match='mismatch'):
        m.bootstrap(args)
    assert not (tmp_path / '.tmp').exists()


@pytest.mark.parametrize('kind', ['python', 'data', 'untracked'])
def test_package_fingerprint_detects_runtime_changes_but_ignores_cache(tmp_path, kind):
    m = load('bootstrap_fingerprint', 'start-desk.py')
    package = tmp_path / 'package'
    package.mkdir()
    (package / 'runtime.py').write_text('runtime = 1')
    (package / 'schema.json').write_text('{"version": 1}')
    baseline = m.package_fingerprint(package)
    (package / '__pycache__').mkdir()
    (package / '__pycache__' / 'runtime.pyc').write_bytes(b'generated cache')
    (package / 'ignored.pyc').write_bytes(b'bytecode')
    assert m.package_fingerprint(package) == baseline
    name = {'python': 'runtime.py', 'data': 'schema.json', 'untracked': 'new-helper.py'}[kind]
    (package / name).write_text('changed actual runtime')
    assert m.package_fingerprint(package) != baseline
    assert (package / name).read_text() == 'changed actual runtime'


def test_new_start_missing_ref_rejects_after_reconcile_before_mutation(repo, tmp_path, monkeypatch):
    m = load('bootstrap_missing_ref_after_reconcile', 'start-desk.py')
    args = args_for(tmp_path, repo)
    source, sldb = Path(args.source_root), Path(args.sldb_root)
    monkeypatch.setattr(m, 'validate', lambda a: (tmp_path, repo, source, sldb, None, 'dummy', {}))
    original = m.run
    queries = []

    def fake_run(command, **kwargs):
        if command[0] == 'git':
            return original(command, **kwargs)
        queries.append(command)
        assert command[:2] == ['scion', 'list']
        return '[]'

    monkeypatch.setattr(m, 'run', fake_run)
    with pytest.raises(ValueError):
        m.bootstrap(args)
    assert len(queries) == 1
    assert not (tmp_path / '.tmp').exists()
    assert call_git(repo, 'worktree', 'list', '--porcelain').count('worktree ') == 1


def test_bootstrap_command_failure_reports_stage_without_output(tmp_path, monkeypatch):
    m = load('bootstrap_safe_stage', 'start-desk.py')
    secret = 'private-command-output-do-not-display'
    def failed(*args, **kwargs):
        raise subprocess.CalledProcessError(19, args[0], output=secret, stderr=secret)
    monkeypatch.setattr(m.subprocess, 'run', failed)
    with pytest.raises(ValueError, match='scion templates.*exit 19') as error:
        m.run(['scion', 'templates', 'sync', secret], cwd=tmp_path)
    assert secret not in str(error.value)
