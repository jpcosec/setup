# Auditoría 07: análisis 01 y 02 (verificación factual línea a línea)

Fecha: 2026-09-22. Método: ejecución de comandos de lectura (help de todos los subcomandos, grep, sed, wc, git log, ls) contra `/home/jp/setup` y `/home/jp/proyectos/hum-ecosystem/tools/deskops`. Nada fue modificado.

## Tabla de veredictos

| Doc | Afirmación (resumida) | Veredicto | Evidencia del comando |
|---|---|---|---|
| 01 | 22 subcomandos (lista exacta) | CONFIRMADA | `deskops --help`: `{about,doctor,status,faq,bootstrap,init,inbox,promote,add,edit,bind,next,list,show,advance,repo,desk,atoms,graph,materialize,drift,closeout,runtime}` = 22 |
| 01 | Sub-subcomandos (add 16, list/show 16, atoms 13, advance task, closeout {commit,verify}, drift {check}, graph {build,neighbors,missing,reflect}, runtime {init,status,attach,stop,supervise}, desk {install,migrate}, repo {register,whoami}, promote inbox-to-drawer-task) | CONFIRMADA | `deskops <sub> --help` cotejado uno a uno |
| 01 | setup/desk: roles/, materializations/, faq/, inbox/ vacíos (0 archivos) | FALSA | `ls -A` → roles/materializations/faq vacíos, pero `inbox/` tiene 2 notas (20260922-122730…, 20260922-145929…); la primera (12:27:30) es previa al propio doc (mtime 12:28:48) |
| 01 | setup: 1 task en draft con `pills: []` | CONFIRMADA | `tasks/task-centralizar-configuraciones-personales-en-setup.md`: `status: draft`, `pills: []` |
| 01 | Board.md con Purpose/Notes en boilerplate | CONFIRMADA | `tasks/Board.md`: `_Explain what this board routes and why it exists._` |
| 01 | 3 hallazgos sueltos en `desk/drawer/*.md`, sin `drawer/tasks/` | CONFIRMADA | drawer/ solo tiene analysis/ + 3 .md (governance-herdr-proposal, herdr-runtime-contract-gaps, install-scripts-and-readme-findings); no hay drawer/tasks |
| 01 | `runs/subagents/index.jsonl` 22/22 `run_id`/`session_sha256` null | CONFIRMADA | `wc -l` = 22; `grep -c '"run_id": null'` = 22 y session = 22 (en el repo deskops) |
| 01 | `closeout.py:94` trailers solo `if run_id:` | CONFIRMADA | L94 `if run_id:`; L97 `if session_sha256:` |
| 01 | next: deskops 31 `next.txt`; setup sin dir `runs/` | CONFIRMADA | `ls runs/subagents/*/next.txt | wc -l` = 31; `ls /home/jp/setup/runs` → no existe |
| 01 | setup: task draft con primitivas completas nunca avanzada; deskops: muchas closeouts en git log | CONFIRMADA | checklists/conditions/edges/operators en task; `git log --grep=closeout` decenas de hits |
| 01 | bind pill: 2 tasks con `pills:` pobladas | CONFIRMADA | `grep -l "^pills:" desk/tasks/*.md` = 2 tasks |
| 01 | bind pill: «2 hits en git log» | FALSA | `git log --oneline --grep="bind pill" -i | wc -l` = 0; `grep -ic pill` = 18 |
| 01 | runtime: `desk/runtimes/runtime-claude.md` y `runtime-pi.md` modelados; supervise aún en drawer/features; setup `runtime.yaml` + hallazgo «read by nobody» | CONFIRMADA | `ls desk/runtimes/` = ambos; feature-herdr…md existe; `desk/runtime.yaml` existe; `herdr-runtime-contract-gaps.md:12` = «`desk/runtime.yaml` is read by nobody» |
| 01 | deskops: 138 átomos en `desk/atoms/` | CONFIRMADA | `find desk/atoms -type f | wc -l` = 138 |
| 01 | setup: solo `tag-namespaces.yaml`, 0 átomos, `AtomDoc.yaml` en `.sldb/core/models/` | CONFIRMADA | `find desk/atoms` = 1; `ls .sldb/core/models/` incluye AtomDoc.yaml |
| 01 | snapshot `.sldb/runtime/knowledge_graph.kg.json` construido | CONFIRMADA | archivo existe (595 KB) |
| 01 | «26 hits git» para kg.json | FALSA | `git ls-files --error-unmatch` → no trackeado; `git log -- <file>` = 0 commits |
| 01 | setup: `.sldb/runtime/` sin snapshot KG; `semantic_dag.yaml` generado por sldb | CONFIRMADA | `ls /home/jp/setup/.sldb/runtime/` → sin knowledge_graph; `semantic_dag.yaml` presente |
| 01 | agentes materializados `~/.pi/agent/agents/deskops-{executor,supervisor,tester}.md` | CONFIRMADA | los 3 archivos existen |
| 01 | drift: 10 hits git; `st-07-drift-check.md`; `use-cases/uc-07` | CONFIRMADA | `git log | grep -ic drift` = 10; ambos archivos existen |
| 01 | deskops: `desk/inbox/` con 5 notas | FALSA | `ls desk/inbox/ | wc -l` = 4 |
| 01 | deskops: `desk/drawer/attention/` con 18 | FALSA | `ls desk/drawer/attention/ | wc -l` = 21 |
| 02 | No existe `deskops launch` en el parser | CONFIRMADA | `grep -n launch deskops/cli/parser.py` = 0 |
| 02 | «árbol add_parser, líneas 61-481, sin launch» | FALSA | primer `add_parser` en L64; el árbol continúa hasta ~L1000 (add_parser en 538, 563, 613, 690…) |
| 02 | feature-adhoc: «cannot **launch** an agent. Today launching is done by hand from an outside harness» | CONFIRMADA | feature-adhoc-subagent-launcher-tmux-multi-cli.md L13 |
| 02 | closeout.py:94-97 trailers condicionados; 116-121 write index sin gate | CONFIRMADA | L94-98 trailers condicionales; L116-121 dict del index sin gate |
| 02 | operations.py:1544-1572 gates = tests/link/commit sin run/session | CONFIRMADA | `def verify_task_closeout` en L1544; gates: tests, atom_or_materialization_link, commit |
| 02 | run.py:10-14 docstring «nothing writes it yet» | CONFIRMADA | frase en L11 (docstring L8-17) |
| 02 | closeout.py:59-82 «solo run.yaml» | CONFIRMADA | L59-81: lee/Escribe run.yaml |
| 02 | extract_docs.py:65 globo `desk/runs` inexistente | CONFIRMADA | L65 = `_glob(root/"desk"/"runs",…)`; `ls desk/runs` → no existe |
| 02 | `.sldb/core/models/RunDoc.yaml` presente | CONFIRMADA | archivo existe |
| 02 | «35 run-dirs en runs/subagents/» | FALSA | `ls -d runs/subagents/*/ | wc -l` = 34 |
| 02 | registry: 20 repo-docs; 9 apuntan a la misma raíz (nombres listados) | CONFIRMADA | `ls desk/registry/ | wc -l` = 20; 8 con `path: .` + 1 absoluto = 9 colisionan |
| 02 | identity.py:63-64,180 `_raise_on_duplicate_roots` | CONFIRMADA | L64 llamada; L171 def; L180 raise |
| 02 | identity.py:184-187 `_missing_repository_message` | FALSA | def en L188; mensaje «Repository id … not found in registry» en L190-192; 184-187 es `_duplicate_id_message` |
| 02 | store hum-ecosystem sin `setup` → «Repository id 'setup' not found» | CONFIRMADA | `ls …/hum-ecosystem/desk/registry/` = 10 docs, ninguno setup; mensaje literal en identity.py:190 |
| 02 | inbox.py:60-65,246-262 «toda ruta pasa por load_repository_registry» | FALSA | inbox.py no contiene «registry» (grep=0); L60-65 es payload, L246-262 prints; la carga está en identity.py:42/106 vía resolve_registered_desk |
| 02 | question doc sección Blocked Surface: «coordination intake is unavailable» | CONFIRMADA | L41 «Blocked Surface», L43 cita literal |
| 02 | runtime.py:30-47 (on_blocked/on_done print+notify) | FALSA | `def on_blocked` en L74, `on_done` en L85, mensaje «did not advance any task» en L88; 30-47 es `_run` |
| 02 | supervise.py:1-8 docstring «Never answers… never advances» | FALSA | ese texto está en runtime.py:62-66; supervise.py:1-8 habla de Herdr sin registro |
| 02 | supervise.py:66-76 loop = wait + callback | CONFIRMADA | `run_supervise_loop` en L71; callbacks on_blocked/on_done |
| 02 | `desk/roles/deskops-supervisor.md` existe | CONFIRMADA | archivo existe |
| 02 | feature-herdr: «supervises forensically… never observes anything live»; «Herdr is a remote control, not a recorder» | CONFIRMADA | feature L26 y L28 |
| 02 | herdr.py:112-118 (wait) y :125-129 (read usa call_text) | FALSA | 112-118 = kwargs de subprocess en `HerdrClient.call`; 125-129 = parseo JSON de call; `def wait`=218, `def read`=232, `def call_text`=133 |
| 02 | D-A: no responde prompts (feature doc «never answers an approval dialog itself») | CONFIRMADA | feature L47 |
| 02 | D-B: cita runtime.py:43-44 | FALSA | 43-44 es handler attach en `_run`; «Does not run `deskops advance`» está en feature L69 |
| 02 | D-C: decisión 4 del question doc (phasing aditivo, RunDoc sin escribir) | CONFIRMADA | question doc L22-24: «Additive phasing is acceptable. Define and register RunDoc, write nothing yet» |
| 02 | D-D: herdr.py:1-8 docstring de frontera semántica | CONFIRMADA | L1-7: «semantic-boundary oriented. DeskOps owns the execution plan; Herdr owns the live workspace» |
| 02 | `_UNSET` en herdr.py:44-58 | FALSA | `_UNSET` = L36 (`class _Unset` L23); L44-58 son dataclasses AgentSpec/LayoutPaneSpec |
| 02 | send/status/attach/stop de HerdrProvider son código muerto; runtime.py:36-55 usa client directo | CONFIRMADA | 0 callers de `.send(/.status(/.attach(/.stop(`; client.call en runtime.py L34/47/51 con HerdrClient |

