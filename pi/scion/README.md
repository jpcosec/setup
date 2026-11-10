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
cp ~/setup/pi/scion/Dockerfile ~/setup/pi/scion/launch.py "$ctx/"
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
sed -i 's/PI_VERSION = "0.73.1"/PI_VERSION = "0.67.3"/' "$bundle/provision.py"
printf 'FROM scion-pi-fork:e9ba9e2\nCMD ["pi"]\n' > "$bundle/Dockerfile"
scion harness-config install --global --name pi "file://$bundle" --force
```

[launch.py](launch.py) vive en la imagen y fija una sesión por agente en
`~/.pi/agent/scion/session.jsonl`. Scion 0.2.21 reinicia el comando original del
contenedor al reanudar: el launcher conserva las opciones del harness pero
suprime la repetición del encargo inicial. Rechaza una sesión inválida o de otro
workspace. `--offline` desactiva consultas de arranque y avisos de actualización;
las llamadas de Pi a DeepSeek siguen funcionando.

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
