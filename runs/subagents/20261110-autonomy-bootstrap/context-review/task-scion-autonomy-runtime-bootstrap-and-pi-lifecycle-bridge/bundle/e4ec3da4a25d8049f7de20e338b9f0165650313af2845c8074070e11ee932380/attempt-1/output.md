REFORMULACION
- Propósito: hacer reproducible y fail-closed el arranque autónomo de Scion con fuentes DeskOps/SLDB vigentes, worktree propio y puente nativo de eventos Pi, sin prompts manuales.
- Resultado: `start-desk.py` valida rutas/ref/procedencia, crea o reutiliza worktree limpio, materializa plantillas y reconcilia coordinadora; `scion-events.ts` traduce eventos Pi al dialecto Claude sin filtrar contenido; tests, docs y átomo.
- Repo: `/home/robocop/setup`; superficie `pi/scion/*`, `tests/test_scion_*.py`, `desk/atoms/...` y TaskDoc.
- Límites: Scion 0.2.21 y fork Pi fijado; sin `pi-subagents` ni motor nuevo; no despachar tareas de producción; preservar secretos, sesiones y agentes ajenos; no resetear originales ni usar symlinks.

AMBIGUEDADES
1. “project sldb-1 UUID b0899ed7-…” frente a “--project d7d9d3cd-…” y “scion-autonomy-lab__d7d9d3cd” del README. Obligaría a inventar qué proyecto usar en la integración real.
2. “pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests”: no nombra el archivo exacto de bridge/bootstrap. Obligaría a decidir si es `tests/test_scion_autonomy.py` y si el skip por Node <22 es aceptable.
3. “Automated fixture may inject…” frente a “fixture has one deterministic transient failure”. Obligaría a decidir si la inyección de fallo es obligatoria o solo posible.

DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, átomo y archivos listados en `files`. Cambios previstos: ajustar bootstrap/launcher/bridge/provisión/config/Dockerfile/README, tests y registrar átomo. Dependencias: fuente DeskOps con `--context-file` y modo tester; fork Pi; Scion 0.2.21; Node 22; Hub/credencial y desk desechable. Validaciones futuras: pytest de runtime y autonomía, prueba real de coordinador/ejecutor/tester, stop/resume sin duplicados y evidencia sanitizada. Sin ejecutar nada.

FUTURO
Otro nodo produce el commit final de DeskOps en `fix/scion-autonomy` y la interfaz `--context-file`; un humano aporta el fixture autorizado, proyecto/credenciales y aprueba la evidencia de integración. Son insumos, no decisiones de este nodo.
