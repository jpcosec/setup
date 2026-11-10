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

Runtime constants: Scion0.2.21; Pi jpcosec/pi-mono e9ba9e2ebce1b49dca85ab20007038c06e486ea5; project sldb-1 UUID b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7; host workspace /mnt/ssd/proyectos/SLDB_1. start-desk.py accepts explicit desk/source/ref/project/workspace/agent options, validates paths and provenance, chooses a clean dedicated worktree of configured canonical ref (origin/main default) without resetting dirty originals and reuses it only when ownership is known. Mount workspace both at /workspace and its real host absolute path via supported Scion volumes, not manual symlinks. Explicit source roots via PYTHONPATH bind tested DeskOps source and /mnt/ssd/proyectos/SLDB_1/sldb/src; verify actual imports before start, never silently use baked stale wheels. User CLI authenticates bootstrap through configured Hub, children use their Scion agent tokens and DeepSeek project secret, never secrets.env mounted. Pi extension maps input/session/agent/tool events to existing sciontool hook Claude dialect events; emit no prompt/tool argument or credential content; generic agent_end is not completed. Reuse sciontool metadata proactive token refresh, verify a real own-agent refresh and preserve tokens without logging; no new refresher service. Stable coordinator/child labels and run identity reconcile before start. Independent tester mode/source contract comes from the DeskOps task branch and is an integration prerequisite. Disposable real Git desk under workspace .tmp, two bounded code tasks with explicit expected functions/tests and dependency, one initial assignment and zero followup messages. Automated fixture may inject one controlled validation/child failure and stop/resume; evidence must show correct refusal to close on failure, recovery, no duplicate child, independent tester, one closeout per task and phase completion. Do not dispatch production tasks. Register source atom before docs and save all sanitized integration evidence.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests
- fresh real Scion coordinator/executor/tester on disposable desk completes closeout and next task without messages
- restart preserves session and no duplicate child

## Done When

_Name the observable condition that makes the task complete._

Runtime state reflects actual work; clean startup uses correct source and Git paths; unattended disposable-desk loop passes; source docs and exact evidence committed. No claim of success from a running container alone.


FILE:README.md
# Personal runtime setup

Versioned configuration for the local interactive workspace:

- **WezTerm**: terminal and outer session
- **Neovim**: human editor
- **Yazi**: filesystem navigator
- **Pi**: agentic worker
- **Herdr**: external runtime for desks, panes, processes, and agents
- **Opsys/DeskOps**: workflow and durable state

Secrets, OAuth state, sessions, caches, and machine-local overrides stay outside
this repository.

The agreed Scion/Pi execution model, fork provenance, and pending migration are
documented in [pi/README.md](pi/README.md).

## Runtime contract

Each DeskOps desk is one Herdr workspace. The file `desk/runtime.yaml` describes
the desired workspace layout without exposing Herdr pane IDs or process IDs.

The workspace identity is durable in Opsys/SLDB; Herdr IDs are runtime
references that may change after reconstruction.

## Tools installed

Managed outside this repo but expected on PATH for daily use:

| Tool | Version | Location |
|---|---|---|
| nvim | latest | `~/.local/nvim/` tarball (not snap) |
| lazygit | latest | `~/.local/bin/lazygit` (override with `LAZYGIT_VERSION`) |
| fd | 10.4.2 | `~/.pi/agent/bin/fd` |
| rg | 14.1.0 | `/usr/bin/rg` (system) |

### Neovim Mason LSPs

Installed via Mason:
- basedpyright
- eslint-lsp
- gopls
- lua-language-server
- marksman
- ruff
- rust-analyzer

## Shell

`shell/yazi.sh` defines `y`, a Yazi wrapper: quitting with `q` leaves the shell
in Yazi's last directory (`Q` quits without changing it). `install/install.sh`
adds a single line to `~/.bashrc` that sources it from this repo, so edits to the
function apply in new shells without reinstalling:

```bash
[ -f ~/setup/shell/yazi.sh ] && . ~/setup/shell/yazi.sh
```

## Bootstrap

```bash
# Create symlinks from this repo to XDG config paths,
# and source shell/yazi.sh from ~/.bashrc (idempotent; safe to rerun)
bash install/install.sh

# Additional tools (tarball-based, no snap)
bash install/nvim.sh
bash install/lazygit.sh

# Start Herdr server and initialize workspace
bash install/init-herdr.sh [--agents]
```



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


FILE:desk/tasks/Board.md
---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-centralizar-configuraciones-personales-en-setup.md
- desk/tasks/task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge.md
# List of pill-xxx paths
pills:
- desk/contexts/pills.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- workspace:desk
---

# setup Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._



## Task Details

_Generated from the task references above._

- Centralizar configuraciones personales en setup [draft] - Crear un repositorio setup versionable que contenga configuraciones públicas, plantillas de secretos y un instalador seguro para reconstruir la configuración local.
- Scion autonomy runtime bootstrap and Pi lifecycle bridge [draft] - A reproducible Scion start uses intended current desk/tools, valid worktree paths and a native Pi event bridge so a disposable authorized desk can run without manual prompts through child execution, independent test and closeout/continuation.


FILE:desk/contexts/pills.md
---
id: contexts-pills
tags:
- workspace:desk
---

# Pills

Pills are reusable context documents for the setup desk routine.

## Notes

- Keep active task-to-pill binding in task docs.
- Add temporary context here only when it affects execution safety or scope.


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


FILE:desk/drawer/tasks/task-scion-autonomy-runtime-bootstrap.md
# Scion autonomy: reproducible startup and Pi lifecycle bridge

Owner request 2026-11-10: iterate with bots and change configuration/code wherever
needed until arriving at a desk can execute authorized work without manual prompts.

Preserve Scion 0.2.21, Pi fork jpcosec/pi-mono at
e9ba9e2ebce1b49dca85ab20007038c06e486ea5, project-scoped secret handling and fixed
Pi session. No pi-subagents. Add a pinned Pi extension bridging native Pi events
to existing sciontool hook events, including clear activity on new input/tool work
and return-to-idle without equating agent_end with DeskOps closeout. Validate
deliberate blocked/completed states and token refresh behavior.

Make startup choose/configure a current isolated desk/source revision, preserve
dirty originals and work ownership, and expose consistent Git worktree paths in
every new container. Commands must import intended DeskOps/SLDB sources rather
than stale baked wheels. Configure explicit child project/auth/workspace and
fresh tester templates. Keep supervision in Scion and task authority in DeskOps.

Deliver a runnable startup recipe, durable configuration and tests, not only
another report. Acceptance uses a disposable desk with bounded tasks: ONE initial
assignment then no follow-up messages through review, child dispatch, independent
test, closeout commit and next-task/phase progress. Include controlled failure,
restart/no duplicate child, and fresh-container reconstruction. No real production
task is dispatched during runtime validation.


FILE:pi/scion/launch.py
#!/usr/bin/env python3
"""Keep one Pi conversation per Scion agent, including Docker stop/resume."""
import json
import os
from pathlib import Path
import sys


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
    os.environ["PI_OFFLINE"] = "1"
    os.environ["PI_SKIP_VERSION_CHECK"] = "1"
    os.execvp("pi", ["pi", "--offline", "--session", str(session), *args])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError):
        print("Pi launch failed: inspect session state and harness options; no arguments displayed.", file=sys.stderr)
        sys.exit(1)


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
# pi has no hook surface scion can listen to, so readiness is a fixed settle.
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
    max_turns: { support: "no", reason: "pi emits no hook events scion can count turns from" }
    max_model_calls: { support: "no", reason: "pi emits no model-start/model-end hook events" }
    max_duration: { support: "yes" }
  telemetry:
    enabled: { support: "no", reason: "pi has no hook or OTel bridge wired for scion" }
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
 && uv pip install --python /opt/deskops-tools/bin/python /opt/setup-wheels/*.whl \
 && chmod -R a+rX /opt/python /opt/deskops-tools
ENV PATH="/opt/deskops-tools/bin:${PATH}"
COPY launch.py /usr/local/lib/scion-pi/launch.py
RUN deskops --help >/dev/null && sldb --help >/dev/null
WORKDIR /workspace
CMD ["pi"]


FILE:/mnt/ssd/proyectos/SLDB_1/deskops-wt-scion-autonomy/desk/tasks/task-scion-autonomy-coordinator-contract.md
---
sldb:
  by: agent
  at: '2026-11-10T14:38:23Z'
  authority: generated
  via: save_document_payload
id: task-scion-autonomy-coordinator-contract
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- e58ee061
- tests/test_scion_runtime.py
depends_on:
- task-scion-autonomy-review-status
pills: []
files:
- deskops/runtime/scion.py
- deskops/cli/registry.py
- desk/roles/deskops-supervisor.md
- desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
- tests/test_scion_runtime.py
- tests/fixtures/golden/help
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-coordinator-contract.md
---

# Scion autonomy: consistent coordinator and tester contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

One coherent source contract makes Scion coordinator recover configured current state, progress routine authorized work, select reviewed ready unowned tasks, dispatch fresh executor/tester and reconcile closeout before continuing.

## Scope

_State what is in scope and what is out of scope._

Role source, generated Scion modes/prompts and command examples, explicit runtime context and durable atoms/docs. No replacement lifecycle engine, automatic policy decisions, pi-subagents or unrelated CC tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Source contract: correct RoleDoc via SLDB, permitting modeled workflow CLI mutations but no implementation by supervisor. Ordinary implementation questions answered from task/source evidence; escalate only unresolved owner decisions, actual ownership conflicts or external credentials/permissions. Never rerun an accepted review with unchanged input; bound technical retries and report precise blockers instead of broad diagnostic loops. Add optional --context-file JSON to existing runtime template command (and matching generator context kwarg); context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project. Emit DESKOPS_DESK_ROOT, DESKOPS_SOURCE_ROOT, DESKOPS_SLDB_SOURCE_ROOT, DESKOPS_WORKSPACE_ROOT, DESKOPS_SCION_PROJECT and PYTHONPATH plus a supported volume source=workspace_root target=workspace_root. No secrets in context. Preserve no-context behavior. Include tester mode in existing --mode choices, auto-detect tester RoleDoc, and separate tester scope/completion instructions. Coordinator recovers this configured current desk/tools, checks canonical/dirty state, board DAG/review gates and existing ownership (labels/RunDoc/worktrees), skips blocked/owned tasks, selects one reviewed ready leaf. Deterministic task+contract-derived agent names and task/role labels: write run intent BEFORE start and reconcile existing matching Scion child before any new start; duplicate-name protection stays Scion native, not a new scheduler/registry. Explicit --project, --workspace, --type, --harness-auth api-key, --non-interactive and correct subcommand --root flags in examples. Executor -> independent tester -> coordinator validates evidence -> deskops closeout -> reconcile phase -> recover/select again. Failed tester cannot close; request bounded correction and fresh test. Waiting-for-child uses Scion blocked/completion notifications (already subscribed); only real human decisions ask_user. Capture source atom before operator docs, generate from source, test YAML/modes/context and actual command examples; runtime task supplies hooks/bootstrap and unattended integration.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_runtime.py
- affected CLI help/output goldens if tester mode adds a choice
- real unattended coordinator -> executor -> independent tester -> closeout/continue integration

## Done When

_Name the observable condition that makes the task complete._

No source/installed instruction contradiction; tester materialization correct; routine questions not blanket ask_user; dispatch checks readiness/ownership and restart identity. Focused tests pass and live integrated experiment demonstrates the loop without parent prompts.


FILE:/home/robocop/scion-build/web-v0.2.21/pkg/sciontool/hooks/handlers/status.go
/*
Copyright 2025 The Scion Authors.
*/

