# 06 — Runbook: cómo regenerar este análisis desde cero

Runbook reproducible para regenerar TODOS los documentos de `desk/drawer/analysis/` (00 a 06) usando workers de herdr. Nada de este runbook depende de memoria de chat: depende de comandos, evidencia en el repo y prompts literales.

## Prerrequisitos

- herdr server corriendo: `herdr agent list` responde sin error.
- deskops en PATH: `which deskops` → `/home/jp/anaconda3/bin/deskops`.
- Worker `pi` disponible. Modelo recomendado: `~deepseek/deepseek-v4-flash-latest` vía openrouter (barato y suficiente para redactar informes legibles).
- `HERDR_TRANSCRIPT` por worker (ver abajo): evita corrupción por escrituras concurrentes sobre `./.herdr-coordination.md`.
- No commits, no `git add`: los informes quedan como borradores en el drawer.

## 1. Recopilar evidencia (antes de despachar)

```bash
cd /home/jp/setup
git status --short                      # árbol sucio/limpio, qué hay sin trackear
deskops --help                          # lista de subcomandos
for s in status doctor drift graph runtime atoms repo desk; do echo "== $s =="; deskops "$s" --help 2>&1; done
ls desk/ desk/drawer/ desk/tasks/ desk/routines/ desk/atoms/ 2>/dev/null
tail -n 5 desk/runs/subagents/index.jsonl 2>/dev/null  # log de ejecuciones; si no existe, anótalo como hallazgo (ver prompt 04)
```

## 2. Spawn de workers

Un spawn por documento (6): repite con `pi-01`…`pi-06` y verifica con `bash /home/jp/setup/herdr/coordination.sh agents`. Usa ese nombre en el dispatch.

```bash
bash /home/jp/setup/herdr/coordination.sh spawn pi pi-01 /home/jp/setup --provider openrouter --model '~deepseek/deepseek-v4-flash-latest'
```

## 3. Dispatch con transcript por worker

Plantilla (cambia `NN` por `01`…`06` y `pi-NN` por tu worker):

```bash
export HERDR_TRANSCRIPT=/tmp/analysis-NN.md
bash /home/jp/setup/herdr/coordination.sh dispatch pi-NN "$TEXTO"
```

Cada worker escribe en su propio `/tmp/analysis-NN.md`, así las escrituras concurrentes no se pisan entre sí.

