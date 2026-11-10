#!/usr/bin/env python3
"""Explicit, fail-closed bootstrap; Scion owns agents, DeskOps owns workflow."""
import argparse
import hashlib
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys


DEFAULT_SOURCE = '/mnt/ssd/proyectos/SLDB_1/deskops-runtime'
DEFAULT_SLDB = '/mnt/ssd/proyectos/SLDB_1/sldb/src'


def run(args, *, cwd, env=None):
    # Capture diagnostics, never print subprocess output (may contain auth data).
    try:
        return subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True,
                              text=True, capture_output=True, timeout=120).stdout.strip()
    except (subprocess.SubprocessError, OSError) as exc:
        parts = list(map(str, args))
        if parts[0] == 'scion' and len(parts) > 1 and parts[1] in {'list', 'start', 'resume', 'templates'}:
            stage = 'scion ' + parts[1]
        elif parts[0] == 'git':
            stage = 'git'
        elif parts[1:3] == ['-m', 'deskops']:
            stage = 'deskops template'
        else:
            stage = 'source import check'
        reason = ('exit ' + str(exc.returncode)) if isinstance(exc, subprocess.CalledProcessError) else ('timeout' if isinstance(exc, subprocess.TimeoutExpired) else 'unavailable')
        raise ValueError(f'Bootstrap {stage} failed ({reason}); command arguments and output suppressed') from exc


def git(root, *args):
    return run(['git', '-C', root, *args], cwd=root)


def absolute(value, workspace=None):
    path = Path(value)
    if not path.is_absolute() or not path.is_dir():
        raise ValueError('Required path must be an existing absolute directory')
    path = path.resolve()
    if workspace is not None and not path.is_relative_to(workspace):
        raise ValueError('Runtime paths must stay inside workspace root')
    return path


def validate(args):
    workspace = absolute(args.workspace_root)
    root = absolute(args.root, workspace)
    source = absolute(args.source_root, workspace)
    sldb = absolute(args.sldb_root, workspace)
    templates = Path(args.templates_dir).expanduser()
    if (not templates.is_absolute() or templates.is_symlink()
            or templates.name != 'templates' or templates.parent.name != '.scion'):
        raise ValueError('Template directory must be an explicit absolute project .scion/templates path')
    if not args.project or not args.agent or any(c.isspace() for c in args.project + args.agent):
        raise ValueError('Explicit project and agent identities are required')
    if not args.hub.startswith(('http://', 'https://')):
        raise ValueError('Hub must be an HTTP URL')
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise ValueError('Desk root must be a Git worktree root')
    # The explicit ref is resolved only for NEW starts, after reconciliation.
    # Known-owned recovery uses the recorded base even when that ref vanished.
    commit = None
    if Path(git(source, 'rev-parse', '--show-toplevel')).resolve() != source:
        raise ValueError('Source root must identify its Git checkout')
    source_commit = git(source, 'rev-parse', '--verify', 'HEAD^{commit}')
    if not (source / 'deskops').is_dir() or not (sldb / 'sldb').is_dir():
        raise ValueError('Source roots do not contain DeskOps/SLDB packages')
    env = dict(os.environ, PYTHONPATH=f'{source}{os.pathsep}{sldb}',
               SCION_HUB_ENABLED='true', SCION_HUB_ENDPOINT=args.hub)
    # Check the actual imports rather than accepting old baked wheels.
    check = ('import deskops,sldb; from pathlib import Path; '
             'assert Path(deskops.__file__).resolve().is_relative_to(Path(' + repr(str(source)) + ')); '
             'assert Path(sldb.__file__).resolve().is_relative_to(Path(' + repr(str(sldb)) + '))')
    run([sys.executable, '-c', check], cwd=workspace, env=env)
    return workspace, root, source, sldb, commit, source_commit, env


