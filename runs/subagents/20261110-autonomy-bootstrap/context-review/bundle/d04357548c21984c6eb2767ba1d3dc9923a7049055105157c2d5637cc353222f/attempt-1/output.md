## REFORMULACIÓN

**Resultado:** implementar en `setup` el arranque reproducible de Scion/Pi y el puente nativo de eventos Pi→sciontool. El resultado debe permitir que un desk desechable y autorizado ejecute, sin mensajes manuales del padre, el ciclo completo: asignación inicial única → hijo ejecutor → prueba independiente → cierre/continuación, con evidencia sanitizada y sin despachar tareas de producción durante la validación.

**Repo:** `setup`; workspace `desk`; tarea `task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge`. Superficies previstas: `pi/scion/start-desk.py`, `launch.py`, `provision.py`, `scion-events.ts`, `Dockerfile`, `harness-config.yaml`, READMEs, tests `test_scion_pi_runtime.py`/`test_scion_autonomy.py` y el átomo indicado.

**Límites citados:** preservar Scion `0.2.21` y Pi `jpcosec/pi-mono` en `e9ba9e2ebce1b49dca85ab20007038c06e486ea5`; secretos vía Hub/proyecto, nunca `secrets.env` montado; continuidad de sesión; sin `pi-subagents` ni nuevo motor de workflow; “Do not dispatch production tasks in validation”; no reescribir `origin` ni hacer fallback silencioso de `--ref`; no usar symlinks manuales; no considerar `agent_end` como cierre DeskOps; no registrar prompts, argumentos de herramienta ni credenciales.

## AMBIGÜEDADES

Ninguna decisión de operador falta en el input. El commit final de `--context-file` se declara expresamente como salida futura de la tarea fuente, no como decisión pendiente: “its final commit is a future dependency output, not a missing operator decision”. El fallo transitorio determinista y el stop/resume ya están acotados por el fixture.

## DRY-RUN

**Lecturas hipotéticas:** tarea, board, rituales, READMEs, código Scion/Pi entregado, tarea fuente del contrato coordinador/tester y tipos de extensión Pi.

**Cambios hipotéticos:** añadir opciones explícitas a `start-desk.py` con validación previa a mutaciones; seleccionar/reutilizar worktree limpio con propiedad conocida; montar workspace en `/workspace` y ruta host real; fijar `PYTHONPATH` a DeskOps y SLDB y verificar imports reales; mapear eventos Pi a dialecto Claude sin contenido sensible; conservar refresh proactivo de token propio; reconciliar etiquetas/identidad de run antes de arrancar; añadir pruebas y documentación/átomo.

**Validaciones hipotéticas:** `pytest` de ambos archivos y pruebas de puente/bootstrap; arranque real con coordinador/ejecutor/tester frescos; dos tareas con dependencia y aserciones pytest; fallo controlado sin cierre, reintento válido, stop/resume sin hijo duplicado; un cierre por tarea; avance de fase; evidencia sanitizada y commit.

## FUTURO

Comprobar al implementar: que los comandos exactos funcionen con `--root`, `--source-root`, `--sldb-root`, `--ref`, `--project`, `--workspace`, `--agent`; que el worktree no resetee originales sucios; que el montaje use volúmenes soportados; que los imports provengan de las fuentes pretendidas y no de wheels obsoletas; que el refresh sea del propio agente y no registre tokens; que las etiquetas permitan reconciliación estable; que el fixture demuestre fallo, recuperación, tester independiente y ausencia de duplicados; y que el cierre no se infiera por contenedor activo ni por `agent_end`.