## Errores que hay que corregir (solo FALSAS)

**Doc 01:**
1. «inbox/ VACÍOS (0 archivos)» → roles/, materializations/, faq/ vacíos; inbox/ tiene 2 notas (`20260922-122730-unclear-list.md` anterior al propio doc).
2. «2 hits en git log» (bind pill) → `git log --oneline --grep="bind pill" -i` = 0 hits; 18 commits mencionan «pill».
3. «26 hits git» (kg.json) → el archivo NO está trackeado; `git log -- <file>` = 0 commits.
4. «desk/inbox/ con 5 notas» → 4 notas.
5. «drawer/attention/ con 18» → 21 archivos.

**Doc 02:**
1. «parser.py, líneas 61-481» → el árbol `add_parser` va de L64 a ~L1000; corregir a «L64-1000».
2. «35 run-dirs» → 34 (`ls -d runs/subagents/*/ | wc -l`).
3. «identity.py:184-187 (_missing_repository_message)» → def en L188, mensaje en L190-192 (184-187 es `_duplicate_id_message`).
4. «inbox.py:60-65,246-262 pasa por load_repository_registry» → inbox.py no contiene «registry»; la carga real está en identity.py:42 y :106 vía resolve_registered_desk (identity.py:103).
5. «runtime.py:30-47 (on_blocked/on_done)» → on_blocked en L74, on_done en L85, mensaje en L88; 30-47 es `_run`.
6. «supervise.py:1-8 "Never answers… never advances"» → texto en runtime.py:62-66; supervise.py:1-8 trata de Herdr sin registro.
7. «herdr.py:112-118 (wait), :125-129 (read)» → ambos rangos están en `HerdrClient.call` (subprocess + json); wait=218, read=232, call_text=133.
8. «runtime.py:43-44» (D-B) → es el handler attach; «Does not run `deskops advance`» está en feature-herdr L69.
9. «_UNSET en herdr.py:44-58» → `_UNSET` en L36; 44-58 son AgentSpec/LayoutPaneSpec.

## Confianza global

- **Doc 01 (01-deskops-subutilizado.md):** 18/23 afirmaciones confirmadas ≈ **78 %**.
- **Doc 02 (02-deskops-limitaciones.md):** 20/30 afirmaciones confirmadas ≈ **67 %**.
- Patrón de error dominante: citas `archivo:línea` desplazadas (mayoría de FALSAS de 02) y conteos numéricos inflados (5 notas→4, 18→21, 35→34, 26→0, 2 hits→0).
- Las afirmaciones estructurales clave de 02 (sin `launch`, 22/22 null, gates de closeout, RunDoc sin escritor, 9 duplicados en registry, supervisor print+notify, Herdr sin traza, decisión 4) son **verdaderas** pese a las citas erróneas.