FILE:desk/tasks/task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge.md
---
id: task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- 18c0007
- tests/test_scion_autonomy.py
- tests/test_scion_pi_runtime.py
- desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
- runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json
depends_on: []
pills: []
files:
- pi/scion/Dockerfile
- pi/scion/harness-config.yaml
- pi/scion/launch.py
- pi/scion/provision.py
- pi/scion/scion-events.ts
- pi/scion/start-desk.py
- pi/scion/README.md
- pi/README.md
- tests/test_scion_pi_runtime.py
- tests/test_scion_autonomy.py
- desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-runtime-bootstrap.md
---

# Scion autonomy runtime bootstrap and Pi lifecycle bridge

## Rationale

_Explain why this task exists or the business driver behind it._

The first coordinator required manual checkout, CLI and state interventions and looped on false review status; native Pi events are not yet connected to Scion.

## Goal

_Describe the concrete result this task must produce._

A reproducible Scion start uses intended current desk/tools, valid worktree paths and a native Pi event bridge so a disposable authorized desk can run without manual prompts through child execution, independent test and closeout/continuation.

## Scope

_State what is in scope and what is out of scope._

setup/pi/scion runtime recipes, lifecycle extension/config, source/root binding and tests/docs/atom. Preserve Scion0.2.21 and pinned Pi fork, secrets, session continuity and unrelated agents; no pi-subagents or new workflow engine. Do not dispatch production tasks in validation.

## Implementation Path

_Outline the expected implementation route or affected surface._

Runtime constants: Scion0.2.21; Pi jpcosec/pi-mono e9ba9e2ebce1b49dca85ab20007038c06e486ea5; project sldb-1 UUID b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7; host workspace /mnt/ssd/proyectos/SLDB_1. start-desk.py accepts explicit desk/source/ref/project/workspace/agent options, validates paths and provenance, chooses a clean dedicated worktree of configured canonical ref (origin/main default) without resetting dirty originals and reuses it only when ownership is known. Mount workspace both at /workspace and its real host absolute path via supported Scion volumes, not manual symlinks. Explicit source roots via PYTHONPATH bind tested DeskOps source and /mnt/ssd/proyectos/SLDB_1/sldb/src; verify actual imports before start, never silently use baked stale wheels. User CLI authenticates bootstrap through configured Hub, children use their Scion agent tokens and DeepSeek project secret, never secrets.env mounted. Pi extension maps input/session/agent/tool events to existing sciontool hook Claude dialect events; emit no prompt/tool argument or credential content; generic agent_end is not completed. Reuse sciontool metadata proactive token refresh, verify a real own-agent refresh and preserve tokens without logging; no new refresher service. Stable coordinator/child labels and run identity reconcile before start. Independent tester mode/source contract comes from the DeskOps task branch and is an integration prerequisite. Disposable real Git desk under workspace .tmp, two bounded code tasks with explicit expected functions/tests and dependency, one initial assignment and zero followup messages. Automated fixture may inject one controlled validation/child failure and stop/resume; evidence must show correct refusal to close on failure, recovery, no duplicate child, independent tester, one closeout per task and phase completion. Do not dispatch production tasks. Register source atom before docs and save all sanitized integration evidence. Concrete configured defaults: operator supplies --root (integration fixture /mnt/ssd/proyectos/SLDB_1/.tmp/scion-autonomy-lab); --source-root defaults /mnt/ssd/proyectos/SLDB_1/deskops-runtime, the stable deployment worktree advanced by the project coordinator to tested main; validation used fix/scion-autonomy before integration; --sldb-root /mnt/ssd/proyectos/SLDB_1/sldb/src. Ref configured solely by --ref (origin/main default; HEAD explicit in fixture), validate via git rev-parse --verify ref^{commit}; fail before mutation if missing, never silent fallback or origin rewriting. Hub default http://127.0.0.1:8080; bootstrap uses existing CLI auth, children own agent tokens. --context-file JSON interface is produced by source task on fix/scion-autonomy; its final commit is a future dependency output, not a missing operator decision. Fixture has two tasks adding greet/farewell with real pytest assertions and explicit dependency. A validation command has one deterministic transient failure; successful retry must still verify actual function outputs. Automated stop/resume injection uses zero parent followup messages; assert one project/task/role child identity and separate executor/tester identities.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests
- fresh real Scion coordinator/executor/tester on disposable desk completes closeout and next task without messages
- restart preserves session and no duplicate child

## Done When

_Name the observable condition that makes the task complete._

Runtime state reflects actual work; clean startup uses correct source and Git paths; unattended disposable-desk loop passes; source docs and exact evidence committed. No claim of success from a running container alone.

FILE:desk/rituals/execution.md
---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for setup.

FILE:desk/rituals/testing.md
---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when setup changes shared behavior.

FILE:desk/rituals/closeout.md
---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a setup task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.

FILE:pi/scion/Dockerfile
# Build context: source-only pi-mono checkout, locally built wheels/, and uv.
# The base is the existing Scion image, retained at its original version.
ARG BASE_IMAGE=scion-pi:latest
FROM ${BASE_IMAGE}
USER root
ARG PI_COMMIT=e9ba9e2ebce1b49dca85ab20007038c06e486ea5
LABEL io.setup.pi.source="https://github.com/jpcosec/pi-mono" \
      io.setup.pi.revision="${PI_COMMIT}" \
      io.setup.pi.version="0.67.3"

# All Pi packages resolve to the fork's locked local workspaces.
RUN npm uninstall -g @mariozechner/pi-coding-agent
COPY pi-mono/ /opt/pi-mono/
WORKDIR /opt/pi-mono
RUN npm ci --no-audit --no-fund \
 && ./node_modules/.bin/tsgo -p packages/tui/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/ai/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/agent/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/coding-agent/tsconfig.build.json \
 && npm run copy-assets --workspace @mariozechner/pi-coding-agent \
 && chmod +x packages/coding-agent/dist/cli.js \
 && ln -s /opt/pi-mono/packages/coding-agent/dist/cli.js /usr/local/bin/pi \
 && test "$(pi --version 2>&1)" = 0.67.3

