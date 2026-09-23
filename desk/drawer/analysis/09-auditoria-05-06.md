# 09 — Auditoría de 05-pendientes-concretos y 06-como-regenerar-este-analisis (2026-09-22)

Auditoría read-only: solo se ejecutaron comandos de lectura. Verificaciones directas en rutas del ecosistema (CWD `/home/jp/proyectos/hum-ecosystem` salvo indicación).

## Veredictos — doc 05

| Id | Veredicto |
|---|---|
| A1 | OK — `.governance/` existe, `git status` → `?? .governance/` (untracked). `INDEX.md` de 2026-06-02 13:53. |
| A2 | OK — `INDEX.md` §3 con 3.1/3.2/3.3/3.5/3.6/3.7/3.8 presentes. |
| A3 | PARCIAL — `INDEX.md` §3.7 y `desk/tasks/Board.md:29` citan `012-map-current-hum-to-hum-knowledge`; pero `012-map-current-wikipu*` ya no existe en `desk/tasks/` (38 archivos, 0 con 012/map-current). Colisión archivada, no viva. |
| A4 | OK — `hum-core/` existe. |
| A5 | OK — `.gitmodules` no existe (coherente con "sin registrar"). |
| A6 | **MAL** — `.gitignore` raíz EXISTE, commiteado (`git ls-files` lo lista), 53 B desde 2026-09-21 18:08, solo cubre `tools/kbsurfaces/`. "Falta .gitignore" es falso: debería decir "existe pero incompleto". |
| B1 | OK con matiz — branch `feature/weltgraph-spec-core` ✓; `.sldb/models+documents` borrados ✓; `core/`+`runtime/`+`tools/deskops` untracked (1279 líneas `??`) ✓. Matiz: `tools/deskops/desk/tasks/046-068` aparecen como ` D` (deleted, tracked), no "untracked". |
| B2 | OK — `tools/sldb`: `## main...origin/main [ahead 21]`, exacto. |
| B3 | PARCIAL — los 12 scripts raíz existen ✓; `hum-core/` ✓; `old/*-hum-*` NO existe. |
| C1 | **MAL** — los 20 `repo-*` existen ✓, pero el error real de hoy NO es `Duplicate repository root`. Error literal: `Error: Repository id 'deskops' not found in registry at '/home/jp/setup/desk/registry'. Supported path: run 'deskops repo register <name> --path <abs>' or add an entry to the ecosystem registry.` (exit 1). El CLI consulta `/home/jp/setup/desk/registry`, no `tools/deskops/desk/registry`; "VERIFICADO hoy" es stale. |
| C2 | OK — `repo-setup.md` existe (299 B) y `deskops inbox list --root /home/jp/setup` → exit 0 ("Delivered inbox note from setup to setup at .../desk/inbox/20260922-145929-unclear-list.md"; "Tracked"). |
| D1 | OK — `runtime.yaml` 677 B ✓; 0 referencias a `runtime.yaml` en el paquete deskops ✓. Matiz: `initializer.py` está en `deskops/runtime/initializer.py`; `deskops/cli/commands/` no existe. |
| D2 | OK — `herdr/init_opsys.py` existe (2906 B). |
| D3 | OK — `~/.config/herdr/herdr-server.log` existe, 3.8 MB. |
| D4 | OK — `closeout.py` líneas 60-72 confirman lectura `run_id`/`session`/`session_sha256` solo de manifest. |
| D5 | OK — `deskops/models/run.py` existe. |
| E1 | OK — `Board.md` ✓; 4 features ✓; iso-lab sldb = 8 tasks (9 archivos − Board) ✓; `task-extract-store-...` con `Status: deferred` ✓. |
| E2 | OK — 3 drafts exactos. |
| E3 | PARCIAL — 12 macros + 50 granulars ✓; `macro-12-ux-stress-hardening.yml` ✓; `ux-stress-test.md` y `vistas-sldb-ui.md` NO están en `drawer/tasks/` (no verificables). |
| E4 | OK — `report-ui-purpose-gap.md` ✓. |
| E5 | PARCIAL — kgdb = **27** tareas (doc: 26, off-by-one); sldb 8 ✓; deskops 1 ✓. |
| E6 | PARCIAL — 11 features ✓, 2 tasks ✓, 38 issues ("~40" aceptable) ✓. Matices: solo 2 questions tienen `Status: deferred` (canonical-runtime-artifact-policy, sldb-kgdb-boundaries); `question-herdr-runtime-open-decisions.md` está `Status: resolved` → "3 abiertas" es stale. "ready to promote" no aparece en `feature-adhoc-subagent-launcher-tmux-multi-cli.md`. |

