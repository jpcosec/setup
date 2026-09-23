---
id: gap-sldb-modelos-repo-local
title: "Gap sldb: modelos repo-local no documentados + bug hash_b (intake roto)"
status: open
created_at: '2026-09-23T11:58:00'
source_feature_doc: /home/jp/proyectos/hum-ecosystem/tools/deskops/desk/drawer/features/feature-herdr-supervised-execution-runtime.md
---

# Gap sldb: modelos repo-local no documentados + bug hash_b

Nota de gap dirigida al repo **sldb**, redactada siguiendo la regla de la skill `use-sldb`:

> "If an expected SLDB path fails, capture the gap in the sibling `sldb` repo instead of silently bypassing SLDB."

No pudo entregarse por el `inbox` de sldb porque el intake cross-repo está roto (verificado hoy, 
2026-09-23, con los errores literales abajo). Queda en el drawer con constancia de por qué.

## Contexto

- El patrón de modelos repo-local se usa en `setup` (repo **sin** `pyproject.toml`) y no está
  documentado en la skill de sldb; y existe un reporte de bug (`hash_b` vacío) originado en un
  feature doc de deskops que hay que cerrar contra el estado actual de sldb.
- Verificación del intake cross-repo ejecutada hoy: falla en ambos extremos, pero **no** con los
  errores que se esperaban (ver "Por qué esta nota está en el drawer").

## Gap 1 — Documentación: la skill `use-sldb` solo muestra model_ref de `deskops`

**Ruta**: `/home/jp/proyectos/hum-ecosystem/tools/sldb/.pi/skills/use-sldb/SKILL.md`

- En el bloque `## Common commands` (líneas 42–76), **12 de los 24 ejemplos** usan `AtomDoc` como
  único modelo de ejemplo y el ref calificado `deskops.models:AtomDoc` aparece **4 veces**:
  - línea 49: `python -m sldb models add deskops.models:AtomDoc --store .sldb --pythonpath .`
  - líneas 70–72: `extract` / `render` / `validate` con `deskops.models:AtomDoc`
- La sección `## Model editing workflow` (líneas 77+) usa el placeholder genérico `<model-ref>`
  (línea 92), así que nunca aparece un `model_ref` que no sea de `deskops`.
- Efecto inducido: **todos los modelos parecen vivir en el repo deskops**. Sin embargo
  `deskops.models` es real (`deskops/models/atom.py` define `AtomDoc`), por lo que los comandos
  de ejemplo *funcionan* y nadie descubre el patrón repo-local.

**El patrón real no está documentado en el repo sldb** (ni en la skill ni en `docs/`):

- `/home/jp/setup/external-resources/models.py` → `class ExternalResourceDoc(StructuredNLDoc)`
- `/home/jp/setup/.sldb/core/models/ExternalResourceDoc.yaml`:
  - `model_ref: external-resources.models:ExternalResourceDoc`
  - `path: external-resources/models.py` (ruta **relativa** al root del repo)
  - `documents_count: 26`, `hash_b` poblado
- `/home/jp/setup` **no tiene `pyproject.toml`**: no es un paquete Python; el modelo se resuelve
  solo por `--pythonpath .` en cada invocación.
- En sldb solo hay menciones genéricas "repo-local" que no cubren el patrón
  (`README.md:228` sobre skill file; `docs/requests/sldb-postulator-integration-guide.md:19`
  sobre `.sldb/` repo-local). Los únicos registros escritos del patrón están como atoms locales
  de setup: `desk/atoms/atom-any-repo-can-declare-structured-doc-models.md`,
  `atom-model-ref-resolves-via-pythonpath-not-packaging.md` y
  `atom-models-live-where-their-content-lives.md`.

**Acción sugerida para sldb**: añadir un ejemplo a `Common commands` con model_ref de otro repo
y aclarar que un repo sin packaging declara sus modelos en un `models.py` local resuelto por
`--pythonpath`, p. ej. `sldb models add external-resources.models:ExternalResourceDoc
--store .sldb --pythonpath .`.

## Gap 2 — Bug reportado (hash_b vacío al registrar modelo con 0 docs): YA CORREGIDO en HEAD

**Origen del reporte**: `/home/jp/proyectos/hum-ecosystem/tools/deskops/desk/drawer/features/feature-herdr-supervised-execution-runtime.md`
- línea 22 (incidental finding): *"registering a document model with zero tracked documents
  (`sldb models add` on `RunDoc` …) leaves `hash_b: ''` in `.sldb/core/models/<Name>.yaml` …
  and `sldb stores check` then FAILs until `sldb models update <Name>` is run once"*.
- sección `### RunDoc` en línea 113. El feature doc está sin commitear (HEAD deskops `529e990`,
  2026-09-09).

**Reproducción ejecutada hoy** (sandbox `/home/jp/setup/.tmp/gap2-repro/`, sldb v0.1.0 editable
desde `/home/jp/proyectos/hum-ecosystem/tools/sldb`):