// Package handlers provides hook handler implementations.
package handlers

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"

	state "github.com/GoogleCloudPlatform/scion/pkg/agent/state"
	"github.com/GoogleCloudPlatform/scion/pkg/sciontool/hooks"
)

// StatusHandler manages agent status in a JSON file.
type StatusHandler struct {
	// StatusPath is the path to the agent-info.json file.
	StatusPath string

	mu sync.Mutex
}

// NewStatusHandler creates a new status handler.
func NewStatusHandler() *StatusHandler {
	home := os.Getenv("HOME")
	if home == "" {
		home = "/home/scion"
	}
	return &StatusHandler{
		StatusPath: filepath.Join(home, "agent-info.json"),
	}
}

// isStickyActivity returns true if the given activity is a "sticky" value that
// should resist being overwritten by normal event-driven updates.
func isStickyActivity(activity string) bool {
	return state.Activity(activity).IsSticky()
}

// eventResult holds the result of mapping an event to phase/activity.
type eventResult struct {
	phase    state.Phase
	activity state.Activity
	isPhase  bool // true if this is a phase-level change
}

// Handle processes an event and updates the agent status.
func (h *StatusHandler) Handle(event *hooks.Event) error {
	result := eventToPhaseActivity(event)
	if result == nil {
		return nil // Event doesn't trigger a state change
	}

	// Phase-level changes (pre-start, post-start, pre-stop, session-end)
	if result.isPhase {
		return h.UpdatePhase(result.phase, result.activity, "")
	}

	// New work events (prompt-submit, agent-start, session-start): always
	// update activity unconditionally — clears any sticky state.
	if isNewWorkEvent(event.Name) {
		return h.UpdateActivity(result.activity, "")
	}

	// Tool-start events require special handling for sticky states.
	if event.Name == hooks.EventToolStart {
		// Claude-specific: ExitPlanMode and AskUserQuestion set waiting_for_input (sticky).
		if event.Dialect == "claude" && (event.Data.ToolName == "ExitPlanMode" || event.Data.ToolName == "AskUserQuestion") {
			return h.UpdateActivity(state.ActivityWaitingForInput, "")
		}

		// Tool-start clears waiting_for_input (user has responded) but
		// preserves completed (tools may fire after task_completed as wrap-up).
		return h.updateActivityIfNotSticky(result.activity, event.Data.ToolName, true)
	}

	// Notification event: set waiting_for_input directly (sticky).
	if event.Name == hooks.EventNotification {
		return h.UpdateActivity(state.ActivityWaitingForInput, "")
	}

	// All other events (tool-end, agent-end, model-end, etc.): update activity
	// only if current activity is not sticky.
	return h.updateActivityIfNotSticky(result.activity, "", false)
}

// UpdateActivity writes the activity to the agent-info.json file atomically.
// Used for runtime activity changes (most events). Preserves the current phase.
func (h *StatusHandler) UpdateActivity(activity state.Activity, toolName string) error {
	h.mu.Lock()
	defer h.mu.Unlock()

	info := h.readAgentInfoMap()

	// Update the activity field
	if activity == "" {
		delete(info, "activity")
	} else {
		info["activity"] = string(activity)
	}

	// Set or clear toolName
	if activity == state.ActivityExecuting && toolName != "" {
		info["toolName"] = toolName
	} else {
		delete(info, "toolName")
	}

	// Remove legacy fields if present
	delete(info, "status")
	delete(info, "sessionStatus")

	return h.writeAgentInfoLocked(info)
}

// UpdatePhase writes both phase and activity to the agent-info.json file atomically.
// Used for lifecycle phase changes (pre-start, post-start, pre-stop, session-end).
func (h *StatusHandler) UpdatePhase(phase state.Phase, activity state.Activity, toolName string) error {
	h.mu.Lock()
	defer h.mu.Unlock()

	info := h.readAgentInfoMap()

	// Update phase
	info["phase"] = string(phase)

	// Update activity
	if activity == "" {
		delete(info, "activity")
	} else {
		info["activity"] = string(activity)
	}

	// Set or clear toolName
	if activity == state.ActivityExecuting && toolName != "" {
		info["toolName"] = toolName
	} else {
		delete(info, "toolName")
	}

	// Remove legacy fields if present
	delete(info, "status")
	delete(info, "sessionStatus")

	return h.writeAgentInfoLocked(info)
}

// SetMessage writes a message to the agent-info.json detail section.
// This is used to persist error messages so the broker heartbeat can
// relay them to the hub even after the container exits.
func (h *StatusHandler) SetMessage(message string) error {
	h.mu.Lock()
	defer h.mu.Unlock()

	info := h.readAgentInfoMap()

	detail, _ := info["detail"].(map[string]interface{})
	if detail == nil {
		detail = make(map[string]interface{})
	}
	if message != "" {
		detail["message"] = message
	} else {
		delete(detail, "message")
	}
	if len(detail) > 0 {
		info["detail"] = detail
	} else {
		delete(info, "detail")
	}

	return h.writeAgentInfoLocked(info)
}

// updateActivityIfNotSticky updates the activity only if the current activity is not
// sticky. If clearWaiting is true, waiting_for_input is also cleared (treated
// as non-sticky for tool-start events where the user has responded).
func (h *StatusHandler) updateActivityIfNotSticky(activity state.Activity, toolName string, clearWaiting bool) error {
	h.mu.Lock()
	defer h.mu.Unlock()

	info := h.readAgentInfoMap()

	currentActivity, _ := info["activity"].(string)

	if isStickyActivity(currentActivity) {
		if clearWaiting && currentActivity == string(state.ActivityWaitingForInput) {
			// waiting_for_input is cleared by tool-start (user has responded)
		} else {
			return nil // Activity is sticky, don't overwrite
		}
	}

	// Update activity
	info["activity"] = string(activity)

	// Set or clear toolName
	if activity == state.ActivityExecuting && toolName != "" {
		info["toolName"] = toolName
	} else {
		delete(info, "toolName")
	}

	// Remove legacy fields if present
	delete(info, "status")
	delete(info, "sessionStatus")

	return h.writeAgentInfoLocked(info)
}

// readAgentInfoMap reads agent-info.json into a generic map, preserving all fields.
// Caller must hold h.mu.
func (h *StatusHandler) readAgentInfoMap() map[string]interface{} {
	info := make(map[string]interface{})
	if data, err := os.ReadFile(h.StatusPath); err == nil {
		_ = json.Unmarshal(data, &info)
	}
	return info
}

// writeAgentInfoLocked writes the agent info map to disk atomically.
// Caller must hold h.mu.
func (h *StatusHandler) writeAgentInfoLocked(info map[string]interface{}) error {
	data, err := json.MarshalIndent(info, "", "  ")
	if err != nil {
		return fmt.Errorf("marshaling status: %w", err)
	}

	dir := filepath.Dir(h.StatusPath)
	tmpFile, err := os.CreateTemp(dir, "agent-info-*.json")
	if err != nil {
		return fmt.Errorf("creating temp file: %w", err)
	}
	tmpPath := tmpFile.Name()

	if _, err := tmpFile.Write(data); err != nil {
		_ = tmpFile.Close()
		_ = os.Remove(tmpPath)
		return fmt.Errorf("writing temp file: %w", err)
	}
	_ = tmpFile.Close()

	// CreateTemp uses mode 0600. Widen to 0644 so the broker process
	// (which may run as a different uid than the container init) can
	// read and converge the file after the container exits.
	os.Chmod(tmpPath, 0644) //nolint:errcheck

	if err := os.Rename(tmpPath, h.StatusPath); err != nil {
		_ = os.Remove(tmpPath)
		return fmt.Errorf("atomic rename: %w", err)
	}

	return nil
}

// isNewWorkEvent returns true for events that indicate new work is starting.
// These events unconditionally update activity, clearing any sticky state.
func isNewWorkEvent(name string) bool {
	switch name {
	case hooks.EventPromptSubmit, hooks.EventAgentStart, hooks.EventSessionStart:
		return true
	}
	return false
}

// eventToPhaseActivity maps normalized events to phase/activity pairs.
// Returns nil if the event doesn't trigger a state change.
func eventToPhaseActivity(event *hooks.Event) *eventResult {
	switch event.Name {
	case hooks.EventPreStart:
		return &eventResult{phase: state.PhaseStarting, isPhase: true}

	case hooks.EventPostStart:
		return &eventResult{phase: state.PhaseRunning, activity: state.ActivityWorking, isPhase: true}

	case hooks.EventSessionStart:
		// session-start clears sticky — treated as activity-only (working)
		return &eventResult{activity: state.ActivityWorking}

	case hooks.EventPromptSubmit, hooks.EventAgentStart:
		return &eventResult{activity: state.ActivityThinking}

	case hooks.EventModelStart:
		return &eventResult{activity: state.ActivityThinking}

	case hooks.EventModelEnd:
		return &eventResult{activity: state.ActivityWorking}

	case hooks.EventToolStart:
		return &eventResult{activity: state.ActivityExecuting}

	case hooks.EventToolEnd, hooks.EventAgentEnd:
		return &eventResult{activity: state.ActivityWorking}

	case hooks.EventResponseComplete:
		return &eventResult{activity: state.ActivityCompleted}

	case hooks.EventNotification:
		return &eventResult{activity: state.ActivityWaitingForInput}

	case hooks.EventPreStop:
		return &eventResult{phase: state.PhaseStopping, isPhase: true}

	case hooks.EventSessionEnd:
		return &eventResult{phase: state.PhaseStopped, isPhase: true}

	default:
		return nil
	}
}

