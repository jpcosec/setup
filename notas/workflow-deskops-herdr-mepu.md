# Coordinar subagentes con herdr + deskops — lo que aprendí en MEPU

Notas de una sesión larga (~12 h) coordinando workers sobre
`repos/mepu/mepu_ocs_dev`: 15 tareas cerradas, de 146 a 253 tests.
Escrito para el próximo que tenga que hacer esto, no como registro de la sesión.

---

## 1. El dry run con un agente incapaz es la mejor inversión del flujo

Idea de jp, y funcionó mejor de lo que esperaba. Antes de despachar la tarea
real, mandás un zero-context a leer el repo y devolver **su plan y sus dudas**.
No para usar el plan: para descubrir qué no estaba en tu brief.

Rendimiento concreto:

- **f1-04 (secrets.py)**: el dry run encontró 2 importadores que yo no vi. Mi
  grep buscaba `import secrets` y `from secrets`, no
  `from src.backend.secrets`. Eran los dos que corren **dentro del contenedor**
  (`ingestas/descargar_historico.py`, `ingestas/sftp_insumos.py`). De haberlos
  perdido, el arreglo pasaba los tests y rompía producción.
- **f4-01 (Dagster)**: sus dudas revelaron dos decisiones que nadie había
  tomado — qué hacer con Airflow, y quién crea la DB `dagster`. Las resolví yo
  antes de despachar, en vez de dejar que el worker improvisara.

Detalle: usá un modelo **capaz pero barato** para el dry run. Probé
`gemma-4-31b:free` y se quedó mudo (8 mensajes, sin respuesta).
`nemotron-3-super-120b:free` investigó de verdad. "Cuanto más incapaz mejor"
tiene un piso.

Contra-ejemplo instructivo: para el dry run de f1-04 (pipeline→Postgres) el
zero-context **no** encontró las trampas reales (`INSERT OR REPLACE`,
`lastrowid`) y encima afirmó que no había sintaxis exclusiva de SQLite. Las
encontré yo grepeando. El dry run reduce puntos ciegos, no los elimina: hay que
hacer la propia investigación igual y usar el dry run como segunda pasada.

---

## 2. Forkear el contexto sale casi gratis, pero no sirve para dry runs

`coordination.sh spawn pi <cwd> --fork <session.jsonl>` arranca un worker con
todo tu contexto. Con `--provider deepseek --model deepseek-flash` (1M de
ventana, contra 128K del mismo modelo vía openrouter) el fork entra completo.

**Pero un fork no sirve para el dry run**: ya sabe todo lo que vos sabés, así
que sus preguntas no revelan tus puntos ciegos. Para eso necesitás un
zero-context real. El fork sirve para ejecutar, no para auditar el brief.

Ojo con `spawn-fork`: descarta los flags de modelo (`cmd_spawn "$kind" "$cwd"
--fork "$path"`, sin reenviar `"$@"`). Usá `spawn ... --fork <path>` directo.

Y el `cwd` se pierde con `--fork`: el worker arranca en `$HOME`. Hay que
decírselo en el prompt.

---

## 3. Verificación por mutación, o no verificaste nada

La regla que más valor produjo: por cada entregable, **saboteá el código y
confirmá que el test correcto falla**. Si pasa todo con el sabotaje puesto, el
test es decorativo.

Casos donde esto encontró algo que la lectura no:

| Sabotaje | Resultado |
|---|---|
| `tiene_marca_ingesta=True` para stock | falló → el test lee el esquema real, no una lista |
| `_run_id` dentro de `_row_hash` | 4 tests fallaron → la estabilidad está cubierta |
| snapshot como "último por clave" | falló el test de la clave que desaparece |
| `i2b` a `blocking=False` | 2 tests fallaron |

Y el caso donde **reveló un test falso**: en f4-03 el worker probaba que
`blocking=True` estuviera *declarado*, no que frenara el DAG. Al escribir yo esa
prueba descubrí que re-materializar el asset borra el defecto inyectado antes de
que el check lo vea — el run daba verde con el defecto puesto. La prueba había
que correrla solo sobre los checks, sin re-materializar.

Corolario: **verificá también con tus propios datos**, fuera de la suite del
worker. En f3-03 corrí dos veces `convertir()` con `run_id` distintos y comparé
hashes a mano. Su test decía lo mismo, pero yo no lo sabía hasta hacerlo.

---

## 4. Lo que rompí, y la lección

Corrí `run_all.py` con `MEPU_DB=$T/fresh.db` creyendo que redirigía la salida.
**Esa variable no existe**: `db.py:15` define `DB_PATH` como constante. Escribió
en la base real de producción, regenerando 3 tablas derivadas.

Recuperable (eran derivadas, `cruces.py` las reconstruye) y las 14 tablas fuente
quedaron intactas. Pero destruí la línea base contra la que se validaba paridad.

Dos lecciones:

1. **Verificá que el override existe antes de confiar en él.** Un `grep MEPU_DB
   src/` de 3 segundos lo habría evitado.
2. El programa **lo dijo en pantalla** (`DB: .../data/mepu.db`) y no lo leí.
   Cuando corrés algo destructivo, leé la salida antes del siguiente comando.

