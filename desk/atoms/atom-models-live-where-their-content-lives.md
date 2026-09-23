---
id: atom-models-live-where-their-content-lives
title: Models Live Where Their Content Lives
five_wh_one_plus: where
tags:
- system:sldb
- system:setup
- layer:document-model
- topic:structurednldoc
---

# Models Live Where Their Content Lives

## Answer

A StructuredNLDoc type is declared in the repo that owns the content that type describes, not in the repo of the tool that processes it. The store entry is only a pointer to that declaration; it never moves the model into the tool's codebase.

Real example in /home/jp/setup: `.sldb/core/store_index.yaml` registers 16 models from the deskops tool repo with absolute paths (e.g. `deskops.models:TaskDoc` → `/home/jp/proyectos/hum-ecosystem/tools/deskops/deskops/models/task.py`), but one model breaks the pattern:

- `model_ref: external-resources.models:ExternalResourceDoc`
- `path: external-resources/models.py` (relative to setup)

`ExternalResourceDoc` describes fichas of external tools/skills/services used by setup — that content belongs to setup, so the model lives in `/home/jp/setup/external-resources/models.py`, not in deskops. If that model had been declared in the deskops repo, deskops would own content it does not maintain.

Rule of thumb for an agent: look at where the **content** the model describes is authored. If the content lives in repo A, the model must be importable from repo A's own source tree and registered in repo A's `.sldb` store. The tool's models live in the tool's repo; your models live in your repo.

How to detect the split in a store: `sldb models list` shows `model_ref` plus `path`. A path relative to the current repo (like `external-resources/models.py`) means the model is locally declared; an absolute path pointing at another repo (like `/home/jp/proyectos/hum-ecosystem/tools/deskops/...`) means it is borrowed from that tool's codebase.