---
id: analysis-02-deskops-limitaciones
title: "Deskops: limitaciones estructurales y decisiones de diseño"
created: 2026-09-22
tags:
- topic:deskops
- topic:workflow-engine
- topic:analysis
---

# Deskops: limitaciones estructurales (verificadas, con evidencia)

Pregunta: ¿en qué cosas concretas deskops se queda corto? Fuentes: `tools/deskops/desk/drawer/features/`, código en `deskops/runtime/` y `deskops/cli/commands/`. Verificado por ejecución real en ambas cabeceras (deskops y setup).

## Limitaciones duras

| # | Qué falla | Evidencia archivo:línea | Impacto operativo | Tipo | Costo arreglo |
|---|---|---|---|---|---|
| 1 | deskops NO puede lanzar un agente. No existe `deskops launch` en el parser; el lanzamiento vive fuera, a mano, en el harness del asistente padre. | `deskops/cli/parser.py` (todo el árbol `add_parser`, líneas 61-481, sin `launch`); `desk/drawer/features/feature-adhoc-subagent-launcher-tmux-multi-cli.md` (sección Problem: "it cannot **launch** an agent. Today launching is done by hand from an outside harness"). | El bundle de contexto que deskops sabe ensamblar (brief/board/task/next/graph) nunca se inyecta al agente; el operador lo re-pasa a mano. Sin lanzamiento nativo no hay autoservicio de tareas: el harness externo copia el rol de controlador. | Falta de feature (diseñada: master-plan FASE 5, T7; retargeting a Herdr pendiente). | Alto |
| 2 | Todas las filas de `runs/subagents/index.jsonl` llevan `run_id: null` y `session_sha256: null` (22/22 filas verificadas). Nada pasa `--session`/`--run-id`; el closeout no valida esos campos. | `runs/subagents/index.jsonl` (22 líneas, todas nulas); `deskops/cli/commands/closeout.py:94-97` (trailers solo si valor presente) y `:116-121` (write index sin gate); `deskops/operations.py:1544-1572` (`verify_task_closeout`: gates = tests/link/commit; sin gate de run/session). | La cadena de trazabilidad sldb/grafo→sesión del agente es ficticia: `index.jsonl` promete integridad pero no la puede probar. Un commit de closeout no es verificable contra el transcript del agente. | Falta de feature (decisión 4/herdr feature: wiring de `--session` pendiente de implementar). | Medio |
| 3 | `RunDoc` está definido y registrado en el store, pero NADIE lo escribe. `run.yaml` queda fuera de `.sldb` y fuera del grafo. | `deskops/models/run.py:10-14` (docstring: "nothing writes it yet"); `deskops/cli/commands/closeout.py:59-82` (solo `run.yaml`); `deskops/graph/extract_docs.py:65` (globo `desk/runs` que no existe: verificado, no hay dir `desk/runs/`); `.sldb/core/models/RunDoc.yaml` presente. | El registro durable de ejecuciones no es consultable ni por el store ni por KGDB: 35 run-dirs en `runs/subagents/` son carpetas huérfanas para el sistema, solo legibles por grep. Toda operación de grafo/next no ve la historia de ejecución. | Decisión consciente de phasing aditivo (decisión 4), pero deja una deuda estructural: dos registros divergentes (`run.yaml` + `index.jsonl`) sin dueño común. | Medio |
| 4 | Intake bloqueado por AMBOS extremos a la vez:
  (a) `desk/registry/` de deskops tiene 20 repo-docs, 9 apuntan a la misma raíz (described-repo, repo-deskops-alt, deskops-dir, deskops, my-repo, myrepo, pythonpath-repo, store-test, tagged-repo) → `SLDBStoreError: Duplicate repository root` en cualquier operación que cargue el registro (inbox deliver/list/ack).
  (b) El store de hum-ecosystem no tiene a `setup` en su registro → `Repository id 'setup' not found`. |
  | (a) `deskops/identity.py:63-64,180` (`_raise_on_duplicate_roots`; verificado por ejecución: 9 entradas colisionan en `.../tools/deskops`); (b) `deskops/identity.py:184-187` (`_missing_repository_message`; verificado: `resolve_registered_desk('setup', None)` desde hum-ecosystem falla). Además `deskops/cli/commands/inbox.py:60-65,246-262` (toda ruta pasa por `load_repository_registry`). | `deskops inbox` (la única superficie declarada de coordinación cross-repo) es inusable desde el repo deskops y hacia setup. La coordinación inter-proyecto se degrada a notas manuales en drawer. El propio repo lo documenta: "coordination intake is unavailable" (`desk/drawer/questions/question-herdr-runtime-open-decisions.md`, sección Blocked Surface). | (a) Basura de datos de stress-test que rompe una función productiva = bug de higiene de datos, no de lógica. (b) Registro distribuido por store sin sincronización = falta de feature (registro canónico único). | (a) Bajo (limpiar 8 docs); (b) Alto (registro canónico cross-store) |
