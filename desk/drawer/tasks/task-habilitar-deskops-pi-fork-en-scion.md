# Habilitar DeskOps con Pi del fork en Scion

Solicitud de JP del 2026-11-10: dejar funcionando el proyecto Scion `sldb-1`
(`b0899ed7-7dec-44c2-a9b9-d0ac92c61cc7`) con Pi procedente exclusivamente de
`https://github.com/jpcosec/pi-mono`, commit
`e9ba9e2ebce1b49dca85ab20007038c06e486ea5`, DeepSeek y plantillas DeskOps.

Entregable: instalación reproducible en setup, credencial inyectada desde el
secrets.env local sin mostrarla, herramientas DeskOps/SLDB disponibles y prueba
real de lectura del desk, respuesta y stop/resume. Conservar Scion v0.2.21.
No implementar un nuevo supervisor, modelo de tasks o protocolo de closeout.
No despachar tareas reales del board ni modificar trabajo ajeno. Los agentes de
prueba usan nombres propios, scope de lectura y evidencia fuera de los repos.

Validación: versión y procedencia del Pi del host y contenedor; importación segura
de DEEPSEEK_API_KEY; descubrimiento de plantillas; respuesta real con lectura de
DeskOps; reanudación de sesión; documentación del comando para usarlo.