## Veredictos — doc 06 (ejecutabilidad)

| Comando/Facto | Veredicto |
|---|---|
| `spawn` | **MAL** — firma real: `spawn <kind> [cwd] [agent-args...]`. NO acepta nombre de worker. `spawn pi pi-01 /home/jp/setup --provider openrouter --model ...` trataría `pi-01` como cwd y `/home/jp/setup` como arg de agente. Nombres son auto-generados: `pi`, `pi2`, `pi3`… (`free_agent_name`); hoy vivos `pi5/pi6/pi7`. No existe worker `pi-01`; `dispatch pi-01` fallaría por target inexistente. |
| `dispatch <T> "<text>"` | OK — acepta texto como argumento; `HERDR_TRANSCRIPT` soportado (`TRANSCRIPT="${HERDR_TRANSCRIPT:-...}"`). Heredoc `$(cat <<'...')` válido. |
| Comandos citados | OK — existen en el `case` final: `agents`, `dispatch`, `spawn`, `workers-close`, `close`, `say`, `read`, `wait`, `spawn-fork`, `workers`, `workers-reap`. |
| Modelo | OK — `~deepseek/deepseek-v4-flash-latest` es el default documentado en `.pi/skills/agent-coordinator/SKILL.md:75,92` y `pi/settings.example.json`. |
| Bug `agent_prompt_stalled` | NO mencionado. Existe en `coordination.sh:82`: `*timeout*|*agent_prompt_stalled*) die "dispatch to $t failed: $status"`. El runbook no advierte del falso negativo (no re-despachar). |
| Bug `close` | NO mencionado. `cmd_close` (línea 174) hace `herdr pane close` y printea `closed`; el runbook no advierte que el worker queda vivo/idle. `workers-close` cierra la tab completa (coherente con el doc). |

## Errores que hay que corregir

- 05/A6: `.gitignore` raíz ya existe y está commiteado — reformular a "incompleto, promesa feature-004 sin cumplir a medias".
- 05/C1: error literal actualizado (ver tabla); "Duplicate repository root" e "intake roto en tools/deskops" no se reproducen con `--root tools/deskops` hoy.
- 05/E3: quitar o reubicar `ux-stress-test.md`/`vistas-sldb-ui.md` (no están en `drawer/tasks/`).
- 05/E5: kgdb 27, no 26.
- 05/E6: questions abiertas = 2 (deferred); herdr-runtime `resolved`. Quitar "ready to promote" sin cita.
- 05/B3: `old/*-hum-*` no existe.
- 06: comando de spawn inválido (paso 2) y dispatches a `pi-NN` imposibles — corregir con `spawn` sin nombre + leer nombre real de `coordination.sh agents`.

## Huecos del runbook (06)

- FALTA advertir el bug `agent_prompt_stalled`: a veces error a los 5 s siendo falso negativo (el prompt SÍ llegó y el worker trabaja); NO re-despachar ni marcar fallo; verificar con `read`/`herdr agent list`.
- FALTA advertir el bug `close`: printea `closed` pero el worker sigue vivo e idle; usar `workers-reap --all` o comprobar pane tras cerrar.
- FALTA paso "leer el nombre real del worker": tras spawn, ejecutar `bash /home/jp/setup/herdr/coordination.sh agents` y usar `pi`, `pi2`… (no `pi-01`) en `dispatch`.
- Menor: no indica el timeout por defecto de dispatch (600000 ms); no cubre recuperación si un document falla o si herdr no responde en el spawn.
- OK: prerequisitos, evidencia, prompts literales, limpieza y secciones 5-6 cubren la reproducción salvo lo anterior.