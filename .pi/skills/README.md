# Skills de Pi — fuente versionada

Este directorio es la **fuente versionada** de las skills de Pi del ecosistema hum. Centraliza en `hum-ecosystem`/`setup`-adjacent lo que antes vivía repartido en `tools/<repo>/.pi/skills/`, desacoplando cada sesión de Pi del repositorio de origen.

## Skills incluidas

| Skill | Origen | Rol |
|---|---|---|
| `use-sldb` | `tools/sldb/.pi/skills` | Modelos StructuredNLDoc, marcadores, render/extract, .sldb stores |
| `use-deskops` | `tools/deskops/.pi/skills` | Workflow deskops (workflow harness / control plane) |
| `deskops-task-lifecycle` | `tools/deskops/.pi/skills` | Ciclo de vida estricto de tareas (Task + Pills + Atoms, Executor/Tester) |
| `deskops-health-and-drift` | `tools/deskops/.pi/skills` | Diagnóstico de salud y deriva en desk/ |
| `deskops-inbox-coordination` | `tools/deskops/.pi/skills` | Comunicación inter-proyecto vía inboxes |
| `use-spec2viz` | `tools/spec2viz/.pi/skills` | CLI spec2viz, renderers, schema export, build HTML |
| `agent-coordinator` | nativo de setup | Coordinación de agentes vía herdr |

`use-kgdb` fue retirada: kgdb fue absorbido por sldb el 2026-09-20. Ver `DEPRECATED-use-kgdb.md`.

## Re-apuntar settings.json

`/home/jp/.pi/agent/settings.json` debe apuntar **solo** a esta ruta en su array `"skills"`:

Antes:

```json
"skills": [
  "/home/jp/proyectos/hum-ecosystem/tools/sldb/.pi/skills",
  "/home/jp/proyectos/hum-ecosystem/tools/deskops/.pi/skills",
  "/home/jp/proyectos/hum-ecosystem/tools/kgdb/.pi/skills",
  "/home/jp/proyectos/hum-ecosystem/tools/spec2viz/.pi/skills",
  "/home/jp/setup/.pi/skills"
]
```

Después (ver `settings-skills.example.json`):

```json
"skills": [
  "/home/jp/setup/.pi/skills"
]
```

Pasos:

1. Editar `/home/jp/.pi/agent/settings.json` y reemplazar el array `"skills"` por el del ejemplo.
2. Reiniciar la sesión de Pi para que recargue las skills desde esta ruta.

Las copias en `tools/<repo>/.pi/skills/` se conservan como orígenes, pero ya no deben usarse como fuente de carga.

## Mantenimiento

- Esta carpeta se versiona con el repo de setup (git).
- Para actualizar una skill: editar aquí y, si el cambio debe volver al repo de origen, sincronizar manualmente.
- La ruta de carga es única: nada de apuntar a múltiples directorios.