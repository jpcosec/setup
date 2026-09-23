# Hermes Agent como sustrato: evaluación, choque con deskops y qué robar

Fecha: 2026-09-23. Fuente: documentación oficial (`hermes-agent.nousresearch.com/docs`),
repo `github.com/NousResearch/hermes-agent` y comparativas de terceros.

**Estado de la evidencia: NO probado localmente.** No hay binario `hermes` en esta máquina;
herdr 0.9.0 lo lista como `kind` soportado pero la integración no está instalada. Todo lo
de abajo es lectura de documentación y código público, no evidencia de runtime. Cualquier
conclusión de estabilidad queda pendiente de un piloto.

## 1. Qué es

- Agente de terminal open source (MIT, self-host gratis; hosting pago "FlyHermes") de Nous
  Research. Se describe a sí mismo como "execution agent inside a managed Agentic OS".
- Python. La doc declara ~25.000 tests en ~1.250 archivos y un repo con decenas de miles de
  issues — escala y churn muy por encima de lo que mantenemos nosotros.
- Motor único `AIAgent` (`run_agent.py` + `agent/conversation_loop.py`): resolución de
  provider, prompt builder, dispatch de tools, retries/fallback, compresión de contexto,
  persistencia.
- 70+ tools / 28 toolsets. Terminal con 7 backends (local, Docker, SSH, Daytona, Modal,
  Singularity, Vercel). Sesiones en SQLite + FTS5 con lineage e aislamiento por plataforma.
- Superficies: CLI/TUI, gateway con 25+ plataformas de mensajería, cron, ACP para editores,
  librería Python, API server, batch runner, dashboard web, app Electron.
- Skills: archivos `SKILL.md` con name/description/procedimiento, carga on-demand. **Misma
  convención que nuestro `.pi/skills`** — el corpus porta casi 1:1.
- Requiere modelos de ≥64K de contexto. Soporta providers que ya pagamos (Copilot OAuth,
  Codex subscription, Anthropic, Kimi, OpenRouter) y endpoints locales (Ollama, LM Studio,
  vLLM, SGLang).

## 2. El choque de axiomas: Kanban vs deskops

Hermes trae un board de tareas (`hermes kanban`). No es un detalle: **compite directamente
con deskops**, y la comparación es incómoda.

- El workflow vive en `~/.hermes/kanban.db` (SQLite local). No es diffable, no viaja en el
  repo, no se revisa en un PR. La doc dice explícitamente: *"kanban is single-host by design"*
  con modelo de amenaza "trusted local user".
- Eso invierte nuestra tesis: acá el workflow se gobierna por artefactos del repo (`desk/`
  en git, documentos tracked por sldb, hashes, diffs revisables).
- Nuestro problema real es **cross-repo** (setup ↔ sldb ↔ deskops ↔ spec2viz). Kanban
  **prohíbe** linkear tareas entre boards y aísla por `HERMES_KANBAN_BOARD`.

**Conclusión: Kanban no se adopta.** Es el único punto de su diseño que contradice lo
nuestro de raíz.

## 3. Dónde Hermes gana hoy (y hay que reconocerlo)

- **Gates mecánicos, no prosa.** Dispatcher con reclaim de workers muertos (match por PID
  *y* fingerprint de spawn, para no señalar un PID reciclado), circuit breaker tras N fallos
  de spawn (default 2), `BLOCK_RECURRENCE_LIMIT` (default 2) que rompe loops
  block→unblock→block y rutea a triage. **El contador de recurrencia sobrevive al unblock y
  el texto de la tarea no puede optar por salirse.**
- **Closeout verificable.** `--completion-contract OWNER/REPO` no deja completar una card
  hasta leer branch protection + required checks del PR real (`gh` autenticado, solo
  lectura). Frase textual de la doc: *"A commit or diff alone never automatically completes
  a task."*
- **Anti-deriva por construcción**: idempotency keys, heartbeats, stall monitor por progreso
  (no wall-clock), transcripciones append-only por subagente.
- **Workspaces tipados**: `scratch` (efímero, se borra al completar), `worktree`, `dir:<abs>`.
  Los paths relativos se **rechazan** explícitamente por vector de confused deputy.
- **Artefactos declarados, no implícitos**: si falta un artefacto declarado, la tarea sigue
  in-flight para que el worker corrija el path — no falla ni cierra.
