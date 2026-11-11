#!/usr/bin/env python3
"""Project the current Claude login through Scion's native file-secret API."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.home() / '.claude/.credentials.json')
    parser.add_argument('--hub', default='http://127.0.0.1:8080')
    parser.add_argument('--project-id', help='Restrict to this project instead of the current Scion user')
    args = parser.parse_args()
    try:
        hub = urlsplit(args.hub)
        if (hub.scheme not in ('http', 'https') or hub.hostname not in ('127.0.0.1', 'localhost', '::1')
                or hub.username or hub.password or hub.query or hub.fragment):
            raise ValueError('Expected local Hub')
        source = args.source.expanduser().resolve(strict=True)
        document = json.loads(source.read_text())
        if not isinstance(document, dict):
            raise ValueError('Invalid Claude login file')
        credential = document.get('claudeAiOauth', {})
        if not isinstance(credential, dict) or not credential.get('accessToken'):
            raise ValueError('Missing Claude login')
        argv = ['scion', '--hub', args.hub, '--non-interactive', 'hub', 'secret', 'set',
                '--type', 'file', '--target', '/home/scion/.claude/.credentials.json']
        argv += ['--project=' + args.project_id] if args.project_id else ['--scope', 'user']
        # Only a file path goes through argv. Scion reads and stores its contents.
        argv += ['CLAUDE_AUTH', '@' + str(source)]
        result = subprocess.run(argv, env=dict(os.environ, SCION_HUB_ENABLED='true'),
                                capture_output=True, text=True, timeout=45)
        if result.returncode:
            raise ValueError('Native secret sync failed')
        print('CLAUDE_AUTH synced; scope=' + ('project' if args.project_id else 'user'))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError):
        print('Claude auth sync failed; credential values and process diagnostics suppressed.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
