# 10 · Tipos de documento TestDoc y StressTestDoc

Diseño de dos modelos sldb para tipar los tests de deskops, siguiendo el patrón de documentos tipados de pron (y de los propios modelos de deskops: `AtomDoc`, `TaskDoc`, `RitualDoc`).

## Decisión en una línea

Definir `TestDoc` como tipo base genérico y `StressTestDoc` como su subtipo (herencia Python + `base_models` + RelationTypeDoc `specializes`) para los 15 `st-XX` de `desk/drawer/stress-tests/`.

## 1. Cómo declara pron sus tipos (patrón de referencia)

Un "modelo sldb" no es solo un YAML: es una clase Pydantic que extiende `StructuredNLDoc` y que el registro materializa en `.sldb/core/models/<Model>.yaml`. Los dos YAML son inseparables:

**A. Clase Python** (`pron/src/pron/models/spec.py`, `sldb/src/sldb/models/surface_doc.py`):

- `__semantics__`: pares `tipo` (`type.knowledge.spec`) y `workspace` (`workspace.knowledge.surfaces`).
- `__template__`: documento Markdown reversible con marcadores `⸢rev•campo⸥`, `⸢optrev•campo⸥` (opcional), `⸢rev,list•campo⸥`, `⸢rev,markdown•campo⸥`, `⸢render•campo⸥`.
- Campos tipados con `Field(description=...)`; opcionales como `str | None = Field(default=None)`; tags como `list[T] = Field(default_factory=list)`.
- `family` opcional (`knowledge`, `relation`) y `__references__` para ids de otros documentos.

**B. Metadata YAML** (generado, en `.sldb/core/models/`, ej. `AnchorDoc.yaml`):

```yaml
name: AnchorDoc
model_ref: pron.models:AnchorDoc
path: src/pron/models/anchor.py
documents_index: .sldb/core/documents/AnchorDoc.yaml
sections_index: .sldb/runtime/sections/AnchorDoc.yaml
hash_b: 426026ad...
documents_count: 5
version: 1
canonical: false
family: knowledge
semantics:
- representation.markdown
- source.document.markdown
- type.knowledge.anchor
- workspace.knowledge.anchors
base_models: []
```

Documentos reales de pron muestran el frontmatter que produce el template: `SurfaceDoc` → `id/surface/system/tags/provenance`; `RelationDoc` → `source_id/target_id/relation_type/condition`; `RelationTypeDoc` → `name/direction/cardinality/axis/source_types/target_types/condition`.

## 2. Convenciones de deskops

Los modelos viven en `deskops/models/*.py` (`model_ref: deskops.models:AtomDoc`), se exportan en `deskops/models/__init__.py`, y su metadata está en `deskops/.sldb/core/models/`.

- Semantics en español de dominio: `type.workflow.task`, `type.knowledge.atom`, `workspace.desk.atoms`, `workspace.desk.runs`.
- `family` en `null` (deskops no usa las familias de pron).
- Tags namespaced `namespace:value` (`AtomTag`, regex `^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$`).
- frontmatter con `id`, `title`, `tags`, `provenance` opcional; cuerpo con H1 renderizado.
- Registro vía CLI sldb: `sldb models add deskops.models:AtomDoc --store .sldb --pythonpath .`.

## 3. Qué necesitan los 21 documentos de `stress-tests/`

Son 21 files: 15 tests `st-01..st-15` + 6 meta-docs (`README`, `METHODOLOGY`, `FINDINGS_INDEX`, `ANCHORED_SUMMARY`, `COMPREHENSIVE_COVERAGE`, `PRIORITIZED_ROADMAP`) + dir `findings/`. De los 15 tests se extrae, de forma consistente:

| Sección actual (markdown suelto) | Campo que necesita |
|---|---|
| `# ST-NN: Title` | `id` (`st-01`) + `title` (`Fresh start orientation stress`) |
| `**Basado en:** UC-01` | `based_on` (`UC-01`) |
| `## Setup` (solo st-04, st-12) | `setup` (opcional) |
| `## Script` (bloque bash) | `script` |
| `## Puntos de estrés` (tabla paso→qué mirar) | `stress_points` |
| `## Modos de fracaso` (lista) | `failure_modes` |
| Tabla del README: Superficie / Énfasis | `surface` (`atoms, graph, faq`) + `emphasis` (`Orientación, primera impresión`) |

