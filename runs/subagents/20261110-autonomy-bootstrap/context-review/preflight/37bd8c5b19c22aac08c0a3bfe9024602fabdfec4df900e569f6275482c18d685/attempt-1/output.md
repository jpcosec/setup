## REFORMULACION

Contrato: tarea `task-scion-autonomy-runtime-bootstrap-and-pi-lifecycle-bridge`, estado `draft`, tipo `task.code`, nodo `ritual-execution`, sin `depends_on`, sin átomos, `inherit_acceptance_context: false`; proviene de `desk/drawer/tasks/task-scion-autonomy-runtime-bootstrap.md`.

Resultado exigido: arranque reproducible de Scion usando desk/tools vigentes, rutas de worktree válidas y puente nativo de eventos Pi, para que un desk desechable autorizado ejecute sin prompts manuales: ejecución hija, test independiente y cierre/continuación.

Alcance: recetas runtime en `setup/pi/scion`, extensión/config de ciclo de vida, binding de fuente/raíz, tests, docs y átomo. Debe preservar Scion 0.2.21, fork Pi fijado, secretos, continuidad de sesión y agentes no relacionados. Excluye `pi-subagents`, nuevo motor de workflow y despacho de tareas productivas en validación.

Superficie declarada: `pi/scion/{Dockerfile,harness-config.yaml,launch.py,provision.py,scion-events.ts,start-desk.py,README.md}`, `pi/README.md`, `tests/test_scion_pi_runtime.py`, `tests/test_scion_autonomy.py`, átomo de bootstrap; referencias `18c0007` y ambos tests.

Ruta: leer contrato del drawer y auditorías; preflight/revisión en frío; conectar eventos nativos Pi a hooks existentes de sciontool; corregir configuración de fuente/bootstrap; fijar proyecto/auth/workspace hijo y refresco de token; integrar contrato DeskOps desde `fix/scion-autonomy`; validar un único prompt inicial de coordinador sin mensajes posteriores en desk desechable, más fallo hijo controlado, reinicio y ausencia de despacho duplicado.

Cierre: estado runtime refleja trabajo real; arranque limpio usa fuente y rutas Git correctas; bucle desechable desatendido pasa; docs fuente y evidencia exacta quedan commiteadas. No basta un contenedor corriendo.

## AMBIGUEDADES

- `summary: ''` y `Rationale: Not provided`: falta el motivo/driver que permita evaluar prioridad, aunque el Goal sí define el resultado.
- “Preserve Scion0.2.21 and pinned Pi fork”: no se identifica el commit/tag exacto del fork Pi.
- “correct current-source/bootstrap path config” y “correct source and Git paths”: no se declaran rutas canónicas ni criterio observable de corrección.
- “explicit child project/auth/workspace and token refresh”: no se define fuente de auth, formato de workspace ni disparador/validez del refresco.

## DRY-RUN

Lecturas hipotéticas: tarea, drawer origen, referencias `18c0007`, tests, átomo y archivos listados; sin ejecutar comandos. Cambios hipotéticos: puente de eventos, configuración de bootstrap, rutas fuente/Git, provisión/auth hijo, refresco de token, integración DeskOps, tests/docs/átomo. Validaciones hipotéticas: `pytest tests/test_scion_pi_runtime.py tests/test_scion_autonomy.py` y pruebas bridge/bootstrap; desk desechable con un solo prompt; fallo hijo controlado; reinicio con sesión preservada y sin duplicado; commit de evidencia. No se despacharán tareas productivas.

## FUTURO

Comprobar al implementar: mapeo e idempotencia de eventos, expiración/refresco de token, resolución real de worktrees, continuidad de sesión, ausencia de doble despacho, evidencia reproducible y ausencia de secretos. No confundir estas comprobaciones con decisiones aún ausentes. No apruebo: el contrato sigue en `draft`.
