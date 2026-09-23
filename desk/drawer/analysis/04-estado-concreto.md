# 04 — Estado concreto del ecosistema (inventario verificable)

Fecha de medición: 2026-09-22. Método: solo lectura (`git log -1 --format=%cd` por repositorio, `git status --short --branch`, inspección de tests). Ningún archivo modificado.

## 1. Inventario por subproyecto

| Proyecto | Capa | Madurez | Último commit (git %cd) | Tests | Evidencia ruta |
|---|---|---|---|---|---|
| sldb | tooling | maduro | 2026-09-22 (repo propio, e91920f) | sí (19 ficheros) | tools/sldb/README.md, src/, tests/, docs/architecture/ |
| kgdb | tooling | legacy (congelado 09-20) | 2026-09-20 (repo propio) | sí (12) | tools/kgdb/README.md ("Absorbed by sldb", "hollow") |
| deskops | tooling | activo | 2026-09-09 (repo propio, main) | sí (273 casos; 268 ok / 5 fail) | tools/deskops/README.md, AGENTS.md, tests/ |
| spec2viz | tooling | activo | 2026-09-09 (repo propio, master) | sí (22) | tools/spec2viz/README.md, spec.md, tests/ |
| marcado | tooling | activo | 2026-09-21 (raíz a1541f8) | sí (10) | tools/marcado/README.md, schema/, tests/ |
| kbsurfaces | tooling | activo (delgado) | 2026-09-21 (raíz a1541f8) | no | tools/kbsurfaces/README.md, cli.py (6 ficheros) |
| iso-lab | tooling | activo (delgado) | 2026-09-21 (raíz a1541f8) | no | tools/iso-lab/README.md, manifest.yaml, docker/ |
| sldb-ui | ui | activo (delgado) | 2026-09-21 (raíz a1541f8) | no | tools/sldb-ui/README.md, package.json (Astro) |
| deskops-pron | tooling | activo (delgado) | 2026-09-20 (repo propio, rama deskops-pron) | sí (42 entradas en tests/) | tools/deskops-pron/README.md (mismos atoms que deskops), runs/, sldb/ |
| graph_ui | ui | activo pero con imports rotos (aviso 09-17) | 2026-09-22 (repo propio, master) | sí (23) | tools/graph_ui/README.md, AVISO-imports-rotos.md, src/ |
| ontomap | knowledge | activo | 2026-09-21 (raíz a1541f8) | sí (3) | tools/ontomap/README.md, converters/, ontology/, tests/ |
| repopackage | tooling | scaffolded (acciones 2026-05-20) | 2026-05-20 (repo propio, master) | sí (12) | tools/repopackage/README.md, compose.yaml, build/ |
| marcado-ui | ui | scaffolded/dormante | 2026-07-21 (repo propio, main) | no (playwright config) | tools/marcado-ui/README.md, package.json, dist/ |
| ontology | knowledge | scaffolded/dormante | 2026-05-19 (repo propio, master) | sí (2) | tools/ontology/README.md, pyproject.toml, tests/ |
| hum-scrapper | tooling | scaffolded/dormante | 2026-06-03 (repo propio, main) | sí (5) | tools/hum-scrapper/README.md, AGENTS.md, src/automation |
| tractatusIR | tooling | seed | 2026-09-21 (raíz a1541f8) | parcial (smoke lisp, sin pytest) | tools/tractatusIR/README.md, lisp/ (6), atomos/ (9) |
| knowledge | knowledge | legacy (congelado 09-07) | 2026-09-07 (repo propio, master) | no | tools/knowledge/README.md ("Congelado"), knowledge_legacy.py |
| hum | core | activo | 2026-09-21 (raíz a1541f8) | no | hum/README.md, pyproject.toml, agent/, workflow/, main.lisp |
| hum-core | core | activo | 2026-09-20 (repo propio, rama kgdb-ontology-split) | sí | hum-core/README.md, AGENTS.md, src/, tests/ |
| core/specyaml | core | scaffolded | 2026-09-21 (raíz a1541f8) | no | core/specyaml/README.md (formato semántico canónico) |
| core/code2specyaml | core | scaffolded | 2026-09-21 (raíz a1541f8) | sí | core/code2specyaml/spec.yml, tests/test_fixture_validation.py |
| core/knowledge | core | seed | 2026-09-21 (raíz a1541f8) | no | core/knowledge/README.md (organ index, 9 ficheros) |
| core/turn_extractor | core | seed | 2026-09-21 (raíz a1541f8) | no | core/turn_extractor/ (9 ficheros) |
| core/knowledge_tests | core | seed | 2026-09-21 (raíz a1541f8) | no | core/knowledge_tests/ (4 ficheros) |
| pilots/repopackage-core | core | seed | 2026-09-21 (raíz a1541f8) | no | pilots/repopackage-core/README.md, compose.yaml |

Nota: "(raíz a1541f8)" = el directorio no tiene `.git` propio; su último commit es el HEAD del repo raíz. Repos con `.git` propio: sldb, deskops, deskops-pron, graph_ui, hum-scrapper, kgdb, knowledge, marcado-ui, marcado_ui, ontology, repopackage, spec2viz, hum-core. Existe además `tools/marcado_ui/` (duplicado no solicitado, con `.git` propio).

## 2. Estado del repo raíz `/home/jp/proyectos/hum-ecosystem`