// GetFormattedState returns the state with tool name if applicable.
func (h *StatusHandler) GetFormattedState(event *hooks.Event) string {
	result := eventToPhaseActivity(event)
	if result == nil {
		return ""
	}
	if result.activity == state.ActivityExecuting && event.Data.ToolName != "" {
		return fmt.Sprintf("%s (%s)", result.activity, event.Data.ToolName)
	}
	if result.isPhase {
		return string(result.phase)
	}
	return string(result.activity)
}


FILE:/home/robocop/scion-build/web-v0.2.21/pkg/sciontool/hooks/dialects/claude.go
/*
Copyright 2025 The Scion Authors.
*/

// Package dialects provides harness-specific event format parsers.
package dialects

import (
	"bufio"
	"encoding/json"
	"os"
	"strings"

	"github.com/GoogleCloudPlatform/scion/pkg/sciontool/hooks"
)

// ClaudeDialect parses Claude Code hook events.
type ClaudeDialect struct{}

// NewClaudeDialect creates a new Claude dialect parser.
func NewClaudeDialect() *ClaudeDialect {
	return &ClaudeDialect{}
}

// Name returns the dialect name.
func (d *ClaudeDialect) Name() string {
	return "claude"
}

// Parse converts Claude Code event format to normalized Event.
//
// Claude Code sends events with the following format:
//
//	{
//	  "hook_event_name": "PreToolUse" | "PostToolUse" | "UserPromptSubmit" | etc.,
//	  "tool_name": "...",
//	  "prompt": "...",
//	  "message": "...",
//	  ...
//	}
func (d *ClaudeDialect) Parse(data map[string]interface{}) (*hooks.Event, error) {
	rawName := getString(data, "hook_event_name")
	if rawName == "" {
		// Fallback to checking other common fields
		rawName = getString(data, "event")
	}

	event := &hooks.Event{
		Name:    d.normalizeEventName(rawName),
		RawName: rawName,
		Dialect: "claude",
		Data: hooks.EventData{
			Prompt:    getString(data, "prompt"),
			ToolName:  getString(data, "tool_name"),
			Message:   getString(data, "message"),
			Reason:    getString(data, "reason"),
			Source:    getString(data, "source"),
			SessionID: getString(data, "session_id"),
			Raw:       data,
		},
	}

	// Extract tool input/output if available
	if val, ok := data["tool_input"]; ok {
		if str, ok := val.(string); ok {
			event.Data.ToolInput = str
		}
	}
	if val, ok := data["tool_output"]; ok {
		if str, ok := val.(string); ok {
			event.Data.ToolOutput = str
		}
	}

	// Extract status fields
	if val, ok := data["success"]; ok {
		if b, ok := val.(bool); ok {
			event.Data.Success = b
		}
	}
	if val, ok := data["error"]; ok {
		if str, ok := val.(string); ok {
			event.Data.Error = str
		}
	}

	// Extract token usage from top-level or nested "usage" object.
	// Claude Code may report tokens at top level or inside a usage map.
	extractTokens(data, &event.Data)

	// Extract file_path from tool_input/tool_response objects
	extractFilePath(data, &event.Data)

	// For main-agent end-of-turn events (Stop only — not SubagentStop),
	// Claude Code passes the final assistant text so downstream handlers
	// can surface it as an outbound agent→user message. Subagent turns
	// are internal to the harness and should not drive scion agent state.
	//
	// Content-type filtering: the extraction pipeline classifies content
	// blocks by type (text, thinking, tool_use, etc.) and stores them in
	// AssistantContent. AssistantText receives only user-visible "text"
	// blocks — thinking/reasoning content is filtered out to prevent it
	// from leaking into chat messages.
	//
	// Preferred source: the top-level "last_assistant_message" field,
	// which Claude Code 2.1+ includes in the Stop hook payload directly.
	// This is authoritative and race-free: the payload is handed to the
	// hook process as structured JSON, not via a file that may still be
	// flushing when we read it.
	//
	// Fallback: read "transcript_path" (a JSONL conversation log) and
	// collect text from the trailing contiguous run of assistant entries.
	// The transcript fallback covers older Claude Code versions that
	// omit last_assistant_message and any harness that exposes only the
	// transcript. It is racy against the harness's own writes, so it is
	// strictly a fallback, not the primary path.
	if event.Name == hooks.EventAgentEnd {
		text, content := extractAssistantContentFromPayload(data)
		if content != nil {
			event.Data.AssistantText = text
			event.Data.AssistantContent = content
		} else if path := getString(data, "transcript_path"); path != "" {
			text, content := extractFinalAssistantContentFromTranscript(path)
			if content != nil {
				event.Data.AssistantText = text
				event.Data.AssistantContent = content
			}
		}
	}

	return event, nil
}

// extractFinalAssistantText reads a Claude Code transcript JSONL file and
// returns the concatenated text blocks from the final assistant turn. A
// "final turn" is the contiguous run of assistant entries at the end of the
// transcript, stopped at the first preceding user entry. Tool-use and other
// non-text content blocks are skipped. On any error the function returns an
// empty string — callers must treat absence as "no assistant text
// available" rather than a failure condition.
func extractFinalAssistantText(path string) string {
	f, err := os.Open(path)
	if err != nil {
		return ""
	}
	defer func() { _ = f.Close() }()

	// Collect text from contiguous assistant entries at the tail of the
	// transcript. Iterate forward once (Claude transcripts are small
	// enough that double-pass or reverse-scan overhead is unnecessary);
	// reset the collected text whenever a user entry is seen so that by
	// the end of the scan we hold exactly the final assistant turn.
	var turnParts []string
	scanner := bufio.NewScanner(f)
	// Transcript lines can contain very long tool outputs; raise the
	// scanner buffer so we don't silently truncate them.
	scanner.Buffer(make([]byte, 0, 64*1024), 16*1024*1024)

	for scanner.Scan() {
		line := scanner.Bytes()
		if len(line) == 0 {
			continue
		}
		var entry struct {
			Type    string `json:"type"`
			Message struct {
				Role    string          `json:"role"`
				Content json.RawMessage `json:"content"`
			} `json:"message"`
		}
		if err := json.Unmarshal(line, &entry); err != nil {
			continue
		}
		entryType := entry.Type
		if entryType == "" {
			entryType = entry.Message.Role
		}

		switch entryType {
		case "user":
			// A user entry ends any prior assistant turn.
			turnParts = turnParts[:0]
		case "assistant":
			if text := assistantContentText(entry.Message.Content); text != "" {
				turnParts = append(turnParts, text)
			}
		}
	}
	// If the scanner hit an error (e.g. a single line exceeded the 16MB
	// buffer limit), return whatever text was collected before the error
	// rather than discarding the entire turn.
	if err := scanner.Err(); err != nil && len(turnParts) == 0 {
		return ""
	}

	return strings.TrimSpace(strings.Join(turnParts, "\n\n"))
}

// assistantContentText extracts text from an assistant message's content
// field, which in Claude transcripts is either a JSON array of typed blocks
// or (rarely) a plain string. Only "text" blocks contribute; tool_use and
// other block types are ignored.
func assistantContentText(content json.RawMessage) string {
	if len(content) == 0 {
		return ""
	}

	// Plain string content (older/simpler transcript shape).
	var s string
	if err := json.Unmarshal(content, &s); err == nil {
		return strings.TrimSpace(s)
	}

	// Typed block array.
	var blocks []struct {
		Type string `json:"type"`
		Text string `json:"text"`
	}
	if err := json.Unmarshal(content, &blocks); err != nil {
		return ""
	}

	var parts []string
	for _, b := range blocks {
		if b.Type == "text" && b.Text != "" {
			parts = append(parts, b.Text)
		}
	}
	return strings.TrimSpace(strings.Join(parts, ""))
}

// extractAssistantContentFromPayload extracts and classifies content from
// the last_assistant_message field in the hook payload. The field value may be:
//
//   - A string: treated as plain text (single text block), or parsed as a
//     JSON array of typed content blocks if it looks like JSON.
//   - A []interface{}: a structured array of content blocks with type fields.
//
// Returns the filtered user-visible text (thinking blocks stripped) and the
// full classified AssistantContent. Returns ("", nil) if no content is found.
func extractAssistantContentFromPayload(data map[string]interface{}) (string, *hooks.AssistantContent) {
	val, ok := data["last_assistant_message"]
	if !ok {
		return "", nil
	}

	switch v := val.(type) {
	case string:
		text := strings.TrimSpace(v)
		if text == "" {
			return "", nil
		}
		// Try to parse as a JSON array of typed content blocks.
		// Claude Code may send structured blocks as a JSON-encoded string.
		if blocks := parseContentBlocksFromJSON(text); len(blocks) > 0 {
			content := &hooks.AssistantContent{Blocks: blocks}
			return content.TextOnly(), content
		}
		// Plain string — treat as a single text block.
		content := &hooks.AssistantContent{
			Blocks: []hooks.ContentBlock{{Type: hooks.ContentBlockText, Text: text}},
		}
		return text, content

	case []interface{}:
		// Structured array of content blocks (already parsed from JSON).
		blocks := parseContentBlocksFromArray(v)
		if len(blocks) == 0 {
			return "", nil
		}
		content := &hooks.AssistantContent{Blocks: blocks}
		return content.TextOnly(), content

	default:
		return "", nil
	}
}

// parseContentBlocksFromJSON attempts to parse a string as a JSON array of
// typed content blocks. Returns nil if the string is not valid JSON or not
// an array of objects with "type" fields.
func parseContentBlocksFromJSON(s string) []hooks.ContentBlock {
	// Quick check: must look like a JSON array.
	if len(s) < 2 || s[0] != '[' {
		return nil
	}

	var rawBlocks []map[string]interface{}
	if err := json.Unmarshal([]byte(s), &rawBlocks); err != nil {
		return nil
	}

	// Validate that at least one entry has a "type" field — this
	// distinguishes a content block array from arbitrary JSON arrays.
	hasType := false
	for _, b := range rawBlocks {
		if _, ok := b["type"]; ok {
			hasType = true
			break
		}
	}
	if !hasType {
		return nil
	}

	var blocks []hooks.ContentBlock
	for _, b := range rawBlocks {
		block := classifyContentBlock(b)
		if block.Type != "" {
			blocks = append(blocks, block)
		}
	}
	return blocks
}

