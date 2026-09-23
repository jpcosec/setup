---
# Human-readable name of the resource
name: SLDB
# Official docs or repository URL
page: git@github.com:jpcosec/sldb.git
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/anaconda3/bin/sldb; repo /home/jp/proyectos/hum-ecosystem/tools/sldb
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:sldb
- layer:document-model
- topic:structured-docs
---

# SLDB

## Summary

_One paragraph: what this resource is and why it matters to this setup._

StructuredNLDoc infrastructure: model contracts, reversible Markdown markers, render/extract flows, and .sldb stores.

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Backs the .sldb store of this repo: 15 deskops models + ExternalResourceDoc registered; all fichas and desk docs tracked and indexed here.
CLI used for docs create/track, fields query (tags), stores update/check, model validate.
Owns document contracts only; deskops owns workflow logic.

## Status

_How it is currently working; keep empty when not installed._

CLI on PATH via anaconda env; store check passing.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._
