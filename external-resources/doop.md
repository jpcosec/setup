---
# Human-readable name of the resource
name: Doop
# Official docs or repository URL
page: https://github.com/plast-lab/doop
# true | false — whether the resource is installed locally
installed: false
# Local install path or install command; set when installed is true
install_path: null
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:doop
- layer:cli
- topic:static-analysis
---

# Doop

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Declarative framework for Java pointer and taint analysis (P/Taint) expressed as Datalog rules; runs on Souffle (default, tested 2.1) or legacy LogicBlox/PA-Datalog. Java 17+; supports jar inputs (local, URL, Maven coordinates) and Android APKs (android_N_V platforms). Also usable as a library via JitPack (com.github.plast-lab:Doop).

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

Not installed. Invocation only from its home directory: ./doop -a <analysis> -i <jar-or-apk> --platform java_25|android_25_fulljars; needs a Souffle build and DOOP_PLATFORMS_LIB JREs directory for platforms.

## Status

_How it is currently working; keep empty when not installed._



## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._
