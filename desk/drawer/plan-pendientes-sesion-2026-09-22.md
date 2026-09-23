# Plan — Pendientes de la sesión 2026-09-22 (gobernanza del desarrollo con herdr, deskops y sldb)

## Kind

plan / pendientes de sesión — formato master-plan

## Status

abierto — nada commiteado. El trabajo de la sesión quedó sin task, sin gates y sin closeout.

## Contexto

Sesión del 2026-09-22 en `/home/jp/setup` sobre la gobernanza del desarrollo con herdr, deskops y sldb.

Alcance: todos los repos del usuario, incluyendo `~/AntonIA`, registrados **por referencia** en setup. Setup es el puesto de trabajo, no absorbe los proyectos.

## Decisiones tomadas (por el usuario)

1. **Alcance**: todos sus repos, incluyendo `~/AntonIA`, registrados por referencia en setup. Setup es el puesto de trabajo; no absorbe los proyectos.
2. **Skills**: traerlas a setup y trackearlas en git.
3. **Superficie**: migrar a la superficie de pron; si a pron le falta algo, arreglarlo y seguir como skill.
4. **herdr**: cablearlo directo, sin seam de transporte por ahora.
5. **spec2viz**: debe estar siempre al día y operar sobre código y atoms, no solo ser superficie documental.
6. **Análisis**: rehacer y trackear los documentos de análisis.
7. **Stress-tests**: deben ser un documento tipado propio (hijo de test) y usar más documentos tipados vía pron.

## Pendientes (por decisión)

1. **Desks faltantes en el registry**: el registry está hecho con 19 repos, pero faltan desks en pron, legos, Matrix, matrix-shrdlu-spec y mepu.
2. **Skills sin trackear**: las skills fueron copiadas a `.pi/skills` pero **no** están trackeadas en git, y `/home/jp/.pi/agent/settings.json` sigue apuntando a hum-ecosystem; solo se dejó `settings-skills.example.json`.
3. **`pron say` roto**: revienta con traceback en `session.py:86`; no está reportado ni arreglado, y la skill de arreglar-y-seguir no existe.
4. **Cableado de herdr**: `deskops launch` no existe; el cableado de herdr es cero.
5. **spec2viz desactualizado**: sus salidas siguen siendo del 22 de mayo de 2026.
6. **Documentos de análisis sin corregir**: los 12 documentos en `desk/drawer/analysis/` fueron auditados (el doc 03 tiene 7 de 7 citas archivo:línea desviadas) pero **no** corregidos, y siguen siendo markdown suelto sin tipar.
7. **TestDoc / StressTestDoc sin declarar**: solo están diseñados en `analysis/10`; no están declarados ni registrados, y los 21 stress-tests siguen sueltos.

## Artefactos producidos (sesión 2026-09-22)

