**REFORMULACION**

- **Resultado:** un arranque reproducible de Scion debe usar el desk/fuentes vigentes, worktrees válidos e imports verificados, y un puente nativo de eventos Pi hacia eventos existentes de `sciontool`, sin secretos ni contenido sensible, para que un desk desechable autorizado ejecute asignación inicial, hijo, prueba independiente y closeout/continuación sin mensajes manuales. Debe cubrir fallo controlado, reinicio sin hijo duplicado y evidencia sanitizada.
- **Repo:** `setup/pi/scion` (`launch.py`, `provision.py`, `start-desk.py`, Dockerfile, config, extensión, README), pruebas `tests/test_scion_pi_runtime.py` y `tests/test_scion_autonomy.py`, más docs y átomo fuente. La tarea DeskOps indicada es prerequisite de integración.
- **Límites:** preservar Scion 0.2.21, fork Pi `e9ba9e2...`, secretos, sesión y agentes no relacionados; no `pi-subagents`, no nuevo motor de workflow, no tareas de producción en validación.

**AMBIGUEDADES**

- No se define la identidad exacta para reconciliar antes de arrancar: “Stable coordinator/child labels and run identity reconcile before start.” Faltan nombres/campos canónicos de etiquetas y RunDoc/clave de identidad.
- No se define cómo ni cuándo inyectar el fallo: “Automated fixture may inject one controlled validation/child failure and stop/resume.” Falta el punto de inyección y el criterio observable de recuperación.
- La dependencia externa no queda fijada: “Independent tester mode/source contract comes from the DeskOps task branch and is an integration prerequisite.” Falta rama/commit/artefacto concreto y cómo demostrar que está integrado.

**DRY-RUN**

- **Lecturas hipotéticas:** tarea y drawdown, READMEs, `launch.py`, `harness-config.yaml`, Dockerfile, `status.go`, `claude.go`, `types.ts` y tarea DeskOps relacionada.
- **Cambios hipotéticos:** opciones explícitas y validación de procedencia en `start-desk.py`; worktree dedicado sin resetear originales; volúmenes y `PYTHONPATH`; extensión que traduzca input/session/agent/tool a dialecto Claude sin prompt/argumentos/credenciales; pruebas, docs y átomo.
- **Validaciones hipotéticas:** `pytest` de runtime/bootstrap/puente; arranque real con imports efectivos; ciclo desechable sin follow-ups; fallo controlado y recuperación; reinicio con sesión preservada y sin hijo duplicado; evidencia sanitizada.

**FUTURO**

Comprobar implementación real: imports no vienen de wheels obsoletas; rutas y volúmenes coinciden; worktrees sucios se preservan; el puente no filtra contenido ni convierte `agent_end` genérico en completed; refresh propio de token sin logs; no hay despacho de producción; la evidencia demuestra rechazo de closeout ante fallo. No apruebo el contrato: lo reformulo y mantengo estas reservas.