# DeskOps requires Python 3.12; the existing image's system Python is 3.11.
# Wheels come from source-only snapshots of the local SLDB and DeskOps checkouts.
COPY uv /usr/local/bin/uv
COPY wheels/ /opt/setup-wheels/
ENV UV_PYTHON_INSTALL_DIR=/opt/python
RUN uv venv --python 3.12 /opt/deskops-tools \
 && uv pip install --python /opt/deskops-tools/bin/python /opt/setup-wheels/*.whl pytest==9.2.0 \
 && chmod -R a+rX /opt/python /opt/deskops-tools
ENV PATH="/opt/deskops-tools/bin:${PATH}"
COPY launch.py scion-events.ts /usr/local/lib/scion-pi/
RUN deskops --help >/dev/null && sldb --help >/dev/null
WORKDIR /workspace
CMD ["pi"]

FILE:pi/scion/harness-config.yaml
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Pi built from jpcosec/pi-mono e9ba9e2ebce1b49dca85ab20007038c06e486ea5, modelled on
# the opencode bundle. DeepSeek Flash is the default model.
harness: pi
image: scion-pi-fork:e9ba9e2
user: scion
provisioner:
  type: container-script
  interface_version: 1
  lib: vendored
  command: ["python3", "/home/scion/.scion/harness/provision.py"]
  timeout: 30s
  lifecycle_events:
    - pre-start
  required_image_tools:
    - python3
    - pi
config_dir: .pi/agent
interrupt_key: C-c
# Native lifecycle events are delivered by the explicit launcher extension.
# pi reads AGENTS.md (cwd and parents, plus ~/.pi/agent/AGENTS.md).
instructions_file: AGENTS.md
system_prompt_file: AGENTS.md
system_prompt_mode: prepend_to_instructions
# provision.py resolves SCION_MODEL through these aliases and writes the result
# to ~/.pi/agent/settings.json (defaultProvider/defaultModel). The model is NOT
# pinned on the command line: a --model flag there would override the alias.
model_aliases:
  small: deepseek-flash
  medium: deepseek-flash
  large: deepseek-v4-pro
  extra-large: deepseek-v4-pro
command:
  # `pi [messages...]`: an initial task is a positional message, so it goes
  # after the base args. Provider/model come from settings.json (see above).
  base: ["python3", "/usr/local/lib/scion-pi/launch.py"]
  resume_flag: "--continue"
  task_position: after_base_args
capabilities:
  limits:
    max_turns: { support: "no", reason: "native event bridge does not enforce turn limits" }
    max_model_calls: { support: "no", reason: "pi emits no model-start/model-end hook events" }
    max_duration: { support: "yes" }
  telemetry:
    enabled: { support: "no", reason: "lifecycle/status hooks only; no OTel instrumentation" }
    native_emitter: { support: "no", reason: "pi has no native OTel emitter" }
  prompts:
    system_prompt: { support: "partial", reason: "System prompt is downgraded into AGENTS.md" }
    agent_instructions: { support: "yes" }
  auth:
    api_key: { support: "yes" }
    auth_file: { support: "yes" }
    oauth_token: { support: "no", reason: "scion does not stage pi OAuth tokens; use an auth-file captured from `pi /login`" }
    vertex_ai: { support: "no", reason: "The pi bundle only configures the DeepSeek provider" }
  mcp:
    stdio: { support: "no", reason: "pi has no MCP client" }
    sse: { support: "no", reason: "pi has no MCP client" }
    streamable_http: { support: "no", reason: "pi has no MCP client" }
    project_scope: { support: "no", reason: "pi has no MCP client" }
  resume: { support: "yes" }
no_auth:
  behavior: drop-to-shell
  command: pi
  message: |
    This agent started without credentials.
    Either restart it with DEEPSEEK_API_KEY available to scion, or
    run `pi`, use /login, then run:
      python3 /home/scion/.scion/harness/capture_auth.py
auth:
  default_type: api-key
  types:
    api-key:
      required_env:
        - any_of: ["DEEPSEEK_API_KEY"]
    auth-file:
      required_files:
        - name: PI_AUTH
          type: file
          target_suffix: "/.pi/agent/auth.json"
          field: PiAuthFile
  autodetect:
    env:
      DEEPSEEK_API_KEY: api-key
    files:
      PI_AUTH: auth-file

FILE:pi/scion/launch.py
#!/usr/bin/env python3
"""Keep one Pi conversation per Scion agent, including Docker stop/resume."""
import json
import os
from pathlib import Path
import sys


BRIDGE = Path("/usr/local/lib/scion-pi/scion-events.ts")
RECOVERY_PROMPT = ("Resume autonomous desk coordination from durable DeskOps state. "
                   "Reconcile existing Scion children before dispatch; inspect their evidence, "
                   "continue independent testing and declared closeout gates. "
                   "Do not replay the initial task or create duplicate children. "
                   "If the phase is complete or a real blocker remains, report it through sciontool.")


VALUE_FLAGS = {
    "--provider", "--model", "--tools", "-t", "--thinking", "--models",
    "--system-prompt", "--append-system-prompt", "--extension", "-e",
    "--skill", "--prompt-template", "--theme",
}
SWITCH_FLAGS = {
    "--offline", "--verbose", "--no-tools", "-nt", "--no-extensions", "-ne",
    "--no-skills", "-ns", "--no-prompt-templates", "-np", "--no-themes",
    "--no-context-files", "-nc",
}


def options_only(args):
    """Retain harness options, but never replay the initial positional task."""
    result = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--continue", "-c", "--resume", "-r"):
            i += 1
            continue
        if arg in VALUE_FLAGS:
            if i + 1 == len(args):
                raise ValueError("Missing Pi option value")
            result.extend(args[i:i + 2])
            i += 2
        elif arg in SWITCH_FLAGS:
            result.append(arg)
            i += 1
        elif arg.startswith("-"):
            raise ValueError("Unsupported Pi option on resume; inspect harness configuration")
        else:
            i += 1
    return result


def main():
    args = sys.argv[1:]
    if any(arg.split("=", 1)[0] in ("--session", "--session-dir", "--no-session", "--fork") for arg in args):
        raise ValueError("Session selection belongs to the Scion Pi launcher")
    agent_dir = Path(os.environ.get("PI_CODING_AGENT_DIR", "~/.pi/agent")).expanduser()
    session = agent_dir / "scion" / "session.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if session.exists():
        with session.open() as stream:
            header = json.loads(stream.readline())
        if (not isinstance(header, dict) or header.get("type") != "session"
                or not isinstance(header.get("id"), str) or not header["id"]
                or not isinstance(header.get("cwd"), str) or not Path(header["cwd"]).is_absolute()):
            raise ValueError("Invalid persisted Pi session; refusing replacement")
        if Path(header.get("cwd", "")).resolve() != Path.cwd():
            raise ValueError("Pi session workspace changed; refusing implicit migration")
        args = options_only(args)
        if os.environ.get("DESKOPS_AUTONOMOUS") == "1":
            args.append(RECOVERY_PROMPT)
    # Explicit loading avoids discovery in cheap --no-extensions review processes.
    if "--no-extensions" not in args and "-ne" not in args and BRIDGE.is_file():
        if str(BRIDGE) not in args:
            args = ["--extension", str(BRIDGE), *args]
    os.environ["PI_OFFLINE"] = "1"
    os.environ["PI_SKIP_VERSION_CHECK"] = "1"
    os.execvp("pi", ["pi", "--offline", "--session", str(session), *args])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError):
        print("Pi launch failed: inspect session state and harness options; no arguments displayed.", file=sys.stderr)
        sys.exit(1)

FILE:pi/scion/provision.py
#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""pi container-side provisioner.

Runs inside the agent container at pre-start (`sciontool harness provision`).
The host has already projected the auth env vars into the harness launch env
(but stripped them from THIS script's env, so we only see their *names* via
inputs/auth-candidates.json) and staged any PI_AUTH file secret.

This script:

  1. Selects the auth method: api-key (DEEPSEEK_API_KEY) > auth-file (PI_AUTH).
  2. Writes ~/.pi/agent/models.json with the DeepSeek provider. Its apiKey is
     the env var NAME "DEEPSEEK_API_KEY": pi resolves it at runtime, so no
     secret value is ever written to disk by this script.
  3. In auth-file mode, installs the staged PI_AUTH secret at
     ~/.pi/agent/auth.json (mode 0600).
  4. Writes ~/.pi/agent/settings.json defaultProvider/defaultModel from the
     resolved model (SCION_MODEL through config.yaml model_aliases, falling
     back to deepseek-flash). Every other existing key is preserved.

Stdlib-only, like every other provisioner.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scion_harness as sh  # noqa: E402

assert sh.INTERFACE_VERSION >= 2, (
    "pi provision.py requires scion_harness INTERFACE_VERSION >= 2; "
    f"got {sh.INTERFACE_VERSION}. Update the staged scion_harness.py."
)

PI_AGENT_DIR = "~/.pi/agent"
PI_AUTH_FILE = PI_AGENT_DIR + "/auth.json"
PI_SETTINGS_FILE = PI_AGENT_DIR + "/settings.json"
PI_MODELS_FILE = PI_AGENT_DIR + "/models.json"

# The pi version pinned in the Dockerfile. Recording it as the last seen
# changelog keeps pi from opening its changelog screen on first launch.
PI_VERSION = "0.67.3"

PROVIDER = "deepseek"
DEFAULT_MODEL = "deepseek-flash"
API_KEY_ENV = "DEEPSEEK_API_KEY"
VALID_AUTH_TYPES = ("api-key", "auth-file")

# Non-secret provider definition (same models the SLDB desks run on).
DEEPSEEK_PROVIDER: dict[str, Any] = {
    "baseUrl": "https://api.deepseek.com/v1",
    "api": "openai-completions",
    # An env var NAME, resolved by pi at runtime — never the key itself.
    "apiKey": API_KEY_ENV,
    "models": [
        {
            "id": "deepseek-flash",
            "name": "DeepSeek V4.1 Flash",
            "reasoning": True,
            "input": ["text", "image"],
            "contextWindow": 1048576,
            "maxTokens": 393216,
        },
        {
            "id": "deepseek-v4-pro",
            "name": "DeepSeek V4 Pro",
            "reasoning": True,
            "input": ["text"],
            "contextWindow": 1048576,
            "maxTokens": 393216,
        },
    ],
}

AUTH = sh.AuthSpec(
    harness="pi",
    methods=[
        sh.env_method("api-key", any_of=[API_KEY_ENV], hint=f"set {API_KEY_ENV}"),
        sh.file_method("auth-file", path=PI_AUTH_FILE, secret_key="PI_AUTH"),
    ],
)


def _load_object(path: str, ctx: sh.ProvisionContext) -> dict[str, Any] | None:
    """Load a JSON object: {} if absent, None if present but unusable."""
    if not os.path.exists(path):
        return {}
    try:
        data = sh.load_json(path)
    except (OSError, ValueError):
        data = None
    if not isinstance(data, dict):
        ctx.warn(f"{path} is not a JSON object and is left unchanged")
        return None
    return data


def _write_models(ctx: sh.ProvisionContext) -> None:
    """Merge providers.deepseek into models.json; other providers are kept."""
    path = sh.expand_path(PI_MODELS_FILE)
    data = _load_object(path, ctx)
    if data is None:
        return
    providers = data.get("providers")
    if not isinstance(providers, dict):
        providers = {}
    providers[PROVIDER] = json.loads(json.dumps(DEEPSEEK_PROVIDER))
    data["providers"] = providers
    sh.atomic_write_json(path, data)


def _resolve_model(ctx: sh.ProvisionContext) -> tuple[str, str]:
    """Return (provider, model). Accepts "model" or "provider/model"."""
    model = sh.resolve_model(ctx) or DEFAULT_MODEL
    provider, sep, model_id = model.partition("/")
    if sep and provider and model_id:
        return provider, model_id
    return PROVIDER, model


def _write_settings(ctx: sh.ProvisionContext, provider: str, model: str) -> None:
    """Shallow merge: scion owns defaultProvider/defaultModel, keeps the rest."""
    path = sh.expand_path(PI_SETTINGS_FILE)
    data = _load_object(path, ctx)
    if data is None:
        return
    data["defaultProvider"] = provider
    data["defaultModel"] = model
    data.setdefault("lastChangelogVersion", PI_VERSION)
    sh.atomic_write_json(path, data)


def _write_auth_file(ctx: sh.ProvisionContext) -> bool:
    """Install the staged PI_AUTH secret as ~/.pi/agent/auth.json (0600)."""
    if "PI_AUTH" not in ctx.file_secret_files:
        return False
    content = ctx.read_file_secret("PI_AUTH")
    if not content.strip():
        raise sh.ProvisionError("PI_AUTH secret is empty")
    try:
        json.loads(content)
    except json.JSONDecodeError as exc:
        raise sh.ProvisionError(f"PI_AUTH secret is not valid JSON: {exc}") from exc
    sh.atomic_write_text(sh.expand_path(PI_AUTH_FILE), content, mode=0o600)
    return True


def provision(ctx: sh.ProvisionContext) -> None:
    explicit = ctx.explicit_type
    if explicit and explicit not in VALID_AUTH_TYPES:
        raise sh.ProvisionError(
            f"pi: unknown auth type {explicit!r}; "
            f"valid types are: {', '.join(VALID_AUTH_TYPES)}"
        )
    resolved = ctx.select_auth(AUTH)

    extra: dict[str, Any] = {}
    if resolved.method == "auth-file":
        extra["auth_file_written"] = _write_auth_file(ctx)

    ctx.write_outputs(resolved, env={}, extra=extra)

    _write_models(ctx)
    provider, model = _resolve_model(ctx)
    _write_settings(ctx, provider, model)

    ctx.info(f"method={resolved.method} provider={provider} model={model}")


if __name__ == "__main__":
    sh.run("pi", provision)

FILE:pi/scion/scion-events.ts
/** Pi 0.67.3 native events -> Scion 0.2.21's existing Claude dialect.
 * Never forward input, tool arguments/results, transcripts or diagnostics.
 */