### Prompt 01 — deskops subutilizado

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-01 "$(cat <<'PI_EOF_01'
Eres un auditador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Estás en un worktree/checkout que NO debes modificar: lee y escribe solo en desk/drawer/analysis/. No hagas commits ni git add.
Investiga qué partes de deskops están subutilizadas en el repo setup (y en el ecosistema hum-ecosystem si es relevante). Evidencia mínima: salida de `deskops --help`, subcomandos que el repo no usa (graph, drift, materialize, closeout, runtime, inbox…), y revisa herdr/coordination.sh, herdr/transcripts/, desk/runtime.yaml, desk/drawer/*.md.
Escribe ESPAÑOL, informativo y concreto, en desk/drawer/analysis/01-deskops-subutilizado.md (máx. 90 líneas; foco en hechos y ejemplos citando rutas exactas; sin relleno). Cita cada ruta que afirmes; si una afirmación no proviene de un archivo leído, descártala.
Responde solo: "LISTO" tras escribir el archivo.
PI_EOF_01
)"
```

### Prompt 02 — limitaciones de deskops

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-02 "$(cat <<'PI_EOF_02'
Eres un auditador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Solo lectura; escribe únicamente en desk/drawer/analysis/. Nada de commits ni git add.
Identifica las limitaciones actuales de deskops (herramienta, capa de workflow del ecosistema). Evidencia mínima: `deskops --help` (solo 1 subcomando por invocación visible en help), doctor, drift, status; lee también desk/runtime.yaml, herdr/coordination.sh, herdr/init_opsys.py y desk/drawer/herdr-runtime-contract-gaps.md. Especifica qué le falta a deskops para gobernar el workflow de setup vía repo/CLI (falta de runbook propio, acoplamiento con runtime herdr, ausencia de logs de ejecución, etc.).
Escribe ESPAÑOL, en desk/drawer/analysis/02-deskops-limitaciones.md (máx. 90 líneas). Cada limitación con ruta citada como evidencia; sin afirmaciones sin fuente. Al terminar, responde solo: "LISTO".
PI_EOF_02
)"
```
### Prompt 03 — integración deskops–herdr

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-03 "$(cat <<'PI_EOF_03'
Eres un auditador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Solo lectura; escribe únicamente en desk/drawer/analysis/. Nada de commits ni git add.
Analiza cómo se integra (o debería integrarse) deskops con herdr en este repo: deskops = capa de workflow/control de tareas; herdr = runtime de agentes. Evidencia: herdr/coordination.sh, herdr/init_opsys.py, desk/runtime.yaml, deskops runtime --help, .herdr-coordination.md, herdr/transcripts/*.md. Señala solapamientos (init_opsys.py duplicando el initializer), contratos (runtime.yaml que nadie lee) y los puntos de unión reales (transcripts, agents, spawn/dispatch).
Escribe ESPAÑOL, en desk/drawer/analysis/03-integracion-deskops-herdr.md (máx. 90 líneas), con el diagrama de flujo en texto ASCII y rutas citadas. Al terminar, responde solo: "LISTO".
PI_EOF_03
)"
```
### Prompt 04 — estado concreto

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-04 "$(cat <<'PI_EOF_04'
Eres un auditador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Solo lectura; escribe únicamente en desk/drawer/analysis/. Nada de commits ni git add.
Documenta el estado CONCRETO del repositorio setup a la fecha de hoy (2026-09-22). Evidencia obligatoria: salida de `git status --short`, `deskops status`, `ls desk/ desk/drawer/ desk/tasks/ desk/routines/ desk/atoms/`, `tail -n 5 desk/runs/subagents/index.jsonl` (si el archivo no existe, decláralo: el repo no tiene log de subagentes; no inventes datos), y herdr/transcripts/ (nombres/fechas de transcript).
Escribe ESPAÑOL, en desk/drawer/analysis/04-estado-concreto.md (máx. 90 líneas): árbol de estado, artefactos presentes, transcript disponibles, huecos de información. Todo afirmado con la ruta exacta; si no lo observaste, no lo afirmes. Al terminar, responde solo: "LISTO".
PI_EOF_04
)"
```
### Prompt 05 — pendientes concretos

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-05 "$(cat <<'PI_EOF_05'
Eres un planificador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Solo lectura; escribe únicamente en desk/drawer/analysis/. Nada de commits ni git add.
A partir de la evidencia del repo, lista los pendientes concretos del ecosistema (setup y hum-ecosystem) para que deskops gobierne el workflow vía repos/CLI y herdr como runtime. Fuentes: desk/drawer/*.md (governance-herdr-proposal.md, herdr-runtime-contract-gaps.md, install-scripts-and-readme-findings.md), herdr/coordination.sh, desk/runtime.yaml, deskops --help. Cada pendiente: qué es, dónde duele (ruta), y qué acción mínima lo resolvería. Ordena por impacto.
Escribe ESPAÑOL, en desk/drawer/analysis/05-pendientes-concretos.md (máx. 90 líneas). Sin pendientes inventados; si una fuente no respalda un ítem, sácalo. Al terminar, responde solo: "LISTO".
PI_EOF_05
)"
```
### Prompt 06 — este runbook

```bash
bash /home/jp/setup/herdr/coordination.sh dispatch pi-06 "$(cat <<'PI_EOF_06'
Eres un documentador del ecosistema hum-ecosystem. CWD: /home/jp/setup. Solo lectura; escribe únicamente en desk/drawer/analysis/. Nada de commits ni git add.
Redacta el runbook reproducible para regenerar TODO el análisis de desk/drawer/analysis/ desde cero con subagentes herdr. Contenido obligatorio: prerrequisitos (herdr corriendo, `which deskops`, modelo worker `~deepseek/deepseek-v4-flash-latest`); comandos exactos de spawn con `bash /home/jp/setup/herdr/coordination.sh spawn pi <cwd> --provider openrouter --model '~deepseek/deepseek-v4-flash-latest'`; comandos de dispatch con HERDR_TRANSCRIPT=/tmp/<n>.md por worker (evita corrupción por escrituras concurrentes); comandos de recolección de evidencia previos (deskops --help por subcomando, git status, ls de desks, tail de runs/subagents/index.jsonl); los 6 prompts literales de los 6 documentos; limpieza con `bash /home/jp/setup/herdr/coordination.sh workers-close`; sección "Cuando re-ejecutar esto" (tras cerrar una fase, tras tocar runtime/, tras migraciones grandes); y una nota honesta: los workers son modelos baratos y hay que verificar sus afirmaciones contra las rutas citadas.
Escribe ESPAÑOL, en desk/drawer/analysis/06-como-regenerar-este-analisis.md (máx. 120 líneas). Al terminar, responde solo: "LISTO".
PI_EOF_06
)"
```
## 4. Revisión y limpieza

```bash
wc -l desk/drawer/analysis/0*.md && grep -nE "deskops|runtime.yaml" desk/drawer/analysis/0*.md | head -20
bash /home/jp/setup/herdr/coordination.sh workers-close  # cierra la pestaña de workers completa
```

## 5. Cuando re-ejecutar esto

- Tras cerrar una fase de trabajo en el ecosistema (04/05 deben reflejar el estado nuevo), o si editas un documento del análisis a mano y quieres comparar con la versión regenerada.
- Después de tocar `runtime/`/`desk/runtime.yaml` o tras migraciones grandes (tooling nueva, reorg de `herdr/`, cambios en el CLI de deskops): re-ejecutar 02/03 (contrato) y 04/05 (estado).

## 6. Nota honesta

Los workers usados aquí son modelos baratos (`deepseek-v4-flash` vía openrouter) promovidos para redactar informes legibles, no para razonar con precisión total. CADA afirmación debe verificarse contra la ruta citada antes de actuar: abre el archivo, confirma la línea, descarta lo que no cuadre. Si un prompt exige un dato que el worker no pudo observar (p. ej. `runs/subagents/index.jsonl` inexistente), el worker debe DECIRLO, no inventarlo.
