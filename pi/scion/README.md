# Pi del fork en Scion

Estas recetas conservan Scion **0.2.21**. Pi host e imagen proceden de
[jpcosec/pi-mono](https://github.com/jpcosec/pi-mono), commit
`e9ba9e2ebce1b49dca85ab20007038c06e486ea5`, versión `0.67.3`.
No usar el paquete npm publicado ni actualizar automáticamente el fork.

## Instalar Pi host e imagen

Con Node >=20.6, npm y Git instalados:

```bash
bash ~/setup/pi/scion/install-pi-fork.sh
export PATH="$HOME/.local/bin:$PATH"
pi --version
git -C ~/bin/pirate/pi-mono rev-parse HEAD
```

El instalador clona en `~/bin/pirate/pi-mono` si falta, verifica origin y revisión,
y rechaza cambios locales sin borrarlos. Ejecuta `npm ci` y el `tsgo` local para
`tui`, `ai`, `agent` y `coding-agent`, copia los assets de CLI y publica el enlace
`~/.local/bin/pi`. No ejecuta `npm run build`: el build de `ai` regenera modelos
consultando servicios externos. El catálogo del commit fijado se conserva.

La receta de contenedor está en [Dockerfile](Dockerfile). El contexto construido
en esta máquina está en `~/scion-build/pi-fork-e9ba9e2`. Usa como base la imagen
anterior `scion-pi:latest`, que se conserva, y publica `scion-pi-fork:e9ba9e2`.
La nueva imagen retira el Pi npm de esa base e instala únicamente los paquetes
Pi del fork. Los snapshots excluyen secretos, sesiones y configuración personal.
Nunca incluir la clave en Dockerfile, argumentos de build, capas, contexto o logs.

Para reconstruir el contexto desde los checkouts locales:

```bash
ctx="$HOME/scion-build/pi-fork-e9ba9e2"
mkdir -p "$ctx/pi-mono" "$ctx/python-src/sldb" "$ctx/python-src/deskops"
git -C ~/bin/pirate/pi-mono archive e9ba9e2ebce1b49dca85ab20007038c06e486ea5 | tar -x -C "$ctx/pi-mono"
tar --exclude=__pycache__ --exclude='*.pyc' -cf - -C /mnt/ssd/proyectos/SLDB_1/sldb pyproject.toml README.md LICENSE src | tar -x -C "$ctx/python-src/sldb"
tar --exclude=__pycache__ --exclude='*.pyc' -cf - -C /mnt/ssd/proyectos/SLDB_1/deskops pyproject.toml README.md deskops | tar -x -C "$ctx/python-src/deskops"
/mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pip wheel --no-deps \
  --wheel-dir "$ctx/wheels" "$ctx/python-src/sldb" "$ctx/python-src/deskops"
cp "$(command -v uv)" "$ctx/uv"
cp ~/setup/pi/scion/Dockerfile ~/setup/pi/scion/launch.py ~/setup/pi/scion/scion-events.ts "$ctx/"
docker build -t scion-pi-fork:e9ba9e2 "$ctx"
```

El bundle original está en la rama local `wt/pi-harness` del checkout
`/mnt/ssd/proyectos/SLDB_1/scion-wt-pi-harness`, commit `7163525f9`.
Para preparar una instalación del harness compatible con Scion 0.2.21:

```bash
bundle="$HOME/scion-build/pi-fork-e9ba9e2/harness"
mkdir -p "$bundle"
git -C /mnt/ssd/proyectos/SLDB_1/scion-wt-pi-harness archive 7163525f9 harnesses/pi | tar -x --strip-components=2 -C "$bundle"
cp ~/setup/pi/scion/harness-config.yaml "$bundle/config.yaml"
cp ~/setup/pi/scion/provision.py "$bundle/provision.py"
printf 'FROM scion-pi-fork:e9ba9e2\nCMD ["pi"]\n' > "$bundle/Dockerfile"
scion harness-config install --global --name pi "file://$bundle" --force
```

[launch.py](launch.py) vive en la imagen y fija una sesión por agente en
`~/.pi/agent/scion/session.jsonl`. Scion 0.2.21 reinicia el comando original del
contenedor al reanudar: el launcher conserva las opciones del harness pero
suprime la repetición del encargo inicial. Rechaza una sesión inválida o de otro
workspace. `--offline` desactiva consultas de arranque y avisos de actualización;
las llamadas de Pi a DeepSeek siguen funcionando.

El launcher también traduce el `--model small` que Scion vuelve a inyectar al
reanudar. Ese valor es un alias de Scion; Pi lo interpreta como una búsqueda
difusa y puede seleccionar un proveedor distinto. Se usa el par
`defaultProvider/defaultModel` ya resuelto por `provision.py`. Los modelos
explícitos distintos del valor de `SCION_MODEL` se conservan; una resolución
ausente o incompleta falla antes de iniciar Pi.

La imagen corregida usa un nombre local calificado para que `image_registry`
no lo reescriba hacia un registro remoto. Se construye sin actualizar el fork,
Scion ni dependencias:

```bash
docker build --pull=false -f ~/setup/pi/scion/Dockerfile.runtime \
  -t local.scion/pi-autonomy:e9ba9e2-r2 ~/setup/pi/scion
```

Los harnesses `pi` y `pi-autonomy` usan esa imagen. Un contenedor detenido sigue
usando su imagen original al reanudar, aunque el CLI acepte `--image`: verificar
el ID real del contenedor antes de declarar desplegada una corrección. No borrar
el home del agente, que contiene su sesión. Las pruebas de reparación usan un
agente nuevo con la imagen corregida y luego reanudan ese mismo agente.

Instalar primero la copia local y luego publicarla al Hub; el modo Hub de
`install` no actualiza la copia local. A partir de un bundle del harness que
contenga `harness-config.yaml` como `config.yaml` y el provisioner vigente:

```bash
for name in pi pi-autonomy; do
  scion --no-hub --global harness-config install --name "$name" "file://$bundle" --force
  SCION_HUB_ENABLED=true scion --hub http://127.0.0.1:8080 --global harness-config sync "$name"
done
```

Una configuración de proyecto tiene precedencia sobre la global. Para actualizar
una existente, usar `harness-config install` en modo Hub con `--project` apuntando
a su directorio real de configuración, no solo al UUID: en esta versión `sync`
publica globalmente. Comprobar por API `scopeId` e imagen después de publicar.
Copiar assets a un contenedor detenido no basta: Scion puede recrearlo con la
imagen guardada en su metadata. Para los agentes anteriores, esta reparación
conserva las imágenes originales en tags `local.scion/archive-pi-*` y hace que
los tags de compatibilidad `scion-pi-fork:e9ba9e2` y
`scion-pi-autonomy:e9ba9e2` resuelvan a la imagen corregida. Se registra cada ID
anterior y su tag de rollback. El home y la sesión no se borran; la migración se
prueba con un agente anterior del laboratorio. El coordinador de producción
permanece detenido.

Para que Claude use el login vigente del host por el mecanismo nativo de secretos:

```bash
python3 ~/setup/pi/scion/sync-claude-secret.py
```

El helper publica `CLAUDE_AUTH` como secreto de archivo del usuario en el Hub
local. `--project-id` permite limitarlo a un proyecto. Solo pasa la ruta del
archivo al CLI de Scion; los tokens no aparecen en argv, salida ni Git. Repetir
la sincronización cuando se renueve el login del host. Esto no instala ni
actualiza Claude.

## Publicar el harness Pi

La imagen local instalada es `scion-pi-fork:e9ba9e2`, con etiquetas de fork y
commit; el host usa Pi `0.67.3` compilado directamente. Publicar la configuración
Pi al Hub con la ruta explícita: en Scion 0.2.21 el sync no resolvió el slug en
este contexto.

```bash
SCION_HUB_ENABLED=true scion harness-config sync pi --project /mnt/ssd/proyectos/SLDB_1 --non-interactive
```

## Plantillas del proyecto

El proyecto registrado es `sldb-1`, UUID
`b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7`. Su directorio de plantillas es
`~/.scion/project-configs/sldb-1__b0899ed7/.scion/templates`.
Generar desde RoleDocs y RuntimeProfileDocs, sin `--task` ni `--agent`: esto
materializa plantillas sin crear RunDocs ni tocar tareas reales.

```bash
SCION_TEMPLATES="$HOME/.scion/project-configs/sldb-1__b0899ed7/.scion/templates"
deskops runtime template role-deskops-executor \
  --root /mnt/ssd/proyectos/SLDB_1/deskops --harness pi \
  --out "$SCION_TEMPLATES/deskops-executor" --task-repo deskops --mode executor
deskops runtime template role-deskops-supervisor \
  --root /mnt/ssd/proyectos/SLDB_1/deskops --harness pi \
  --out "$SCION_TEMPLATES/deskops-coordinator" --task-repo deskops --mode coordinator
scion templates sync deskops-executor --project sldb-1
scion templates sync deskops-coordinator --project sldb-1
scion templates list --project sldb-1
```

Comprobar también el descubrimiento por API del proyecto usado por la UI. La
plantilla coordinadora queda disponible; **no se lanza automáticamente**.
DeskOps/SLDB conservan tareas, validación, evidencia y cierre. La supervisión de
runtime de DeskOps sigue siendo Herdr; estas plantillas Scion son opcionales.
Integrar supervisión y trazabilidad avanzada requiere trabajo posterior.

## Credencial y autenticación

```bash
python3 ~/setup/pi/scion/sync-deepseek-secret.py
```

El helper lee únicamente `DEEPSEEK_API_KEY` desde `~/.pi/agent/secrets.env` y el
Bearer token desde `~/.scion/dev-token`, sin evaluar shell. Admite una asignación
simple, opcionalmente `export`, con comillas simples/dobles coincidentes; no
interpreta expansiones ni escapes. Rechaza claves ausentes, vacías o duplicadas.
Codifica el valor en base64 como exige la API de Scion 0.2.21 (no es cifrado).
Publica el secreto con scope de proyecto y `injectionMode: as_needed` mediante
`PUT /api/v1/secrets/DEEPSEEK_API_KEY` en `http://127.0.0.1:8080`.
`--help` describe overrides de rutas, proyecto y Hub. No pasar el valor por argv.
Los errores no muestran cuerpos HTTP, valores ni tokens; el éxito solo indica
nombre, scope y estado. La credencial queda fuera del repositorio y la imagen.

La autenticación del CLI contra Hub es independiente de la credencial del
proveedor que necesita Pi dentro del agente. El token del helper autentica la
petición al Hub; el secreto de proyecto permite al Host/Runtime Broker entregar
`DEEPSEEK_API_KEY` al harness. Que el CLI pueda listar proyectos no demuestra que
el Host pueda ejecutar DeepSeek. Verificar la respuesta real del agente.

## Smoke de lectura y sesión

Usar un agente de prueba propio y un nonce nuevo. Mantener `--project sldb-1`
en todas las operaciones para evitar resolver otro proyecto por el cwd.
El prompt de smoke debe limitar explícitamente la plantilla ejecutora a lectura.
No ejecutar tareas reales, mutaciones de DeskOps, ni comandos Herdr durante este
smoke. No cargar `pi-subagents` dentro de Scion.

Lanzar y reanudar desde `/mnt/ssd/proyectos/SLDB_1`, el workspace compartido de
varios repositorios que intencionalmente no es un repositorio Git. Scion 0.2.21
exige Git >=2.47 si el cwd está dentro de Git, incluso con `--workspace`
explícito; el host tiene Git 2.43. Usar esta raíz evita esa comprobación sin
cambiar Git.

```bash
cd /mnt/ssd/proyectos/SLDB_1
scion start pi-fork-read-smoke \
  'Prueba SOLO LECTURA: recuerda el nonce <NONCE_NUEVO>. Ejecuta deskops list tasks --root /workspace/deskops e informa el resultado. No edites archivos, tareas ni configuración. Espera instrucciones.' \
  --type deskops-executor --project sldb-1 --harness-auth api-key --non-interactive
scion look pi-fork-read-smoke --plain --project sldb-1
scion message pi-fork-read-smoke 'Confirma que completaste la lectura y espera.' --project sldb-1
scion stop pi-fork-read-smoke --project sldb-1
cd /mnt/ssd/proyectos/SLDB_1
scion resume pi-fork-read-smoke --project sldb-1 --non-interactive
scion message pi-fork-read-smoke 'Indica el nonce que te di antes de detenerte, sin releerlo de archivos. Mantén el modo solo lectura.' --project sldb-1
scion look pi-fork-read-smoke --plain --project sldb-1
scion stop pi-fork-read-smoke --project sldb-1
```

Guardar evidencia sanitizada de revisión del fork, versión, descubrimiento de
plantillas, respuesta DeepSeek, lectura CLI y nonce conservado tras stop/resume.
No repetir el nonce en el prompt de reanudación. Revisar agentes antes y después
para demostrar que se conservaron los ajenos.

**Estado verificado el 2026-11-10:** build del host y contenedor, secreto en API,
plantillas publicadas, lectura de DeskOps y respuesta DeepSeek correctos. El
agente `deskops-pi-ready-20261110` conservó la sesión
`01a1c3a1-1449-77e4-8e78-b43dbb40370f` después de stop/resume y recordó un nonce
enviado por un mensaje posterior al arranque, sin repetir el encargo inicial.
Los agentes de prueba quedaron detenidos; no se despachó ninguna tarea real.
Veinte pruebas independientes validan launcher y redacción de secretos.
La evidencia sanitizada está en `runs/subagents/20261110-scion-pi-fork/`.


## Bootstrap explícito y eventos nativos

Regla fuente: [átomo de autoridad de runtime y workflow](../../desk/atoms/atom-scion-bootstrap-preserves-runtime-and-workflow-authority.md).
[start-desk.py](start-desk.py) prepara un worktree separado del desk, comprueba
imports reales y materializa ejecutor, tester y coordinador mediante la API
`deskops runtime template --context-file`. Requiere la implementación de esa
interfaz y del modo `tester` en la fuente DeskOps probada. La raíz del fixture
ya debe ser un repositorio Git con sus tareas, roles y rituales comprometidos.
No se prepara ni despacha un desk de producción durante estas pruebas.

Scion v0.2.21 resuelve la plantilla local desde el directorio de ejecución;
`--project` elige el destino Hub. Por eso `--templates-dir` exige el layout
`<config-del-proyecto>/.scion/templates` y sync, start y resume corren desde esa configuración,
sin seleccionar una plantilla homónima de otro proyecto. Los errores muestran
solo la etapa conocida y la clasificación de salida; omiten argumentos y salida
del subproceso.

El provider local del broker apunta al directorio externo de configuración
Scion, fuera del repositorio Git. En su `settings.yaml`, `workspace_path`
identifica el workspace compartido absoluto. El Hub deriva el montaje de esa
configuración y puede descartar el `--workspace` de la petición; vincular el
provider al checkout Git haría que Scion intentara crear otro worktree por agente.
El worktree de tareas queda bajo la autoridad de DeskOps/bootstrap.

Ejemplo de laboratorio autorizado (el directorio de plantillas pertenece al
proyecto explícito; no copiarlo para otro proyecto):

```bash
/mnt/ssd/proyectos/SLDB_1/.venv/bin/python ~/setup/pi/scion/start-desk.py \
  --root /mnt/ssd/proyectos/SLDB_1/.tmp/scion-autonomy-lab-v2 \
  --workspace-root /mnt/ssd/proyectos/SLDB_1 \
  --source-root /mnt/ssd/proyectos/SLDB_1/deskops-runtime \
  --sldb-root /mnt/ssd/proyectos/SLDB_1/sldb/src \
  --ref HEAD --project d7d9d3cd-60a1-46be-9a63-b56722521061 --agent autonomy-lab-coordinator-v2 \
  --templates-dir "$HOME/.scion/project-configs/scion-autonomy-lab__d7d9d3cd/.scion/templates"
```

`--ref` tiene el valor predeterminado `origin/main`; un arranque nuevo con ref
inválido falla antes de crear un worktree o plantillas. La recuperación de una
coordinadora propia usa su commit base registrado incluso si ese ref desapareció. No hay fallback a `HEAD`, reset del checkout
original ni modificación de remotes. Se registra revisión del desk y fuente en
`.tmp/scion-bootstrap/<identidad>/provenance.json`. El directorio adyacente tiene
un marcador de propiedad y un worktree dedicado; uno desconocido se rechaza.
Los commits propios pueden avanzar desde el commit base registrado. Una
coordinadora existente solo se reconcilia con nombre, proyecto, etiquetas y
provenance coincidentes; al recuperarla se conservan también los archivos
sucios de hijos en curso. No se crea otro worktree ni se sigue un ref movido. Se comparan fingerprints
SHA-256 del contenido de `deskops/` y `sldb_root/sldb` (fuentes y datos, sin
cachés ni bytecode); cambios sin commit también invalidan la recuperación.
Cambios ajenos en desk/docs/evidencia o commits de solo documentación no la
bloquean. Un lock nativo sobre el directorio original serializa invocaciones y
la lista de agentes se vuelve a leer bajo ese lock.
Sin esa identidad existente se exige un worktree limpio. Todos los paths del contexto deben ser absolutos dentro del workspace.
`source_root` contiene el paquete `deskops`; `sldb_root` es directamente `src`,
no la raíz del checkout SLDB. `PYTHONPATH` enlaza ambos, y se verifican los
`__file__` importados antes del arranque.

El generador materializa `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`,
`PYTHONPATH` y un volumen soportado de workspace a su misma ruta absoluta.
Scion monta además el workspace en `/workspace`; no se crean symlinks manuales.
Bootstrap usa la autenticación existente del CLI contra el Hub explícito
(`--hub`, predeterminado `http://127.0.0.1:8080`). Los hijos usan sus tokens
Scion y el secreto DeepSeek del proyecto; `secrets.env` nunca se monta.
El metadata server existente de `sciontool` sigue refrescando los tokens.

Tras sincronizar las tres plantillas, bootstrap reconcilia el nombre y etiquetas
de la coordinadora. Una identidad ajena, duplicada o en error exige resolución
operativa; una activa no recibe otro prompt, y una detenida se reanuda. El primer
arranque recibe una sola asignación operativa. Un archivo `--config` propio del
bootstrap activa `DESKOPS_AUTONOMOUS=1` únicamente para la coordinadora, sin
editar las plantillas generadas. En esa modalidad el launcher añade una
instrucción de recuperación al reanudar la sesión fija; conserva el historial y
suprime la asignación inicial. Las sesiones manuales conservan su comportamiento.
Scion y DeskOps siguen siendo las únicas autoridades de runtime y lifecycle.

[scion-events.ts](scion-events.ts) carga explícitamente desde el launcher.
`session_start`, `input`, `agent_start`, `agent_end` y los dos eventos de ejecución
de tools se traducen al dialecto Claude ya soportado por `sciontool hook`.
`agent_end` se traduce a `Stop` (working), nunca `task_completed`. Las nuevas
entradas y sesiones limpian waiting mediante el handler existente, mientras
sus reglas conservan estados deliberados de blocked/completed durante wrap-up.
Solo se envían nombres de evento y nombres/identificadores acotados de tool;
ningún prompt, argumento, resultado, transcript ni diagnóstico del hijo sale
por ese canal. Cada llamada usa stdin y un timeout de cinco segundos. Un fallo
emite un aviso fijo sin datos del proceso. `--no-extensions` y `-ne` excluyen el
puente también en procesos baratos de revisión.

Las pruebas de `tests/test_scion_autonomy.py` verifican los contratos con repositorios temporales y comandos simulados. La integración real quedó registrada en `runs/subagents/20261110-autonomy-bootstrap/acceptance-v2.json`: dos tareas cerradas, dos fases, cero mensajes de seguimiento, recuperación de la coordinadora y tester independiente nuevo después de un fallo real. Las seis sesiones Pi son distintas y no hubo hijos duplicados. La validación final independiente pasó con los tests originales intactos. El probe de lifecycle y renovación real del token tiene evidencia separada en el mismo directorio; no se afirma una ejecución de diez horas.

## Sesión base compartida (fork, DSP-1)

Si al primer arranque de un agente existe `/workspace/.scion/fork-from/<SCION_AGENT_NAME>.jsonl`, `launch.py` la
bifurca a la sesión del agente igual que `pi --fork` (`SessionManager.forkFrom`): encabezado nuevo con id propio, el cwd
del agente y `parentSession`, y el resto de las entradas copiadas. Varios ejecutores de una misma fase pueden partir de
una sesión base que ya leyó el contexto común; ese prefijo se cobra como caché. El coordinador copia (no enlaza: el
contenedor solo ve `/workspace`) la sesión base a ese nombre antes de `scion start`. Sin archivo, nada cambia.
