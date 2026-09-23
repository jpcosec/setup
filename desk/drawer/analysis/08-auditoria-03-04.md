# Auditoría de 03-integracion-deskops-herdr.md y 04-estado-concreto.md

Método: solo lectura (grep/git/pytest/ps). Cita archivo:línea desviada ⇒ FALSA. Fecha: 2026-09-22.

## Doc 03 — integración deskops ↔ herdr

| Doc | Afirmación | Veredicto | Evidencia |
|---|---|---|---|
| 03 | `initializer.py:41-50` check label sobre `workspace list` | FALSA | check real en `initializer.py:30-33`; la 41 es `panes.extend(build_role_agent_panes)` |
| 03 | `initializer.py:33-42` layout hardcodeado | FALSA | panes en `initializer.py:35-38`; 33 es `return DeskRuntimeInfo(...)` |
| 03 | `build_role_agent_panes` en `initializer.py:50-79` | FALSA | función real `48-76`; 79 es `def ensure_herdr_server` |
| 03 | `init_opsys.py:52-59` misma comprobación literal | FALSA | bloque real `init_opsys.py:47-54` (comparación en 50); 52-53 ya imprimen "already exists" |
| 03 | `init_opsys.py:30-38` mismos 3 `LayoutPaneSpec` | FALSA | panes en `init_opsys.py:36-40`; 30-32 es el gate de identity |
| 03 | `init_opsys.py:44-47` hardcode `AgentSpec("executor"/"tester", kind="pi")` | FALSA | real `init_opsys.py:43-44`; 47 es `client = HerdrClient()` |
| 03 | `runtime.py:48-50` llama `client.call` directo (status/attach/stop) | FALSA | sustancia cierta, líneas desviadas: list=34, focus=47, close=51; status no usa call propio |
| 03 | B≡C: mismos gate `unknown-project`, `list_tasks()`, imports, 3 panes `("nvim",".")`/`("yazi",".")`/`("pytest",)` | CONFIRMADA | literal en ambos archivos (initializer.py:25,27,35-38; init_opsys.py:30,33,36-40) |
| 03 | ids `executor`/`tester` divergen de RoleDocs `deskops-executor`/`deskops-tester` (kind: pi) + `runtime-pi.md` | CONFIRMADA | roles en desk/roles/ con `kind: pi`; runtime-pi.md existe |
| 03 | `grep runtime.yaml` en deskops (\*.py) = cero | CONFIRMADA | 0 hits con y sin filtro `.py` en todo deskops/ |
| 03 | "En setup, solo README.md y el gap-doc citan runtime.yaml" | FALSA | lo citan 8+ rutas: README.md, desk/drawer/README.md, governance-herdr-proposal.md, herdr-runtime-contract-gaps.md, analysis/{01,03,05,06}-*.md, .sldb/runtime/cache/extracted.json, external-resources/yazi.md |
| 03 | `deskops launch` no existe; parser solo llega a `runtime` | CONFIRMADA | help: subcomandos `{...runtime}`; grep launch en cli/ = 0 |
| 03 | coordination.sh: spawn, spawn-fork, free_agent_name, workers_pane, dispatch, say, read, wait, workers-tab/focus/close, close, workers-reap, WORKERS_DB, need_herdr | CONFIRMADA | funciones en líneas 241 (workers_pane), 265 (free_agent_name), WORKERS_DB=151, need_herdr=42 |
| 03 | `need_herdr` solo comprueba PATH | CONFIRMADA | línea 42: `command -v herdr` |
| 03 | `ensure_herdr_server` arranca y hace poll 30×200ms | CONFIRMADA | initializer.py:79-91 (bucle 30, `time.sleep(0.2)`) |
| 03 | herdr binario ELF static-pie 24MB | CONFIRMADA | `file`: ELF static-pie; 24.644.488 B |
| 03 | supervise único con `state_change_seq` (anti busy-spin) | CONFIRMADA | supervise.py:10-11,37,60 |
| 03 | WORKERS_DB TSV por `$HERDR_PANE_ID` + transcript `.herdr-coordination.md` | CONFIRMADA | coordination.sh:151,155; `.herdr-coordination.md` untracked en setup |
| 03 | WorkspaceHandle no deriva IDs de deskops | CONFIRMADA | docstring + `runtime_document()` "without making IDs semantic" (herdr.py:83-95) |
| 03 | `deskops runtime {init,status,attach,stop,supervise}` implementado | CONFIRMADA | `python -m deskops runtime --help`; init=19-30, supervise usa provider |
| 03 | "≈90% del cuerpo de init_opsys.py copia initializer.py" | NO VERIFICABLE | cuantificación subjetiva; la duplicación estructural sí es real |