1. `gap2repro/models.py` con `class VoidDoc(StructuredNLDoc)` (cero documentos trackeados).
2. `sldb stores init --path .` → `Initialized store at ...`
3. `sldb models add gap2repro.models:VoidDoc --store .sldb --pythonpath .` → `Registered 'VoidDoc'`
4. `.sldb/core/models/VoidDoc.yaml` → `hash_b: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
   (= `sha256("[]")`, el hash del índice de documentos vacío; **no vacío**), `documents_count: 0`.
5. `sldb stores check --store .sldb` → `PASS: store integrity` (**no falla**).
6. `sldb models update VoidDoc --store .sldb --pythonpath .` → no-op; `hash_b` idéntico.

**Resultado**: el bug descrito **no se reproduce** con el sldb actual.

- Fix: `src/sldb/cli/commands/model_add.py`, `_create_models_index` — fija
  `hash_b=hash_documents_index(DocumentsIndex())` desde el registro; el comentario del código
  describe este fallo exacto ("…not the empty string"). Commit `1b04515e` (2026-09-15).
- Test de regresión existente: `tests/store/test_cli_store.py` (~líneas 150–160: docstring
  "hash_b registration bug, now fixed"; ~líneas 283–298: `hash_b == hash_documents_index(DocumentsIndex())`
  y `!= ""`); también `tests/store/test_models_io.py:87`.

**Acción sugerida para sldb**: dar por cerrado el incidente reportado desde deskops, añadir
entrada de changelog/nota si no existe, y **no duplicar el fix**.

## Por qué esta nota está en el drawer y no en el inbox

Intake cross-repo verificado el 2026-09-23 (CWD `/home/jp/setup`). Ninguno de los dos comandos
falló con el error esperado; falla de otras formas:

**1)** `deskops inbox list --root /home/jp/setup` → **exit 0, sin error**; hace lo incorrecto:
interpreta `list` como el *mensaje* (el flag real de listado es `--list`; `message` es posicional,
`parser.py:_add_inbox_commands`) y auto-entrega una nota basura setup→setup. Stdout literal:

```
Delivered inbox note from setup to setup at /home/jp/setup/desk/inbox/20260923-115256-unclear-list.md
Tracked '20260923-115256-unclear-list'
```

(efecto secundario de esta misma verificación: escribió y trackeó
`desk/inbox/20260923-115256-unclear-list.md`, body "list"). No apareció el esperado
`Repository id 'setup' not found in registry`.

**2)** `deskops inbox list --root /home/jp/proyectos/hum-ecosystem/tools/deskops` → **exit 1**.
Stdout literal:

```
Error: Repository id 'deskops' not found in registry at '/home/jp/setup/desk/registry'. Supported path: run 'deskops repo register <name> --path <abs>' or add an entry to the ecosystem registry.
```

- **No** es el `Duplicate repository root` hipotetizado: los ~20 repo docs de stress-test viven en
  `deskops/desk/registry`, pero el intake resuelve el registro del ecosistema desde el store del
  **CWD** (`identity.py:resolve_store_context` → `find_local_store()` → `/home/jp/setup/.sldb` →
  `/home/jp/setup/desk/registry`), no desde `--root`. Ahí **no están registrados** ni `deskops` ni
  `sldb` ni `spec2viz` ni `kgdb` (solo `hum-ecosystem` como monorepo), por lo que falla antes, en el
  lookup por id (`identity.py:_missing_repository_message`).
- Consecuencia: tampoco existe delivery a `sldb` hoy (`sldb` no está en el registro del ecosistema),
  así que esta nota no puede ir por inbox.

## Cómo entregarla cuando el intake funcione

1. Registrar sldb en el registro del ecosistema (una vez, desde `/home/jp/setup`):
   ```
   deskops repo register sldb --id sldb --path /home/jp/proyectos/hum-ecosystem/tools/sldb
   ```
   (idem para `deskops` si se quiere delivery cruzado con su drawer.)
2. Entregar desde `/home/jp/setup` (sender = `setup`), **sin** `--root` (con `--root` el target se
   desvía al repo local, `inbox.py:_desk_root` prioriza `--root` sobre `--repo`):
   ```
   deskops inbox "<cuerpo de esta nota>" --repo sldb --kind suggestion --title "gap sldb: modelos repo-local y hash_b"
   ```
3. Triaje (regla deskops `atom-used-source-artifacts-are-deleted`): tras ack de sldb, eliminar la
   fuente del inbox, cerrar/borrar esta nota del drawer y actualizar `desk/drawer/README.md`.

## Notas

- `deskops inbox --list --root .` es la forma correcta de listar (con guion doble), no
  `deskops inbox list ...`.
- Fuera de `setup` no se modificó nada y no se hizo `git commit`.