Los 6 meta-docs quedan fuera del alcance inicial (no son tests; se pueden tipar después si se quiere).

## 4. TestDoc — modelo base propuesto

**Clase** (`deskops/models/test.py`):

```python
from pydantic import Field
from sldb import StructuredNLDoc
from .atom import AtomTag


class TestDoc(StructuredNLDoc):
    """One executable test of a deskops capability, declared as an sldb
    model with a reversible Markdown document (pron-style). Generic base
    for every future test type; StressTestDoc extends it."""

    __semantics__ = {
        "type": ["workflow", "test"],
        "workspace": ["desk", "drawer", "tests"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Purpose

⸢rev•purpose⸥

## Script

⸢rev,markdown•script⸥

## Failure Modes

- ⸢rev,list•failure_modes⸥
""".strip()

    id: str = Field(description="Stable test id, conventionally 'st-<NN>' or 'test-<slug>'.")
    title: str = Field(description="Short descriptive title, shown as the H1.")
    purpose: str = Field(description="What capability this test exercises and why.")
    script: str = Field(description="Ordered commands/steps the test runs (markdown or code block).")
    failure_modes: list[str] = Field(
        default_factory=list,
        description="Concrete ways the experience breaks — not code bugs, but user-visible degradation.",
    )
    tags: list[AtomTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags in the form namespace:value (system:, kind:, status:).",
    )
    provenance: str | None = Field(
        default=None,
        description="Path or URL of the source this test documents.",
    )
```

**Metadata YAML** generado en `.sldb/core/models/TestDoc.yaml`:

```yaml
name: TestDoc
model_ref: deskops.models:TestDoc
path: deskops/models/test.py
documents_index: .sldb/core/documents/TestDoc.yaml
sections_index: .sldb/runtime/sections/TestDoc.yaml
hash_b: <calculado por sldb>
documents_count: 0
version: 1
canonical: false
family: null
semantics:
- type.workflow.test
- workspace.desk.drawer.tests
base_models: []
```

## 5. StressTestDoc — modelo hijo propuesto

Amplía `TestDoc` con la dimensión UX que los `st-XX` ya piden: origen (`based_on`), superficies, énfasis, setup y puntos de estrés. Hereda `id`, `title`, `purpose`, `script`, `failure_modes`, `tags`, `provenance`.

**Clase** (`deskops/models/stress_test.py`):

```python
from pydantic import Field
from .test import TestDoc


class StressTestDoc(TestDoc):
    """A UX stress test: a TestDoc (inherits all its fields) plus the
    experience dimension — the use case it stresses, CLI surfaces hit,
    per-step stress points, and failure modes a user would notice."""

    __semantics__ = {
        "type": ["workflow", "stress_test"],
        "workspace": ["desk", "drawer", "stress_tests"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
based_on: ⸢rev•based_on⸥
surface: ⸢rev•surface⸥
emphasis: ⸢rev•emphasis⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Purpose

⸢rev•purpose⸥

## Setup

⸢optrev,markdown•setup⸥

## Script

⸢rev,markdown•script⸥

## Stress Points

⸢rev,markdown•stress_points⸥

## Failure Modes

- ⸢rev,list•failure_modes⸥
""".strip()

    based_on: str = Field(description="Use case this test stresses, e.g. UC-02.")
    surface: str = Field(description="CLI surfaces exercised, comma separated (atoms, graph, faq).")
    emphasis: str = Field(description="Human emphasis of the test, one short phrase.")
    setup: str | None = Field(
        default=None,
        description="Optional setup steps required before the script (breaking commands, fixtures).",
    )
    stress_points: str = Field(
        description="Markdown table: each script step mapped to what to observe (not just 'works').",
    )
```

**Metadata YAML** en `.sldb/core/models/StressTestDoc.yaml`: igual que TestDoc pero con `model_ref: deskops.models:StressTestDoc`, `path: deskops/models/stress_test.py`, `workspace.desk.drawer.stress_tests` y la herencia explícita:

