## REFORMULACION

Encargo ejecutable `task.code`: hacer reproducible el arranque de Scion 0.2.21 con el fork Pi fijado (`e9ba9e2…`) para que un desk desechable y autorizado funcione sin intervención manual: worktree limpio y deduplicado, raíces de import explícitas, bridge nativo Pi→eventos Claude de sciontool, refresco de tokens propio, etiquetas/identidad reconciliadas, y un bucle hijo-ejecutor/tester independiente con cierre por tarea. Resultado: código en `pi/scion/*`, tests, docs, átomo y evidencia saneada commiteados. Repo: desk del workspace, raíz de fixture `/mnt/ssd/proyectos/SLDB_1/.tmp/scion-autonomy-lab`, fuente `deskops-runtime`. Límites: conservar Scion/Pi fijados, secretos, continuidad de sesión y agentes ajenos; sin `pi-subagents` ni motor de workflow nuevo; no despachar tareas de producción ni declarar éxito por contenedor vivo.

## AMBIGUEDADES

1. «start-desk.py accepts explicit desk/source/ref/project/workspace/agent options» — solo se nombran `--root`, `--source-root`, `--sldb-root`, `--ref`, `--context-file`; habría que inventar los nombres del resto.
2. «via supported Scion volumes» — obliga a inventar la sintaxis de volúmenes de Scion 0.2.21 para montar `/workspace` y la ruta host.
3. «maps input/session/agent/tool events to existing sciontool hook Claude dialect events» — sin tabla de correspondencia; obliga a inventar qué evento Pi produce qué hook.
4. «Reuse sciontool metadata proactive token refresh» — no se cita el esquema de metadatos; obliga a inventar campos y condición de refresco.
5. «two bounded code tasks with explicit expected functions/tests» — solo se fijan `greet`/`farewell`; contenido exacto de tests y payload queda a inventar.
6. «A validation command has one deterministic transient failure» — no se especifica el comando ni el fallo; obliga a inventarlo.
7. «Register source atom before docs» — el átomo se referencia pero no se transcribe su contenido/estado.

## DRY-RUN

Lecturas: TaskDoc, `acceptance-v2.json`, ambos tests, átomo, y los diez ficheros de `pi/scion` más `pi/README.md`. Cambios previstos: constantes en `launch.py`/`provision.py`, opciones y validación de ref en `start-desk.py`, mapeo en `scion-events.ts`, config en `harness-config.yaml`, `Dockerfile`, READMEs y tests. Dependencias: commit final de `fix/scion-autonomy` (context-file y contrato de tester), binario Scion 0.2.21, fork Pi, Hub `127.0.0.1:8080`, pytest. Validaciones futuras: `git rev-parse --verify` antes de mutar; verificar imports reales; pytest de runtime y bridge; ciclo real coordinador/ejecutor/tester con fallo inyectado, stop/resume, sin duplicar hijo; restaurar sesión.

## FUTURO

Otro nodo aporta el commit final de `fix/scion-autonomy` (interfaz `--context-file` y contrato de tester independiente). Un humano aporta operador/credenciales Hub y aprueba la evidencia de integración.