// parseContentBlocksFromArray converts a []interface{} (from JSON
// unmarshalling) into classified ContentBlocks.
func parseContentBlocksFromArray(arr []interface{}) []hooks.ContentBlock {
	var blocks []hooks.ContentBlock
	for _, item := range arr {
		m, ok := item.(map[string]interface{})
		if !ok {
			continue
		}
		block := classifyContentBlock(m)
		if block.Type != "" {
			blocks = append(blocks, block)
		}
	}
	return blocks
}

// classifyContentBlock converts a raw content block map into a typed
// ContentBlock. Supported block types:
//   - "text": user-visible text (text field)
//   - "thinking": reasoning/thinking traces (thinking field)
//   - "tool_use": tool invocations (name + input)
//   - "tool_result": tool outputs (content field)
func classifyContentBlock(m map[string]interface{}) hooks.ContentBlock {
	blockType := getString(m, "type")
	switch blockType {
	case "text":
		return hooks.ContentBlock{
			Type: hooks.ContentBlockText,
			Text: getString(m, "text"),
		}
	case "thinking":
		// Claude's thinking blocks use "thinking" field, not "text".
		text := getString(m, "thinking")
		if text == "" {
			text = getString(m, "text")
		}
		return hooks.ContentBlock{
			Type: hooks.ContentBlockThinking,
			Text: text,
		}
	case "tool_use":
		// Summarize as "tool_name: <name>" for downstream consumers.
		name := getString(m, "name")
		return hooks.ContentBlock{
			Type: hooks.ContentBlockToolUse,
			Text: name,
		}
	case "tool_result":
		text := getString(m, "content")
		if text == "" {
			text = getString(m, "text")
		}
		return hooks.ContentBlock{
			Type: hooks.ContentBlockToolResult,
			Text: text,
		}
	default:
		if blockType == "" {
			return hooks.ContentBlock{}
		}
		// Unknown block type — preserve with original type string.
		text := getString(m, "text")
		if text == "" {
			text = getString(m, "content")
		}
		return hooks.ContentBlock{Type: blockType, Text: text}
	}
}

// extractFinalAssistantContentFromTranscript reads a Claude Code transcript
// JSONL file and returns both filtered text and classified content blocks
// from the final assistant turn. This is the content-type-aware version of
// extractFinalAssistantText that populates AssistantContent.
func extractFinalAssistantContentFromTranscript(path string) (string, *hooks.AssistantContent) {
	f, err := os.Open(path)
	if err != nil {
		return "", nil
	}
	defer func() { _ = f.Close() }()

	var turnBlocks []hooks.ContentBlock
	scanner := bufio.NewScanner(f)
	scanner.Buffer(make([]byte, 0, 64*1024), 16*1024*1024)

	for scanner.Scan() {
		line := scanner.Bytes()
		if len(line) == 0 {
			continue
		}
		var entry struct {
			Type    string `json:"type"`
			Message struct {
				Role    string          `json:"role"`
				Content json.RawMessage `json:"content"`
			} `json:"message"`
		}
		if err := json.Unmarshal(line, &entry); err != nil {
			continue
		}
		entryType := entry.Type
		if entryType == "" {
			entryType = entry.Message.Role
		}

		switch entryType {
		case "user":
			turnBlocks = turnBlocks[:0]
		case "assistant":
			blocks := classifyTranscriptContent(entry.Message.Content)
			turnBlocks = append(turnBlocks, blocks...)
		}
	}

	if len(turnBlocks) == 0 {
		return "", nil
	}

	content := &hooks.AssistantContent{Blocks: turnBlocks}
	return content.TextOnly(), content
}

// classifyTranscriptContent parses assistant message content from a transcript
// entry and returns classified ContentBlocks. Content may be a JSON array of
// typed blocks or (rarely) a plain string.
func classifyTranscriptContent(content json.RawMessage) []hooks.ContentBlock {
	if len(content) == 0 {
		return nil
	}

	// Plain string content (older/simpler transcript shape).
	var s string
	if err := json.Unmarshal(content, &s); err == nil {
		text := strings.TrimSpace(s)
		if text == "" {
			return nil
		}
		return []hooks.ContentBlock{{Type: hooks.ContentBlockText, Text: text}}
	}

	// Typed block array.
	var rawBlocks []map[string]interface{}
	if err := json.Unmarshal(content, &rawBlocks); err != nil {
		return nil
	}

	var blocks []hooks.ContentBlock
	for _, b := range rawBlocks {
		block := classifyContentBlock(b)
		if block.Type != "" {
			blocks = append(blocks, block)
		}
	}
	return blocks
}

// normalizeEventName maps Claude Code event names to normalized names.
func (d *ClaudeDialect) normalizeEventName(name string) string {
	switch name {
	case "SessionStart":
		return hooks.EventSessionStart
	case "SessionEnd":
		return hooks.EventSessionEnd
	case "UserPromptSubmit":
		return hooks.EventPromptSubmit
	case "PreToolUse":
		return hooks.EventToolStart
	case "PostToolUse":
		return hooks.EventToolEnd
	case "Stop":
		return hooks.EventAgentEnd
	case "SubagentStop":
		return hooks.EventSubagentEnd
	case "Notification":
		return hooks.EventNotification
	case "BeforeModel", "ModelRequest":
		return hooks.EventModelStart
	case "AfterModel", "ModelResponse":
		return hooks.EventModelEnd
	default:
		return name
	}
}


FILE:/home/robocop/bin/pirate/pi-mono/packages/coding-agent/src/core/extensions/types.ts
/**
 * Extension system types.
 *
 * Extensions are TypeScript modules that can:
 * - Subscribe to agent lifecycle events
 * - Register LLM-callable tools
 * - Register commands, keyboard shortcuts, and CLI flags
 * - Interact with the user via UI primitives
 */

import type {
	AgentMessage,
	AgentToolResult,
	AgentToolUpdateCallback,
	ThinkingLevel,
} from "@mariozechner/pi-agent-core";
import type {
	Api,
	AssistantMessageEvent,
	AssistantMessageEventStream,
	Context,
	ImageContent,
	Model,
	OAuthCredentials,
	OAuthLoginCallbacks,
	SimpleStreamOptions,
	TextContent,
	ToolResultMessage,
} from "@mariozechner/pi-ai";
import type {
	AutocompleteItem,
	Component,
	EditorComponent,
	EditorTheme,
	KeyId,
	OverlayHandle,
	OverlayOptions,
	TUI,
} from "@mariozechner/pi-tui";
import type { Static, TSchema } from "@sinclair/typebox";
import type { Theme } from "../../modes/interactive/theme/theme.js";
import type { BashResult } from "../bash-executor.js";
import type { CompactionPreparation, CompactionResult } from "../compaction/index.js";
import type { EventBus } from "../event-bus.js";
import type { ExecOptions, ExecResult } from "../exec.js";
import type { ReadonlyFooterDataProvider } from "../footer-data-provider.js";
import type { KeybindingsManager } from "../keybindings.js";
import type { CustomMessage } from "../messages.js";
import type { ModelRegistry } from "../model-registry.js";
import type {
	BranchSummaryEntry,
	CompactionEntry,
	ReadonlySessionManager,
	SessionEntry,
	SessionManager,
} from "../session-manager.js";
import type { SlashCommandInfo } from "../slash-commands.js";
import type { SourceInfo } from "../source-info.js";
import type { BashOperations } from "../tools/bash.js";
import type { EditToolDetails } from "../tools/edit.js";
import type {
	BashToolDetails,
	BashToolInput,
	EditToolInput,
	FindToolDetails,
	FindToolInput,
	GrepToolDetails,
	GrepToolInput,
	LsToolDetails,
	LsToolInput,
	ReadToolDetails,
	ReadToolInput,
	WriteToolInput,
} from "../tools/index.js";

export type { ExecOptions, ExecResult } from "../exec.js";
export type { AgentToolResult, AgentToolUpdateCallback };
export type { AppKeybinding, KeybindingsManager } from "../keybindings.js";

// ============================================================================
// UI Context
// ============================================================================

/** Options for extension UI dialogs. */
export interface ExtensionUIDialogOptions {
	/** AbortSignal to programmatically dismiss the dialog. */
	signal?: AbortSignal;
	/** Timeout in milliseconds. Dialog auto-dismisses with live countdown display. */
	timeout?: number;
}

/** Placement for extension widgets. */
export type WidgetPlacement = "aboveEditor" | "belowEditor";

/** Options for extension widgets. */
export interface ExtensionWidgetOptions {
	/** Where the widget is rendered. Defaults to "aboveEditor". */
	placement?: WidgetPlacement;
}

/** Raw terminal input listener for extensions. */
export type TerminalInputHandler = (data: string) => { consume?: boolean; data?: string } | undefined;

/**
 * UI context for extensions to request interactive UI.
 * Each mode (interactive, RPC, print) provides its own implementation.
 */
export interface ExtensionUIContext {
	/** Show a selector and return the user's choice. */
	select(title: string, options: string[], opts?: ExtensionUIDialogOptions): Promise<string | undefined>;

	/** Show a confirmation dialog. */
	confirm(title: string, message: string, opts?: ExtensionUIDialogOptions): Promise<boolean>;

	/** Show a text input dialog. */
	input(title: string, placeholder?: string, opts?: ExtensionUIDialogOptions): Promise<string | undefined>;

	/** Show a notification to the user. */
	notify(message: string, type?: "info" | "warning" | "error"): void;

	/** Listen to raw terminal input (interactive mode only). Returns an unsubscribe function. */
	onTerminalInput(handler: TerminalInputHandler): () => void;

	/** Set status text in the footer/status bar. Pass undefined to clear. */
	setStatus(key: string, text: string | undefined): void;

	/** Set the working/loading message shown during streaming. Call with no argument to restore default. */
	setWorkingMessage(message?: string): void;

	/** Set the label shown for hidden thinking blocks. Call with no argument to restore default. */
	setHiddenThinkingLabel(label?: string): void;

	/** Set a widget to display above or below the editor. Accepts string array or component factory. */
	setWidget(key: string, content: string[] | undefined, options?: ExtensionWidgetOptions): void;
	setWidget(
		key: string,
		content: ((tui: TUI, theme: Theme) => Component & { dispose?(): void }) | undefined,
		options?: ExtensionWidgetOptions,
	): void;

	/** Set a custom footer component, or undefined to restore the built-in footer.
	 *
	 * The factory receives a FooterDataProvider for data not otherwise accessible:
	 * git branch and extension statuses from setStatus(). Token stats, model info,
	 * etc. are available via ctx.sessionManager and ctx.model.
	 */
	setFooter(
		factory:
			| ((tui: TUI, theme: Theme, footerData: ReadonlyFooterDataProvider) => Component & { dispose?(): void })
			| undefined,
	): void;

