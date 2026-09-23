---
id: atom-herdr-jerarquia-workspace-tab-pane
status: draft
tags: [system:herdr, layer:runtime, topic:workspace]
---

# Jerarquia workspace / tab / pane en herdr

## Que hace

Explica como herdr anida los tres niveles de layout y por que los comandos de creacion devuelven varios IDs de una vez.

## El modelo

```
workspace (wX)               <- contexto de proyecto, nivel top
└── tab (wX:t1)              <- layout de terminal dentro del workspace
    └── root pane (wX:t1:p1) <- primer terminal del tab
        ├── split (wX:t1:p2) <- segundo terminal, solo si el layout lo necesita
        └── split (wX:t1:p3)
```

- Un **workspace** es un contexto de trabajo top-level. Contiene uno o mas **tabs**.
- Un **tab** es un layout de terminal dentro del workspace. Contiene uno o mas **panes**.
- Un **pane** es una terminal individual; siempre hay un root pane por tab.

## Reglas de creacion (doc oficial)

1. **`workspace create` crea su primer tab y su root pane a la vez.** La respuesta trae los tres objetos juntos:
   - `.result.workspace` → el workspace (`workspace_id`)
   - `.result.tab` → su primer tab (`tab_id`)
   - `.result.root_pane` → el primer terminal usable (`pane_id`)

2. **`tab create` crea su root pane a la vez.** La respuesta trae dos objetos:
   - `.result.tab` → el tab (`tab_id`)
   - `.result.root_pane` → el primer terminal usable (`pane_id`)

3. **Solo se hace split cuando el layout necesita otra terminal.** `pane split <pane_id>` sobre un pane existente devuelve el nuevo pane como `.result.pane.pane_id`. No se crean panes extra por crear el workspace o el tab.

## Extraer los IDs con jq (la forma correcta)

```bash
# workspace create: tres IDs de una sola respuesta
created=$(herdr workspace create --cwd ~/proyectos/legos --label legos --no-focus)
ws_id=$(printf '%s' "$created" | jq -r '.result.workspace.workspace_id')
tab_id=$(printf '%s' "$created" | jq -r '.result.tab.tab_id')
pane_id=$(printf '%s' "$created" | jq -r '.result.root_pane.pane_id')

# tab create: dos IDs de una sola respuesta
created=$(herdr tab create --workspace "$ws_id" --label tests --no-focus)
tab_id=$(printf '%s' "$created" | jq -r '.result.tab.tab_id')
pane_id=$(printf '%s' "$created" | jq -r '.result.root_pane.pane_id')

# split: solo cuando el layout necesita otro terminal
split=$(herdr pane split "$pane_id" --direction right --no-focus)
new_pane=$(printf '%s' "$split" | jq -r '.result.pane.pane_id')
```

## Consecuencias practicas

- Un pane "usable" para lanzar el primer proceso es SIEMPRE el `.result.root_pane.pane_id` de la creacion — no hay que listar ni adivinar nada.
- El segundo terminal no existe hasta que se hace `pane split`: no predigas `...:p2`; captura `.result.pane.pane_id` (ver atom-herdr-captura-de-ids).
- Cerrar el ultimo tab de un workspace cierra el workspace completo (relacion tab ↔ workspace invertida).
- `pane move` puede mover un pane a un tab, un tab nuevo o un workspace nuevo; el pane conserva proceso y terminal pero cambia su id de pane (ver atom-herdr-captura-de-ids).