| Artefacto | Qué es | Cuántos | Estado |
|---|---|---|---|
| `desk/atoms/herdr/` | Documentación tipada de los comandos de herdr con el modelo `HerdrCommandDoc` | 80 tipados por CLI + 11 conceptuales a mano = 91 | Los 80 emitidos con `sldb docs create`; los 11 conceptuales sin verificar contra el contrato `AtomDoc` |
| `desk/atoms/` (raíz) | 3 atoms sobre el conocimiento tácito de modelos repo-local: `atom-models-live-where-their-content-lives`, `atom-any-repo-can-declare-structured-doc-models`, `atom-model-ref-resolves-via-pythonpath-not-packaging` | 3 | Escritos; sin verificar si cumplen el contrato `AtomDoc` |
| `herdr/models.py` | Modelo repo-local `HerdrCommandDoc` registrado con `model_ref herdr.models:HerdrCommandDoc` y path relativo | 1 | Registrado y validado, PERO contiene 2 ediciones a mano que nunca pasaron por el flujo draft-validate-promote; no confiable como referencia |
| `herdr/derive_docs.py` | Derivador que genera los payloads parseando el `--help` real del binario herdr; regenera los 80 documentos cuando cambie la versión de herdr | 1 | Funciona; falta un modo `--check` tipo `pron docs` que detecte deriva sin reescribir |
| `desk/registry/` | Registro de todas las unidades de trabajo del usuario, personales y de AntonIA, por referencia | 19 repo docs + 1 README índice | Hecho; faltan desks en pron, legos, Matrix, matrix-shrdlu-spec y mepu |
| `desk/drawer/analysis/` | 12 documentos de análisis sobre deskops, herdr, spec2viz y tipos de documento | 12 | Escritos y auditados (07, 08, 09 son las auditorías); el doc 03 tiene 7 de 7 citas archivo:línea desviadas y NINGUNO fue corregido; siguen siendo markdown suelto sin tipar |
| `.pi/skills/` | Copia versionable de las skills de pi traídas desde hum-ecosystem | 6 skills + `DEPRECATED-use-kgdb.md` + `README.md` + `settings-skills.example.json` | Copiadas y parcheadas (use-sldb ganó la sección "Declaring a repo-local model"; use-deskops ganó la línea 161 sobre no forzar tipos en AtomDoc); NO trackeadas en git y `settings.json` sigue apuntando a hum-ecosystem |
| `desk/drawer/gap-sldb-modelos-repo-local.md` | Nota de gap dirigida a sldb (skill sin ejemplo de model_ref repo-local + bug de `hash_b`) | 1 | El gap doc existe y ya hay una nota equivalente **entregada por archivo** al inbox de sldb (`/home/jp/proyectos/hum-ecosystem/tools/sldb/desk/inbox/20260923-130322-suggestion-documentar-modelo-repo-local-y-cerrar-reporte-hash-b.md`); ambas quedan **duplicadas** — pendiente decidir cuál sobrevive |
| Handoff del bug de sldb `models fields add` | Texto de handoff para el agente que repare el bug del newline final en `insert_field_block` | 1 | El trabajo ya arrancó en el worktree `/home/jp/proyectos/_worktrees/sldb-fields-newline`; el texto del handoff en sí sigue sin persistirse como archivo |
| `desk/inbox/` | Notas entrantes | 3 | Sin trackear |
| `external-resources/` | Fichas de herramientas externas, tipadas con el modelo repo-local `ExternalResourceDoc` | 27 | Sin trackear; es el ejemplo canónico del patrón de modelo repo-local |

Notas:

- Los artefactos de otras sesiones (`hermes-agent-evaluacion.md` y la actualización del README del drawer) **no** forman parte de estos pendientes.
- Todo lo listado está **sin commitear**.

## Bloqueantes

- **Nada está commiteado**: 4 modified y untracked en setup — los 22 originales más los 2 artefactos de la sesión 2026-09-23 (hermes-agent-evaluacion.md y el propio plan).
- **Store sldb en `valid: false`**: 78 `HerdrCommandDoc` y 26 `ExternalResourceDoc` en `data_mutation`.
- **Ediciones a mano en `herdr/models.py`**: 2 ediciones que nunca pasaron por el flujo draft-validate-promote.
- **Handoff del bug de sldb**: el texto del handoff sigue sin persistirse como archivo; el trabajo del fix ya arrancó en el worktree /home/jp/proyectos/_worktrees/sldb-fields-newline.

## Higiene (no requería decisión)

- Limpiar ~9 repo docs de stress-test del registry de deskops que rompen el intake.
- Limpiar la basura de `desk/drawer/attention` (`aaaaaa`, `prueba corta`, `inbox-note-none`).
- Agregar a la skill `use-deskops` los comandos que existen y no menciona: `closeout verify`, `drift check`, `runtime supervise`.

## Estado del trabajo

- La documentación de herdr quedó como 80 comandos tipados con el modelo `HerdrCommandDoc`, emitidos por CLI, más 11 atoms conceptuales escritos a mano y sin verificar.
- Existe `herdr/derive_docs.py`, que deriva los payloads del `--help` del binario.
- El backup de los 89 originales es volátil, en `/tmp`: se pierde al reiniciar.
- Falta un `--check` tipo `pron docs` que detecte cuándo cambió la superficie de herdr.

## Artefactos producidos (sesión 2026-09-23)

- `desk/drawer/hermes-agent-evaluacion.md` — evaluación de Hermes Agent como sustrato (10 secciones). Marcado explícitamente como **no verificado en runtime**: no hay binario `hermes` en esta máquina.
- `desk/drawer/README.md` — línea agregada para el documento de Hermes.
- Nota entregada por archivo al inbox de sldb (el intake cross-repo está roto, ver Hallazgos): `/home/jp/proyectos/hum-ecosystem/tools/sldb/desk/inbox/20260923-130322-suggestion-documentar-modelo-repo-local-y-cerrar-reporte-hash-b.md` — 3 puntos: patrón de modelo repo-local sin documentar, cierre del reporte de `hash_b` (ya corregido) y consulta sobre la jerarquía de modelos de evidencia.
- `desk/drawer/gap-sldb-modelos-repo-local.md` (146 líneas) — mismo gap, escrito a las 12:04 por un worker de otra sesión. **Queda duplicado con la nota del inbox de sldb.**
- Sandbox de reproducción del bug `hash_b`: `/home/jp/setup/.tmp/gap2-repro` (modelo `gap2repro.models:VoidDoc`, sin documentos).
- `.herdr-coordination.md` — transcript del dispatch de diagnóstico.