	/** Set a custom header component (shown at startup, above chat), or undefined to restore the built-in header. */
	setHeader(factory: ((tui: TUI, theme: Theme) => Component & { dispose?(): void }) | undefined): void;

	/** Set the terminal window/tab title. */
	setTitle(title: string): void;

	/** Show a custom component with keyboard focus. */
	custom<T>(
		factory: (
			tui: TUI,
			theme: Theme,
			keybindings: KeybindingsManager,
			done: (result: T) => void,
		) => (Component & { dispose?(): void }) | Promise<Component & { dispose?(): void }>,
		options?: {
			overlay?: boolean;
			/** Overlay positioning/sizing options. Can be static or a function for dynamic updates. */
			overlayOptions?: OverlayOptions | (() => OverlayOptions);
			/** Called with the overlay handle after the overlay is shown. Use to control visibility. */
			onHandle?: (handle: OverlayHandle) => void;
		},
	): Promise<T>;

	/** Paste text into the editor, triggering paste handling (collapse for large content). */
	pasteToEditor(text: string): void;

	/** Set the text in the core input editor. */
	setEditorText(text: string): void;

	/** Get the current text from the core input editor. */
	getEditorText(): string;

	/** Show a multi-line editor for text editing. */
	editor(title: string, prefill?: string): Promise<string | undefined>;

	/**
	 * Set a custom editor component via factory function.
	 * Pass undefined to restore the default editor.
	 *
	 * The factory receives:
	 * - `theme`: EditorTheme for styling borders and autocomplete
	 * - `keybindings`: KeybindingsManager for app-level keybindings
	 *
	 * For full app keybinding support (escape, ctrl+d, model switching, etc.),
	 * extend `CustomEditor` from `@mariozechner/pi-coding-agent` and call
	 * `super.handleInput(data)` for keys you don't handle.
	 *
	 * @example
	 * ```ts
	 * import { CustomEditor } from "@mariozechner/pi-coding-agent";
	 *
	 * class VimEditor extends CustomEditor {
	 *   private mode: "normal" | "insert" = "insert";
	 *
	 *   handleInput(data: string): void {
	 *     if (this.mode === "normal") {
	 *       // Handle vim normal mode keys...
	 *       if (data === "i") { this.mode = "insert"; return; }
	 *     }
	 *     super.handleInput(data);  // App keybindings + text editing
	 *   }
	 * }
	 *
	 * ctx.ui.setEditorComponent((tui, theme, keybindings) =>
	 *   new VimEditor(tui, theme, keybindings)
	 * );
	 * ```
	 */
	setEditorComponent(
		factory: ((tui: TUI, theme: EditorTheme, keybindings: KeybindingsManager) => EditorComponent) | undefined,
	): void;

	/** Get the current theme for styling. */
	readonly theme: Theme;

	/** Get all available themes with their names and file paths. */
	getAllThemes(): { name: string; path: string | undefined }[];

	/** Load a theme by name without switching to it. Returns undefined if not found. */
	getTheme(name: string): Theme | undefined;

	/** Set the current theme by name or Theme object. */
	setTheme(theme: string | Theme): { success: boolean; error?: string };

	/** Get current tool output expansion state. */
	getToolsExpanded(): boolean;

	/** Set tool output expansion state. */
	setToolsExpanded(expanded: boolean): void;
}

// ============================================================================
// Extension Context
// ============================================================================

export interface ContextUsage {
	/** Estimated context tokens, or null if unknown (e.g. right after compaction, before next LLM response). */
	tokens: number | null;
	contextWindow: number;
	/** Context usage as percentage of context window, or null if tokens is unknown. */
	percent: number | null;
}

export interface CompactOptions {
	customInstructions?: string;
	onComplete?: (result: CompactionResult) => void;
	onError?: (error: Error) => void;
}

/**
 * Context passed to extension event handlers.
 */
export interface ExtensionContext {
	/** UI methods for user interaction */
	ui: ExtensionUIContext;
	/** Whether UI is available (false in print/RPC mode) */
	hasUI: boolean;
	/** Current working directory */
	cwd: string;
	/** Session manager (read-only) */
	sessionManager: ReadonlySessionManager;
	/** Model registry for API key resolution */
	modelRegistry: ModelRegistry;
	/** Current model (may be undefined) */
	model: Model<any> | undefined;
	/** Whether the agent is idle (not streaming) */
	isIdle(): boolean;
	/** The current abort signal, or undefined when the agent is not streaming. */
	signal: AbortSignal | undefined;
	/** Abort the current agent operation */
	abort(): void;
	/** Whether there are queued messages waiting */
	hasPendingMessages(): boolean;
	/** Gracefully shutdown pi and exit. Available in all contexts. */
	shutdown(): void;
	/** Get current context usage for the active model. */
	getContextUsage(): ContextUsage | undefined;
	/** Trigger compaction without awaiting completion. */
	compact(options?: CompactOptions): void;
	/** Get the current effective system prompt. */
	getSystemPrompt(): string;
}

/**
 * Extended context for command handlers.
 * Includes session control methods only safe in user-initiated commands.
 */
export interface ExtensionCommandContext extends ExtensionContext {
	/** Wait for the agent to finish streaming */
	waitForIdle(): Promise<void>;

	/** Start a new session, optionally with initialization. */
	newSession(options?: {
		parentSession?: string;
		setup?: (sessionManager: SessionManager) => Promise<void>;
	}): Promise<{ cancelled: boolean }>;

	/** Fork from a specific entry, creating a new session file. */
	fork(entryId: string): Promise<{ cancelled: boolean }>;

	/** Navigate to a different point in the session tree. */
	navigateTree(
		targetId: string,
		options?: { summarize?: boolean; customInstructions?: string; replaceInstructions?: boolean; label?: string },
	): Promise<{ cancelled: boolean }>;

	/** Switch to a different session file. */
	switchSession(sessionPath: string): Promise<{ cancelled: boolean }>;

	/** Reload extensions, skills, prompts, and themes. */
	reload(): Promise<void>;
}

// ============================================================================
// Tool Types
// ============================================================================

/** Rendering options for tool results */
export interface ToolRenderResultOptions {
	/** Whether the result view is expanded */
	expanded: boolean;
	/** Whether this is a partial/streaming result */
	isPartial: boolean;
}

/** Context passed to tool renderers. */
export interface ToolRenderContext<TState = any, TArgs = any> {
	/** Current tool call arguments. Shared across call/result renders for the same tool call. */
	args: TArgs;
	/** Unique id for this tool execution. Stable across call/result renders for the same tool call. */
	toolCallId: string;
	/** Invalidate just this tool execution component for redraw. */
	invalidate: () => void;
	/** Previously returned component for this render slot, if any. */
	lastComponent: Component | undefined;
	/** Shared renderer state for this tool row. Initialized by tool-execution.ts. */
	state: TState;
	/** Working directory for this tool execution. */
	cwd: string;
	/** Whether the tool execution has started. */
	executionStarted: boolean;
	/** Whether the tool call arguments are complete. */
	argsComplete: boolean;
	/** Whether the tool result is partial/streaming. */
	isPartial: boolean;
	/** Whether the result view is expanded. */
	expanded: boolean;
	/** Whether inline images are currently shown in the TUI. */
	showImages: boolean;
	/** Whether the current result is an error. */
	isError: boolean;
}

/**
 * Tool definition for registerTool().
 */
export interface ToolDefinition<TParams extends TSchema = TSchema, TDetails = unknown, TState = any> {
	/** Tool name (used in LLM tool calls) */
	name: string;
	/** Human-readable label for UI */
	label: string;
	/** Description for LLM */
	description: string;
	/** Optional one-line snippet for the Available tools section in the default system prompt. Custom tools are omitted from that section when this is not provided. */
	promptSnippet?: string;
	/** Optional guideline bullets appended to the default system prompt Guidelines section when this tool is active. */
	promptGuidelines?: string[];
	/** Parameter schema (TypeBox) */
	parameters: TParams;
	/** Controls whether ToolExecutionComponent renders the standard colored shell or the tool renders its own framing. */
	renderShell?: "default" | "self";

	/** Optional compatibility shim to prepare raw tool call arguments before schema validation. Must return an object conforming to TParams. */
	prepareArguments?: (args: unknown) => Static<TParams>;

	/** Execute the tool. */
	execute(
		toolCallId: string,
		params: Static<TParams>,
		signal: AbortSignal | undefined,
		onUpdate: AgentToolUpdateCallback<TDetails> | undefined,
		ctx: ExtensionContext,
	): Promise<AgentToolResult<TDetails>>;

	/** Custom rendering for tool call display */
	renderCall?: (args: Static<TParams>, theme: Theme, context: ToolRenderContext<TState, Static<TParams>>) => Component;

	/** Custom rendering for tool result display */
	renderResult?: (
		result: AgentToolResult<TDetails>,
		options: ToolRenderResultOptions,
		theme: Theme,
		context: ToolRenderContext<TState, Static<TParams>>,
	) => Component;
}

type AnyToolDefinition = ToolDefinition<any, any, any>;

/**
 * Preserve parameter inference for standalone tool definitions.
 *
 * Use this when assigning a tool to a variable or passing it through arrays such
 * as `customTools`, where contextual typing would otherwise widen params to
 * `unknown`.
 */
export function defineTool<TParams extends TSchema, TDetails = unknown, TState = any>(
	tool: ToolDefinition<TParams, TDetails, TState>,
): ToolDefinition<TParams, TDetails, TState> & AnyToolDefinition {
	return tool;
}

// ============================================================================
// Resource Events
// ============================================================================

/** Fired after session_start to allow extensions to provide additional resource paths. */
export interface ResourcesDiscoverEvent {
	type: "resources_discover";
	cwd: string;
	reason: "startup" | "reload";
}

/** Result from resources_discover event handler */
export interface ResourcesDiscoverResult {
	skillPaths?: string[];
	promptPaths?: string[];
	themePaths?: string[];
}

// ============================================================================
// Session Events
// ============================================================================

/** Fired when a session is started, loaded, or reloaded */
export interface SessionStartEvent {
	type: "session_start";
	/** Why this session start happened. */
	reason: "startup" | "reload" | "new" | "resume" | "fork";
	/** Previously active session file. Present for "new", "resume", and "fork". */
	previousSessionFile?: string;
}

/** Fired before switching to another session (can be cancelled) */
export interface SessionBeforeSwitchEvent {
	type: "session_before_switch";
	reason: "new" | "resume";
	targetSessionFile?: string;
}

