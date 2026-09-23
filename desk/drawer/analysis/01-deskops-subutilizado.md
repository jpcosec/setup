# Análisis 01: ¿Qué debería cubrir deskops y no estamos aprovechando?

Status: análisis — drawer, no promovido.
Fecha: 2026-09-22. Método: superficie CLI real (`deskops --help` + `--help` de los 22 subcomandos) contrastada contra dos desks: `tools/deskops/desk` y `setup/desk`. Todo verificado por inspección directa; lo no verificable se marca como tal.

## Verificaciones previas (hechas, no asumidas)

- Superficie real: 22 subcomandos (about doctor status faq bootstrap init inbox promote add edit bind next list show advance repo desk atoms graph materialize drift closeout runtime), con sub-subcomandos: `add` 16 tipos, `list/show` 16 tipos, `atoms` 13 ops, `advance task`, `closeout {commit,verify}`, `drift {check}`, `graph {build,neighbors,missing,reflect}`, `runtime {init,status,attach,stop,supervise}`, `desk {install,migrate}`, `repo {register,whoami}`, `promote inbox-to-drawer-task`.
- `setup/desk`: roles/, materializations/, faq/, inbox/ VACÍOS (0 archivos); 1 sola task en `status: draft` con `pills: []`; Board.md con Purpose/Notes en boilerplate; 3 hallazgos como markdown suelto en `desk/drawer/*.md` sin `drawer/tasks/` (no existen como drawer tasks).
- `runs/subagents/index.jsonl`: 22/22 filas con `run_id: null` y `session_sha256: null`; `closeout.py` escribe los trailers solo `if run_id:` → el gate de trazabilidad se salta en silencio. Gate de closeout = no-op confirmado.
- No verifiqué: opciones internas de `graph build`, `drift check`, `runtime supervise` (no consulté sus `--help`), ni el status de las 2 tasks activas del desk deskops.

## Tabla: capacidades vs uso real

| Capacidad deskops | Comando | Estado de uso | Evidencia (ruta concreta) | Qué ganaríamos al adoptarla |
|---|---|---|---|---|
| Cierre trazable de tareas | `closeout verify` | sin usar (gate no-op) | `runs/subagents/index.jsonl`: 22/22 `run_id`/`session_sha256` null; `deskops/cli/commands/closeout.py:94` omite trailers sin `run_id` | Garantía real de que cada cierre tiene evidencia, commit y sesión; hoy el gate valida nada |
| Siguiente acción del workflow | `next` | parcial (solo deskops) | deskops: 31 `runs/subagents/*/next.txt`; setup: sin dir `runs/` ni uso | Reanudación de contexto cero sin re-leer el task; setup no explota la máquina de estados |
| Avance de tareas por gates | `advance task` | parcial | setup: task en `draft` con primitivas completas (checklists/conditions/edges/operators) nunca avanzada; deskops: muchas closeouts en git log | Ejecución guiada por gates en vez de edición manual de `current_node` |
| Vinculación de pills a tasks | `bind pill` | sin usar (setup) / parcial (deskops) | setup: `pills: []` en el task; deskops: 2 tasks con `pills:` pobladas, 2 hits en git log | El contexto de ejecución (pills ligadas) llega al subagente sin improvisación |
| Supervisión del runtime | `runtime supervise` | sin usar | deskops: `desk/runtimes/runtime-claude.md`, `runtime-pi.md` modelados pero supervise sigue en `drawer/features/feature-herdr-supervised-execution-runtime.md`; setup: `desk/runtime.yaml` "read by nobody" (hallazgo `drawer/herdr-runtime-contract-gaps.md`) | Ejecución real de agentes despachados, bloqueo/resolución y trazas; hoy herdr opera al margen del harness |
| Conocimiento durable en átomos | `atoms` | usado (deskops) / sin usar (setup) | deskops: 138 átomos en `desk/atoms/`; setup: solo `desk/atoms/tag-namespaces.yaml`, 0 átomos pese a tener `AtomDoc.yaml` en `.sldb/core/models/` | Los hallazgos de setup pasarían de markdown suelto a conocimiento destilado y consultable |
| Validación de enlaces del grafo | `graph missing` | parcial | deskops: snapshot construido (`.sldb/runtime/knowledge_graph.kg.json`, 26 hits git); setup: `.sldb/runtime/` sin snapshot KG, `semantic_dag.yaml` generado por sldb, no por deskops | Detección de referencias colgadas/dangling antes de que rompan la navegación de agentes |
| Materialización de roles | `materialize` | usado (deskops) / sin usar (setup) | deskops: `~/.pi/agent/agents/deskops-{executor,supervisor,tester}.md` instalados desde `desk/roles/`; setup: `desk/roles/` y `desk/materializations/` vacíos | Setup tendría agentes materializados específicos (ej. supervisor de su propio desk) en vez de solo los de deskops |
| Detección de deriva rol↔agente | `drift check` | parcial | deskops: 10 hits git, `desk/drawer/stress-tests/st-07-drift-check.md`, `use-cases/uc-07`; setup: sin roles → no aplica | Alertar cuando el rol fuente cambie y el agente instalado quede desincronizado |
| Captura de entradas cruzadas | `inbox` | usado (deskops) / sin usar (setup) | deskops: `desk/inbox/` con 5 notas y `desk/drawer/attention/` con 18; setup: `desk/inbox/` vacío | Triaje formal de sugerencias/hallazgos con `promote` en vez de drawer suelto a mano |
| Board como superficie de ruta | `list boards`/`show board` | parcial | Ambos: `tasks/Board.md` con Purpose y Notes en boilerplate (`_Explain what this board..._`), tasks listadas pero sin narrativa de ruta | Onboarding de agentes guiado por el board sin re-leer el repo entero |