## Doc 04 — estado concreto

| Doc | Afirmación | Veredicto | Evidencia |
|---|---|---|---|
| 04 | Raíz: rama feature/weltgraph-spec-core, HEAD a1541f8 09-21 "kbsurfaces: descubrir..." | CONFIRMADA | git log/branch |
| 04 | Raíz status: 788 líneas, 326 ??, 271 M, 190 D, 1 m, 0 staged | FALSA (parcial) | hoy: 326 ?? / 190 D / 0 staged ✓; total porcelain 788 ✓; pero **272 M** (no 271) y **0 m** (no 1) |
| 04 | `.sldb` viejo: 27 D + M semantic_index.yaml | CONFIRMADA | 27 D; ` M .sldb/semantic_index.yaml` |
| 04 | Nuevo `.sldb` sin trackear: 73 entradas con `--untracked-files=all` | FALSA | hoy **45** entradas (no 73); colapsado: solo `core/` y `runtime/` |
| 04 | wikipu: 31 líneas; hum/ con 62 ficheros trazados | CONFIRMADA | grep -i wikipu=31; `git ls-files hum`=62 |
| 04 | tools/opsys borrado (1 D, dir no existe) + `?? desk/registry/repo-opsys.md` | CONFIRMADA | dir ausente; repo-opsys.md presente |
| 04 | Raíz traza tools/deskops en 39 líneas (7 D + 1 M + 31 ??) | FALSA | hoy **40** líneas |
| 04 | `.gitmodules` no existe → 0 submódulos | CONFIRMADA | archivo ausente |
| 04 | sldb +21 vs origin/main | CONFIRMADA | `rev-list --left-right` = 0 21 |
| 04 | hum-core +1; "1 fichero modificado (.skills/sldb/SKILL.md)" | FALSA (parcial) | +1 ✓; hoy >90 ficheros sucios (no 1) |
| 04 | deskops 0/0 sync; "1 mod local (.gitignore)" | FALSA (parcial) | 0/0 ✓; hoy ~100 ficheros sucios (deriva del mismo día) |
| 04 | 0/0 en: kgdb, spec2viz, hum-scrapper, repopackage, knowledge, marcado-ui | CONFIRMADA | rev-list = 0 0 en los 6 |
| 04 | "Sin remote: graph_ui, ontology, deskops-pron" | FALSA (parcial) | graph_ui y ontology ✓ sin remote; **deskops-pron SÍ tiene origin** |
| 04 | Setup: main, HEAD 09-07, status 17 líneas (4 M + 13 ??) | FALSA (parcial) | rama/HEAD ✓; hoy **4 M + 14 ?? = 18** (13ª lista omitía `desk/inbox/`) |
| 04 | Tests sldb 19 / kgdb 12 / spec2viz 22 / graph_ui 23 / ontomap 3 / repopackage 12 / ontology 2 / marcado 10 | CONFIRMADA | conteos de tests/*.py (sldb=top-level) |
| 04 | hum-scrapper "sí (5)" | FALSA | hoy 22 ficheros `test_*.py` |
| 04 | deskops-pron: repo propio, rama deskops-pron, 09-20, 42 entradas en tests/ | CONFIRMADA | rama deskops-pron, 9c818cd 09-20, 42 \*.py |
| 04 | deskops: 273 casos, 268 ok / 5 FAIL, ~95s; "252 no se reproduce" | CONFIRMADA | `pytest -q`: 5 failed, 268 passed, 96.07s; collect = 273 |
| 04 | runs/subagents/index.jsonl: 22 líneas; run_id null 22/22; session_sha256 null 22/22; commit poblado | CONFIRMADA | wc=22; grep run_id null=0 no-null; tail muestra commit e293475c |
| 04 | herdr vivo: pids 6086/6087 | CONFIRMADA | ps |
| 04 | `deskops drift check` → "No role-agent drift found.", exit 0 | CONFIRMADA | ejecutado |
| 04 | Tarea actual con `HERDR_TRANSCRIPT=/tmp/h-d5.md` | NO VERIFICABLE | /tmp/h-d5.md existe (12:33), pero /proc/6086/environ no contiene HERDR_TRANSCRIPT |
| 04 | tractatusIR lisp=6/atomos=9; core/knowledge=9, turn_extractor=9, knowledge_tests=4 | CONFIRMADA | conteos |
| 04 | kbsurfaces "cli.py (6 ficheros)" | FALSA | 7 ficheros top-level hoy (cli, config, discovery, \_\_init\_\_, \_\_main\_\_, service, README) |
| 04 | 13 repos con .git propio + `tools/marcado_ui/` duplicado | CONFIRMADA | los 13 confirmados (incluye marcado_ui y deskops-pron) |
| 04 | sldb-ui Astro ^7.1.3; knowledge "Congelado 09-07"; kgdb "Absorbed/hollow" | CONFIRMADA | package.json; READMEs |

## Errores que hay que corregir

Doc 03 (7 citas desviadas = 7 FALSAS):
- `initializer.py:41-50` → `initializer.py:30-33`
- `initializer.py:33-42` → `initializer.py:35-38`
- `initializer.py:50-79` → `initializer.py:48-76`
- `init_opsys.py:52-59` → `init_opsys.py:47-54`
- `init_opsys.py:30-38` → `init_opsys.py:36-40`
- `init_opsys.py:44-47` → `init_opsys.py:43-44`
- `runtime.py:48-50` → `client.call` en 34 (list), 47 (focus), 51 (close)
- Falsa de contenido: "en setup solo README y gap-doc citan runtime.yaml" → reescribir: "ningún `.py` de deskops lo lee; en setup lo citan 8+ rutas (ninguna ejecuta)"

Doc 04 (snapshot; deriva del mismo día):
- "271 M / 1 m" → "272 M / 0 m" (total porcelain 788 se mantiene)
- "73 entradas .sldb untracked" → "45"
- "13 ??" setup → "14 ??" (añadir `desk/inbox/`)
- "hum-scrapper (5)" → "(22 test_*.py)"
- "Sin remote: deskops-pron" → "con remote origin"
- "deskops 1 mod / hum-core 1 mod" → re-medir al regenerar (hoy ~100 / >90); indicar "medido el mismo día, cambia por trabajo en curso"
- "tools/deskops 39 líneas" → "40"
- "kbsurfaces (6 ficheros)" → "(7)"

## Confianza

- **Doc 03: 50%** — núcleo analítico (duplicación B≡C, runtime.yaml sin lectores .py, comandos de A, supervise, binario herdr) confirmado al 100%, pero **todas** las citas archivo:línea están desviadas (7/7 FALSAS) y hay 1 afirmación de alcance falsa; un lector que confíe en las líneas no puede replicar.
- **Doc 04: 85%** — la mayoría de fechas/commits/ramas/conteos confirmados; errores concentrados en conteos de snapshot (hum-scrapper 5, setup 13??, .sldb 73) y 2 afirmaciones de "1 fichero modificado" que no se reproducen hoy por trabajo en curso el mismo día.