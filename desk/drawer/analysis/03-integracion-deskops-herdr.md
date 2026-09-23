# Análisis: integración deskops ↔ herdr — duplicación y seam de transporte

Sospecha del usuario: **CONFIRMADA, con dos grados distintos**:

- **B vs C es duplicación literal** (≈90% del cuerpo de `init_opsys.py` copia `initializer.py`), y `desk/runtime.yaml` es **config muerta** (cero lectores en `.py`).
- **A vs B es duplicación funcional** (mismo verbo CLI de herdr, orquestación distinta), no línea a línea. Es el solape que la tabla de abajo cuantifica.

## 1) Mapa de duplicación

| Capacidad | A: `herdr/coordination.sh` | B: `deskops/runtime/` (herdr.py + initializer.py + supervise.py) | C: `herdr/init_opsys.py` | Dueño único |
|---|---|---|---|---|
| Crear workspace por label + reúso idempotente | (solo traza de tab al spawn) | `initializer.py:41-50` (check label sobre `workspace list`) | `init_opsys.py:52-59`, **misma comprobación literal** | B → provider (`find_or_create_workspace`) |
| Layout base nvim / yazi / pytest | — | `initializer.py:33-42` hardcodeado | `init_opsys.py:30-38`, **mismos 3 `LayoutPaneSpec` literales** | `runtime.yaml` (única fuente) leído por B |
| Lanzar agentes por rol | `spawn` / `spawn-fork` + `free_agent_name` + `workers_pane` | `build_role_agent_panes` (RoleDoc + RuntimeProfileDoc, `initializer.py:50-79`) | hardcode `AgentSpec("executor"/"tester", kind="pi")` (`init_opsys.py:44-47`) — ids **divergen** de los RoleDocs reales `deskops-executor`/`deskops-tester` | B (role-driven); A conserva solo el registro de ownership |
| Prompt / read / wait | `dispatch` `say` `read` `wait` | `send()` `read()` `wait()` | — | B como primitiva; A como fachada shell |
| Lifecycle workspace (status/attach/stop) | `workers-tab/focus/close` | `status()` `attach()` `stop()` | — | B |
| Cierre/reap de agentes | `close` `workers-reap` + registro `WORKERS_DB` (único) | — (solo `stop` de workspace entero) | — | A mientras no exista `close_pane()` en B |
| Supervisión blocked/done (backoff `state_change_seq`) | — | `supervise.py` (único, sin duplicado) | — | B |
| Ensure server | `need_herdr` (solo PATH) | `ensure_herdr_server` (arranca + poll 30×200ms) | — | B |
| Contrato declarativo de layout | **nadie lo lee** | hardcoded en `initializer.py:33-42` | hardcoded en `init_opsys.py:30-38` | `runtime.yaml` |

**Evidencia de que `runtime.yaml` no lo lee nadie:** `grep -rn "runtime.yaml"` en `deskops/` (solo `*.py`) = **cero hits**; las únicas menciones son el feature-doc y este gap-doc. En setup, solo `README.md` y el gap-doc lo citan. El layout real vive hardcodeado en B y C.

**Evidencia línea a línea B≡C:** imports idénticos (`DeskConfig`, `DeskopsOperations`, `HerdrClient/Provider`, `AgentSpec/ExecutionPlan/LayoutPaneSpec/ProcessSpec`); mismo gate `project_identity == "unknown-project"`; mismo `tasks = list_tasks()`; mismos 3 panes `("nvim", ".")`, `("yazi", ".")`, `("pytest",)`; mismo reúso por label sobre `workspace list`. Única diferencia real: B deriva agentes de RoleDocs, C los hardcodea — y como hay `desk/roles/deskops-executor.md` + `desk/roles/deskops-tester.md` (`kind: pi`) + `desk/runtimes/runtime-pi.md`, B ya produce lo que C duplica a mano.

## 2) Superficie de contacto deskops ↔ herdr que YA funciona

- Binario externo cerrado (`/home/jp/.local/bin/herdr`, ELF static-pie 24MB): integración 100% por CLI JSON desde fuera, tal como la restricción obliga. `HerdrClient.call()` es el único punto de acoplamiento del proceso.
- Frontera de identidad sana: **Herdr es la autoridad de IDs**; `WorkspaceHandle` no deriva IDs de deskops (lo declara su docstring y `runtime_document()`).
- `deskops runtime init` (arranca server vía `ensure_herdr_server`, crea/reusa espacio por label, panes + agentes de rol), `status`, `attach`, `stop`.
- `deskops runtime supervise` ya mide contra herdr: `wait` + `state_change_seq` anticuenta el busy-spin del socket.
- En setup, `coordination.sh` ya orquesta workers multi-coordinador por CLI, con registro propio de ownership (`WORKERS_DB` TSV por `$HERDR_PANE_ID`) y transcript a disco (`.herdr-coordination.md`).
- Falta en el contacto: **`deskops launch` no existe** (el CLI solo llega a `runtime`); el parser no tiene `launch` (grep: cero).

