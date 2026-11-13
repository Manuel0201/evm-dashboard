# Plan por fases

Fecha límite fijada: 2026-11-12 a las 24:00 (oficial: por confirmar con Talento Humano). Inicio del plan: 19:15 aprox. Presupuesto total: ~4 h 45 min.

Estados: `PENDIENTE` · `EN CURSO` · `CHECKPOINT` · `HECHA`

Cada fase termina con: pruebas y linter en verde, commit aprobado por el usuario, PR a `develop` aprobado, y checkpoint respondido.

| # | Fase | Rama | Tiempo | Estado |
|---|------|------|--------|--------|
| 0 | Repo y Gitflow | `feature/project-setup` | 15 min | HECHA |
| 1 | Entender EVM (a mano) y decisiones de negocio | (sin código) | 25 min | HECHA |
| 2 | Cálculos EVM puros + pruebas unitarias | `feature/evm-calculations` | 35 min | HECHA |
| 3 | Base de datos, modelos y script de inicialización | `feature/database-models` | 25 min | HECHA |
| 4 | API de proyectos y actividades + consolidado + pruebas de integración | `feature/projects-activities-api` | 45 min | HECHA |
| 5 | Documentación OpenAPI en `/api-docs` | `feature/openapi-docs` | 10 min | HECHA |
| 6 | Frontend: tabla, consolidado, semáforo CPI/SPI, gráfica | `feature/frontend-dashboard` | 50 min | HECHA |
| 7 | Verificar que los números tienen sentido (cálculos a mano vs sistema) | (sin código) | 15 min | APLAZADA (el usuario la dejó para después, prompt #65; debe hacerse antes de cerrar AI_PROCESS.md) |
| 8 | Release: `release/1.0.0`, merge a `main`, tag | `release/1.0.0` | 15 min | EN CURSO |
| 9 | README, AI_PROCESS.md, guion del video, checklist final | `feature/documentation` | 60 min | PENDIENTE |

## Detalle por fase

### Fase 0 — Repo y Gitflow
- Objetivo: tener el repositorio listo con la estructura de ramas del PDF.
- Se entrega: `git init`, `.gitignore`, `.env.example`, `README.md` inicial, `CLAUDE.md`, `PROMPTS_LOG.md`, `AI_PROCESS.md` (esqueleto), `docs/`; ramas `main` y `develop`; repo en GitHub.
- Pruebas: ninguna.
- Checkpoint: qué es `develop` frente a `main` y por qué cada feature entra por Pull Request.

### Fase 1 — Entender EVM (sin código)
- Objetivo: aprender PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC con un ejemplo numérico; el usuario calcula uno a mano.
- Decisiones del usuario (con pros y contras): división por cero (CPI con AC=0, EAC con CPI=0, SPI con PV=0), consolidación (sumar y recalcular vs promediar), Decimal vs float, porcentajes 0–100 vs 0–1, cálculo al vuelo vs guardado.
- Se entrega: decisiones registradas en este plan; hechos en `AI_PROCESS.md`.
- Checkpoint: calcular a mano un caso completo e interpretar CPI y SPI.

### Fase 2 — Cálculos EVM puros
- Antes de programar: pregunta de la decisión de arquitectura independiente (dónde viven los cálculos, cómo se organizan las capas). El usuario responde primero.
- Objetivo: funciones puras (sin BD, sin FastAPI) que reciben números y devuelven indicadores e interpretaciones.
- Pruebas: unitarias con valores reales y casos borde (AC=0, sin actividades, avance real=0, avance planificado=0). Cobertura ≥80% con `--cov-fail-under=80`.
- Checkpoint: por qué se consolida como se consolida y qué devuelve el sistema con AC=0.

### Fase 3 — Base de datos
- Objetivo: tablas `projects` y `activities` en PostgreSQL, modelos SQLAlchemy, script `database/init.sql`, `.env` local.
- Pruebas: conexión y creación de tablas.
- Checkpoint: relación proyecto → actividades y qué hace `DELETE` en cascada.

### Fase 4 — API
- Objetivo: CRUD de proyectos y actividades; endpoint de indicadores por actividad y consolidados con interpretación CPI/SPI. Capas: routers → servicios → repositorio/modelos. Validación con Pydantic.
- Decisión del usuario: cómo probar la API contra la BD.
- Pruebas: al menos un test de integración por endpoint validando el contrato y valores calculados.
- Checkpoint: qué recibe y devuelve un endpoint y dónde está la lógica de negocio.

### Fase 5 — OpenAPI
- Objetivo: Swagger en `/api-docs` con descripción, esquemas y códigos de error por endpoint.
- Pruebas: test que verifica que `/api-docs` responde y que `/openapi.json` incluye los endpoints.
- Checkpoint: qué es un contrato de API.

### Fase 6 — Frontend
- Objetivo: React + Vite (JavaScript) + Recharts; formulario y tabla de actividades, consolidado, semáforo CPI/SPI, gráfica PV/EV/AC por actividad. Textos en español.
- Pruebas: ESLint limpio; verificación manual de la demo (1 proyecto, 3 actividades).
- Checkpoint: de dónde salen los números que muestra la pantalla.

### Fase 7 — Verificación de números
- Objetivo: el usuario calcula a mano un proyecto con 3 actividades y lo compara con la API y la pantalla. Se anota en `AI_PROCESS.md`.

### Fase 8 — Release
- `release/1.0.0` desde `develop`, ajustes finales, merge a `main` (solo con confirmación explícita del usuario), tag `v1.0.0`, merge de vuelta a `develop`.

### Fase 9 — Documentos y video
- README con instrucciones para correr y el script de BD; `AI_PROCESS.md` completo (el usuario redacta sus desviaciones, razones, decisión de arquitectura y reflexión); guion del video; checklist final contra el PDF.

## Qué se recorta si vamos tarde
1. Docker opcional (no se hace).
2. Fase 5 se fusiona con la 4.
3. La gráfica y el semáforo se hacen en su versión más simple.
Lo que NO se recorta: cálculos con pruebas, API, Gitflow con PR y release, README, `AI_PROCESS.md`, video.

## Decisiones registradas
1. Consolidación del proyecto (prompt #25): sumar BAC, PV, EV y AC de las actividades y recalcular los índices con las fórmulas del PDF sobre los totales. Coincide con la recomendación de la IA.
2. Divisiones por cero (prompt #26): devolver null (sin dato) en CPI (AC=0), SPI (PV=0), EAC y VAC (CPI nulo o 0); la interpretación dice "No calculable". Aplica también a proyecto sin actividades. Coincide con la recomendación de la IA.
3. Dinero (prompt #27): Decimal para montos; índices redondeados a 4 decimales. Coincide con la recomendación de la IA.
4. Porcentajes (prompt #27): escala 0–100 en API, base de datos y pantalla; validación entre 0 y 100; se divide entre 100 con una constante con nombre. Coincide con la recomendación de la IA.
5. Indicadores (prompt #28): se calculan al vuelo a partir de los datos base; no se guardan en la base de datos. Coincide con la recomendación de la IA.
6. Arquitectura (prompt #33, decisión independiente: el usuario dio primero su idea en el prompt #32 y luego eligió entre alternativas): tres capas, routers → servicios → cálculos (funciones puras por indicador), más modelos para la base de datos. Coincide con la recomendación de la IA.
7. Pruebas contra la base de datos (prompt #40): PostgreSQL de pruebas (evm_db_test), con el mismo script de inicialización que producción; no SQLite ni mocks. Coincide con la recomendación de la IA.
8. Linter del frontend (prompt #57): ESLint (la plantilla de Vite traía oxlint). Coincide con la recomendación de la IA.
9. Login (prompts #57 y #58): el PDF no lo pide. Se hace después del MVP y solo si sobra tiempo, como fase opcional 10 en la rama feature/login; el usuario pidió un login completo (usuarios, registro, contraseñas cifradas), mientras la IA recomendó empezar por uno simple.