- **Clasificación de fallo de infraestructura**: `metadata.infrastructure: true` **no**
  incrementa el contador de fallos ni bloquea la card; solo espacia reintentos.
- **Superficie headless**: `hermes chat -q "..." --format stream-json` emite JSONL por línea
  (`system/init`, `text`, tool events con `duration_ms`/`is_error`, y un `result` final con
  `session_id`, `exit_code`, `tokens`, `duration_ms`). `--usage-file` escribe reporte de costo
  y tokens. Exit codes discriminantes (one-shot: `0` completado, `1` fallo/partial/presupuesto,
  `130` interrumpido).
- **Subagentes**: `delegate_task` con contexto fresco, hasta 10 paralelos por defecto,
  `max_iterations` configurable, `delegation.model` barato mientras el padre queda en frontier.
  Un hijo **nunca** hereda más toolsets que el padre, y hay blocklist fija (`delegate`,
  `clarify`, `memory`, `send_message`, `cronjob`).
- **Bloque gestionado en materialización** (`hermes codex-runtime migrate`): proyecta config
  a un archivo co-editado por humanos dejando el texto externo verbatim, preservando y
  reportando entradas del usuario que colisionan, validando antes de una escritura atómica,
  y con exit 1 si hay errores.

Traducción incómoda: buena parte de `feature-herdr-supervised-execution-runtime` (`RunDoc`,
`session_sha256`, `outcome`, `run_dir`) es **reconstruir algo que Hermes ya trae**.

## 4. Dónde deskops ya gana

- **Stores federados y versionados.** Hermes tiene un SQLite mono-host; nosotros tenemos
  stores por repo que viajan en git. Es una ventaja real y la estamos desaprovechando.
- **Gobernanza por artefactos revisables** (PR, diff, hash).
- **sldb**: contratos de modelo, Markdown reversible, extract/render, hashes, búsqueda
  semántica. Hermes no tiene equivalente — su "memoria" es SQLite + skills.

## 5. Qué robar, por ratio valor/costo

### Tier 1 — barato, encaja en primitives

1. **Taxonomía de salida, no booleano.** `completed / failed / partial / budget / interrupted`.
   Nuestro `TransitionResult` solo tiene `progressed`/`blocked`.
2. **Anti-thrash determinista.** Contador de recurrencia que sobrevive al unblock y solo se
   resetea al completar. Es un campo más una condición.
3. **Un commit o un diff nunca completan una tarea.** El anti-mock como regla de máquina.
4. **Idempotency keys.** Hoy tenemos tres `unclear-list` idénticas en el inbox de setup por
   correr el mismo comando tres veces.
5. **Fail-closed por defecto.** `dispatch_profiles` vacío/ilegible → no reclama nada. Nuestro
   `identity.py` hace lo opuesto: sin `--store` adivina el registry desde el CWD.

### Tier 2 — patrones de diseño, cambian arquitectura

6. **Bloque gestionado en materialización.** El más subestimado. Hoy `deskops materialize`
   renderiza *encima*; con bloque gestionado el drift se vuelve calculable.
7. **Dos superficies, una capa.** El modelo opera por tools, el humano por CLI, sobre la misma
   capa. Hoy el agente shellea `deskops ...`: no auditado, sin transacción.
8. **Herencia estricta de privilegios en subagentes.**
9. **Taxonomía de workspace + rechazo de paths relativos.**
10. **Degradación elegante de output estructurado**: si el schema no valida, conservan el texto
    crudo y marcan `schema_valid: false`; nunca re-ejecutan una tarea larga por un fallo de parseo.

### Tier 3 — estilo