/** Fired before forking a session (can be cancelled) */
export interface SessionBeforeForkEvent {
	type: "session_before_fork";
	entryId: string;
}

/** Fired before context compaction (can be cancelled or customized) */
export interface SessionBeforeCompactEvent {
	type: "session_before_compact";
	preparation: CompactionPreparation;
	branchEntries: SessionEntry[];
	customInstructions?: string;
	signal: AbortSignal;
}

/** Fired after context compaction */
export interface SessionCompactEvent {
	type: "session_compact";
	compactionEntry: CompactionEntry;
	fromExtension: boolean;
}

/** Fired on graceful process shutdown paths such as Ctrl+C, Ctrl+D, SIGHUP, and SIGTERM. */
export interface SessionShutdownEvent {
	type: "session_shutdown";
}

/** Preparation data for tree navigation */
export interface TreePreparation {
	targetId: string;
	oldLeafId: string | null;
	commonAncestorId: string | null;
	entriesToSummarize: SessionEntry[];
	userWantsSummary: boolean;
	/** Custom instructions for summarization */
	customInstructions?: string;
	/** If true, customInstructions replaces the default prompt instead of being appended */
	replaceInstructions?: boolean;
	/** Label to attach to the branch summary entry */
	label?: string;
}

/** Fired before navigating in the session tree (can be cancelled) */
export interface SessionBeforeTreeEvent {
	type: "session_before_tree";
	preparation: TreePreparation;
	signal: AbortSignal;
}

/** Fired after navigating in the session tree */
export interface SessionTreeEvent {
	type: "session_tree";
	newLeafId: string | null;
	oldLeafId: string | null;
	summaryEntry?: BranchSummaryEntry;
	fromExtension?: boolean;
}

export type SessionEvent =
	| SessionStartEvent
	| SessionBeforeSwitchEvent
	| SessionBeforeForkEvent
	| SessionBeforeCompactEvent
	| SessionCompactEvent
	| SessionShutdownEvent
	| SessionBeforeTreeEvent
	| SessionTreeEvent;

// ============================================================================
// Agent Events
// ============================================================================

/** Fired before each LLM call. Can modify messages. */
export interface ContextEvent {
	type: "context";
	messages: AgentMessage[];
}

/** Fired before a provider request is sent. Can replace the payload. */
export interface BeforeProviderRequestEvent {
	type: "before_provider_request";
	payload: unknown;
}

/** Fired after user submits prompt but before agent loop. */
export interface BeforeAgentStartEvent {
	type: "before_agent_start";
	prompt: string;
	images?: ImageContent[];
	systemPrompt: string;
}

/** Fired when an agent loop starts */
export interface AgentStartEvent {
	type: "agent_start";
}

/** Fired when an agent loop ends */
export interface AgentEndEvent {
	type: "agent_end";
	messages: AgentMessage[];
}

/** Fired at the start of each turn */
export interface TurnStartEvent {
	type: "turn_start";
	turnIndex: number;
	timestamp: number;
}

/** Fired at the end of each turn */
export interface TurnEndEvent {
	type: "turn_end";
	turnIndex: number;
	message: AgentMessage;
	toolResults: ToolResultMessage[];
}

/** Fired when a message starts (user, assistant, or toolResult) */
export interface MessageStartEvent {
	type: "message_start";
	message: AgentMessage;
}

/** Fired during assistant message streaming with token-by-token updates */
export interface MessageUpdateEvent {
	type: "message_update";
	message: AgentMessage;
	assistantMessageEvent: AssistantMessageEvent;
}

/** Fired when a message ends */
export interface MessageEndEvent {
	type: "message_end";
	message: AgentMessage;
}

/** Fired when a tool starts executing */
export interface ToolExecutionStartEvent {
	type: "tool_execution_start";
	toolCallId: string;
	toolName: string;
	args: any;
}

/** Fired during tool execution with partial/streaming output */
export interface ToolExecutionUpdateEvent {
	type: "tool_execution_update";
	toolCallId: string;
	toolName: string;
	args: any;
	partialResult: any;
}

/** Fired when a tool finishes executing */
export interface ToolExecutionEndEvent {
	type: "tool_execution_end";
	toolCallId: string;
	toolName: string;
	result: any;
	isError: boolean;
}

// ============================================================================
// Model Events
// ============================================================================

export type ModelSelectSource = "set" | "cycle" | "restore";

/** Fired when a new model is selected */
export interface ModelSelectEvent {
	type: "model_select";
	model: Model<any>;
	previousModel: Model<any> | undefined;
	source: ModelSelectSource;
}

// ============================================================================
// User Bash Events
// ============================================================================

/** Fired when user executes a bash command via ! or !! prefix */
export interface UserBashEvent {
	type: "user_bash";
	/** The command to execute */
	command: string;
	/** True if !! prefix was used (excluded from LLM context) */
	excludeFromContext: boolean;
	/** Current working directory */
	cwd: string;
}

// ============================================================================
// Input Events
// ============================================================================

/** Source of user input */
export type InputSource = "interactive" | "rpc" | "extension";

/** Fired when user input is received, before agent processing */
export interface InputEvent {
	type: "input";
	/** The input text */
	text: string;
	/** Attached images, if any */
	images?: ImageContent[];
	/** Where the input came from */
	source: InputSource;
}

/** Result from input event handler */
export type InputEventResult =
	| { action: "continue" }
	| { action: "transform"; text: string; images?: ImageContent[] }
	| { action: "handled" };

// ============================================================================
// Tool Events
// ============================================================================

interface ToolCallEventBase {
	type: "tool_call";
	toolCallId: string;
}

export interface BashToolCallEvent extends ToolCallEventBase {
	toolName: "bash";
	input: BashToolInput;
}

export interface ReadToolCallEvent extends ToolCallEventBase {
	toolName: "read";
	input: ReadToolInput;
}

export interface EditToolCallEvent extends ToolCallEventBase {
	toolName: "edit";
	input: EditToolInput;
}

export interface WriteToolCallEvent extends ToolCallEventBase {
	toolName: "write";
	input: WriteToolInput;
}

export interface GrepToolCallEvent extends ToolCallEventBase {
	toolName: "grep";
	input: GrepToolInput;
}

export interface FindToolCallEvent extends ToolCallEventBase {
	toolName: "find";
	input: FindToolInput;
}

export interface LsToolCallEvent extends ToolCallEventBase {
	toolName: "ls";
	input: LsToolInput;
}

export interface CustomToolCallEvent extends ToolCallEventBase {
	toolName: string;
	input: Record<string, unknown>;
}

/**
 * Fired before a tool executes. Can block.
 *
 * `event.input` is mutable. Mutate it in place to patch tool arguments before execution.
 * Later `tool_call` handlers see earlier mutations. No re-validation is performed after mutation.
 */
export type ToolCallEvent =
	| BashToolCallEvent
	| ReadToolCallEvent
	| EditToolCallEvent
	| WriteToolCallEvent
	| GrepToolCallEvent
	| FindToolCallEvent
	| LsToolCallEvent
	| CustomToolCallEvent;

interface ToolResultEventBase {
	type: "tool_result";
	toolCallId: string;
	input: Record<string, unknown>;
	content: (TextContent | ImageContent)[];
	isError: boolean;
}

export interface BashToolResultEvent extends ToolResultEventBase {
	toolName: "bash";
	details: BashToolDetails | undefined;
}

export interface ReadToolResultEvent extends ToolResultEventBase {
	toolName: "read";
	details: ReadToolDetails | undefined;
}

export interface EditToolResultEvent extends ToolResultEventBase {
	toolName: "edit";
	details: EditToolDetails | undefined;
}

export interface WriteToolResultEvent extends ToolResultEventBase {
	toolName: "write";
	details: undefined;
}

export interface GrepToolResultEvent extends ToolResultEventBase {
	toolName: "grep";
	details: GrepToolDetails | undefined;
}

export interface FindToolResultEvent extends ToolResultEventBase {
	toolName: "find";
	details: FindToolDetails | undefined;
}

export interface LsToolResultEvent extends ToolResultEventBase {
	toolName: "ls";
	details: LsToolDetails | undefined;
}

export interface CustomToolResultEvent extends ToolResultEventBase {
	toolName: string;
	details: unknown;
}

/** Fired after a tool executes. Can modify result. */
export type ToolResultEvent =
	| BashToolResultEvent
	| ReadToolResultEvent
	| EditToolResultEvent
	| WriteToolResultEvent
	| GrepToolResultEvent
	| FindToolResultEvent
	| LsToolResultEvent
	| CustomToolResultEvent;

// Type guards for ToolResultEvent
export function isBashToolResult(e: ToolResultEvent): e is BashToolResultEvent {
	return e.toolName === "bash";
}
export function isReadToolResult(e: ToolResultEvent): e is ReadToolResultEvent {
	return e.toolName === "read";
}
export function isEditToolResult(e: ToolResultEvent): e is EditToolResultEvent {
	return e.toolName === "edit";
}
export function isWriteToolResult(e: ToolResultEvent): e is WriteToolResultEvent {
	return e.toolName === "write";
}
export function isGrepToolResult(e: ToolResultEvent): e is GrepToolResultEvent {
	return e.toolName === "grep";
}
export function isFindToolResult(e: ToolResultEvent): e is FindToolResultEvent {
	return e.toolName === "find";
}
export function isLsToolResult(e: ToolResultEvent): e is LsToolResultEvent {
	return e.toolName === "ls";
}

/**
 * Type guard for narrowing ToolCallEvent by tool name.
 *
 * Built-in tools narrow automatically (no type params needed):
 * ```ts
 * if (isToolCallEventType("bash", event)) {
 *   event.input.command;  // string
 * }
 * ```
 *
 * Custom tools require explicit type parameters:
 * ```ts
 * if (isToolCallEventType<"my_tool", MyToolInput>("my_tool", event)) {
 *   event.input.action;  // typed
 * }
 * ```
 *
 * Note: Direct narrowing via `event.toolName === "bash"` doesn't work because
 * CustomToolCallEvent.toolName is `string` which overlaps with all literals.
 */
