## REFORMULACION

**Resultado:** contrato para un bootstrap reproducible del runtime de autonomía Scion y un puente nativo de eventos Pi, de modo que un desk desechable autorizado ejecute sin prompts manuales: ejecución hija, test independiente y closeout/continuación. El estado final debe reflejar trabajo real, no solo un contenedor en marcha.

**Repo/superficie:** `desk/tasks/...` con referencias `18c0007`, `tests/test_scion_autonomy.py`, `tests/test_scion_pi_runtime.py`; archivos en `pi/scion/` (Dockerfile, harness-config, launch, provision, scion-events.ts, start-desk, README), `pi/README.md`, tests y átomo `atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md`. Host declarado: `/mnt/ssd/proyectos/SLDB_1`.

**Límites:** preservar Scion 0.2.21, fork Pi `jpcosec/pi-mono e9ba9e2e...`, secretos, continuidad de sesión y agentes no relacionados; prohibido `pi-subagents` o nuevo motor de workflow; no despachar tareas de producción en validación; no cerrar por contenedor activo.

## AMBIGUEDADES

- “configured Hub” y “configured canonical ref (origin/main default)”: no se define dónde se configura ni valores exigidos. Cita: *“authenticates bootstrap through configured Hub”*; *“configured canonical ref (origin/main default)”*.
- “DeskOps task branch” no identifica rama/commit, pese a ser *“integration prerequisite”*. Cita: *“Independent tester mode/source contract comes from the DeskOps task branch”*.
- “bridge/bootstrap tests” no nombra archivos ni casos. Cita: *“pytest tests/test_scion_pi_runtime.py and bridge/bootstrap tests”*.
- Evidencia: no fija ruta, formato ni criterio de sanitización. Cita: *“save all sanitized integration evidence”*.
- Fixture: “may inject” deja opcional algo cuya evidencia de fallo/recuperación se exige. Cita: *“Automated fixture may inject one controlled validation/child failure and stop/resume”*.
- “two bounded code tasks” no define funciones, tests ni dependencia concreta. Cita: *“two bounded code tasks with explicit expected functions/tests and dependency”*.
- “zero followup messages” no define canal ni ventana de medición. Cita: *“one initial assignment and zero followup messages”*.

## DRY-RUN

**Lecturas hipotéticas:** `start-desk.py`, `provision.py`, `launch.py`, `scion-events.ts`, Dockerfile, harness-config, tests y READMEs; átomo fuente; referencias `18c0007`.

**Cambios hipotéticos:** constantes de runtime; opciones CLI explícitas; validación de rutas/provenance; selección de worktree limpio sin resetear originales; mounts en `/workspace` y ruta host absoluta; `PYTHONPATH` a fuentes testeadas; extensión Pi que mapea eventos sin contenido sensible; refresh proactivo de tokens; labels/run identity; fixture de fallo/reanudación; docs/átomo/evidencia.

**Validaciones hipotéticas:** pytest indicado y tests de puente; coordinador/executor/tester reales en desk desechable completan closeout y siguiente tarea sin mensajes; reinicio preserva sesión y no duplica hijo; evidencia de rechazo a cerrar en fallo, recuperación, tester independiente y un closeout por tarea.

## FUTURO

Comprobar implementación: imports reales antes de arrancar y ausencia de wheels obsoletos; refresh de token propio verificado sin logs; eventos sin prompts/argumentos/credenciales; `agent_end` genérico no tratado como completed; mounts efectivos; worktree reutilizado solo con ownership conocido; secretos no montados desde `secrets.env`; ninguna tarea de producción despachada; evidencia sanitizada y commit de docs/átomo.
