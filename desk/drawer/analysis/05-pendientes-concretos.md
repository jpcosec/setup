# Pendientes concretos — inventario accionable (2026-09-22)

Inventario READ-ONLY de pendientes verificados hoy. Salvo los comandos de diagnóstico citados (inbox, greps, conteos), nada fue modificado, commiteado ni staged. Cada fila: | Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |.

## BLOQUE A — Decisiones bloqueantes

| Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |
|---|---|---|---|---|---|
| A1 | `.governance/` marcado **DELETE AFTER REVIEW** (README interno), stale desde 2026-06-02, sigue untracked | `/hum-ecosystem/.governance/` | decisión | Sección UNCLEAR entera | Revisado y borrado: `git status` sin `?? .governance/` |
| A2 | Sección 3 UNCLEAR sin resolver: 3.1 rename opsys→deskops (¿borrar repo-opsys.md? ¿repo-deskops.md?), 3.2 política de submodulos, 3.3 hum-core/migrate_hum_scrapper/.worktree/.playwright-mcp, 3.5 registry fantasma (ontology, test-repo, truth-machine), 3.6 branch "weltgraph", 3.8 turns_session perdido | `.governance/INDEX.md` §3 | decisión | Cierre del pase de limpieza 2026-06-02 | Cada sub-ítem con decisión escrita + acción; luego eliminar `.governance/` |
| A3 | Colisión de task id 012 (`map-current-wikipu`→`map-current-hum`): Board usa el nuevo, queda referencias viejas por renumerar | `.governance/INDEX.md` §3.7; `desk/tasks/` | decisión | dependencias `depends_on` futuras | ID único por tarea; sin referencias al id 012 viejo |
| A4 | Destino de `hum-core/` (repo git anidado, sandbox de la extracción de `knowledge`): ¿keep o delete cuando termine la extracción? | `/hum-ecosystem/hum-core/` | decisión | Commit del split hum/knowledge (RFC no adoptado, scaffolding ya aplicado) | Decisión escrita; hum-core commiteado o eliminado + docs apuntan a `core/knowledge/` |
| A5 | Política de submodulos inexistente: ¿bump de punteros en commit padre o por-repo?; 6 submodulos con drift | `.gitmodules` (sin registrar); ver B2 | decisión | Entrega de tools/sldb, kgdb, spec2viz | Política escrita en docs; punteros sincronizados y commiteados |
| A6 | Falta `.gitignore` raíz (prometido por feature-004): `__pycache__/`, `.pytest_cache/`, `cc/cc`, `.deskops.log`, `.sldb/runtime/` ensucian todo `git status` | raíz de hum-ecosystem | decisión | Visibilidad de B1/B3 | `.gitignore` commiteado; `git status` sin ruido de cachés |

## BLOQUE B — Higiene de repositorio

| Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |
|---|---|---|---|---|---|
| B1 | Migración masiva sin commitear en rama `feature/weltgraph-spec-core`: `.sldb/` modelos/documents borrados (nuevo `core/`+`runtime/` untracked), rename wikipu→hum a medias, `tools/opsys` borrado, `tools/deskops/` entero untracked, src de sldb-ui untracked, `tools/deskops/desk/tasks/046-068` untracked | todo hum-ecosystem | higiene | Flujo de trabajo de agentes y review | Commits en tandas coherentes (A6 primero); `git status` refleja solo trabajo nuevo real |
| B2 | Drift de submodulos: `tools/sldb` **21 commits ahead de origin sin pushear**; kgdb/spec2viz/repopackage/hum-scrapper/graph_ui con contenido modificado/untracked; `m tools/ontology` | `/hum-ecosystem/tools/*` | higiene | Entrega de sldb (necesidad de decision A5) | `tools/sldb` pusheado (0 ahead); resto sin drift reportado |
| B3 | Scratch en la raíz sin commitear: `check.py`, `cleanup_desk.py`, `fix.py`, `fix_all.py`, `fix_frontmatters.py`, `fix_imports2.py`, `fix_pills_final.py`, `patch_test.py`, `patch_test2.py`, `split_atom.py`, `extract_ontology.py`, `migrate_hum_scrapper.sh`, `hum-core/`, `old/*-hum-*` | raíz de hum-ecosystem | higiene | Claridad de B1 | Cada archivo promovido, movido, o borrado (decisión en A4) |