export function isToolCallEventType(toolName: "bash", event: ToolCallEvent): event is BashToolCallEvent;
export function isToolCallEventType(toolName: "read", event: ToolCallEvent): event is ReadToolCallEvent;
export function isToolCallEventType(toolName: "edit", event: ToolCallEvent): event is EditToolCallEvent;
export function isToolCallEventType(toolName: "write", event: ToolCallEvent): event is WriteToolCallEvent;
export function isToolCallEventType(toolName: "grep", event: ToolCallEvent): event is GrepToolCallEvent;
export function isToolCallEventType(toolName: "find", event: ToolCallEvent): event is FindToolCallEvent;
export function isToolCallEventType(toolName: "ls", event: ToolCallEvent): event is LsToolCallEvent;
export function isToolCallEventType<TName extends string, TInput extends Record<string, unknown>>(
	toolName: TName,
	event: ToolCallEvent,
): event is ToolCallEvent & { toolName: TName; input: TInput };
export function isToolCallEventType(toolName: string, event: ToolCallEvent): boolean {
	return event.toolName === toolName;
}

/** Union of all event types */
export type ExtensionEvent =
	| ResourcesDiscoverEvent
	| SessionEvent
	| ContextEvent
	| BeforeProviderRequestEvent
	| BeforeAgentStartEvent
	| AgentStartEvent
	| AgentEndEvent
	| TurnStartEvent
	| TurnEndEvent
	| MessageStartEvent
	| MessageUpdateEvent
	| MessageEndEvent
	| ToolExecutionStartEvent
	| ToolExecutionUpdateEvent
	| ToolExecutionEndEvent
	| ModelSelectEvent
	| UserBashEvent
	| InputEvent
	| ToolCallEvent
	| ToolResultEvent;

// ============================================================================
// Event Results
// ============================================================================

export interface ContextEventResult {
	messages?: AgentMessage[];
}

export type BeforeProviderRequestEventResult = unknown;

export interface ToolCallEventResult {
	/** Block tool execution. To modify arguments, mutate `event.input` in place instead. */
	block?: boolean;
	reason?: string;
}

/** Result from user_bash event handler */
export interface UserBashEventResult {
	/** Custom operations to use for execution */
	operations?: BashOperations;
	/** Full replacement: extension handled execution, use this result */
	result?: BashResult;
}

export interface ToolResultEventResult {
	content?: (TextContent | ImageContent)[];
	details?: unknown;
	isError?: boolean;
}

export interface BeforeAgentStartEventResult {
	message?: Pick<CustomMessage, "customType" | "content" | "display" | "details">;
	/** Replace the system prompt for this turn. If multiple extensions return this, they are chained. */
	systemPrompt?: string;
}

export interface SessionBeforeSwitchResult {
	cancel?: boolean;
}

export interface SessionBeforeForkResult {
	cancel?: boolean;
	skipConversationRestore?: boolean;
}

export interface SessionBeforeCompactResult {
	cancel?: boolean;
	compaction?: CompactionResult;
}

export interface SessionBeforeTreeResult {
	cancel?: boolean;
	summary?: {
		summary: string;
		details?: unknown;
	};
	/** Override custom instructions for summarization */
	customInstructions?: string;
	/** Override whether customInstructions replaces the default prompt */
	replaceInstructions?: boolean;
	/** Override label to attach to the branch summary entry */
	label?: string;
}

// ============================================================================
// Message Rendering
// ============================================================================

export interface MessageRenderOptions {
	expanded: boolean;
}

export type MessageRenderer<T = unknown> = (
	message: CustomMessage<T>,
	options: MessageRenderOptions,
	theme: Theme,
) => Component | undefined;

// ============================================================================
// Command Registration
// ============================================================================

export interface RegisteredCommand {
	name: string;
	sourceInfo: SourceInfo;
	description?: string;
	getArgumentCompletions?: (argumentPrefix: string) => AutocompleteItem[] | null | Promise<AutocompleteItem[] | null>;
	handler: (args: string, ctx: ExtensionCommandContext) => Promise<void>;
}

export interface ResolvedCommand extends RegisteredCommand {
	invocationName: string;
}

// ============================================================================
// Extension API
// ============================================================================

/** Handler function type for events */
// biome-ignore lint/suspicious/noConfusingVoidType: void allows bare return statements
export type ExtensionHandler<E, R = undefined> = (event: E, ctx: ExtensionContext) => Promise<R | void> | R | void;

/**
 * ExtensionAPI passed to extension factory functions.
 */
export interface ExtensionAPI {
	// =========================================================================
	// Event Subscription
	// =========================================================================

	on(event: "resources_discover", handler: ExtensionHandler<ResourcesDiscoverEvent, ResourcesDiscoverResult>): void;
	on(event: "session_start", handler: ExtensionHandler<SessionStartEvent>): void;
	on(
		event: "session_before_switch",
		handler: ExtensionHandler<SessionBeforeSwitchEvent, SessionBeforeSwitchResult>,
	): void;
	on(event: "session_before_fork", handler: ExtensionHandler<SessionBeforeForkEvent, SessionBeforeForkResult>): void;
	on(
		event: "session_before_compact",
		handler: ExtensionHandler<SessionBeforeCompactEvent, SessionBeforeCompactResult>,
	): void;
	on(event: "session_compact", handler: ExtensionHandler<SessionCompactEvent>): void;
	on(event: "session_shutdown", handler: ExtensionHandler<SessionShutdownEvent>): void;
	on(event: "session_before_tree", handler: ExtensionHandler<SessionBeforeTreeEvent, SessionBeforeTreeResult>): void;
	on(event: "session_tree", handler: ExtensionHandler<SessionTreeEvent>): void;
	on(event: "context", handler: ExtensionHandler<ContextEvent, ContextEventResult>): void;
	on(
		event: "before_provider_request",
		handler: ExtensionHandler<BeforeProviderRequestEvent, BeforeProviderRequestEventResult>,
	): void;
	on(event: "before_agent_start", handler: ExtensionHandler<BeforeAgentStartEvent, BeforeAgentStartEventResult>): void;
	on(event: "agent_start", handler: ExtensionHandler<AgentStartEvent>): void;
	on(event: "agent_end", handler: ExtensionHandler<AgentEndEvent>): void;
	on(event: "turn_start", handler: ExtensionHandler<TurnStartEvent>): void;
	on(event: "turn_end", handler: ExtensionHandler<TurnEndEvent>): void;
	on(event: "message_start", handler: ExtensionHandler<MessageStartEvent>): void;
	on(event: "message_update", handler: ExtensionHandler<MessageUpdateEvent>): void;
	on(event: "message_end", handler: ExtensionHandler<MessageEndEvent>): void;
	on(event: "tool_execution_start", handler: ExtensionHandler<ToolExecutionStartEvent>): void;
	on(event: "tool_execution_update", handler: ExtensionHandler<ToolExecutionUpdateEvent>): void;
	on(event: "tool_execution_end", handler: ExtensionHandler<ToolExecutionEndEvent>): void;
	on(event: "model_select", handler: ExtensionHandler<ModelSelectEvent>): void;
	on(event: "tool_call", handler: ExtensionHandler<ToolCallEvent, ToolCallEventResult>): void;
	on(event: "tool_result", handler: ExtensionHandler<ToolResultEvent, ToolResultEventResult>): void;
	on(event: "user_bash", handler: ExtensionHandler<UserBashEvent, UserBashEventResult>): void;
	on(event: "input", handler: ExtensionHandler<InputEvent, InputEventResult>): void;

	// =========================================================================
	// Tool Registration
	// =========================================================================

	/** Register a tool that the LLM can call. */
	registerTool<TParams extends TSchema = TSchema, TDetails = unknown, TState = any>(
		tool: ToolDefinition<TParams, TDetails, TState>,
	): void;

	// =========================================================================
	// Command, Shortcut, Flag Registration
	// =========================================================================

	/** Register a custom command. */
	registerCommand(name: string, options: Omit<RegisteredCommand, "name" | "sourceInfo">): void;

	/** Register a keyboard shortcut. */
	registerShortcut(
		shortcut: KeyId,
		options: {
			description?: string;
			handler: (ctx: ExtensionContext) => Promise<void> | void;
		},
	): void;

	/** Register a CLI flag. */
	registerFlag(
		name: string,
		options: {
			description?: string;
			type: "boolean" | "string";
			default?: boolean | string;
		},
	): void;

	/** Get the value of a registered CLI flag. */
	getFlag(name: string): boolean | string | undefined;

	// =========================================================================
	// Message Rendering
	// =========================================================================

	/** Register a custom renderer for CustomMessageEntry. */
	registerMessageRenderer<T = unknown>(customType: string, renderer: MessageRenderer<T>): void;

	// =========================================================================
	// Actions
	// =========================================================================

	/** Send a custom message to the session. */
	sendMessage<T = unknown>(
		message: Pick<CustomMessage<T>, "customType" | "content" | "display" | "details">,
		options?: { triggerTurn?: boolean; deliverAs?: "steer" | "followUp" | "nextTurn" },
	): void;

	/**
	 * Send a user message to the agent. Always triggers a turn.
	 * When the agent is streaming, use deliverAs to specify how to queue the message.
	 */
	sendUserMessage(
		content: string | (TextContent | ImageContent)[],
		options?: { deliverAs?: "steer" | "followUp" },
	): void;

	/** Append a custom entry to the session for state persistence (not sent to LLM). */
	appendEntry<T = unknown>(customType: string, data?: T): void;

	// =========================================================================
	// Session Metadata
	// =========================================================================

	/** Set the session display name (shown in session selector). */
	setSessionName(name: string): void;

	/** Get the current session name, if set. */
	getSessionName(): string | undefined;

	/** Set or clear a label on an entry. Labels are user-defined markers for bookmarking/navigation. */
	setLabel(entryId: string, label: string | undefined): void;

	/** Execute a shell command. */
	exec(command: string, args: string[], options?: ExecOptions): Promise<ExecResult>;

	/** Get the list of currently active tool names. */
	getActiveTools(): string[];

	/** Get all configured tools with parameter schema and source metadata. */
	getAllTools(): ToolInfo[];

	/** Set the active tools by name. */
	setActiveTools(toolNames: string[]): void;

	/** Get available slash commands in the current session. */
	getCommands(): SlashCommandInfo[];

	// =========================================================================
	// Model and Thinking Level
	// =========================================================================

	/** Set the current model. Returns false if no API key available. */
	setModel(model: Model<any>): Promise<boolean>;

	/** Get current thinking level. */
	getThinkingLevel(): ThinkingLevel;

	/** Set thinking level (clamped to model capabilities). */
	setThinkingLevel(level: ThinkingLevel): void;

	// =========================================================================
	// Provider Registration
	// =========================================================================

