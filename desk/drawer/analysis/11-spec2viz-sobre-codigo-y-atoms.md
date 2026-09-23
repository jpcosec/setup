# 11 — spec2viz: de superficie documental a herramienta sobre código y atoms

Fecha: 2026-09-23. Método: solo lectura (spec2viz/README.md, spec.md, DEVELOPER_GUIDE.md, CHANGELOG.md, cli.py, generators/, deskops.py, tests/; git log de docs/architecture; kgdb/README.md). Ningún archivo modificado, ningún repo tocado, sin commits.

## Tesis

El YAML de diagrama deja de ser fuente de verdad escrita a mano y pasa a ser un **artefacto derivado** de dos fuentes vivas: el código real (AST) y los atoms de cada desk. spec2viz deja de ser "la capa que renderiza YAML" y pasa a ser el **motor de proyección** (derivar spec → validar → render) más una capa de **verificación de drift**. El render (Mermaid/PlantUML/HTML) queda como proyección de esa proyección.

```
código real (AST)  ──┐
                     ├──> IR derivado (spec YAML generada, no editable a mano) ──> catalogo HTML + .mmd/.puml
atoms de cada desk ──┘                              │
                                                     └──> chequeo de drift contra codigo (refactor rules)
```

## 1. Qué compila spec2viz hoy (verificado)

- Pipeline establecido: `Model (Pydantic) -> Compiler -> IR -> Renderer`. Tipos: activity, class_diagram, component, deployment, matrix, reflection, sequence, state.
- CLI agrupada en `diagram` (`validate|render|lint|schema|generate`) y `catalog` (`build|schema|serve`), con `about` y alias legacy. Forma canónica: `spec2viz diagram ...` / `python -m spec2viz.cli ...`.
- Renderers: `plantuml`, `mermaid`, `vega`, `d2`, `antonia-html`, `tree`, `graph`, `json`.
- **Ya existe germen de lo pedido** (no hay que partir de cero):
  - `spec2viz diagram generate --src-dir X --out Y` → `spec2viz/generators/python_ast.py`: escanea módulos/clases/imports con `ast` estándar y emite spec `component` YAML.
  - `spec2viz catalog build --atoms-dir ...` → `spec2viz/deskops.py::SldbAtomResolver`: lee `AtomDoc` de stores `.sldb` (vía `sldb.cli.model_utils.resolve_model_ref` y `extract_model_data`) y los inyecta como `window.ATOMS_DB` en el HTML. `parse_atoms`, `build_atoms_by_view`, `build_coverage_by_view` ya existen y tienen tests.
  - Modelo `reflection` (CHANGELOG 0.2.0, 2026-05-01): `ReflectionNode/ReflectionEdge` con metadata 6D (who/what/where/when/how/why) y `EnforcementArtifact` con `facts` + `fingerprint` — el fingerprint es exactamente la pieza que sirve para detectar drift.

## 2. El problema constatado

- Única spec fuente: `tools/…/docs/architecture/component/hum-ecosystem.component.yml` — fecha 2026-05-22 11:29, último commit que la toca b3e919a (2026-05-19).
- Salidas `docs/architecture/out/hum-ecosystem.component.{mmd,puml}` — también 2026-05-22. **4 meses viejas.**
- Está estructuralmente mal desde 2026-09-20: sigue modelando `KGDB` como nodo `database` separado con aristas (`feeds`, `uses`, `powers`, `exports`, `queries`, `informs`, `validates`) cuando kgdb fue absorbido por sldb (kgdb/README.md: "Absorbed by sldb (2026-09-20)", repo "hollow", re-exports de sldb). Tampoco refleja kbsurfaces, marcado, iso-lab, tractatusIR, sldb-ui, deskops-pron.
- Causa raíz: el YAML se edita a mano. Nadie lo reescribió cuando el ecosistema cambió. La mano humana no escala a 17+ repos.

## 3. Referencias externas a incorporar

### 3.1 `refactor` (Python, isidentical) — motor AST para Python