Lo bueno del accidente: expuso un bug real. `master_oc` se construía como
`set(api) | set(pdf)`, metiendo 17 OCs que solo existían en PDF. jp lo zanjó en
una línea — *"el PDF no es la fuente, está ahí solo pa comparar con API"* — y ahí
quedó claro que el test tenía razón y el pipeline estaba mal. Sin la corrida
accidental, el bug seguía dormido porque la base de producción tenía
`master_oc` desalineado desde antes.

**No ajustes un test para que pase después de haber alterado datos.** Estuve a
punto y frené para preguntar. Era el pipeline el que estaba mal.

---

## 5. Herramienta: lo que no funciona

- **Leer panes está roto**: `coordination.sh read` devuelve columnas de 2
  caracteres, ilegible. Monitoreá por
  `~/.pi/agent/sessions/--<slug>--/*.jsonl`, parseando el último bloque de texto.
  Script de 10 líneas, indispensable.
- **`deskops add task` se rompió a mitad de sesión**: drift entre repos. `sldb`
  cambió `render_payload(self, ref_root)` y `deskops/models/task.py:30` quedó con
  la firma vieja. Solo afecta a `TaskDoc` — pills y atoms siguieron andando. 8
  tareas quedaron sin registro formal.
- **Workers que mueren al final**: uno completó todo el trabajo y murió
  escribiendo su `REPORTE.md` (`AttributeError` en su script de evidencia). El
  trabajo estaba bien. **Verificá el árbol, no la existencia del reporte.**
- **Nombres de worker no son estables**: pedís `spawn` y te da `pi2` en otro
  workspace, no el `pi7` que esperabas. Leé el nombre real de la salida de
  `spawn` antes de `say`.
- **`agent_pane_busy`**: si un spawn falla así, `reap --finished` y reintentá.

---

## 6. Aislamiento: worktree + base por worker

Lo que funcionó sin fricción:

```bash
git worktree add -b wt/<task> ../mepu_wt/<task> dev
ln -sfn <repo>/data/mepu.db ../mepu_wt/<task>/data/mepu.db   # evidencia, RO
cp .env ../mepu_wt/<task>/.env
psql -c "CREATE DATABASE mepu_<task> OWNER mepu"             # una por worker
```

Reglas:

- **Una base Postgres por worker.** Compartir base entre workers paralelos = un
  `DROP SCHEMA` de uno cuelga al otro.
- **Paralelizá solo tareas sin archivos en común.** f3-01/02/03 en paralelo, sin
  problema. La fase 4 fue secuencial porque f4-02 importa de f4-01.
- **El worker no commitea.** Yo leo el diff, escribo el mensaje, mergeo con
  `--no-ff`. El mensaje explica *por qué*, no *qué* — el diff ya dice qué.
- **Symlinká la base real como solo-lectura y decilo en el brief.** Ningún worker
  la tocó en 15 tareas. El único que escribió ahí fui yo.

Y un detalle que costó diagnóstico: **borrar la base de test de un worker
anterior hace aparecer skips** en tareas nuevas que dependían de ella. Dos tests
"desaparecidos" fueron mi propia limpieza, no un bug.

---

## 7. El brief: lo que hace la diferencia

Los briefs que produjeron buen trabajo tenían esto:

1. **Las trampas ya verificadas, con archivo y línea.** No "cuidado con las
   incompatibilidades" sino "`veredicto.py:252` usa `INSERT OR REPLACE`, que
   Postgres rechaza y `pg.py` no traduce".
2. **El porqué, no solo el qué.** "Si un SKU desaparece del snapshot y lo tratás
   como último-por-clave, el pipeline ofrece surtir producto que ya no existe."
   Con eso, el worker defiende el invariante en casos que no anticipé.
3. **Decisiones tomadas explícitamente**, para que no las revisite: "Dagster
   CONVIVE con Airflow, no lo reemplaza en esta tarea."
4. **Qué NO tocar**, por nombre de archivo.
5. **Prohibido mocks, stubs, TODOs, datos inventados.** Sin esto, aparecen.
6. **"Si algo te bloquea de verdad, pará y reportá en vez de inventar una
   salida."** Produjo hallazgos honestos en lugar de parches: un worker reportó
   que `test_poblacion.py` no podía correr contra Postgres y **no** lo modificó
   para forzar el verde.

Lo que más me sorprendió: un worker **corrigió mi brief**. Le dije que la PK de
`veredicto_llm` era `(oc_codigo, linea, material)`; es `(oc_codigo, linea)`.
Lo verificó en el schema y en la base antes de escribir código. Con mi dato,
habría fallado en Postgres.

---

## 8. Resumen operativo

```
1. Investigá vos: grep las trampas, leé el código, medí los conteos reales.
2. Dry run zero-context (modelo capaz pero barato): pedí plan + dudas.
3. Blindá el brief con lo que el dry run reveló + lo que vos encontraste.
4. Worktree + base propia + symlink RO de la evidencia.
5. Despachá con fork si podés (deepseek nativo, 1M de contexto).
6. Monitoreá por .jsonl, con sleeps largos. No leas el pane.
7. Verificá: suite completa, mutación del contrato central, y una prueba tuya
   con datos propios.
8. Vos commiteás. El mensaje explica el porqué.
9. reap, borrá worktree, dropeá la base.
```

