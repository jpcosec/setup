
--- 2026-09-22 03:36:54 dispatch -> w14:p6 ---
PROMPT: Trabajas en /home/jp/proyectos/_worktrees/graph_ui-mindmap (worktree de /home/jp/proyectos/hum-ecosystem/tools/graph_ui, rama fix/mindmap-verificacion). NO cambies de rama, NO push, NO toques el repo principal ni otros worktrees.

CONTEXTO: el CLAUDE.md de ese repo dice que el desarrollo ACTIVO es frontends/mindmap/ (servidor Python stdlib serve.py, UI React por CDN, sin bundler) y que apps/review-workbench/ es un editor React RETIRADO que queda solo como referencia. Los docs de ese repo MIENTEN seguido: verifica la afirmacion contra git log --oneline y contra el codigo antes de creerle a cualquier doc.

OBJETIVO (esta tarea es READ-ONLY: no edites codigo, no commitees, no "arregles" nada; si algo esta roto, se reporta con evidencia):
1. Confirmar contra git log y el arbol actual cual es el desarrollo activo (frontends/mindmap vs apps/review-workbench vs src/ vs legacy/). Cita commits que lo prueben.
2. Correr la verificacion REAL que el repo declara, y pegar salida literal de cada una:
   - python3 -m pytest tests -q
   - node --test tests/mindmap-model.test.mjs
   - python3 -m pytest tests/test_mindmap_contract.py tests/test_mindmap_adapter.py tests/test_mindmap_persistence.py tests/test_mindmap_compiler.py tests/test_mindmap_endpoints.py tests/test_mindmap_quick_capture.py -q
   - python3 -m pytest tests/test_mindmap_skin.py -q
3. Levantar el server activo y probarlo contra un store SLDB REAL: python3 frontends/mindmap/serve.py 8088 (lee frontends/mindmap/README.md para saber que store usa y como se le apunta una KB). Verifica con curl los endpoints que ese README documente. NO uses el .sldb de un repo que tenga cambios sin commitear de otro agente; si necesitas escribir, copia el store a /tmp primero.
4. Reportar que esta roto y que no, con el output crudo del primer fallo de cada suite.

REPORTA: tabla suite -> resultado -> primer fallo; cual es el desarrollo activo con evidencia; si el server levanta y contra que store; y si el desk/ del repo (deskops) tiene tareas abiertas que contradigan lo que encontraste (deskops list tasks --root .). Todo con evidencia; nada de "deberia funcionar".
OUTPUT (tail):
��─────────────┤
 │ _worktrees/graph_ui-review-workbench │ fix/review-workbench-honest-save       │ mis 3 arreglos del workbench, fuera de master (master quedó limpio) │
 ├──────────────────────────────────────┼────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
 │ _worktrees/graph_ui-mindmap          │ fix/mindmap-verificacion               │ ya existía; verificación del stack activo                           │
 └──────────────────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────┘

 Workers forkeados de mi sesión (pi + DeepSeek, ninguno Claude)

 - pi5 w15:pC (feature-ui) → terminado: 3 commits (5ec9cd12 wiki, 95879071 decisiones+fixtures, 9c5308c6 run doc) y docs/ui/KNOWLEDGE-OS-RUN.md. Lo verifiqué yo:
 tsc 0, 24/24 tests, build OK, árbol limpio.
 - pi9 w15:pG (sldb-runtime-cache) → trabajando en el cache que escribe dentro del store + tests.
 - pi12 w18:p1 (graph_ui-mindmap) → tu prompt verbatim, corriendo.
 - pi13 w19:p1 (os-mount) → investigación para servir el dist/ bajo una ruta nueva detrás del gate de Cognito; entrega docs/ui/KNOWLEDGE-OS-MOUNT.md, sin tocar
 rutas existentes.
 - pi10 w15:pK quedó idle en graph_ui/master con la misma tarea que ahora tiene pi12: se puede cerrar.

 Detalles que importan
 - spawn fallaba con agent_pane_busy (el tab subagents de w15 está lleno), así que levanté workspaces propios: w18 (mindmap) y w19 (os-mount).
 - spawn-fork no pasa flags de modelo (argv queda pi --fork <file>), así que los workers corren con el default de pi: deepseek-v4-pro. Si los querés en Flash, hay
 que arrancarlos a mano con --provider openrouter --model '~deepseek/deepseek-v4-flash-latest'.
 - No toqué ningún agente ajeno (pi2/pi3/pi4/pi6/pi7/pi8/pi11 siguen siendo de otras sesiones). A pi7 le devolví su directorio: saqué el worktree que había creado
 encima y lo puse en _worktrees/sldb-runtime-cache.
 - Verifico leyendo el repo y corriendo las suites yo, no el pane (los panes son demasiado angostos para leer salida).

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
~/proyectos/_worktrees/graph_ui-mindmap (fix/mindmap-verificacion)
↑191k ↓221k R46M $0.299 31.4%/1.0M (auto)                                                                                                 (deepseek) deepseek-flash
