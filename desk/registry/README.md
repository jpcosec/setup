# Registro de Repositorios del Usuario

Puesto de control de setup. Cada unidad de trabajo está **registrada por referencia** (repo-&lt;id&gt;.md en este directorio); setup no absorbe ni toca los proyectos.

Convención de status según último commit:
- **active** — commit en septiembre 2026
- **maintenance** — commit entre junio y agosto 2026
- **archived** — sin commit antes de junio 2026

## Personales — /home/jp/proyectos

| id | path | rama | último commit | status | desk | .sldb |
|---|---|---|---|---|---|---|
| hum-ecosystem | /home/jp/proyectos/hum-ecosystem | feature/weltgraph-spec-core | 2026-09-21 | active | yes | yes |
| matrix-shrdlu-spec | /home/jp/proyectos/matrix-shrdlu-spec | main | 2026-09-21 | active | no | no |
| pron | /home/jp/proyectos/pron | master | 2026-09-21 | active | no | yes |
| legos | /home/jp/proyectos/legos | master | 2026-09-20 | active | no | no |
| Matrix | /home/jp/proyectos/Matrix | master | 2026-09-20 | active | no | no |
| TraderBot | /home/jp/proyectos/TraderBot | master | 2026-09-20 | active | yes | yes |
| pron-plnr | /home/jp/proyectos/pron-plnr | plnr | 2026-09-18 | active | no | no |
| gemini-test | /home/jp/proyectos/gemini_test | dev | 2026-09-16 | active | yes | yes |
| mepu | /home/jp/proyectos/mepu | dev | 2026-09-08 | active | no | no |
| kimun | /home/jp/proyectos/kimun | main | 2026-09-07 | active | yes | yes |
| humble | /home/jp/proyectos/humble | master | 2026-06-07 | maintenance | yes | yes |

## AntonIA — /home/jp/AntonIA

| id | path | rama | último commit | status | desk | .sldb |
|---|---|---|---|---|---|---|
| antonia | /home/jp/AntonIA | knowledge_taxonomy | 2026-09-22 | active | yes | yes |
| antonia-aws-infra | /home/jp/AntonIA/repos/AWS_Infra | dev | 2026-09-22 | active | yes | yes |
| antonia-agentskbs | /home/jp/AntonIA/repos/AgentsKBs | dev | 2026-09-22 | active | no | no |
| antonia-mepu-ocs-dev | /home/jp/AntonIA/repos/mepu/mepu_ocs_dev | feat/homologacion-isp | 2026-09-16 | active | no | no |
| antonia-mepu-ocs | /home/jp/AntonIA/repos/mepu/mepu_ocs | master | 2026-09-15 | active | no | no |
| antonia-gian-repo | /home/jp/AntonIA/gian-repo | docs-teva | 2026-07-26 | maintenance | no | no |

## Notas

- Se registraron repos reales de nivel 1 en `proyectos/` y hasta depth 3 en `AntonIA/` (incluyendo `repos/`, `software/`, `projects/`).
- Duplicados no registrados: symlinks `AntonIA/software/kb-agent-runtime → proyectos/gemini_test` y `AntonIA/software/mepu-api/code → proyectos/mepu`; worktrees `AntonIA/repos/AWS_Infra_worktrees/*` y `proyectos/_worktrees/*`.
- Repos anidados dentro de `proyectos/hum-ecosystem/tools/` (sldb, deskops, kgdb, spec2viz, etc.) no se registraron por estar fuera del scope de nivel 1 de `proyectos/`.