- Una regla = `class MiRule(refactor.Rule)` con `match(node) -> BaseAction`.
- **Contrato = asserts**: `assert isinstance(node, ast.BinOp)` … Cualquier `AssertionError` en `match()` es señal de *saltar al siguiente nodo* — no un fallo. Recomendado por la doc sobre ifs.
- **Acciones**: `Replace(node, target)`, `InsertAfter(node, stmt)`, `Erase(node)`, `EraseOrReplace(node)`, y variantes lazy (`LazyReplace(node)` con `build()`). `InvalidActionError` si la acción produciría código no parseable (ej. borrar el único statement de un bloque → `pass`).
- **Ejecución**: `refactor.run(rules=[...])` como `__main__` genera un CLI que muestra diff; `Session(rules=[...]).run(code)` embebido.
- **Sin dependencias**: instalable como dev-dependency de spec2viz sin arrastrar árbol pesado.
- Aplicación para spec2viz: (a) reglas para *extraer hechos* (match() que devuelve un hecho en vez de una acción), (b) asserts como *contrato de arquitectura* (si la regla deja de matchear el código → drift, en CI), (c) acciones `Replace`/`InsertAfter` para *auto-remediar* drift mecánico.

### 3.2 `dcyfr-ai-code-gen` (TypeScript / ts-morph) — patrón para frontends TS

- `createGeneratorRegistry()` + `registry.run("component", {...}) -> result.files[]`: generadores pre-construidos (component, api-route, model, test).
- `TemplateEngine` (Handlebars) con `renderSource(tpl, data)` y helpers: `camelCase`, `pascalCase`, `snakeCase`, `kebabCase`, `constantCase`, `#if/#unless`, `eq/neq/or/and/not`, `pluralize`, `join`, `typeAnnotation`, `genericType`.
- Módulo AST: `parseSource/parseFile` → declaraciones (classes, interfaces, functions, types, enums, imports, exports) + métricas; `transform(source, ops[])` con ops tipadas (`add-import`, `remove-import`, `add-property`, `add-method`, `rename`, `add-export`); `analyzeCode` (dead-code, complexity, naming, missing-jsdoc, large-file); `compareStructure(old, new)` → added/removed/modified; `formatTypeScript`.
- Para spec2viz es el *espejo TS* del patrón refactor: sirve de referencia cuando haya que derivar specs desde los frontends del ecosistema (sldb-ui, graph_ui, marcado-ui). No se porta; se copia el patrón (parse → decls → hechos → comparación estructural).

## 4. Cómo se deriva la spec desde código y atoms

### 4.1 Fuentes y qué aporta cada una

| Fuente | Qué da | Commando/mecanismo |
|---|---|---|
| Código Python real (AST) | Nodos (`module_X`, `class_Y`) y aristas `defines`/`imports`/`calls`; firma de clases y funciones | `spec2viz diagram generate --src-dir <repo>/src --out ...` (ya existe, se extiende) |
| Atoms de cada desk | Semántica que el AST no puede inferir: `kind` (core/boundary/database/service), roles 6D, boundaries, propósito | `spec2viz catalog build --atoms-dir <repo>/desk/atoms ...` (ya existe vía `SldbAtomResolver`) |
| Índice de aristas de sldb | Relaciones tipadas entre repos/nodos a nivel macro | nuevo `spec2viz graph ingest --store <repo>/.sldb` leyendo el edge index (`sldb edges`) |
| Overlay de intención (única parte manual) | Relaciones semánticas no inferibles: `orchestrates`, `feeds`, `documents` | `docs/architecture/component/*.overlay.yml` (delgado, estable) |
| manifiestos repo (deskops `repo register` / `config.json` `project_identity`) | Nodos raíz por repo y sus boundaries | lectura de `desk/config.json` + `~/.deskops` |

### 4.2 Flujo concreto propuesto