import { spawn } from "node:child_process";

const EVENTS = {
  session_start: "SessionStart",
  input: "UserPromptSubmit",
  agent_start: "agent-start",
  agent_end: "Stop",
  tool_execution_start: "PreToolUse",
  tool_execution_end: "PostToolUse",
};

export function payload(event) {
  const hook_event_name = EVENTS[event.type];
  if (!hook_event_name) return undefined;
  const result = { hook_event_name };
  if (event.type.startsWith("tool_execution_")) {
    // Names and ids only; bound and reject arbitrary text in these fields.
    if (typeof event.toolName === "string" && /^[\w.-]{1,80}$/.test(event.toolName))
      result.tool_name = event.toolName;
    if (typeof event.toolCallId === "string" && /^[\w:.-]{1,160}$/.test(event.toolCallId))
      result.tool_use_id = event.toolCallId;
  }
  return result;
}

export function emit(event, run = spawn) {
  const data = payload(event);
  if (!data) return Promise.resolve(true);
  return new Promise((resolve) => {
    let done = false;
    let timer;
    const finish = (ok) => { if (!done) { done = true; clearTimeout(timer); resolve(ok); } };
    try {
      const child = run("sciontool", ["hook", "--dialect=claude"],
        { stdio: ["pipe", "ignore", "ignore"] });
      timer = setTimeout(() => { child.kill("SIGKILL"); finish(false); }, 5000);
      child.on("error", () => finish(false));
      child.on("close", (code) => finish(code === 0));
      child.stdin.on("error", () => finish(false));
      child.stdin.end(JSON.stringify(data));
    } catch { finish(false); }
  });
}