def owned_worktree(root, workspace, commit, *, recovery=False):
    common = str(Path(git(root, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve())
    key = hashlib.sha256((common + '\0' + str(root)).encode()).hexdigest()[:16]
    directory = workspace / '.tmp' / 'scion-bootstrap' / key
    if directory.is_symlink() or not directory.resolve().is_relative_to(workspace):
        raise ValueError('Bootstrap directory must stay inside workspace')
    target, marker = directory / 'desk', directory / 'ownership.json'
    expected = {'git_common_dir': common, 'base_commit': commit,
                'original_root': str(root), 'worktree': str(target)}
    if target.exists() or marker.exists():
        if not marker.is_file() or marker.is_symlink() or not target.is_dir() or target.is_symlink():
            raise ValueError('Refusing unknown bootstrap worktree ownership')
        recorded = json.loads(marker.read_text())
        if (not isinstance(recorded, dict) or set(recorded) != set(expected)
                or any(recorded.get(k) != expected[k] for k in expected if k != 'base_commit')
                or not isinstance(recorded.get('base_commit'), str)):
            raise ValueError('Refusing unknown bootstrap worktree ownership')
        # Own closeout commits may advance HEAD. Never follow a newly moving ref,
        # reset/rebase the desk or discard child evidence during recovery.
        git(target, 'merge-base', '--is-ancestor', recorded['base_commit'], 'HEAD')
        if (str(Path(git(target, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()) != common
                or (not recovery and git(target, 'status', '--porcelain'))):
            raise ValueError('Owned worktree changed; refusing reset or implicit reuse')
        return target, directory
    if recovery:
        raise ValueError('Existing coordinator has no owned bootstrap worktree')
    directory.mkdir(parents=True, exist_ok=False)
    git(root, 'worktree', 'add', '--detach', str(target), commit)
    marker.write_text(json.dumps(expected, indent=2) + '\n')
    return target, directory


def reconcile(agents, name, labels):
    if (not isinstance(agents, list) or any(not isinstance(a, dict)
            or not isinstance(a.get('labels', {}), dict) for a in agents)):
        raise ValueError('Malformed Scion agent listing')
    owned = [a for a in agents if all(a.get('labels', {}).get(k) == v for k, v in labels.items())]
    if len(owned) > 1:
        raise ValueError('Duplicate coordinator ownership')
    matches = [a for a in agents if a.get('slug', a.get('name')) == name or a.get('name') == name]
    if len(matches) > 1:
        raise ValueError('Duplicate coordinator identities')
    if not matches:
        if any(all(a.get('labels', {}).get(k) == v for k, v in labels.items()) for a in agents):
            raise ValueError('Coordinator ownership already exists under another name')
        return 'start'
    agent = matches[0]
    if any(agent.get('labels', {}).get(k) != v for k, v in labels.items()):
        raise ValueError('Coordinator name belongs to another run')
    phase = agent.get('phase')
    if phase in ('running', 'starting', 'provisioning'):
        return 'existing'
    if phase == 'stopped':
        return 'resume'
    raise ValueError('Coordinator requires explicit operator recovery')


def package_fingerprint(package):
    """Hash actual runtime code/data, excluding generated caches and bytecode."""
    digest = hashlib.sha256()
    excluded = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.git'}
    for directory, dirs, files in os.walk(package, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excluded)
        for name in [*dirs, *sorted(files)]:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValueError('Runtime package symlinks are not supported')
        for name in sorted(files):
            if name.endswith(('.pyc', '.pyo')):
                continue
            path = Path(directory) / name
            relative = path.relative_to(package).as_posix().encode()
            content = path.read_bytes()
            digest.update(len(relative).to_bytes(8, 'big') + relative)
            digest.update((path.stat().st_mode & 0o111).to_bytes(2, 'big'))
            digest.update(len(content).to_bytes(8, 'big') + content)
    return digest.hexdigest()


def bootstrap(args):
    # Lock the original directory inode: no lock-file creation, no scheduler,
    # and concurrent invocations re-read Scion state after acquiring the lock.
    root = absolute(args.root)
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        return _bootstrap_locked(args)
    finally:
        os.close(descriptor)


def _bootstrap_locked(args):
    workspace, root, source, sldb, commit, source_commit, env = validate(args)
    template_context = Path(args.templates_dir).expanduser().parent.parent
    identity = hashlib.sha256((args.project + '\0' + str(root)).encode()).hexdigest()[:16]
    labels = {'deskops.desk': identity, 'deskops.role': 'coordinator'}
    agents = json.loads(run(['scion', 'list', '--project', args.project, '--format', 'json'], cwd=workspace, env=env))
    action = reconcile(agents, args.agent, labels)
    if action == 'start':
        commit = git(root, 'rev-parse', '--verify', args.ref + '^{commit}')
    source_content = {'deskops': package_fingerprint(source / 'deskops'),
                      'sldb': package_fingerprint(sldb / 'sldb')}
    desk, directory = owned_worktree(root, workspace, commit, recovery=action != 'start')
    override_file = directory / 'coordinator-config.json'
    context = {'project': args.project, 'workspace_root': str(workspace),
               'desk_root': str(desk), 'source_root': str(source), 'sldb_root': str(sldb)}
    if action != 'start':
        previous = json.loads((directory / 'provenance.json').read_text())
        ownership = json.loads((directory / 'ownership.json').read_text())
        if (not isinstance(previous, dict)
                or previous.get('desk_commit') != ownership['base_commit']
                or json.loads((directory / 'context.json').read_text()) != context
                or any(previous.get(k) != v for k, v in context.items())
                or previous.get('source_content') != source_content
                or previous.get('agent') != args.agent
                or json.loads(override_file.read_text()) != {'env': {'DESKOPS_AUTONOMOUS': '1'}}):
            raise ValueError('Existing coordinator provenance differs from explicit runtime context')
        if action == 'resume':
            run(['scion', 'resume', args.agent, '--project', args.project,
                 '--config', override_file, '--non-interactive'], cwd=template_context, env=env)
        return {'action': action, 'agent': args.agent, 'provenance': str(directory / 'provenance.json')}
    context_file = directory / 'context.json'
    context_file.write_text(json.dumps(context, indent=2) + '\n')
    provenance = {'agent': args.agent, 'desk_commit': commit, 'source_commit': source_commit, 'source_content': source_content, 'ref': args.ref, **context}
    (directory / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    templates = Path(args.templates_dir).expanduser()
    if not templates.is_absolute():
        raise ValueError('Template directory must be absolute')
    for mode, role in [('executor', 'executor'), ('tester', 'tester'), ('coordinator', 'supervisor')]:
        name = f'deskops-{mode}'
        run([sys.executable, '-m', 'deskops', 'runtime', 'template', f'role-deskops-{role}',
             '--root', source, '--harness', 'pi', '--out', templates / name,
             '--task-repo', root.name, '--mode', mode, '--context-file', context_file], cwd=workspace, env=env)
        # Scion v0.2.21 resolves LOCAL template sources from cwd, independently
        # of --project (which chooses the Hub destination). Avoid another project's
        # same-named template by resolving from this explicit project config root.
        run(['scion', 'templates', 'sync', name, '--project', args.project, '--non-interactive'],
            cwd=templates.parent.parent, env=env)
    override_file = directory / 'coordinator-config.json'
    override_file.write_text(json.dumps({'env': {'DESKOPS_AUTONOMOUS': '1'}}) + '\n')
    if source_content != {'deskops': package_fingerprint(source / 'deskops'),
                          'sldb': package_fingerprint(sldb / 'sldb')}:
        raise ValueError('Runtime package contents changed during bootstrap')
    if action == 'start':
        prompt = (f'Coordinate the authorized desk at {desk} autonomously using its board and gates. '
                  'Recover durable state and existing children before dispatch. Execute ready tasks '
                  'through independent testing, declared closeout and phase reconciliation until '
                  'complete or genuinely blocked. Scion owns child sessions; DeskOps owns lifecycle. '
                  'Use configured source tools and explicit project/workspace. Do not ask for per-step prompts.')
        command = ['scion', 'start', args.agent, prompt, '--type', 'deskops-coordinator',
                   '--project', args.project, '--workspace', workspace, '--config', override_file, '--harness-auth', 'api-key', '--non-interactive']
        for key, value in labels.items():
            command.extend(['--label', f'{key}={value}'])
        run(command, cwd=template_context, env=env)
    return {'action': action, 'agent': args.agent, 'provenance': str(directory / 'provenance.json')}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True)
    p.add_argument('--source-root', default=DEFAULT_SOURCE)
    p.add_argument('--sldb-root', default=DEFAULT_SLDB)
    p.add_argument('--workspace-root', required=True)
    p.add_argument('--project', required=True)
    p.add_argument('--agent', required=True)
    p.add_argument('--templates-dir', required=True)
    p.add_argument('--ref', default='origin/main')
    p.add_argument('--hub', default='http://127.0.0.1:8080')
    return p


def main():
    try:
        print(json.dumps(bootstrap(parser().parse_args())))
        return 0
    except (ValueError, OSError) as exc:
        print(f'Scion bootstrap refused: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