1. **`spec2viz diagram generate --src-dir tools/spec2viz/spec2viz --out build/generated/code.component.yml`** — AST del código real (extender `generators/python_ast.py` para incluir funciones, firmas y `calls`).
2. **`spec2viz atoms merge --atoms-dir tools/spec2viz/desk/atoms --spec build/generated/code.component.yml --out build/generated/semantic.component.yml`** — nuevo: re-etiqueta nodos con `kind`/provenance desde los `AtomDoc` (`five_wh_one_plus`, `tags: system:`, `tags: topic:`, `provenance:`) que ya resuelve `SldbAtomResolver`.
3. **`spec2viz graph ingest --store tools/sldb/.sldb --spec ...`** — nuevo: inyecta aristas tipadas desde el edge index de sldb (que absorbió a kgdb).
4. **`spec2viz diagram validate build/generated/semantic.component.yml`** — sin cambios.
5. **`spec2viz diagram render ... --out docs/architecture/out/`** y **`spec2viz catalog build --config docs/architecture/catalog.yml --atoms-dir ... --out docs/architecture/out/architecture.html`** — proyecciones finales.

Regla de oro del directorio:

- `docs/architecture/component/*.component.yml` = **derivado de build**. Se regenera, nunca se edita a mano (igual que hoy nadie edita el `.puml` a mano — mismo principio, un nivel más atrás).
- `docs/architecture/component/*.overlay.yml` = única superfície de edición manual, para intención arquitectónica.
- `docs/architecture/out/*` = proyección regenerable.
- El `reflection`/`EnforcementArtifact`(fingerprint) ya da el patrón para versionar el "contrato" derivado.

### 4.3 A qué niveles

- **Micro (dentro de un repo)**: nodo = módulo/clase; aristas = imports + llamadas reales. Sirve para el vendoring del propio spec2viz y de cada tool.
- **Macro (ecosistema, docs/architecture)**: nodo = repo/tool; aristas = imports en requirements/manifests, contracts de repopackage, y `provenance` de atoms. El YAML de hum-ecosystem.component.yml se regenera desde los 17 repos, no se reescribe. El nodo `KGDB` desaparece solo porque el código ya no lo declara.

## 5. Rol del motor AST estilo refactor (Python)

No es para render: es la capa que **edita y verifica código con contrato**.

1. **Extracción de hechos**: una regla `match()` que en vez de devolver acción devuelve un hecho `{source, target, kind}`. Cada assert en el contrato define exactamente qué shape de código cuenta como "una dependencia" — la misma biblioteca que refactor usa para transformar sirve para *medir*.
2. **Contrato de arquitectura en CI**: regla del tipo "todo `import X` en `tools/*/spec2viz/**` apunta a `spec2viz.*`" — si el assert deja de matchear en código nuevo, el `spec2viz project check --fail-on-drift` falla. **Los asserts SON el YAML de arquitectura ejecutable.**
3. **Auto-remediación**: `LazyReplace`/`InsertAfter` para normalización mecánica de drift (renombres de módulo, anotaciones que faltan, exports ausentes) — con `InvalidActionError` protegiendo parseabilidad.
4. **Sin dependencias**: entra como dev-dependency limpia.

Equivalencia directa con el modelo spec2viz:

| refactor | spec2viz |
|---|---|
| `match()` + asserts (contrato) | parte semántica del YAML derivado |
| `Replace`/`InsertAfter`/`Erase` | qué significa la arista en términos de código |
| hecho devuelto por la regla | fila del IR (`nodes`/`edges`) |
| `refactor.run`/`Session` | `spec2viz project check` en CI |

## 6. Cómo se mantiene siempre al día

Tres disparadores complementarios; el código cambia ⇒ la spec cambia, sin intervención humana:

| Cuándo | Qué corre | Quién |
|---|---|---|
| Pre-commit en cada repo con spec | `spec2viz project refresh --src-dir . --atoms-dir desk/atoms --out docs/generated/` (compone generate+atoms merge+graph ingest+validate+render) | hook `.git/hooks/pre-commit` de los repos del ecosistema |
| Cierre de tarea deskops | `deskops ritual run refresh-diagrams` (o post-closeout) — el momento natural donde el código ya cambió | ritual en `desk/rituals/` de cada repo |
| CI del ecosistema (raíz hum-ecosystem) | `spec2viz project check --fail-on-drift`: regenera IR en temp, compara fingerprint (`EnforcementArtifact.fingerprint` / `compareStructure`), falla si difiere del commiteado | pipeline root / Makefile |
| Trigger opcional | `sldb journal` / edge index nuevo → notifica a `spec2viz project refresh` | cron/evento |

