---
id: atom-herdr-completion
status: draft
tags: [system:herdr, layer:runtime, topic:completion]
---

# herdr completion

## Que hace

Genera el script de completado de shell para el shell indicado.

## Sintaxis

```bash
herdr completion <SHELL>
```

## Argumentos y opciones

| Argumento | Tipo | Obligatorio | Que hace |
| --- | --- | --- | --- |
| `<SHELL>` | valor enumerado | si | Shell destino: `bash`, `elvish`, `fish`, `powershell`, `zsh` |

Sin opciones adicionales (verificado en `herdr completion --help`).

## Que devuelve

El script de completado por stdout. Verificado:

```bash
herdr completion bash | wc -l   # 2662
herdr completion bash | head -3
# _herdr() {
#     local i cur prev opts cmd
#     COMPREPLY=()
```

Es texto plano de shell, no JSON; no hay IDs que capturar con jq.

## Ejemplo real

```bash
# zsh: guardar y cargar via fpath
herdr completion zsh > ~/.zfunc/_herdr
# (anade ~/.zfunc a fpath y ejecuta compinit en .zshrc)

# bash: source directo en ~/.bashrc
herdr completion bash > ~/.local/share/herdr-completion.bash
echo 'source ~/.local/share/herdr-completion.bash' >> ~/.bashrc
```

## Errores conocidos

| Codigo | Significado |
| --- | --- |
| valor de `<SHELL>` fuera de la lista | Error de parseo de clap al validar el argumento posicional (mensaje exacto no verificado) |
| stdout redirigido a ruta sin permiso | Error del shell, no de herdr |

## Notas

- Verificado 2026-09-23: `herdr completion bash` genera el completado sin tocar el servidor; es puramente local.
- El completado es estatico sobre la CLI declarada por el binario: si el binary cambia de version, hay que regenerar el script.
- No genera completado para `herdr --remote <target>` ni para argumentos pasados tras `--` a un agente.