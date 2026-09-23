---
id: atom-any-repo-can-declare-structured-doc-models
title: Any Repo Can Declare StructuredDoc Models
five_wh_one_plus: how
tags:
- system:sldb
- system:setup
- layer:document-model
- topic:structurednldoc
---

# Any Repo Can Declare StructuredDoc Models

## Answer

Any repo — even one that is not a Python package — can declare its own StructuredNLDoc models in a local `models.py` and register them in its own store. Do not add your model to the deskops or sldb repos; declare it locally.

Full flow, as done for `ExternalResourceDoc` in /home/jp/setup:

1. **Declare** — write `/home/jp/setup/external-resources/models.py` with a class that subclasses `StructuredNLDoc` and defines `__semantics__` and `__template__`, exactly like the deskops models. Example: `class ExternalResourceDoc(StructuredNLDoc)` with `__semantics__ = {"type": ["external", "resource"], "workspace": ["external-resources"]}` and a Markdown `__template__` with `⸢rev•field⸥` placeholders.

2. **Add** — register it in the repo's store, telling sldb where to resolve the module from:
   ```bash
   sldb models add external-resources.models:ExternalResourceDoc --store .sldb --pythonpath .
   ```
   Result in `.sldb/core/store_index.yaml`:
   `model_ref: external-resources.models:ExternalResourceDoc`, `path: external-resources/models.py` (relative), plus a generated models index `.sldb/core/models/ExternalResourceDoc.yaml`.

3. **Validate & promote** — confirm the draft and promote it to the real model:
   ```bash
   sldb models validate ExternalResourceDoc --store .sldb --pythonpath . --promote
   ```

4. **Stores update** — after any model change, recompute store state so hashes stay consistent:
   ```bash
   sldb stores update
   ```

Key flags, verified against `sldb models add --help` and `sldb models validate --help`:

- `--store .sldb` — which store registers the model (use the current repo's store).
- `--pythonpath .` — the module search root that makes `external-resources.models` importable at registration/validation time.
- `--promote` — on validate, turns the draft into the canonical model definition.

Every flag must be passed together: `add` needs `--pythonpath` to find the module just like `validate` does. Forgetting `--pythonpath .` is the most common failure — sldb cannot import `external-resources.models` without it.