**REFORMULACION**

Contrato reformulado, no aprobado. Resultado: arranque reproducible de Scion con fuentes y worktree correctos, montajes en `/workspace` y ruta host real, autenticación Hub/CLI para bootstrap y tokens propios para hijos, y puente nativo de eventos Pi hacia el dialecto Claude de `sciontool`. Debe permitir un desk desechable autorizado, sin mensajes manuales, con ejecución hija, tester independiente, closeout y continuación.

Repos/superficie: DeskOps (`pi/scion`, tests, README y átomo) y workspace SLDB_1 como fixture. Se preservan Scion 0.2.21 y el fork Pi fijado; no se tocan secretos, continuidad de sesión ni agentes no relacionados.

Límites: sin `pi-subagents`, sin nuevo motor de workflow y sin tareas de producción en validación. Prohibido depender de wheels obsoletos, symlinks manuales, `secrets.env` montado, contenido de prompts/argumentos/credenciales en eventos, o tratar `agent_end` genérico como completado. El commit final de la rama fuente y el contrato JSON son salidas futuras de dependencia, no decisiones faltantes.

**AMBIGUEDADES**

Ninguna decisión operativa falta. El input ya fija `--root`, `--source-root`, `--sldb-root`, `--ref`, Hub por defecto y fixture. Cita: “its final commit is a future dependency output, not a missing operator decision”; “its final commit is a future dependency output, not a missing operator decision”. El commit probado se registrará tras el closeout de fuente; no debe convertirse en fallback silencioso.

**DRY-RUN**

Lecturas hipotéticas: tarea, referencias `18c0007`, tests, rama `fix/scion-autonomy`, configuración y átomo. Cambios hipotéticos: constantes/runtime en `start-desk.py`, recetas Scion, extensión/config de ciclo de vida, tests de bootstrap/puente, README y átomo. Validaciones: `pytest tests/test_scion_pi_runtime.py` y pruebas de bridge/bootstrap; ejecución real desechable con coordinador/ejecutor/tester; fallo transitorio y reintento; parada/reanudación sin duplicar hijo; un closeout por tarea.

**FUTURO**

Comprobar al implementar: imports reales antes de arrancar; rechazo temprano de ref inválida; worktree limpio y propiedad conocida sin resetear originales; montajes duales soportados; mapeo de eventos sin datos sensibles; refresco real de token propio sin logs; reconciliación de etiquetas/identidad; cero mensajes de seguimiento; identidades separadas ejecutor/tester; negativa correcta a cerrar tras fallo; recuperación y fase completada; registro del commit fuente y evidencia saneada.