| 5 | `deskops runtime supervise` es print+notify: en `blocked` notifica y muestra excerpt; en `done` imprime y avisa; nunca avanza `deskops advance`, nunca captura evidencia en el run dir, nunca cierra el run. | `deskops/cli/commands/runtime.py:30-47` (`on_blocked`/`on_done`: solo `print` + `notify`; mensaje literal "did not advance any task"); `deskops/runtime/supervise.py:1-8,66-76` (docstring "Never answers... never advances"; loop = wait + callback). | Supervisar no ahorra operación: un agente bloqueado queda esperando al humano igual que sin supervisor; un run `done` requiere intervención manual completa (digest, closeout). El supervisor es un timbre, no un portero. | Decisión de diseño CORRECTA y explícita (anti-patrón de auto-approve; ver `desk/roles/deskops-supervisor.md`). La carencia real es que ni siquiera la etapa segura (captura automática de evidencia en `done`) está implementada. | Medio |
| 6 | La supervisión es forense, no observa en vivo: el supervisor solo lee archivos escritos por el agente DESPUÉS de que el lane termina; no ve prompts bloqueados en vivo. Herdr (el control remoto) no deja traza: log sin eventos `agent.*`, scrollback 10MB en memoria, pantalla alterna de TUI fuera del scrollback. | `desk/drawer/features/feature-herdr-supervised-execution-runtime.md` (sección Problem: "supervises **forensically**... never observes anything live... Herdr is a remote control, not a recorder"); `deskops/runtime/herdr.py:112-118` (`wait`), `:125-129` (`read`, usa call_text). | Toda decisión de supervisión depende de evidencia post-hoc escrita a mano por el executor; no existe detección de agente atascado en tiempo real salvo `wait --until blocked` (que sí trae Herdr). | (deskops) Falta de feature: el lado observador en vivo existe en Herdr pero no se usa para capturar/registrar, solo para esperar. (Herdr) Topología: es control remoto sin memoria. | Bajo a medio (wrap de wait/read en el bucle ya existe; falta persistenciar el estado) |

## Decisiones de diseño que PARECEN limitación (y no lo son)

| # | Aspecto | Por qué es correcto | Evidencia |
|---|---|---|---|
| A | `supervise` no responde prompts de aprobación bloqueados | Auto-aprobar es el mecanismo exacto por el que un agente sin vigilancia hace algo destructivo. El supervisor debe escalar al humano, nunca contestar. | `deskops/runtime/supervise.py:1-8`; `desk/drawer/features/feature-herdr-supervised-execution-runtime.md` (desired outcome: "it never answers an approval dialog itself") |
| B | `supervise` no avanza estado en `done` | "The desk does not change state unobserved": avanzar sin revisión humana rompe la invariante central del modelo de workflow. El `[H]` o el agente deciden; el motor solo reporta. | `deskops/cli/commands/runtime.py:43-44`; `feature-herdr...md` (loop step 3: "Does not run `deskops advance`") |
| C | `RunDoc` vacío por phasing aditivo | Registro aditivo evita migración destructiva del store; el coste es que la huella duradera aún no existe. La decisión 4 del question doc lo autoriza explícitamente. | `desk/drawer/questions/question-herdr-runtime-open-decisions.md` (decisión 4) |
| D | El supervisor nunca posee el control del workspace, Herdr sí | División deliberada: Herdr = control en vivo/efímero; deskops = traza durable/fuente de verdad. Duplicar el control en deskops crearía dos autoridades del runtime. | `deskops/runtime/herdr.py:1-8` (docstring de frontera semántica) |

## Notas de verificación

- El bug del sentinel de timeout en `herdr.py` (toque-de-muerte para `wait` de larga duración, citado como blocker en el feature doc) YA está arreglado: `_UNSET` en `deskops/runtime/herdr.py:44-58` distingue "omitido" de "sin límite". No se lista arriba como limitación vigente.
- `send`/`status`/`attach`/`stop` de `HerdrProvider` son código muerto: `runtime.py:36-55` habla con el cliente directamente. No es limitación funcional, es deuda de mantenimiento.
- Costes de arreglo: solo la limpieza del registro (4a) es de costo bajo e impacto inmediato; el resto son trabajo de feature real (launcher, wiring de sesión, RunDoc escritor, supervisor activo), no parches.

---

**Resumen (8 líneas):**

1. Deskops no puede lanzar agentes: no existe `deskops launch` (`parser.py`); todo lanzamiento es manual desde el harness externo, y el bundle de contexto que deskops ensambla nunca llega al agente.
2. `runs/subagents/index.jsonl` tiene 22/22 filas con `run_id`/`session_sha256` null; closeout no valida nada de eso (`closeout.py:94-121`; gates reales en `operations.py:1544`).
3. `RunDoc` está registrado en el store pero nadie lo escribe (`run.py:10-14`); `run.yaml` y los 35 run-dirs quedan fuera de sldb y del grafo KGDB.
4. Intake bloqueado en ambos extremos: registro de deskops con 9 entradas duplicadas → `Duplicate repository root` (`identity.py:180`); store de hum-ecosystem sin `setup` → `Repository id 'setup' not found` (`identity.py:184`).
5. El supervisor es print+notify: no contesta, no avanza, no captura evidencia (`runtime.py:30-47`); es un timbre, no un portero.
6. La supervisión es forense (lee archivos post-hoc) y Herdr, el control en vivo, no registra nada: no hay observación en tiempo real ni traza.
7. No-sorprendas: NO contestar prompts bloqueados ni avanzar estado a ciegas son decisiones correctas y explícitas (anti-patrones documentados), no bugs.
8. Prioridad de arreglo: limpiar `desk/registry/` (costo bajo, desbloquea inbox); el resto son features reales (launcher, session-wiring, escritor de RunDoc, supervisor activo).

**Ruta:** `/home/jp/setup/desk/drawer/analysis/02-deskops-limitaciones.md`