El paso 7 es el que no se puede delegar. Todo lo demás sí.

---

## 9. Lo que salió mal en la segunda mitad (fases 5-8)

Anotado después de cerrar las 21 tareas. Son errores míos, no del harness.

### El fork del coordinador produce un worker que no trabaja

`spawn --fork <sesión>` le da al worker todo mi contexto, y eso incluye **el rol**.
Dos workers forkeados de mi sesión se dedicaron a monitorear otros workers en vez
de ejecutar su tarea: uno avanzó 2 mensajes en 9 minutos escribiendo
`watch.sh`. El síntoma es inconfundible: la sesión crece y no aparece ningún
archivo.

El fork sirve para **contexto de dominio** (qué es este repo, qué convenciones),
no para tareas de ejecución. Para f6-02, f7-01 y f8-01 usé `spawn` limpio con el
brief como única entrada, y los tres funcionaron sin intervención.

Corolario: el brief tiene que ser autosuficiente de todos modos. Si lo es, el
fork no aporta.

### Restaurar con `git checkout HEAD --` destruye trabajo del worker

Para probar una mutación copié el archivo, lo rompí, y restauré con
`git checkout HEAD -- infra/aws/*.tf`. Eso no restauró **mi** backup: revirtió
los cambios **del worker**, que estaban sin commitear. Perdí el
`aws_s3_bucket_notification` de f7-01 y dos ramas de la máquina de estados, y lo
detecté porque 2 tests pasaron a fallar.

Regla: para mutar, `cp archivo /tmp/x.bak` y restaurar **desde el backup**, nunca
desde git, mientras el árbol esté sucio. Y verificar `git status` después de
restaurar.

### Sabotear la base no prueba nada si el fixture la reconstruye

En f5-02 vacié `reporting.stock` en Postgres y los 12 tests siguieron verdes.
Concluí que el test no servía. Estaba equivocado: el fixture reaplica
`sql/reporting.sql` en cada test, así que mi sabotaje se deshacía antes de la
comparación.

Al sabotear el **archivo fuente**, 4 tests fallaron y el mensaje nombró los
endpoints degradados. La mutación tiene que atacar la **fuente de verdad** del
sistema, no un efecto transitorio.

### El caché de `.pyc` me hizo creer que había un agujero de seguridad

Probando `run_job('os')` vi que ejecutaba módulos arbitrarios. Era mi propia
mutación anterior, servida desde `__pycache__` después de haber restaurado el
`.py`. Con el caché limpio, la lista cerrada rechaza todo.

`find . -name __pycache__ -exec rm -rf {} +` antes de cualquier prueba de
seguridad.

### Un test verde puede tapar un agujero real

En f8-01 el test del umbral pasaba con una mutación que quitaba la reevaluación
de `conf < UMBRAL_HUMANO`. Pasaba porque el caso probado tenía
`requiere_humano=1`, y el segundo término del `or` lo salvaba. El agujero real —
caché con `requiere_humano=0` y confianza baja — no estaba cubierto.

Escribí el test que faltaba y verifiqué que **falla con el sabotaje y pasa sin
él**. Sin esa verificación, el test nuevo podría haber sido decorativo igual que
el anterior.

Lección: la mutación no solo valida el código, valida **el test**. Un test que no
falla ante ninguna mutación no está probando nada.

### Dos verificaciones mías dieron falso positivo por herramienta, no por código

- `psycopg` sin `autocommit` **difiere** el error de permisos: un `INSERT`
  prohibido devolvió "OK" hasta el `commit`. Parecía que `mepu_dash` podía
  escribir en `core`. Con `autocommit=True` aparece el `42501` real.
- `LIKE '%__%'` en SQL trata `_` como comodín: "10.022 filas de prueba" eran
  todas las filas. Con `GLOB '__*'` el conteo real era 0.

Ambos me hicieron reportar un problema inexistente. Antes de declarar un bug,
verificar que la herramienta de medición no sea el bug.

### Lo que sí funcionó

- **Brief con el hueco ya medido.** En f5-02 la tarea decía "migrar los endpoints
  y listo"; midiendo antes encontré que 9 de 17 tablas no tenían vista y que
  `POST /runs` no existía. El brief salió con eso escrito, y el worker no perdió
  tiempo redescubriéndolo.
- **Decirle al worker qué NO hacer.** «No crees `POST /runs`, no existe y la
  parte de SQS de esta tarea es vacua» ahorró una implementación sin consumidor.
- **Dos workers en paralelo** (f7-01 y f8-01) sobre tareas independientes, con una
  base Postgres cada uno. Ninguno pisó al otro.
- **Tests que leen los `.tf`.** Encontraron que la región default era `us-east-1`
  mientras `terraform.tfvars` —gitignorado— la corregía: un `apply` sin ese
  archivo creaba medio stack en la región equivocada. Eso no lo ve una revisión a
  ojo.