## Hallazgos (sesión 2026-09-23)

### Deskops: estado real

- Worktree limpio en `529e990`: **7 failed / 212 passed**. Los rojos son **preexistentes**, no producto del árbol sucio.
- Árbol de trabajo: 5 failed / 268 passed, con ~62 archivos sin commitear y último toque **2026-09-17**.
- `sldb stores check --store .sldb`: **FAIL**, exit code 1.
- `deskops doctor --root .`: 1 finding legacy (`stores check` falla), ~239 "untracked desk documents" y ~94 "invalid desk documents", **todos `data_mutation`**.
- Uno de los rojos ya estaba documentado en el feature doc: `tests/test_cli.py::test_cli_help_uses_deskops_name` falla porque `529e990` agregó el subcomando `runtime` sin actualizar la lista esperada.

### Deskops: el gap de determinismo

- `deskops/runtime/primitives.py` **es** una máquina de estados determinista: `Condition.evaluate` (equals, not_equals, truthy, falsy, not_empty, contains), `Operator.apply` (set_field, append_list), `Routine.advance`, `validate_integrity`.
- El problema no es el grafo: **todo predicado lee el payload extraído del Markdown de la tarea**, es decir, campos auto-reportados.
- `TaskDoc.validation` es `list[str]`: comandos como texto, nunca ejecutados.
- El único `subprocess` del ciclo es `git add/commit` en closeout (`operations.py:1487-1510`): registra, no verifica.
- El hook de extensión **ya existe**: `operations.py:1029` inyecta `closeout_evidence_verified` y `pill_graduation_verified` al payload antes de `routine.advance()`.
- `advance --to` (`operations.py:1006-1023`) fuerza `complete` + `status: closed` saltando todos los gates.
- Faltante propuesto: `ProofDoc` (command, cwd, timeout, expect_exit_code → exit_code, duration_ms, stdout_sha256, head_sha) + predicados `exit_code_is` / `probe_fresh` + allowlist en `desk/config.json` + `deskops add probe`.

### Deskops: deuda estructural

- `deskops/operations.py`: **2.765 líneas** (loaders, transiciones, closeout, auto-commit, parseo de args).
- Las relaciones se resuelven por **substring del nombre de archivo** (`operations.py:2433`, `1533`, `555`; `_resolve_glob` aparece 8 veces), pese a que los modelos tienen `__references__` y el store tiene índice de documentos.
- Importa solo APIs de bajo nivel (`sldb.store.io`, `sldb.runtime.validation`); **cero** uso de búsqueda semántica, `find` o `sldb.api`.
- Medición corregida: 571 `.md` en `desk/` con 134 trackeados, pero `doctor` clasifica `drawer/`, `inbox/`, `features/`, `logbook/`, `runtimes/` y `README.md` como "ignored by design". La deuda real es el subconjunto que el doctor reporta roto, no el total.

### Intake cross-repo: errores literales obtenidos

- `deskops inbox list --root /home/jp/setup` → exit 0, pero **no lista**: interpreta `list` como el mensaje posicional (el flag correcto es `--list`) y entrega una nota basura de setup a sí mismo: `Delivered inbox note from setup to setup at /home/jp/setup/desk/inbox/20260923-115256-unclear-list.md` + `Tracked '20260923-115256-unclear-list'`.
- `deskops inbox list --root /home/jp/proyectos/hum-ecosystem/tools/deskops` → exit 1: `Error: Repository id 'deskops' not found in registry at '/home/jp/setup/desk/registry'. Supported path: run 'deskops repo register <name> --path <abs>' or add an entry to the ecosystem registry.`
- Causa: `resolve_canonical_project_identity` resuelve el registry del ecosistema desde el store del **CWD** (`find_local_store()`), no desde `--root`. En ese registry no están `sldb`, `deskops`, `spec2viz` ni `kgdb`: solo `hum-ecosystem`. Por eso `deskops inbox ... --repo sldb` tampoco habría funcionado.