- Documentar los deadlocks propios (su sección "no linkees la support card al padre que
  bloquea" es exactamente el tipo de trampa que tenemos y no escribimos).
- Recovery toolkit con orden canónico.

### NO robar

Kanban como fuente de verdad. Gateway / voz / Electron / cron / proxy / secrets (superficie
ajena, churn ajeno). Estado global en `~/.hermes` (nosotros somos por repo).

## 6. Corrección de una medición propia

En una pasada anterior conté "571 `.md` en `desk/`, 134 trackeados = 23%" y lo leí como deuda
de adopción masiva. **Estaba mal.** `deskops doctor` ya distingue categorías:

- Superficies modeladas con tracking roto → esto sí es deuda.
- `desk/drawer/**`, `desk/inbox/**`, `desk/features/**`, `desk/logbook/**`, `desk/runtimes/**`,
  `desk/README.md` → **"ignored by design"**, prosa que no debe trackearse.

La deuda real es el subconjunto que `doctor` clasifica como roto, y el estado actual incluye
~95 atoms en `data_mutation` (contenido del `.md` que ya no corresponde al hash registrado),
lo que es consistente con una migración de store a medio aplicar.

## 7. Problema estructural detectado en deskops

- `deskops/operations.py` tiene **2.765 líneas** y concentra loaders, transiciones, closeout,
  auto-commit y parseo de args. Es la causa raíz de que cada cambio se sienta caro.
- El lookup de relaciones se hace **por substring en el nombre de archivo**
  (`operations.py:2433 if task.id not in path.stem`, `1533 prim_dir.glob(f"*-{task_id}*.md")`,
  `555 selector.lower() in path.stem.lower()`, `_resolve_glob` ×8), teniendo `__references__`
  en los modelos y un índice de documentos en el store.
- deskops importa `sldb.store.io` (`load_documents_index`, `load_models_index`,
  `load_store_index`) y `sldb.runtime.validation` (`extract_model_data`,
  `render_model_markdown`): lo de bajo nivel. **Cero uso** de búsqueda semántica, de `find`,
  o de `sldb.api`.

O sea: **no falta arquitectura, falta usar la que ya está registrada e indexada.**

## 8. Capacidad ausente real: condiciones sobre hechos ejecutables

`deskops/runtime/primitives.py` es una máquina de estados determinista de verdad
(`Condition.evaluate` con 6 predicados, `Operator.apply`, `Routine.advance`,
`validate_integrity`). El problema no es el grafo: es **qué evalúa**.

- Todas las condiciones leen el `payload` extraído del Markdown de la tarea, es decir,
  campos auto-reportados por el agente.
- `TaskDoc.validation` es `list[str]`: texto de comandos, sin ejecución.
- El único `subprocess` del ciclo es `git add/commit` en closeout: registra, no verifica.

Resultado: `advance` es determinista *respecto al documento*, y el documento es un reporte
propio. Lo que falta es un tipo de evidencia ejecutable (`ProofDoc`: comando, `exit_code`,
`duration_ms`, hash de salida, `head_sha`) para que las condiciones lean hechos y no
declaraciones. Nota: `operations.py:1029` **ya** inyecta valores calculados al payload antes
de `routine.advance()`, así que el hook de extensión existe.

Vecinos ya presentes: `RunDoc` (`deskops/models/run.py`, definido y registrado, sin escritor)
y el par `TestDoc`/`StressTestDoc` diseñado en `desk/drawer/analysis/10-`. Conviene definir la
jerarquía de evidencia una vez, no crear tres modelos sueltos.

## 9. Recomendación

1. **No adoptar Kanban.** Sí considerar Hermes como *runtime de worker* headless, consumido
   por deskops vía `--format stream-json` + `--usage-file`. Reversible: borrar `~/.hermes` no
   pierde ningún artefacto.
2. **Primero la línea base de deskops**: suite verde, `stores check` PASS, `doctor` sin
   `data_mutation`. Hoy hay 5 tests rojos y 62 archivos sin commitear (último toque
   2026-09-17).
3. **Después el refactor** de `operations.py` (loaders / transiciones / closeout / CLI) sin
   cambio de comportamiento.
4. **Después** el lookup por índice en lugar de glob/substring.
5. **Recién entonces `ProofDoc`**, que nace consultable.

## 10. Decisiones abiertas

- ¿Se hace piloto de Hermes como worker headless, o se posterga hasta cerrar la línea base?
- ¿El refactor de `operations.py` entra antes o después de `ProofDoc`?
- Jerarquía de modelos de evidencia: `base_models` + herencia Python (¿`family`?) — hay una
  consulta enviada al inbox de sldb.
- El bug de intake cross-repo en `deskops/identity.py` (registro resuelto desde el store del
  CWD, no desde `--root`; `sldb`/`deskops`/`spec2viz`/`kgdb` no están en el registry del
  ecosistema) sigue sin nota propia del lado de deskops.
