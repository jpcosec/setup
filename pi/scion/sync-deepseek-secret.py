#!/usr/bin/env python3
"""Upload only the local DeepSeek key; never display credentials or API bodies."""
import argparse
import base64
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.home() / '.pi/agent/secrets.env')
    parser.add_argument('--project-id', default='b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7')
    parser.add_argument('--hub', default='http://127.0.0.1:8080')
    parser.add_argument('--token-file', type=Path, default=Path.home() / '.scion/dev-token')
    args = parser.parse_args()
    try:
        hub = urlsplit(args.hub)
        if (hub.scheme not in ('http', 'https') or not hub.hostname or hub.username
                or hub.password or hub.query or hub.fragment):
            raise ValueError()
        if hub.scheme == 'http' and hub.hostname not in ('localhost', '127.0.0.1', '::1'):
            raise ValueError()
        values = []
        for line in args.source.expanduser().read_text().splitlines():
            match = re.match(r'^\s*(?:export\s+)?DEEPSEEK_API_KEY\s*=(.*)$', line)
            if match:
                value = match.group(1).strip()
                if value.startswith(('"', "'")):
                    if len(value) < 2 or value[-1] != value[0]:
                        raise ValueError()
                    value = value[1:-1]
                if not value or '\n' in value or '\r' in value:
                    raise ValueError()
                values.append(value)
        if len(values) != 1:
            raise ValueError()
        token = args.token_file.expanduser().read_text().strip()
        if not token or '\n' in token or '\r' in token:
            raise ValueError()
        payload = {'value': base64.b64encode(values[0].encode()).decode(), 'scope': 'project', 'scopeId': args.project_id,
                   'type': 'environment', 'target': 'DEEPSEEK_API_KEY', 'injectionMode': 'as_needed'}
        request = Request(args.hub.rstrip('/') + '/api/v1/secrets/DEEPSEEK_API_KEY',
                          data=json.dumps(payload).encode(), method='PUT',
                          headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
        # Do not forward credentials through environment proxies or redirects.
        with build_opener(ProxyHandler({}), NoRedirect()).open(request, timeout=30) as response:
            if not 200 <= response.status < 300:
                raise ValueError()
        print('DEEPSEEK_API_KEY scope=project status=synced')
        return 0
    except KeyboardInterrupt:
        print('Secret sync interrupted; no credential details displayed.', file=sys.stderr)
        return 1
    except Exception:
        print('Secret sync failed; check source, token, project and Hub locally. Credential details suppressed.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
