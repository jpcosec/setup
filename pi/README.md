# Pi y Scion

Decisión acordada con JP el 2026-11-09.

## Contrato de ejecución

- Scion crea, aísla y coordina agentes, su comunicación y sus sesiones.
- Pi ejecuta la tarea de cada agente como harness de Scion.
- DeepSeek es el proveedor del modelo de Pi; no es una capa de orquestación.
- DeskOps/SLDB conservan la autoridad sobre tareas, validación, evidencia y cierre.
- Pi no carga `pi-subagents`: no se anida otra orquestación dentro de Scion.

## Procedencia de Pi

El Pi del host y el de la imagen de Scion deben compilarse desde
<https://github.com/jpcosec/pi-mono>, fijando explícitamente el commit.
El commit observado al acordar esta decisión es
`e9ba9e2ebce1b49dca85ab20007038c06e486ea5` (versión declarada `0.67.3`).
No sustituirlo por paquetes publicados desde upstream ni ejecutar actualizaciones
automáticas que cambien esta procedencia. Las extensiones deben ser compatibles
con el fork; una incompatibilidad no autoriza migrar Pi a upstream.

## Estado operativo verificado: 2026-11-10

- Pi del host apunta al build del fork en `~/bin/pirate/pi-mono`, versión `0.67.3`.
  La instalación npm `@earendil-works/pi-coding-agent` se retiró.
- Scion conserva `v0.2.21`. Su harness `pi` usa `scion-pi-fork:e9ba9e2`, con el
  mismo fork/commit y herramientas DeskOps/SLDB sobre Python 3.12.
- El proyecto `sldb-1` tiene plantillas `deskops-executor` y `deskops-coordinator`
  generadas desde los roles de DeskOps. Preparar la coordinadora no la lanza.
  Scion admite otros harnesses; el contrato del fork aplica a los agentes Pi.
- `DEEPSEEK_API_KEY` se sincroniza desde `~/.pi/agent/secrets.env` al secreto del
  proyecto. Solo se entrega cuando el harness la necesita; no entra en Git,
  argumentos de proceso ni imagen.
- `pi-subagents` no está instalado en Pi del proyecto deskops ni en la imagen.
- El smoke real leyó el board mediante la CLI, recibió respuesta de DeepSeek y
  conservó la misma sesión y un dato posterior al arranque tras stop/resume.
  Los agentes de prueba quedaron detenidos. Veinte pruebas independientes pasaron.

Recetas, comandos y límites actuales: [Scion con Pi del fork](scion/README.md).
La supervisión `deskops runtime` sigue ligada a Herdr; no se implementó un
supervisor Scion nuevo ni la correlación avanzada de intentos con closeout.

Antecedentes: [evaluación de Scion](../desk/drawer/scion-reemplazo-herdr.md)
y [ficha histórica de Pi](../external-resources/pi.md). Sus descripciones de
instalación son históricas y deben contrastarse con este contrato y el host.

## Interfaz web de Scion en esta máquina

Corrección local del 2026-11-10: el binario `scion v0.2.21` no incluía assets web.
Se compiló únicamente la web desde `homebrew-scion/scion`, commit
`55b9930538a14efeb9bc746de410ee7b12155afe`, que coincide con el binario instalado.
Las fuentes y el build están en `~/scion-build/web-v0.2.21/`.

El servidor se inició como daemon en loopback, conservando Hub y Runtime Broker:

```bash
scion server start --enable-hub --enable-runtime-broker --enable-web \
  --dev-auth --auto-provide \
  --web-assets-dir "$HOME/scion-build/web-v0.2.21/web/dist/client"
```

La web se sirve en `http://127.0.0.1:8080`. Se verificaron respuestas HTTP 200
del HTML, `/assets/main.js` y `/auth/me`, y la ausencia del mensaje
`Web UI Not Available`. El binario de Scion conserva su versión.
`scion server restart` reutiliza los argumentos guardados por el daemon.