	/**
	 * Register or override a model provider.
	 *
	 * If `models` is provided: replaces all existing models for this provider.
	 * If only `baseUrl` is provided: overrides the URL for existing models.
	 * If `oauth` is provided: registers OAuth provider for /login support.
	 * If `streamSimple` is provided: registers a custom API stream handler.
	 *
	 * During initial extension load this call is queued and applied once the
	 * runner has bound its context. After that it takes effect immediately, so
	 * it is safe to call from command handlers or event callbacks without
	 * requiring a `/reload`.
	 *
	 * @example
	 * // Register a new provider with custom models
	 * pi.registerProvider("my-proxy", {
	 *   baseUrl: "https://proxy.example.com",
	 *   apiKey: "PROXY_API_KEY",
	 *   api: "anthropic-messages",
	 *   models: [
	 *     {
	 *       id: "claude-sonnet-4-20250514",
	 *       name: "Claude 4 Sonnet (proxy)",
	 *       reasoning: false,
	 *       input: ["text", "image"],
	 *       cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
	 *       contextWindow: 200000,
	 *       maxTokens: 16384
	 *     }
	 *   ]
	 * });
	 *
	 * @example
	 * // Override baseUrl for an existing provider
	 * pi.registerProvider("anthropic", {
	 *   baseUrl: "https://proxy.example.com"
	 * });
	 *
	 * @example
	 * // Register provider with OAuth support
	 * pi.registerProvider("corporate-ai", {
	 *   baseUrl: "https://ai.corp.com",
	 *   api: "openai-responses",
	 *   models: [...],
	 *   oauth: {
	 *     name: "Corporate AI (SSO)",
	 *     async login(callbacks) { ... },
	 *     async refreshToken(credentials) { ... },
	 *     getApiKey(credentials) { return credentials.access; }
	 *   }
	 * });
	 */
	registerProvider(name: string, config: ProviderConfig): void;

	/**
	 * Unregister a previously registered provider.
	 *
	 * Removes all models belonging to the named provider and restores any
	 * built-in models that were overridden by it. Has no effect if the provider
	 * is not currently registered.
	 *
	 * Like `registerProvider`, this takes effect immediately when called after
	 * the initial load phase.
	 *
	 * @example
	 * pi.unregisterProvider("my-proxy");
	 */
	unregisterProvider(name: string): void;

	/** Shared event bus for extension communication. */
	events: EventBus;
}

// ============================================================================
// Provider Registration Types
// ============================================================================

/** Configuration for registering a provider via pi.registerProvider(). */
export interface ProviderConfig {
	/** Base URL for the API endpoint. Required when defining models. */
	baseUrl?: string;
	/** API key or environment variable name. Required when defining models (unless oauth provided). */
	apiKey?: string;
	/** API type. Required at provider or model level when defining models. */
	api?: Api;
	/** Optional streamSimple handler for custom APIs. */
	streamSimple?: (model: Model<Api>, context: Context, options?: SimpleStreamOptions) => AssistantMessageEventStream;
	/** Custom headers to include in requests. */
	headers?: Record<string, string>;
	/** If true, adds Authorization: Bearer header with the resolved API key. */
	authHeader?: boolean;
	/** Models to register. If provided, replaces all existing models for this provider. */
	models?: ProviderModelConfig[];
	/** OAuth provider for /login support. The `id` is set automatically from the provider name. */
	oauth?: {
		/** Display name for the provider in login UI. */
		name: string;
		/** Run the login flow, return credentials to persist. */
		login(callbacks: OAuthLoginCallbacks): Promise<OAuthCredentials>;
		/** Refresh expired credentials, return updated credentials to persist. */
		refreshToken(credentials: OAuthCredentials): Promise<OAuthCredentials>;
		/** Convert credentials to API key string for the provider. */
		getApiKey(credentials: OAuthCredentials): string;
		/** Optional: modify models for this provider (e.g., update baseUrl based on credentials). */
		modifyModels?(models: Model<Api>[], credentials: OAuthCredentials): Model<Api>[];
	};
}

/** Configuration for a model within a provider. */
export interface ProviderModelConfig {
	/** Model ID (e.g., "claude-sonnet-4-20250514"). */
	id: string;
	/** Display name (e.g., "Claude 4 Sonnet"). */
	name: string;
	/** API type override for this model. */
	api?: Api;
	/** Whether the model supports extended thinking. */
	reasoning: boolean;
	/** Supported input types. */
	input: ("text" | "image")[];
	/** Cost per token (for tracking, can be 0). */
	cost: { input: number; output: number; cacheRead: number; cacheWrite: number };
	/** Maximum context window size in tokens. */
	contextWindow: number;
	/** Maximum output tokens. */
	maxTokens: number;
	/** Custom headers for this model. */
	headers?: Record<string, string>;
	/** OpenAI compatibility settings. */
	compat?: Model<Api>["compat"];
}

/** Extension factory function type. Supports both sync and async initialization. */
export type ExtensionFactory = (pi: ExtensionAPI) => void | Promise<void>;

// ============================================================================
// Loaded Extension Types
// ============================================================================

export interface RegisteredTool {
	definition: ToolDefinition;
	sourceInfo: SourceInfo;
}

export interface ExtensionFlag {
	name: string;
	description?: string;
	type: "boolean" | "string";
	default?: boolean | string;
	extensionPath: string;
}

export interface ExtensionShortcut {
	shortcut: KeyId;
	description?: string;
	handler: (ctx: ExtensionContext) => Promise<void> | void;
	extensionPath: string;
}

type HandlerFn = (...args: unknown[]) => Promise<unknown>;

export type SendMessageHandler = <T = unknown>(
	message: Pick<CustomMessage<T>, "customType" | "content" | "display" | "details">,
	options?: { triggerTurn?: boolean; deliverAs?: "steer" | "followUp" | "nextTurn" },
) => void;

export type SendUserMessageHandler = (
	content: string | (TextContent | ImageContent)[],
	options?: { deliverAs?: "steer" | "followUp" },
) => void;

export type AppendEntryHandler = <T = unknown>(customType: string, data?: T) => void;

export type SetSessionNameHandler = (name: string) => void;

export type GetSessionNameHandler = () => string | undefined;

export type GetActiveToolsHandler = () => string[];

/** Tool info with name, description, parameter schema, and source metadata */
export type ToolInfo = Pick<ToolDefinition, "name" | "description" | "parameters"> & {
	sourceInfo: SourceInfo;
};

export type GetAllToolsHandler = () => ToolInfo[];

export type GetCommandsHandler = () => SlashCommandInfo[];

export type SetActiveToolsHandler = (toolNames: string[]) => void;

export type RefreshToolsHandler = () => void;

export type SetModelHandler = (model: Model<any>) => Promise<boolean>;

export type GetThinkingLevelHandler = () => ThinkingLevel;

export type SetThinkingLevelHandler = (level: ThinkingLevel) => void;

export type SetLabelHandler = (entryId: string, label: string | undefined) => void;

/**
 * Shared state created by loader, used during registration and runtime.
 * Contains flag values (defaults set during registration, CLI values set after).
 */
export interface ExtensionRuntimeState {
	flagValues: Map<string, boolean | string>;
	/** Provider registrations queued during extension loading, processed when runner binds */
	pendingProviderRegistrations: Array<{ name: string; config: ProviderConfig; extensionPath: string }>;
	/**
	 * Register or unregister a provider.
	 *
	 * Before bindCore(): queues registrations / removes from queue.
	 * After bindCore(): calls ModelRegistry directly for immediate effect.
	 */
	registerProvider: (name: string, config: ProviderConfig, extensionPath?: string) => void;
	unregisterProvider: (name: string, extensionPath?: string) => void;
}

/**
 * Action implementations for pi.* API methods.
 * Provided to runner.initialize(), copied into the shared runtime.
 */
export interface ExtensionActions {
	sendMessage: SendMessageHandler;
	sendUserMessage: SendUserMessageHandler;
	appendEntry: AppendEntryHandler;
	setSessionName: SetSessionNameHandler;
	getSessionName: GetSessionNameHandler;
	setLabel: SetLabelHandler;
	getActiveTools: GetActiveToolsHandler;
	getAllTools: GetAllToolsHandler;
	setActiveTools: SetActiveToolsHandler;
	refreshTools: RefreshToolsHandler;
	getCommands: GetCommandsHandler;
	setModel: SetModelHandler;
	getThinkingLevel: GetThinkingLevelHandler;
	setThinkingLevel: SetThinkingLevelHandler;
}

/**
 * Actions for ExtensionContext (ctx.* in event handlers).
 * Required by all modes.
 */
export interface ExtensionContextActions {
	getModel: () => Model<any> | undefined;
	isIdle: () => boolean;
	getSignal: () => AbortSignal | undefined;
	abort: () => void;
	hasPendingMessages: () => boolean;
	shutdown: () => void;
	getContextUsage: () => ContextUsage | undefined;
	compact: (options?: CompactOptions) => void;
	getSystemPrompt: () => string;
}

/**
 * Actions for ExtensionCommandContext (ctx.* in command handlers).
 * Only needed for interactive mode where extension commands are invokable.
 */
export interface ExtensionCommandContextActions {
	waitForIdle: () => Promise<void>;
	newSession: (options?: {
		parentSession?: string;
		setup?: (sessionManager: SessionManager) => Promise<void>;
	}) => Promise<{ cancelled: boolean }>;
	fork: (entryId: string) => Promise<{ cancelled: boolean }>;
	navigateTree: (
		targetId: string,
		options?: { summarize?: boolean; customInstructions?: string; replaceInstructions?: boolean; label?: string },
	) => Promise<{ cancelled: boolean }>;
	switchSession: (sessionPath: string) => Promise<{ cancelled: boolean }>;
	reload: () => Promise<void>;
}

/**
 * Full runtime = state + actions.
 * Created by loader with throwing action stubs, completed by runner.initialize().
 */
export interface ExtensionRuntime extends ExtensionRuntimeState, ExtensionActions {}

/** Loaded extension with all registered items. */
export interface Extension {
	path: string;
	resolvedPath: string;
	sourceInfo: SourceInfo;
	handlers: Map<string, HandlerFn[]>;
	tools: Map<string, RegisteredTool>;
	messageRenderers: Map<string, MessageRenderer>;
	commands: Map<string, RegisteredCommand>;
	flags: Map<string, ExtensionFlag>;
	shortcuts: Map<KeyId, ExtensionShortcut>;
}

/** Result of loading extensions. */
export interface LoadExtensionsResult {
	extensions: Extension[];
	errors: Array<{ path: string; error: string }>;
	/** Shared runtime - actions are throwing stubs until runner.initialize() */
	runtime: ExtensionRuntime;
}

// ============================================================================
// Extension Error
// ============================================================================

export interface ExtensionError {
	extensionPath: string;
	event: string;
	error: string;
	stack?: string;
}