## BLOQUE C — Intake roto en ambos extremos

| Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |
|---|---|---|---|---|---|
| C1 | **VERIFICADO hoy**: `deskops inbox list` desde `tools/deskops` falla: `Duplicate repository root` — 20 repo-docs de stress-test en `desk/registry/` generan 9 entradas duplicadas del mismo root | `/hum-ecosystem/tools/deskops/desk/registry/` (20 archivos `repo-*`) | bug (higiene) | Inbox/coordinación del propio deskops | `deskops inbox list` OK; registry con 1 entrada por root |
| C2 | **CORRECCIÓN vs nota previa**: `deskops inbox list` desde `/home/jp/setup` YA FUNCIONA (verificado hoy; incluso entregó nota pendiente). `Repository id 'setup' not found` quedó resuelto: existe `desk/registry/repo-setup.md` (id: setup, path `/home/jp/setup`) | `/home/jp/setup/desk/registry/repo-setup.md`; nota `desk/drawer/herdr-runtime-contract-gaps.md` §4 | stale | — (ya desbloqueado) | Actualizar la nota del drawer (quitar "Blocked intake"); `deskops inbox list` OK en setup |

## BLOQUE D — Deuda de runtime

| Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |
|---|---|---|---|---|---|
| D1 | `desk/runtime.yaml` **no lo lee nadie** — VERIFICADO: 0 referencias a `runtime.yaml` en el paquete deskops; el layout real está hardcodeado en `initializer.py:33-42` | `/home/jp/setup/desk/runtime.yaml` (677 B) | deuda/decisión | D4/D5 (contrato de runtime) | `initializer.py` lo lee, o el archivo se borra; no hay dos fuentes de layout |
| D2 | `herdr/init_opsys.py` duplica el initializer de deskops (mismos panes nvim/yazi/pytest, mismos `AgentSpec(kind="pi")`) | `/home/jp/setup/herdr/init_opsys.py` | deuda | Deriva futura de layouts (ya pasó con ROLE_AGENT_SPECS) | `init_opsys.py` es wrapper de `deskops runtime init` o se elimina; `install/init-herdr.sh` actualizado |
| D3 | Log de herdr sin rotación ni límite de trazabilidad: servidor guarda solo estado vivo, TUI agents fuera de scrollback, sin transcript persistente | `~/.config/herdr/herdr-server.log` | bug/deuda | Auditoría de ejecución | Política de rotación/prune implementada y documentada (o trace movido a pi `--session`) |
| D4 | `--session` no cableado: `closeout.py:64-69` lee `run_id`/`session_sha256` solo del manifest (default null); ningún path los escribe | `/hum-ecosystem/tools/deskops/deskops/cli/commands/closeout.py` | feature pendiente | RunDoc sin trazabilidad real | closeout emite `Run-Id:`/`Session-Sha256:` no vacíos tras ejecución de subagente |
| D5 | `RunDoc` registrado en el modelo pero **nadie lo escribe**: únicas referencias en `deskops/models/run.py` (modelo) y `closeout.py` (lectura); sin comando que lo cree | `/hum-ecosystem/tools/deskops/deskops/models/run.py` | feature pendiente | Trazabilidad de ejecuciones | Existe comando que materializa RunDoc en `runs/` tras cada ejecución |

## BLOQUE E — Tareas deferred/abiertas en drawers, por repo (conteo real verificado)