## 3) Falta para el seam de transporte (herdr | tmux)

**Veredicto sobre la abstracción actual:** `HerdrProvider` + `ExecutionPlan` + `AgentSpec` + `LayoutPaneSpec` ya son **~80% de un seam válido** (métodos con firma de transporte, testables con `runner` fake). Faltan exactamente:

1. `RuntimeProvider` como `Protocol` + factory `get_runtime_provider(name: str, executable: str) -> RuntimeProvider`.
2. Mover el reúso-por-label (hoy duplicado en `initializer.py:41-50` y `init_opsys.py:52-59`) al provider: `find_or_create_workspace(plan) -> WorkspaceHandle`.
3. `ensure_server()` como método del provider (hoy `ensure_herdr_server` suelto en initializer).
4. `supervise.py` y `runtime.py` tipando contra el `Protocol` (hoy `runtime.py:48-50` llama `client.call` directo para status/attach/stop, saltándose el provider).
5. Flag `--transport {herdr|tmux}` en el parser, con default leído de `runtime.yaml` → **primer lector real de ese archivo**.
6. Métodos que hoy solo existen en A: `close_pane(handle, pane_key)`, `list_agents()`. A queda como fachada shell o se absorbe.
7. `deskops launch <task> --agent ...` (feature) sobre `provider.send` + bundle de contexto ya existente; transport-agnóstico.

**Interfaz concreta propuesta:**

```python
class RuntimeProvider(Protocol):
    def ensure_server(self, executable: str) -> None: ...
    def find_or_create_workspace(self, plan: ExecutionPlan) -> WorkspaceHandle: ...
    def start_process(self, ws, pane_key, spec: ProcessSpec) -> dict: ...
    def start_agent(self, ws, pane_key, spec: AgentSpec) -> dict: ...
    def send(self, ws, agent_id, message, *, wait=False) -> dict: ...
    def wait(self, agent_id, *, until=(), timeout_ms=None) -> dict: ...
    def read(self, agent_id, *, lines=200) -> str: ...
    def status(self, ws) -> dict: ...
    def attach(self, ws) -> dict: ...
    def stop(self, ws) -> dict: ...
    def close_pane(self, ws, pane_key) -> None: ...          # nuevo (hoy solo en A)
    def list_agents(self) -> list[dict]: ...                 # nuevo (hoy solo en A)
def get_runtime_provider(name: str, executable: str) -> RuntimeProvider: ...
```

**Reconciliación de la decisión 3:** el seam convierte "herdr **o** tmux" en "herdr **y** tmux vía un contrato único". La feature de tmux (launch ad-hoc) y la decisión de retargetear a herdr dejan de ser incompatibles: herdr = provider por defecto para el runtime supervisado (estados `idle/working/blocked/done` ya existentes), `TmuxProvider` = idéntico contrato sin estados de agente — shim de lifecycle por logfile + sentinel `result-summary.md`, siguiendo el patrón ya documentado en la feature (`new-session -d -s deskops-<id> 'cmd | tee console.log'`, `has-session` = status, `attach`, `kill-session` = stop). El default sale de `runtime.yaml` `runtime.provider`; el usuario fuerza `--transport tmux` donde no haya herdr.

## 4) Plan de deduplicación (pasos ordenados y reversibles)

| Paso | Acción | Reversible |
|---|---|---|
| P0 | Golden test: capturar salida de `herdr workspace list` + `agent list` + salida de `coordination.sh agents` antes de tocar nada | baseline guardable |
| P1 | Añadir `RuntimeProvider` Protocol + `get_runtime_provider`; `HerdrProvider` lo implementa; no se borra nada | borrar el archivo |
| P2 | Mover reúso-por-label a `find_or_create_workspace`; `initializer` se vuelve delgado; test: `deskops runtime init` 2× → mismo workspace | revertir el método |
| P3 | `supervise.py` y `runtime.py` contra el Protocol (status/attach/stop por provider, no `client.call`) | revertir el import |
| P4 | `git mv herdr/init_opsys.py herdr/init_opsys.py.deprecated` y apuntar `install/init-herdr.sh` a `deskops runtime init`; borrar tras validar workspace byte-igual | el `.deprecated` queda como respaldo |
| P5 | Cargar layout desde `desk/runtime.yaml` (reader nuevo en B) con fallback al layout hardcoded; `runtime.yaml` deja de ser decorativo | fallback = estado actual |
| P6 | `deskops launch` (bundle de contexto + `provider.send` + run-dir); absorber `close`/`workers-reap` como `close_pane`/`list_agents` o dejar A como fachada shell única de ownership | feature detrás de flag |
| P7 | `TmuxProvider` + flag `--transport` + default desde `runtime.yaml`; cerrar la feature tmux y la decisión 3 como reconciliadas | flag con default herdr |

Regla de reversibilidad global: cada paso es aditivo o mantiene el archivo viejo vivo hasta que el paso siguiente se valida; nada se borra en el mismo paso que se reemplaza.