```yaml
name: StressTestDoc
model_ref: deskops.models:StressTestDoc
path: deskops/models/stress_test.py
documents_index: .sldb/core/documents/StressTestDoc.yaml
sections_index: .sldb/runtime/sections/StressTestDoc.yaml
hash_b: <calculado por sldb>
documents_count: 0
version: 1
canonical: false
family: null
semantics:
- type.workflow.stress_test
- workspace.desk.drawer.stress_tests
base_models:
- TestDoc
```

`base_models: [TestDoc]` hace que el edge index genere automáticamente el `extends` structural (el builtin `extends` de sldb: "instances of the source are instances of the target").

## 6. Relación padre-hijo como RelationTypeDoc al estilo pron

El índice distingue entre el edge structural `extends` (heredado de `base_models`) y el vínculo semántico documentado. Se declara un RelationTypeDoc autorado, `specializes`, como pron declara `implements`, con source/target limitados a los dos modelos:

**`sldb/relation_types/specializes.md`** (payload YAML):

```yaml
name: specializes
direction: directed
cardinality: many_to_one
axis: WHAT
source_types:
- StressTestDoc
target_types:
- TestDoc
condition: ''
---

# specializes

## Description

A document model specializes another document model: it inherits all its
fields (id, title, purpose, script, failure_modes, tags, provenance) and
adds fields that narrow its meaning. A StressTestDoc IS a TestDoc; the
template renders the child payload as a child document whose parent model
contract is the base.
```

Cardinalidad `many_to_one`: varios subtipos pueden especializar un mismo base, pero un subtipo especializa un único padre. El edge index valida todo `RelationDoc` con `relation_type: specializes` contra este documento.

La instancia de relación (RelationDoc, como los de `pron/knowledge/relations/`):

```yaml
source_id: StressTestDoc
target_id: TestDoc
relation_type: specializes
condition: ''
title: specializes--StressTestDoc--TestDoc
notes: |
  StressTestDoc hereda de TestDoc (base_models) y añade
  based_on, surface, emphasis, setup y stress_points.
  Cualquier documento StressTestDoc es válido como TestDoc.
```

## 7. Ejemplos reales migrando st-01

### 7a. Como TestDoc (el padre genérico — visión base)

`desk/drawer/stress-tests/st-01-fresh-start-orientation.md` migrado con los campos base:

```yaml
id: st-01
title: Fresh start orientation stress
tags:
- system:deskops
- kind:ux-stress
provenance: desk/drawer/stress-tests/st-01-fresh-start-orientation.md
---

# Fresh start orientation stress

## Purpose

Estresar la orientación de un recién llegado: `about`, `faq`, `atoms list/show` y `graph build/neighbors` en un desk recién clonado.

## Script

```bash
deskops about
deskops faq --topic atoms
deskops atoms list --tag system:deskops
deskops atoms show atom-deskops
deskops graph build
deskops graph neighbors atom-deskops
```

## Failure Modes

- El usuario tiene que leer código fuente para entender qué hace deskops
- `about` y `faq` describen un mundo distinto al que `atoms list` muestra
- `graph build` requiere setup manual que no está documentado en el error
- No hay un estado claro de "ok, ya entendí"
```

### 7b. Como StressTestDoc (el hijo — versión completa)

El mismo st-01 con la dimensión UX que hoy está suelta en `## Puntos de estrés` y en la tabla del README:

```yaml
id: st-01
title: Fresh start orientation stress
based_on: UC-01
surface: atoms, graph, faq
emphasis: Orientación, primera impresión
tags:
- system:deskops
- kind:ux-stress
- status:active
provenance: desk/drawer/stress-tests/st-01-fresh-start-orientation.md
---

# Fresh start orientation stress

## Purpose

Estresar la orientación de un recién llegado: `about`, `faq`, `atoms list/show` y `graph build/neighbors` en un desk recién clonado.

## Setup

```bash
git clone <repo> && cd <repo> && deskops init
```

## Script

```bash
deskops about
deskops faq
deskops faq --topic atoms
deskops atoms list --tag system:deskops
deskops atoms show atom-deskops
deskops graph build
deskops graph neighbors atom-deskops
```

## Stress Points

| Paso | Qué mirar |
|---|---|
| `about` | ¿Invita a seguir explorando o es un callejón sin salida? |
| `faq` | ¿Las preguntas coinciden con lo que un recién llegado se preguntaría? |
| `atoms list` | ¿La salida es scrolleable y agrupable? |
| `graph build` primera vez | ¿El error dice qué hacer o explota con traceback? |
| `graph neighbors` | ¿Dice "no hay conexiones" si no hay vecinos? |

## Failure Modes

- El usuario tiene que leer código fuente para entender qué hace deskops
- `about` y `faq` describen un mundo distinto al que `atoms list` muestra
- `graph build` requiere setup manual que no está documentado en el error
- No hay un estado claro de "ok, ya entendí"
```

