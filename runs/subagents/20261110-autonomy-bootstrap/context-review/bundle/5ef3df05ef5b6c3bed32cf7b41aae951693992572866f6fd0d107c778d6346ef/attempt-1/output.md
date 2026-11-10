## REFORMULACIÓN
**Resultado:** entregar un arranque reproducible de Scion que use el desk/tools vigentes, rutas de worktree válidas y un puente nativo de eventos Pi→sciontool, de modo que un desk desechable autorizado ejecute sin mensajes manuales: asignación inicial única, despacho de hijo, prueba independiente, cierre/commit y continuación. Debe incluir receta ejecutable, configuración durable, pruebas, documentación y átomo; no solo un informe.

**Repo:** `setup`, según `README.md` (“Personal runtime setup”). Superficie declarada: `pi/scion/*`, `tests/test_scion_pi_runtime.py`, `tests/test_scion_autonomy.py` y `desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md`.

**Límites:** preservar Scion 0.2.21, Pi fork `jpcosec/pi-mono` en `e9ba9e2ebce1b49dca85ab20007038c06e486ea5`, secretos por proyecto, continuidad de sesión y agentes no relacionados. Sin `pi-subagents` ni nuevo motor de workflow. No despachar tareas de producción durante validación. La autoridad de tarea/validación/cierre sigue en DeskOps/SLDB; Scion mantiene supervisión. No declarar éxito solo porque el contenedor corre.

## AMBIGÜEDADES
- Falta decidir la política concreta de “current isolated desk/source revision” y la convención de rutas Git, porque solo se pide: “Make startup choose/configure a current isolated desk/source revision” y “expose consistent Git worktree paths”.
- Faltan valores o fuente de verdad para proyecto/auth/workspace hijo y plantillas tester; el contrato solo dice “Configure explicit child project/auth/workspace and fresh tester templates”.
- No se define el mecanismo/cadencia de refresco de token, aunque se exige “Validate … token refresh behavior”.
- No se especifica el fixture de “bounded tasks” ni el criterio observable de “no duplicate child” tras reinicio.

## DRY-RUN
**Lecturas hipotéticas:** contrato del drawer, tarea, board, rituals, pills, `pi/README.md`, receta `pi/scion/README.md`, `launch.py`, `harness-config.yaml`, `Dockerfile`, hooks de estado/dialecto y tipos de extensión Pi.
**Cambios hipotéticos:** implementar/ajustar `scion-events.ts` para mapear eventos nativos Pi a hooks existentes; separar actividad, retorno a idle y cierre DeskOps; corregir selección de fuente/rutas en bootstrap/launch/config; fijar proyecto/auth/workspace y plantillas; actualizar pruebas, documentación y átomo.
**Validaciones hipotéticas:** ejecutar `pytest tests/test_scion_pi_runtime.py` y pruebas de puente/bootstrap; verificar arranque limpio, fallo controlado, restart sin duplicado y flujo completo en desk desechable con un solo prompt inicial.

## FUTURO
Comprobar implementación: commit/fork y versión reales; imports desde fuentes previstas, no wheels obsoletos; `cwd` y sesión Pi preservados; eventos no confunden `agent_end` con closeout; actividad se limpia/actualiza correctamente; secretos no aparecen en Git, argumentos ni imagen; ausencia de `pi-subagents`; idempotencia tras restart; evidencia y docs exactos commiteados. No apruebo el contrato: faltan las decisiones citadas.