export default function scionEvents(pi) {
  for (const name of Object.keys(EVENTS)) {
    pi.on(name, async (event) => {
      if (!(await emit(event))) {
        // No child errors or payloads: hook diagnostics can contain credentials.
        process.stderr.write("Scion event delivery failed.\n");
      }
    });
  }
}

FILE:pi/scion/start-desk.py
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

FILE:pi/scion/README.md
# Pi del fork en Scion

Estas recetas conservan Scion **0.2.21**. Pi host e imagen proceden de
[jpcosec/pi-mono](https://github.com/jpcosec/pi-mono), commit
`e9ba9e2ebce1b49dca85ab20007038c06e486ea5`, versión `0.67.3`.
No usar el paquete npm publicado ni actualizar automáticamente el fork.

## Instalar Pi host e imagen

Con Node >=20.6, npm y Git instalados:

```bash
bash ~/setup/pi/scion/install-pi-fork.sh
export PATH="$HOME/.local/bin:$PATH"
pi --version
git -C ~/bin/pirate/pi-mono rev-parse HEAD
```

El instalador clona en `~/bin/pirate/pi-mono` si falta, verifica origin y revisión,
y rechaza cambios locales sin borrarlos. Ejecuta `npm ci` y el `tsgo` local para
`tui`, `ai`, `agent` y `coding-agent`, copia los assets de CLI y publica el enlace
`~/.local/bin/pi`. No ejecuta `npm run build`: el build de `ai` regenera modelos
consultando servicios externos. El catálogo del commit fijado se conserva.

La receta de contenedor está en [Dockerfile](Dockerfile). El contexto construido
en esta máquina está en `~/scion-build/pi-fork-e9ba9e2`. Usa como base la imagen
anterior `scion-pi:latest`, que se conserva, y publica `scion-pi-fork:e9ba9e2`.
La nueva imagen retira el Pi npm de esa base e instala únicamente los paquetes
Pi del fork. Los snapshots excluyen secretos, sesiones y configuración personal.
Nunca incluir la clave en Dockerfile, argumentos de build, capas, contexto o logs.

Para reconstruir el contexto desde los checkouts locales:

```bash
ctx="$HOME/scion-build/pi-fork-e9ba9e2"
mkdir -p "$ctx/pi-mono" "$ctx/python-src/sldb" "$ctx/python-src/deskops"
git -C ~/bin/pirate/pi-mono archive e9ba9e2ebce1b49dca85ab20007038c06e486ea5 | tar -x -C "$ctx/pi-mono"
tar --exclude=__pycache__ --exclude='*.pyc' -cf - -C /mnt/ssd/proyectos/SLDB_1/sldb pyproject.toml README.md LICENSE src | tar -x -C "$ctx/python-src/sldb"
tar --exclude=__pycache__ --exclude='*.pyc' -cf - -C /mnt/ssd/proyectos/SLDB_1/deskops pyproject.toml README.md deskops | tar -x -C "$ctx/python-src/deskops"
/mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pip wheel --no-deps \
  --wheel-dir "$ctx/wheels" "$ctx/python-src/sldb" "$ctx/python-src/deskops"
cp "$(command -v uv)" "$ctx/uv"
cp ~/setup/pi/scion/Dockerfile ~/setup/pi/scion/launch.py ~/setup/pi/scion/scion-events.ts "$ctx/"
docker build -t scion-pi-fork:e9ba9e2 "$ctx"
```

El bundle original está en la rama local `wt/pi-harness` del checkout
`/mnt/ssd/proyectos/SLDB_1/scion-wt-pi-harness`, commit `7163525f9`.
Para preparar una instalación del harness compatible con Scion 0.2.21:

```bash
bundle="$HOME/scion-build/pi-fork-e9ba9e2/harness"
mkdir -p "$bundle"
git -C /mnt/ssd/proyectos/SLDB_1/scion-wt-pi-harness archive 7163525f9 harnesses/pi | tar -x --strip-components=2 -C "$bundle"
cp ~/setup/pi/scion/harness-config.yaml "$bundle/config.yaml"
cp ~/setup/pi/scion/provision.py "$bundle/provision.py"
printf 'FROM scion-pi-fork:e9ba9e2\nCMD ["pi"]\n' > "$bundle/Dockerfile"
scion harness-config install --global --name pi "file://$bundle" --force
```

[launch.py](launch.py) vive en la imagen y fija una sesión por agente en
`~/.pi/agent/scion/session.jsonl`. Scion 0.2.21 reinicia el comando original del
contenedor al reanudar: el launcher conserva las opciones del harness pero
suprime la repetición del encargo inicial. Rechaza una sesión inválida o de otro
workspace. `--offline` desactiva consultas de arranque y avisos de actualización;
las llamadas de Pi a DeepSeek siguen funcionando.

## Publicar el harness Pi

La imagen local instalada es `scion-pi-fork:e9ba9e2`, con etiquetas de fork y
commit; el host usa Pi `0.67.3` compilado directamente. Publicar la configuración
Pi al Hub con la ruta explícita: en Scion 0.2.21 el sync no resolvió el slug en
este contexto.

```bash
SCION_HUB_ENABLED=true scion harness-config sync pi --project /mnt/ssd/proyectos/SLDB_1 --non-interactive
```

## Plantillas del proyecto

El proyecto registrado es `sldb-1`, UUID
`b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7`. Su directorio de plantillas es
`~/.scion/project-configs/sldb-1__b0899ed7/.scion/templates`.
Generar desde RoleDocs y RuntimeProfileDocs, sin `--task` ni `--agent`: esto
materializa plantillas sin crear RunDocs ni tocar tareas reales.

```bash
SCION_TEMPLATES="$HOME/.scion/project-configs/sldb-1__b0899ed7/.scion/templates"
deskops runtime template role-deskops-executor \
  --root /mnt/ssd/proyectos/SLDB_1/deskops --harness pi \
  --out "$SCION_TEMPLATES/deskops-executor" --task-repo deskops --mode executor
deskops runtime template role-deskops-supervisor \
  --root /mnt/ssd/proyectos/SLDB_1/deskops --harness pi \
  --out "$SCION_TEMPLATES/deskops-coordinator" --task-repo deskops --mode coordinator
scion templates sync deskops-executor --project sldb-1
scion templates sync deskops-coordinator --project sldb-1
scion templates list --project sldb-1
```

Comprobar también el descubrimiento por API del proyecto usado por la UI. La
plantilla coordinadora queda disponible; **no se lanza automáticamente**.
DeskOps/SLDB conservan tareas, validación, evidencia y cierre. La supervisión de
runtime de DeskOps sigue siendo Herdr; estas plantillas Scion son opcionales.
Integrar supervisión y trazabilidad avanzada requiere trabajo posterior.

## Credencial y autenticación

```bash
python3 ~/setup/pi/scion/sync-deepseek-secret.py
```

El helper lee únicamente `DEEPSEEK_API_KEY` desde `~/.pi/agent/secrets.env` y el
Bearer token desde `~/.scion/dev-token`, sin evaluar shell. Admite una asignación
simple, opcionalmente `export`, con comillas simples/dobles coincidentes; no
interpreta expansiones ni escapes. Rechaza claves ausentes, vacías o duplicadas.
Codifica el valor en base64 como exige la API de Scion 0.2.21 (no es cifrado).
Publica el secreto con scope de proyecto y `injectionMode: as_needed` mediante
`PUT /api/v1/secrets/DEEPSEEK_API_KEY` en `http://127.0.0.1:8080`.
`--help` describe overrides de rutas, proyecto y Hub. No pasar el valor por argv.
Los errores no muestran cuerpos HTTP, valores ni tokens; el éxito solo indica
nombre, scope y estado. La credencial queda fuera del repositorio y la imagen.

La autenticación del CLI contra Hub es independiente de la credencial del
proveedor que necesita Pi dentro del agente. El token del helper autentica la
petición al Hub; el secreto de proyecto permite al Host/Runtime Broker entregar
`DEEPSEEK_API_KEY` al harness. Que el CLI pueda listar proyectos no demuestra que
el Host pueda ejecutar DeepSeek. Verificar la respuesta real del agente.

## Smoke de lectura y sesión

Usar un agente de prueba propio y un nonce nuevo. Mantener `--project sldb-1`
en todas las operaciones para evitar resolver otro proyecto por el cwd.
El prompt de smoke debe limitar explícitamente la plantilla ejecutora a lectura.
No ejecutar tareas reales, mutaciones de DeskOps, ni comandos Herdr durante este
smoke. No cargar `pi-subagents` dentro de Scion.

Lanzar y reanudar desde `/mnt/ssd/proyectos/SLDB_1`, el workspace compartido de
varios repositorios que intencionalmente no es un repositorio Git. Scion 0.2.21
exige Git >=2.47 si el cwd está dentro de Git, incluso con `--workspace`
explícito; el host tiene Git 2.43. Usar esta raíz evita esa comprobación sin
cambiar Git.

```bash
cd /mnt/ssd/proyectos/SLDB_1
scion start pi-fork-read-smoke \
  'Prueba SOLO LECTURA: recuerda el nonce <NONCE_NUEVO>. Ejecuta deskops list tasks --root /workspace/deskops e informa el resultado. No edites archivos, tareas ni configuración. Espera instrucciones.' \
  --type deskops-executor --project sldb-1 --harness-auth api-key --non-interactive
scion look pi-fork-read-smoke --plain --project sldb-1
scion message pi-fork-read-smoke 'Confirma que completaste la lectura y espera.' --project sldb-1
scion stop pi-fork-read-smoke --project sldb-1
cd /mnt/ssd/proyectos/SLDB_1
scion resume pi-fork-read-smoke --project sldb-1 --non-interactive
scion message pi-fork-read-smoke 'Indica el nonce que te di antes de detenerte, sin releerlo de archivos. Mantén el modo solo lectura.' --project sldb-1
scion look pi-fork-read-smoke --plain --project sldb-1
scion stop pi-fork-read-smoke --project sldb-1
```

Guardar evidencia sanitizada de revisión del fork, versión, descubrimiento de
plantillas, respuesta DeepSeek, lectura CLI y nonce conservado tras stop/resume.
No repetir el nonce en el prompt de reanudación. Revisar agentes antes y después
para demostrar que se conservaron los ajenos.

**Estado verificado el 2026-11-10:** build del host y contenedor, secreto en API,
plantillas publicadas, lectura de DeskOps y respuesta DeepSeek correctos. El
agente `deskops-pi-ready-20261110` conservó la sesión
`01a1c3a1-1449-77e4-8e78-b43dbb40370f` después de stop/resume y recordó un nonce
enviado por un mensaje posterior al arranque, sin repetir el encargo inicial.
Los agentes de prueba quedaron detenidos; no se despachó ninguna tarea real.
Veinte pruebas independientes validan launcher y redacción de secretos.
La evidencia sanitizada está en `runs/subagents/20261110-scion-pi-fork/`.


## Bootstrap explícito y eventos nativos

Regla fuente: [átomo de autoridad de runtime y workflow](../../desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md).
[start-desk.py](start-desk.py) prepara un worktree separado del desk, comprueba
imports reales y materializa ejecutor, tester y coordinador mediante la API
`deskops runtime template --context-file`. Requiere la implementación de esa
interfaz y del modo `tester` en la fuente DeskOps probada. La raíz del fixture
ya debe ser un repositorio Git con sus tareas, roles y rituales comprometidos.
No se prepara ni despacha un desk de producción durante estas pruebas.

Scion v0.2.21 resuelve la plantilla local desde el directorio de ejecución;
`--project` elige el destino Hub. Por eso `--templates-dir` exige el layout
`<config-del-proyecto>/.scion/templates` y sync, start y resume corren desde esa configuración,
sin seleccionar una plantilla homónima de otro proyecto. Los errores muestran
solo la etapa conocida y la clasificación de salida; omiten argumentos y salida
del subproceso.

El provider local del broker apunta al directorio externo de configuración
Scion, fuera del repositorio Git. En su `settings.yaml`, `workspace_path`
identifica el workspace compartido absoluto. El Hub deriva el montaje de esa
configuración y puede descartar el `--workspace` de la petición; vincular el
provider al checkout Git haría que Scion intentara crear otro worktree por agente.
El worktree de tareas queda bajo la autoridad de DeskOps/bootstrap.

Ejemplo de laboratorio autorizado (el directorio de plantillas pertenece al
proyecto explícito; no copiarlo para otro proyecto):

```bash
/mnt/ssd/proyectos/SLDB_1/.venv/bin/python ~/setup/pi/scion/start-desk.py \
  --root /mnt/ssd/proyectos/SLDB_1/.tmp/scion-autonomy-lab-v2 \
  --workspace-root /mnt/ssd/proyectos/SLDB_1 \
  --source-root /mnt/ssd/proyectos/SLDB_1/deskops-runtime \
  --sldb-root /mnt/ssd/proyectos/SLDB_1/sldb/src \
  --ref HEAD --project d7d9d3cd-60a1-46be-9a63-b56722521061 --agent autonomy-lab-coordinator-v2 \
  --templates-dir "$HOME/.scion/project-configs/scion-autonomy-lab__d7d9d3cd/.scion/templates"
```

`--ref` tiene el valor predeterminado `origin/main`; un arranque nuevo con ref
inválido falla antes de crear un worktree o plantillas. La recuperación de una
coordinadora propia usa su commit base registrado incluso si ese ref desapareció. No hay fallback a `HEAD`, reset del checkout
original ni modificación de remotes. Se registra revisión del desk y fuente en
`.tmp/scion-bootstrap/<identidad>/provenance.json`. El directorio adyacente tiene
un marcador de propiedad y un worktree dedicado; uno desconocido se rechaza.
Los commits propios pueden avanzar desde el commit base registrado. Una
coordinadora existente solo se reconcilia con nombre, proyecto, etiquetas y
provenance coincidentes; al recuperarla se conservan también los archivos
sucios de hijos en curso. No se crea otro worktree ni se sigue un ref movido. Se comparan fingerprints
SHA-256 del contenido de `deskops/` y `sldb_root/sldb` (fuentes y datos, sin
cachés ni bytecode); cambios sin commit también invalidan la recuperación.
Cambios ajenos en desk/docs/evidencia o commits de solo documentación no la
bloquean. Un lock nativo sobre el directorio original serializa invocaciones y
la lista de agentes se vuelve a leer bajo ese lock.
Sin esa identidad existente se exige un worktree limpio. Todos los paths del contexto deben ser absolutos dentro del workspace.
`source_root` contiene el paquete `deskops`; `sldb_root` es directamente `src`,
no la raíz del checkout SLDB. `PYTHONPATH` enlaza ambos, y se verifican los
`__file__` importados antes del arranque.

El generador materializa `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`,
`PYTHONPATH` y un volumen soportado de workspace a su misma ruta absoluta.
Scion monta además el workspace en `/workspace`; no se crean symlinks manuales.
Bootstrap usa la autenticación existente del CLI contra el Hub explícito
(`--hub`, predeterminado `http://127.0.0.1:8080`). Los hijos usan sus tokens
Scion y el secreto DeepSeek del proyecto; `secrets.env` nunca se monta.
El metadata server existente de `sciontool` sigue refrescando los tokens.

Tras sincronizar las tres plantillas, bootstrap reconcilia el nombre y etiquetas
de la coordinadora. Una identidad ajena, duplicada o en error exige resolución
operativa; una activa no recibe otro prompt, y una detenida se reanuda. El primer
arranque recibe una sola asignación operativa. Un archivo `--config` propio del
bootstrap activa `DESKOPS_AUTONOMOUS=1` únicamente para la coordinadora, sin
editar las plantillas generadas. En esa modalidad el launcher añade una
instrucción de recuperación al reanudar la sesión fija; conserva el historial y
suprime la asignación inicial. Las sesiones manuales conservan su comportamiento.
Scion y DeskOps siguen siendo las únicas autoridades de runtime y lifecycle.

[scion-events.ts](scion-events.ts) carga explícitamente desde el launcher.
`session_start`, `input`, `agent_start`, `agent_end` y los dos eventos de ejecución
de tools se traducen al dialecto Claude ya soportado por `sciontool hook`.
`agent_end` se traduce a `Stop` (working), nunca `task_completed`. Las nuevas
entradas y sesiones limpian waiting mediante el handler existente, mientras
sus reglas conservan estados deliberados de blocked/completed durante wrap-up.
Solo se envían nombres de evento y nombres/identificadores acotados de tool;
ningún prompt, argumento, resultado, transcript ni diagnóstico del hijo sale
por ese canal. Cada llamada usa stdin y un timeout de cinco segundos. Un fallo
emite un aviso fijo sin datos del proceso. `--no-extensions` y `-ne` excluyen el
puente también en procesos baratos de revisión.

Las pruebas de `tests/test_scion_autonomy.py` verifican los contratos con repositorios temporales y comandos simulados. La integración real quedó registrada en `runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json`: dos tareas cerradas, dos fases, cero mensajes de seguimiento, recuperación de la coordinadora y tester independiente nuevo después de un fallo real. Las seis sesiones Pi son distintas y no hubo hijos duplicados. La validación final independiente pasó con los tests originales intactos. El probe de lifecycle y renovación real del token tiene evidencia separada en el mismo directorio; no se afirma una ejecución de diez horas.

FILE:pi/README.md
# Pi y Scion

Decisión acordada con JP el 2026-11-09.

## Contrato de ejecución

- Scion crea, aísla y coordina agentes, su comunicación y sus sesiones.
- Pi ejecuta la tarea de cada agente como harness de Scion.
- DeepSeek es el proveedor del modelo de Pi; no es una capa de orquestación.
- DeskOps/SLDB conservan la autoridad sobre tareas, validación, evidencia y cierre.
- Pi no carga `pi-subagents`: no se anida otra orquestación dentro de Scion.

## Procedencia de Pi

El Pi del host y el de la imagen de Scion deben compilarse desde
<https://github.com/jpcosec/pi-mono>, fijando explícitamente el commit.
El commit observado al acordar esta decisión es
`e9ba9e2ebce1b49dca85ab20007038c06e486ea5` (versión declarada `0.67.3`).
No sustituirlo por paquetes publicados desde upstream ni ejecutar actualizaciones
automáticas que cambien esta procedencia. Las extensiones deben ser compatibles
con el fork; una incompatibilidad no autoriza migrar Pi a upstream.

## Estado operativo verificado: 2026-11-10

- Pi del host apunta al build del fork en `~/bin/pirate/pi-mono`, versión `0.67.3`.
  La instalación npm `@earendil-works/pi-coding-agent` se retiró.
- Scion conserva `v0.2.21`. Su harness `pi` usa `scion-pi-fork:e9ba9e2`, con el
  mismo fork/commit y herramientas DeskOps/SLDB sobre Python 3.12.
- El proyecto `sldb-1` tiene plantillas `deskops-executor` y `deskops-coordinator`
  generadas desde los roles de DeskOps. Preparar la coordinadora no la lanza.
  Scion admite otros harnesses; el contrato del fork aplica a los agentes Pi.
- `DEEPSEEK_API_KEY` se sincroniza desde `~/.pi/agent/secrets.env` al secreto del
  proyecto. Solo se entrega cuando el harness la necesita; no entra en Git,
  argumentos de proceso ni imagen.
- `pi-subagents` no está instalado en Pi del proyecto deskops ni en la imagen.
- El smoke real leyó el board mediante la CLI, recibió respuesta de DeepSeek y
  conservó la misma sesión y un dato posterior al arranque tras stop/resume.
  Los agentes de prueba quedaron detenidos. Veinte pruebas independientes pasaron.

Recetas, comandos y límites actuales: [Scion con Pi del fork](scion/README.md).
La supervisión `deskops runtime` sigue ligada a Herdr; no se implementó un
supervisor Scion nuevo ni la correlación avanzada de intentos con closeout.

Antecedentes: [evaluación de Scion](../desk/drawer/scion-reemplazo-herdr.md)
y [ficha histórica de Pi](../external-resources/pi.md). Sus descripciones de
instalación son históricas y deben contrastarse con este contrato y el host.

## Interfaz web de Scion en esta máquina

Corrección local del 2026-11-10: el binario `scion v0.2.21` no incluía assets web.
Se compiló únicamente la web desde `homebrew-scion/scion`, commit
`55b9930538a14efeb9bc746de410ee7b12155afe`, que coincide con el binario instalado.
Las fuentes y el build están en `~/scion-build/web-v0.2.21/`.

El servidor se inició como daemon en loopback, conservando Hub y Runtime Broker:

```bash
scion server start --enable-hub --enable-runtime-broker --enable-web \
  --dev-auth --auto-provide \
  --web-assets-dir "$HOME/scion-build/web-v0.2.21/web/dist/client"
```

La web se sirve en `http://127.0.0.1:8080`. Se verificaron respuestas HTTP 200
del HTML, `/assets/main.js` y `/auth/me`, y la ausencia del mensaje
`Web UI Not Available`. El binario de Scion conserva su versión.
`scion server restart` reutiliza los argumentos guardados por el daemon.


## Bootstrap autónomo reproducible

El runtime tiene ahora un [bootstrap explícito](scion/start-desk.py) y un
[puente de eventos Pi](scion/scion-events.ts). La receta y sus límites están en
[bootstrap y eventos nativos](scion/README.md#bootstrap-explícito-y-eventos-nativos).
La regla está capturada en el [átomo de autoridad](../desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md).
El bootstrap valida fuentes/refs/paths, conserva checkouts originales, materializa
las tres funciones de agente y reconcilia una coordinadora determinista. Requiere
el contrato `--context-file` y tester de la fuente DeskOps probada. La validación
unitaria usa únicamente fixtures; la autonomía real requiere evidencia de
integración separada. Scion conserva sesiones y refresh de tokens; DeskOps/SLDB
conservan validación y closeout.

FILE:tests/test_scion_pi_runtime.py
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
    assert calls[-1][1][-3:] == ['--extension', str(bridge), 'Original task']
    invoke(monkeypatch, module, ['--no-extensions', 'Review only'])
    assert '--extension' not in calls[-1][1]

FILE:tests/test_scion_autonomy.py
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

FILE:desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md
---
id: atom-scion-bootstrap-preserves-runtime-and-workflow-authority
title: Scion bootstrap preserves runtime and workflow authority
five_wh_one_plus: how
tags:
- system:scion
- system:deskops
- topic:runtime
provenance: desk/tasks/task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge.md
---

# Scion bootstrap preserves runtime and workflow authority

## Answer

Scion bootstrap binds explicit validated current DeskOps and SLDB sources and an owned clean worktree of an explicit canonical ref, preserving original dirty checkouts. Recovery requires matching project, coordinator name, labels, worktree ownership and runtime package content fingerprints; preserve its own descendant commits and dirty child evidence using its recorded base even if the original ref vanished. Runtime source and data edits fail provenance checks, while unrelated desk/docs/evidence changes and generated caches do not. Serialize bootstrap against the original directory inode and reconcile again under the native lock. Mount the workspace at its host absolute path and /workspace through supported volumes. Scion owns agent identity, sessions, notifications and token refresh; DeskOps owns the task lifecycle, independent testing, evidence and closeout. Native Pi events send only normalized event names and tool identifiers to sciontool; generic agent end is working, never task completion. Autonomous resume reconciles durable desk and existing children in the preserved session, without replaying the initial assignment. Native Scion v0.2.21 template sync resolves its local source from the working directory independently of the --project Hub destination. Materialize only to an explicit project .scion/templates path and synchronize from its owning project configuration root; never resolve a same-named template from another project. Bootstrap failures expose only the known command stage and exit classification, never arguments, subprocess output or credentials. The same cwd-dependent local template selection applies to native start and resume, so those commands also run from the explicit project configuration root. A linked local broker provider binds the external non-Git Scion configuration directory, with workspace_path set to the explicit shared workspace; Hub dispatch derives the workspace from those settings and may clear the request workspace override. DeskOps owns the task Git worktree rather than asking Scion to create another per-agent copy.

FILE:instruccion
Cold-bundle de la tarea task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests
- fresh real Scion coordinator/executor/tester on disposable desk completes closeout and next task without messages
- restart preserves session and no duplicate child

