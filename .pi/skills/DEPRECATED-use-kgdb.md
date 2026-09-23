# DEPRECATED — use-kgdb

- La skill `use-kgdb` fue retirada de la fuente versionada el 2026-09-23.
- Motivo: kgdb fue absorbido por sldb el 2026-09-20 (ver `hum-ecosystem/hum-core/AVISO-kgdb-sldb.md`).
- Los contratos de grafo y el lenguaje de query de kgdb ahora son re-exports de sldb: una sola clase por concepto.
- Ya no existe un repositorio kgdb independiente como fuente de skills; `tools/kgdb/.pi/skills/use-kgdb` queda fuera de esta centralización.
- Para trabajo nuevo de grafo usa `sldb.store.graph` / `sldb.api.graph` (mapa completo en `hum-ecosystem/tools/kgdb/README.md`).
- El contenido de la antigua skill (nodos, edges, provenance, comandos graph build/missing/neighbors) vive ahora en `use-sldb/SKILL.md`.
- El comando del CLI sigue existiendo bajo la superficie de deskops, pero la skill que lo documentaba es redundante con `use-sldb`.
- Referencias a kgdb en `settings.json` deben eliminarse (ver `README.md` y `settings-skills.example.json`).
- No hay acción de migración pendiente: nada que ejecutar para los flujos existentes.
- Fuente de la decisión: `hum-ecosystem/hum-core/AVISO-kgdb-sldb.md` (2026-09-20).