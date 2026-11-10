"""Observe the disposable lab; inject one stop/resume without task prompts."""
import datetime
import json
import pathlib
import subprocess
import time
import urllib.request

PROJECT = 'd7d9d3cd-60a1-46be-9a63-b56722521061'
NAME = 'autonomy-lab-coordinator-v2'
WORKSPACE = pathlib.Path('/mnt/ssd/proyectos/SLDB_1')
ROOT = WORKSPACE / '.tmp/scion-autonomy-lab-v2'
EVIDENCE = pathlib.Path(__file__).resolve().parent
COMMAND = [str(WORKSPACE / '.venv/bin/python'), '/home/robocop/setup/pi/scion/start-desk.py',
           '--root', str(ROOT), '--workspace-root', str(WORKSPACE),
           '--source-root', str(WORKSPACE / 'deskops-wt-scion-autonomy'),
           '--sldb-root', str(WORKSPACE / 'sldb/src'), '--ref', 'HEAD',
           '--project', PROJECT, '--agent', NAME,
           '--templates-dir', '/home/robocop/.scion/project-configs/scion-autonomy-lab__d7d9d3cd/.scion/templates']


def log(event, **data):
    item = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'event': event, **data}
    with (EVIDENCE / 'live-lab-events.jsonl').open('a') as stream:
        stream.write(json.dumps(item) + '\n')
    print(json.dumps(item), flush=True)


def agents():
    token = pathlib.Path.home().joinpath('.scion/dev-token').read_text().strip()
    request = urllib.request.Request('http://127.0.0.1:8080/api/v1/agents?projectId=' + PROJECT,
                                     headers={'Authorization': 'Bearer ' + token})
    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.load(response)
    rows = data.get('agents', data.get('items', [])) if isinstance(data, dict) else data
    return [{k: row.get(k) for k in ['id', 'name', 'slug', 'phase', 'activity', 'labels', 'harnessConfig']}
            for row in rows]


def command(argv):
    result = subprocess.run(argv, cwd=WORKSPACE, capture_output=True, text=True, timeout=180)
    if result.returncode:
        log('command_failed', program=pathlib.Path(argv[0]).name, returncode=result.returncode, diagnostic=result.stderr.strip() if len(argv) > 1 and argv[1].endswith('start-desk.py') else 'subprocess output suppressed')
        raise SystemExit(result.returncode)
    return result.stdout


def main():
    log('initial_bootstrap', output=command(COMMAND).strip())
    prior = None
    fault = False
    events = EVIDENCE / 'live-lab-events.jsonl'
    if events.exists():
        for line in events.read_text().splitlines():
            try:
                event = json.loads(line)
                if event.get('event') == 'fault_resume' and json.loads(event.get('output', '{}')).get('agent') == NAME:
                    fault = True
            except (ValueError, TypeError):
                continue
    deadline = time.monotonic() + 2400
    while time.monotonic() < deadline:
        rows = agents()
        state = json.dumps(rows, sort_keys=True)
        if state != prior:
            log('agents', agents=rows)
            prior = state
        children = [row for row in rows if str(row.get('slug', row.get('name'))).startswith(('deskops-e-', 'deskops-t-'))]
        active_executors = [row for row in children if str(row.get('slug', row.get('name'))).startswith('deskops-e-')
                            and row.get('phase') == 'running' and row.get('activity') != 'completed']
        if active_executors and not fault:
            # Fault injection only; no task or implementation message is sent.
            log('fault_stop', coordinator=NAME, children=active_executors)
            command(['scion', 'stop', NAME, '--project', PROJECT, '--non-interactive'])
            stop_deadline = time.monotonic() + 45
            while time.monotonic() < stop_deadline:
                stopped = next((row for row in agents() if row.get('slug', row.get('name')) == NAME), None)
                if stopped and stopped.get('phase') == 'stopped':
                    break
                time.sleep(1)
            else:
                log('stop_not_observed')
                raise SystemExit(1)
            log('fault_resume', output=command(COMMAND).strip())
            fault = True
        coordinator = next((row for row in rows if row.get('slug', row.get('name')) == NAME), None)
        if coordinator and coordinator.get('activity') == 'completed':
            log('coordinator_completed', fault_injected=fault, children=children)
            return
        time.sleep(5)
    log('deadline_reached', fault_injected=fault)
    raise SystemExit(1)


if __name__ == '__main__':
    main()
