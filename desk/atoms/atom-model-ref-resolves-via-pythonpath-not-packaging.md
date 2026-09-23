---
id: atom-model-ref-resolves-via-pythonpath-not-packaging
title: Model Ref Resolves via Pythonpath, Not Packaging
five_wh_one_plus: how
tags:
- system:sldb
- system:setup
- layer:document-model
- topic:structurednldoc
---

# Model Ref Resolves via Pythonpath, Not Packaging

## Answer

`model_ref` is resolved through `--pythonpath`, not through Python packaging. The store keeps only the reference (`model_ref`) and a memoized path, never the code. That is why a repo with no `pyproject.toml` — /home/jp/setup — can still have its own registered models.

How it works:

1. `sldb models add external-resources.models:ExternalResourceDoc --store .sldb --pythonpath .` tells sldb: find module `external-resources.models` by adding `.` (the repo root) to `sys.path`, then import the class. `--pythonpath` is the resolution mechanism; it plays the role that `pip install -e` + entry points would play in a packaged project.

2. The store then persists only declarative data: `model_ref: external-resources.models:ExternalResourceDoc`, `path: external-resources/models.py`, `version: 1`, semantics. After registration, sldb does not re-derive the class from packaging metadata; on later operations you repeat `--pythonpath .` so the import succeeds again from the same repo root.

Proof from /home/jp/setup:

- `.sldb/core/store_index.yaml` contains the `ExternalResourceDoc` entry above.
- `find . -name pyproject.toml` returns nothing (outside `.venv`), so setup is not a Python package and is not pip-installable.
- Yet `external-resources/models.py` imports cleanly because `from sldb import StructuredNLDoc` works from an installed sldb (on `PYTHONPATH`/site-packages) and the repo's own module resolves via the `--pythonpath .` flag.

Implications for an agent:

- A relative `path` in the store is relative to the repo holding the store, and is only informational — the importable truth is `model_ref` + `--pythonpath`.
- Never run `sldb models validate/add` on a repo-local model without `--pythonpath .`; the model_ref is a module path, not a PyPI name, and no `pip install` will ever make it importable.
- The 16 `deskops.models:*` entries in the same store also resolve this way, but their modules live in the deskops repo; the store records their absolute path because there is no relative route from setup to them.