## 8. Comandos exactos de registro (desde `hum-ecosystem/tools/deskops`)

```bash
cd /home/jp/proyectos/hum-ecosystem/tools/deskops

# 1. Crear deskops/models/test.py y deskops/models/stress_test.py
#    y exportar TestDoc, StressTestDoc en deskops/models/__init__.py

# 2. Registrar los dos modelos
sldb models add deskops.models:TestDoc --store .sldb --pythonpath .
sldb models add deskops.models:StressTestDoc --store .sldb --pythonpath .
sldb models show StressTestDoc --store .sldb --pythonpath .   # verificar base_models: [TestDoc]

# 3. Validar contratos y promover
sldb models validate StressTestDoc --promote --store .sldb --pythonpath .
sldb models validate TestDoc --promote --store .sldb --pythonpath .

# 4. Regenerar índices
sldb stores update --store .sldb --pythonpath .

# 5. Registrar la RelationTypeDoc del vínculo padre-hijo
sldb docs create --model RelationTypeDoc -o sldb/relation_types/specializes.md \
  --name reltype-specializes --store .sldb --pythonpath . <payload-specializes.yaml>

# 6. Afirmar la RelationDoc StressTestDoc -specializes-> TestDoc
sldb docs create --model RelationDoc -o desk/relations/specializes--StressTestDoc--TestDoc.md \
  --store .sldb --pythonpath . <payload-relation.yaml>

# 7. Migrar los 15 st-XX existentes (extract → adaptar payload → render → track)
sldb extract deskops.models:StressTestDoc desk/drawer/stress-tests/st-01-fresh-start-orientation.md /tmp/st-01.yaml --pythonpath .
# editar /tmp/st-01.yaml: añadir based_on, surface, emphasis, setup, stress_points
sldb render deskops.models:StressTestDoc /tmp/st-01.yaml desk/drawer/stress-tests/st-01-fresh-start-orientation.md --pythonpath .
sldb docs track desk/drawer/stress-tests/st-01-fresh-start-orientation.md --model StressTestDoc --store .sldb --pythonpath .

# loop equivalente para st-02..st-15:
for f in desk/drawer/stress-tests/st-*.md; do
  sldb docs track "$f" --model StressTestDoc --store .sldb --pythonpath .
done

# 8. Verificación
sldb validate deskops.models:StressTestDoc --input desk/drawer/stress-tests/st-01-fresh-start-orientation.md --pythonpath .
sldb find type.workflow.stress_test --in semantic --store .sldb --pythonpath .
sldb stores update --store .sldb --pythonpath .
deskops graph build
```

Alternativa para el paso 2: `deskops bootstrap` registra los modelos deskops en el store global; el registro local explícito con `sldb models add` es lo que genera `deskops/.sldb/core/models/*.yaml`.

## Alcance y exclusiones

- Objectivo: 15 `st-XX` → `StressTestDoc`; `TestDoc` queda como base instanciable para tests futuros no-UX (integración, CI).
- Los 6 meta-docs (`README`, `METHODOLOGY`, `FINDINGS_INDEX`, `ANCHORED_SUMMARY`, `COMPREHENSIVE_COVERAGE`, `PRIORITIZED_ROADMAP`) y `findings/` se quedan como markdown sin tipo; tiparlos sería otro modelo (p. ej. `StressReportDoc` / `FindingDoc`).
- No se modifica ningún repo: este documento es solo el diseño.