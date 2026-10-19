#!/usr/bin/env bash
# Recordatorio de orquestación MEPU.
# Cada INTERVALO escribe un prompt en el pane del coordinador para que
# revise sus workers y cierre los que terminaron.
#
#   uso:  nohup bash mepu-orquesta-loop.sh w1F:p1 30 > /tmp/mepu-loop.log 2>&1 &
#   stop: kill $(cat /tmp/mepu-orquesta-loop.pid)

set -uo pipefail

PANE="${1:?falta PANE_ID, ej: w1F:p1}"
MINUTOS="${2:-30}"
HERDR="${HERDR_BIN_PATH:-/home/jp/.local/bin/herdr}"
PIDFILE=/tmp/mepu-orquesta-loop.pid

echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

MSG='Pasada de orquestacion MEPU: corre `bash /home/jp/setup/herdr/coordination.sh agents`, revisa cada worker despachado, cierra con `close <name>` los que terminaron, reporta en una linea por worker (tarea / estado / que falta) y lanza la siguiente ola si hay capacidad. Recuerda: la cadena S1->S2->S3->S5->S6 es serial sobre la misma SQLite, no la paralelices.'

while true; do
  sleep $(( MINUTOS * 60 ))
  # solo interrumpe si el coordinador esta libre
  estado=$("$HERDR" agent list 2>/dev/null \
    | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except Exception: print('unknown'); raise SystemExit
for a in d.get('result',{}).get('agents',[]):
    if a.get('pane_id')=='$PANE':
        print(a.get('agent_status','unknown')); break
else: print('unknown')
" 2>/dev/null)

  if [ "$estado" = "working" ] || [ "$estado" = "blocked" ]; then
    echo "$(date +%H:%M) ocupado ($estado), reintento en $MINUTOS min"
    continue
  fi

  echo "$(date +%H:%M) -> recordatorio enviado"
  "$HERDR" pane run "$PANE" "$MSG"
done