### Bug `hash_b` de sldb: cerrado

- El bug reportado en el feature doc de deskops (`hash_b: ''` con cero documentos y `stores check` en FAIL) **no se reproduce en el HEAD actual**.
- Repro: `hash_b: 4f53cda1...` (= `sha256("[]")`, el hash del índice vacío), `documents_count: 0` y `stores check` → **PASS**. `models update` es no-op.
- Fix: `src/sldb/cli/commands/model_add.py`, `_create_models_index` (líneas ~54-64), atribuido por `git blame` a **1b04515e** (2026-09-15). Regresión cubierta en `tests/store/test_cli_store.py:298`.
- Acción pendiente: solo cierre formal (mencionarlo en CHANGELOG).

### Hermes Agent

- **Kanban descartado** como fuente de verdad: SQLite mono-host en `~/.hermes/kanban.db`, no diffable, sin links entre boards.
- Opción viable: Hermes como **runtime de worker headless** (`hermes chat -q --format stream-json`, `--usage-file`), consumido por deskops. herdr 0.9.0 ya lista `hermes` como kind.
- Detalle completo, patrones a robar por tier y lo que no se roba: `desk/drawer/hermes-agent-evaluacion.md`.

### Correcciones propias de esta sesión

- "571 `.md`, 134 trackeados = 23% de deuda" estaba **mal medido** (ver deuda estructural).
- "Los gates de deskops son prosa" fue **impreciso**: el grafo de transición es determinista; lo que falta son fuentes de hecho ejecutables.

### Riesgo de colisión

- Hay una **segunda sesión pi en `/home/jp/setup`** (pane `wX:pF`, idle) que escribió `desk/drawer/gap-sldb-modelos-repo-local.md` (12:04) vía un worker.
- `herdr/models.py` tiene mtime **2026-09-23 15:53:52**, ajeno a esta sesión; su contenido es idéntico a HEAD (`git diff` vacío), así que no hubo pérdida.
- Dos coordinadores en el mismo cwd: riesgo de pisarse en archivos compartidos.

## Pendientes agregados (sesión 2026-09-23)

1. **Arreglar los 7 rojos de HEAD en deskops** antes de cualquier trabajo nuevo.
2. **`ProofDoc`** + predicados + allowlist + `deskops add probe`, en la secuencia: línea base → A (modelo + runner + predicados) → B (CLI, allowlist, `--to` auditado).
3. **Decidir** si el refactor de `operations.py` (2.765 líneas) va antes o después de `ProofDoc`.
4. **Sustituir** el lookup por substring/glob por consulta al índice de documentos.
5. **Definir la jerarquía de modelos de evidencia** (`ProofDoc` / `RunDoc` / `TestDoc` / `StressTestDoc`) — consulta ya enviada al inbox de sldb.
6. **Reportar del lado deskops** el bug de intake (`identity.py`: registry resuelto desde el store del CWD; `sldb`/`deskops`/`spec2viz`/`kgdb` ausentes del registry del ecosistema).
7. **Resolver el duplicado** de la nota de gap a sldb (drawer vs inbox).
8. **Decidir** el piloto de Hermes como worker headless, o postergarlo hasta cerrar la línea base.
9. **Decidir** el destino del árbol sucio de deskops (~62 archivos, 6 días): commitear, descartar o terminar la migración.

## Bloqueantes agregados (sesión 2026-09-23)

- **Deskops sin línea base**: ~62 archivos sin commitear (último toque 2026-09-17) y 7 tests rojos en HEAD.
- **Store de deskops en FAIL**: `sldb stores check` exit 1 y ~94 documentos en `data_mutation`.
- **Intake cross-repo inutilizable** en ambos extremos (ver errores literales).
- Verificación de cifras del bloque original: `modified: 4` ✅ · `untracked: 24` = los 22 del plan **+ los 2 artefactos nuevos de esta sesión** (`hermes-agent-evaluacion.md` y este plan) · store `valid: False` ✅ · `ExternalResourceDoc`: 26 docs ✅ · `HerdrCommandDoc`: 80 docs ✅.

## Nota de trazabilidad

Reconocer que toda esta sesión produjo ~120 archivos sin task, sin gates y sin closeout: es el mismo anti-patrón que `desk/drawer/analysis/01-deskops-subutilizado.md` denuncia sobre otros hallazgos previos.