| Id | Qué es | Ubicación | Tipo | Bloquea a | Criterio de cierre verificable |
|---|---|---|---|---|---|
| E1 | **sldb**: Board del drawer lista **8 tareas** diferidas (addressability-model, mapear-arquitectura-real, arquitectura-objetivo-modular, ast-query-primitives, estrategia-extracción, refactor-núcleo, composition-modes, export-provenance-contract) — los archivos existen con `status: active` en el worktree iso-lab; + `task-extract-store-into-generic-typed-document-engine` `Status: deferred`; + **4 features open** (decoupled-AST, executable-markdown-hooks, nested-primitives, separate-ast-template) | `tools/sldb/desk/drawer/tasks/Board.md`, `drawer/features/*`, `tools/iso-lab/worktrees/sldb/desk/tasks/` (8 archivos) | deferred | Refactor del núcleo sldb | Cada tarea promovida a desk/tasks con estado cerrado, o Board reescrito sin backlog muerto |
| E2 | **spec2viz**: **3 tareas draft** (mermaid-pipeline-robustness, migration-and-spec-provenance, v2-orchestration-and-templating) | `tools/spec2viz/desk/drawer/tasks/` | deferred | V2 del pipeline | Drafts → activas o archivadas con decisión |
| E3 | **sldb-ui**: **12 macros + 50 granulars** (yml) + `macro-12-ux-stress-hardening`, `ux-stress-test.md`, `vistas-sldb-ui.md` sin estado | `tools/sldb-ui/desk/drawer/tasks/{macro-*.yml,granular/}` | deferred | Suite UX/e2e v1-v10 | Escenarios consumidos por e2e o marcados no-vigentes |
| E4 | **marcado-ui**: `report-ui-purpose-gap.md` (hallazgos sin acción) | `tools/marcado-ui/desk/drawer/` | deferred | Decisión de rumbo del UI | Hallazgos convertidos en tareas o reporte cerrado |
| E5 | **iso-lab worktrees**: kgdb **26 tareas** (provenance FR-2/4/5/6/7/9, boundary, ingest, trace-query, preserve-provenance), sldb 8 (mismas que E1), deskops 1 (`task-write-end-to-end-deskops-operator-manual`) | `tools/iso-lab/worktrees/{kgdb,sldb,deskops}/desk/tasks/` | abierto | Provenance KGDB + doc operador | Por columna/estado del Board de cada worktree al cerrarse |
| E6 | **deskops drawer**: **11 features** diferidas (herdr-runtime con "decisión 3 abierta", adhoc-subagent-launcher "ready to promote", semantic-execution-adapter, workflow-execution-engine, router/supervisor/executor, sldb-ui-surface-inspection, doc-materialization, pi-artifact-materialization, master-plan), **2 tasks** diferidas (launcher, role-prompts-sldb), **3 questions** abiertas (herdr-runtime, canonical-runtime-artifact-policy, sldb-kgdb-boundaries), ~**40 issues** (destacan session-20260910-handoff nada commiteado, monolithic-api-anti-pattern, init-spawns-one-process-per-model) | `tools/deskops/desk/drawer/{features,tasks,questions,issues}/` | deferred | Hoja de ruta deskops | Cada feature/issue con estado cerrado o decisión escrita |

## Los 7 que desbloquean más cosas (ordenados por desbloqueo)

1. **C1 — limpiar registry de deskops** (borrar ~19 repo-docs de stress-test, dejar 1 por root): desbloquea el inbox de deskops y la coordinación inter-proyecto completa. Cierre: `deskops inbox list` OK en `tools/deskops`.
2. **A6 — `.gitignore` raíz**: desbloquea la visibilidad de B1/B3 y hace review-able todo lo demás; sin esto, cada pase siguiente re-inventa este inventario.
3. **A4+B1 — decisión hum-core/ y commit de la migración** (en tandas): desbloquea el estado del repo para agentes y futuros commits; quita el riesgo de pérdida del árbol actual.
4. **A5+B2 — política de submodulos + push de `tools/sldb`** (21 commits): desbloquea la entrega de sldb y normaliza 6 punteros.
5. **D1+D2 — decidir fuente del layout** (runtime.yaml leído por initializer, o borrado; init_opsys.py como wrapper): desbloquea D4/D5 y mata la deriva de layouts.
6. **A2 — resolver UNCLEAR §3.5** (registry fantasma ontology/test-repo/truth-machine + rename opsys) y **§3.6/§3.8**: deja cerrado el pase 2026-06-02, habilitando borrar `.governance/` (A1).
7. **A3 — renumerar task id 012**: rápido, barato, evita colisiones `depends_on` futuras y deja el Board sin ambigüedad.

## Notas de verificación

- Comandos ejecutados hoy: `deskops inbox list` en `tools/deskops` (falla: C1) y en `/home/jp/setup` (OK: C2, con entrega incidental de una nota pendiente del inbox), grep `runtime.yaml` (0 refs: D1), grep `session_sha256`/`RunDoc` (solo modelo+lectura: D4/D5), conteos de drawers (E1–E6).