## Hallazgos transversales

- El desk `setup` se creó con `deskops init` (modelos SLDB registrados, primitivas de la task generadas, `runtime.yaml` con layout herdr), pero nadie lo opera: ni advanca, ni cierra, ni materializa, ni enlaza.
- Los 3 hallazgos reales de setup (`governance-herdr-proposal.md`, `herdr-runtime-contract-gaps.md`, `install-scripts-and-readme-findings.md`) están fuera del ciclo: no son drawer tasks, no tienen `promote`, no generan tareas.
- El `desk/roles/` vacío de setup es la raíz de la mitad de los subusos: sin role docs no hay materialize, ni drift, ni runtime supervise de verdad.

## Top 5 adopciones de mayor retorno

1. **Arreglar el cierre**: cada cierre debe producir evidencia real. Comando: `deskops closeout verify --root . --task <task_id>` tras `deskops advance task <task_id>` (empezar por `task-centralizar-configuraciones-personales-en-setup` en `/home/jp/setup`).
2. **Activar `next` como reanudación**: comando: `deskops next task-centralizar-configuraciones-personales-en-setup --root /home/jp/setup` — devuelve la siguiente acción válida sin mutar.
3. **Poblar pills y avanzar la task de setup**: comando: `deskops bind pill task-centralizar-configuraciones-personales-en-setup <pill> --root /home/jp/setup` y luego `deskops advance task task-centralizar-configuraciones-personales-en-setup --root /home/jp/setup`.
4. **Convertir los 3 hallazgos en drawer tasks**: reescribir como `deskops add task --root /home/jp/setup --title "..." --goal "..." --scope "..." --validation "..."` y borrar el markdown suelto de `desk/drawer/` (raíz de pérdida de trazabilidad).
5. **Encender roles+materialize del desk setup**: comando: `deskops add materialization --root /home/jp/setup` para cada rol deseado y `deskops materialize --root /home/jp/setup`, seguido de `deskops drift check` en CI para detectar deriva.

## Precisión

- Todo lo de la tabla está verificado por inspección directa salvo los tres puntos marcados en "Verificaciones previas".
- El gate de closeout es un no-op verificado por código (`if run_id:` en `closeout.py:94`) + datos (22/22 null). Es la pérdida de mayor valor porque invalida la única garantía dura del ciclo.