- Rama actual: **feature/weltgraph-spec-core**. HEAD: a1541f8 (2026-09-21 18:08, "kbsurfaces: descubrir y cambiar de KB sin reiniciar las UIs").
- `git status --short --branch` → **788 líneas**: 326 `??` (dirs colapsadas), 271 `M`, 190 `D`, 1 `m` (tools/ontology, repo anidado con contenido distinto del índice del raíz). 0 archivos staged. Confirma **migración masiva sin commitear**:
  - `.sldb` viejo borrado: 27 entradas `D` bajo `.sldb/` (documents/, models/, store_index.yaml) + `M semantic_index.yaml`; nuevo `.sldb/runtime/` y `.sldb/core/` sin trackear (73 entradas bajo `.sldb` con `--untracked-files=all`).
  - wikipu→hum: 31 líneas con "wikipu" (selfdocs concepts wikipu borrados, docs/architecture/WIKIPU_MIGRATION_MAP*.md borrados); `hum/` tiene 62 ficheros trazados en el raíz.
  - `tools/opsys` borrado: 1 entrada `D tools/opsys`; el directorio no existe en disco; aparece `?? desk/registry/repo-opsys.md`.
  - `tools/deskops` sin trackear salvo 8 heredados: el raíz traza 8 ficheros (7 `D` + 1 `M`) + 31 `??` = 39 líneas bajo esa ruta; el contenido vivo está en su repo anidado.

## 3. Submódulos y drift

- `.gitmodules` no existe → **0 submódulos declarados**.
- Los 13 repos anidados (`.git` propio) vs su upstream, medido con `rev-list --left-right --count upstream...HEAD`:
  - sldb: **adelante 21** (0 atrás) vs origin/main (HEAD e91920f, 2026-09-22).
  - hum-core: **adelante 1** vs origin/kgdb-ontology-split; 1 fichero modificado (`.skills/sldb/SKILL.md`).
  - deskops: 0/0 en sincronía, pero 1 mod local (`.gitignore`).
  - En sincronía 0/0: kgdb, spec2viz, hum-scrapper, repopackage, knowledge, marcado-ui.
  - Sin remote (no medible): graph_ui, ontology, deskops-pron.
  - El resto (tractatusIR, ontomap, marcado, kbsurfaces, iso-lab, sldb-ui, hum, core/*, pilots/*) no son repos: versionados por el raíz.

## 4. Estado del repo `/home/jp/setup`

- Rama: **main** (en sincronía con origin/main). HEAD: 2026-09-07 "fix(setup): initialize from DeskOps desk identity".
- `git status --short` → **17 líneas**: 4 `M` (README.md, desk/drawer/README.md, nvim/lazy-lock.json, wezterm/keybindings.lua), 13 `??` (`.pi/`, `herdr/coordination.sh`, `herdr/transcripts/`, `desk/registry/`, `desk/drawer/analysis/`, «desk/drawer/governance-herdr-proposal.md», «herdr-runtime-contract-gaps.md», «install-scripts-and-readme-findings.md», `.herdr-coordination.md`, `external-resources/`, `install/lazygit.sh`, `install/nvim.sh`, `herdr/coordination.sh.bak-20260917`). 0 staged. Este documento vive en una ruta untracked (`desk/drawer/analysis/`).

## 5. Estado del runtime deskops ↔ herdr

- `deskops runtime {init,status,attach,stop,supervise}`: implementado y verificado vía `--help`; módulos `deskops/runtime/initializer.py`, `runtime/herdr.py`, `runtime/supervise.py`, `operations.py`, `bootstrap.py`.
- Drift check: `python -m deskops drift check` → "No role-agent drift found.", exit 0.
- Suite de tests: **273 casos** en `tools/deskops` (`pytest --collect-only`), ejecución real `-q`: **268 ok, 5 FAIL**, en 95s. El número "252" no se reproduce hoy. Fallos visibles (2 de 5, tail truncado): `tests/test_model_templates.py::test_model_templates_roundtrip_with_instructional_text[InboxNoteDoc-payload7]` y `test_inbox_note_model_remains_backward_compatible_without_new_optional_fields`.
- `runs/subagents/index.jsonl`: **22 líneas**; `run_id` es null en las 22 (`grep -cv '"run_id": null'` → 0), `session_sha256` es null en 22/22; el campo `commit` sí está poblado en las filas visibles (tail).
- herdr: proceso vivo (`herdr` pid 6086; `herdr server` pid 6087, `~/.local/bin/herdr`); la tarea actual se ejecuta como dispatch de `herdr/coordination.sh` con `HERDR_TRANSCRIPT=/tmp/h-d5.md`; existe backup `coordination.sh.bak-20260917`.

## Foto en una frase

1. El ecosistema está a medio migrar, sin commitear: 788 líneas de status en `feature/weltgraph-spec-core` (326 untracked, 271 M, 190 D).
2. sldb es el único entregable maduro y activo (HEAD 2026-09-22, +21 commits sobre origin, ya absorbió kgdb).
3. deskops es el harness vivo, pero su suite no está verde: 268/273 con 5 fallos en test_model_templates; el runtime herdr sí está completo y operativo.
4. La capa de conocimiento (ontomap, marcado, kbsurfaces, iso-lab) está commiteada en el raíz y activa; kgdb y knowledge están congelados.
5. Todo el trabajo operativo reciente (herdr, registry, análisis, instaladores) vive sin trackear en /home/jp/setup sobre main.