El chequeo de drift es la pieza clave: sin él, "regenerar" vuelve a ser un YAML a mano. Con él, si algo cambió en código y la spec commiteada no, la CI se rompe.

## 7. Plan por fases

| Fase | Alcance | Entregable verificable | Salida |
|---|---|---|---|
| **0 — Baseline** | Congelar edición manual de `docs/architecture/component/*.yml`; generar por primera vez `hum-ecosystem.component.yml` desde código real con el comando existente | El nodo `KGDB` desaparece / pasa a `sldb` reflejando el estado real | commit de bootstrap |
| **1 — AST + atoms en un repo** | Extender `generators/python_ast.py` (funciones, firmas, `calls`); promover `atoms merge` a CLI de primera clase; pilotear en `tools/spec2viz` y `tools/sldb` (sus specs ya tienen desk/atoms) | `spec2viz diagram generate` + `atoms merge` + `catalog build` regeneran sin edición manual; tests nuevos en `tools/spec2viz/tests/` | docs/generated/ por repo |
| **2 — Multirrepo + aristas de sldb** | `spec2viz graph ingest --store` desde el edge index (sucesor de kgdb); boundaries desde `desk/config.json`/provenance; `*.overlay.yml` para intención | `docs/architecture/component/hum-ecosystem.component.yml` regenerado cubre los 17 repos | YAML derivado correcto |
| **3 — Reglas como contrato + auto-fix** | Adoptar `refactor` (dev-dependency); reglas de invariantes; `spec2viz project check --fail-on-drift` en CI; acciones `Replace`/`InsertAfter` para remediación | CI rojo si drift mecánico; auto-reparación de renombres/imports rotos | puerta de CI |
| **4 — Frontends TS** | Espejar el patrón de dcyfr-ai-code-gen (`parseSource`/`analyzeCode`/`compareStructure`) para sldb-ui, graph_ui, marcado-ui — sin portar; el IR de specYaml queda único | nodos UI en el catálogo con boundaries reales | catálogo completo |

Regla de avance: cada fase requiere tests en `tools/spec2viz/tests/` y N días consecutivos con `project check` verde antes de pasar a la siguiente.

## 8. Alineación con el ecosistema (contexto)

- `core/code2specyaml` (repositorio seed, 2026-09-21) ya marca la dirección: "code is truth, specs are intent", treesitter como sustrato, salida hacia `specYaml` canónico, con `sldb` como capa opcional de reconciliación. La propuesta de este documento hace que **spec2viz consuma** esa corriente (IR specYaml → render) en vez de generar el YAML semántico a mano.
- `kgdb` absorbido: toda lectura de grafo pasa por `sldb edges` / `sldb graph`; nada nuevo debe leer de `tools/kgdb/`.
- Los atoms de spec2viz ya viven como `AtomDoc` en `tools/spec2viz/desk/atoms/` (ej. `atom-ast-compilers-*.md`, `atom-cli-entrypoint-*.md`) — la Fase 1 los convierte en input del pipeline, no solo en ventana de HTML.

## 9. Resumen

1. El YAML deja de ser fuente de verdad: pasa a ser derivado de código real (AST) + atoms de cada desk + edge index de sldb, con `*.overlay.yml` como única edición manual.
2. `refactor` (Python) aporta el motor AST con contratos-assert, extracción de hechos y transformaciones `Replace`/`InsertAfter` — incluyendo el chequeo de drift en CI.
3. `dcyfr-ai-code-gen` (TypeScript) es el patrón espejo para derivar specs de los frontends TS del ecosistema.
4. La actualización corre por hook pre-commit + ritual deskops post-closeout + `spec2viz project check --fail-on-drift` en CI.
5. El germen ya existe (`diagram generate`, `SldbAtomResolver`, modelo `reflection`): el plan promueve esas piezas y añade `atoms merge`, `graph ingest`, `project refresh` y `project check`.