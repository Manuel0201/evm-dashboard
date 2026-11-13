# Plan por fases

Fecha lÃ­mite fijada: 2026-11-12 a las 24:00 (oficial: por confirmar con Talento Humano). Inicio del plan: 19:15 aprox. Presupuesto total: ~4 h 45 min.

Estados: `PENDIENTE` Â· `EN CURSO` Â· `CHECKPOINT` Â· `HECHA`

Cada fase termina con: pruebas y linter en verde, commit aprobado por el usuario, PR a `develop` aprobado, y checkpoint respondido.

| # | Fase | Rama | Tiempo | Estado |
|---|------|------|--------|--------|
| 0 | Repo y Gitflow | `feature/project-setup` | 15 min | EN CURSO |
| 1 | Entender EVM (a mano) y decisiones de negocio | (sin cÃ³digo) | 25 min | PENDIENTE |
| 2 | CÃ¡lculos EVM puros + pruebas unitarias | `feature/evm-calculations` | 35 min | PENDIENTE |
| 3 | Base de datos, modelos y script de inicializaciÃ³n | `feature/database-models` | 25 min | PENDIENTE |
| 4 | API de proyectos y actividades + consolidado + pruebas de integraciÃ³n | `feature/projects-activities-api` | 45 min | PENDIENTE |
| 5 | DocumentaciÃ³n OpenAPI en `/api-docs` | `feature/openapi-docs` | 10 min | PENDIENTE |
| 6 | Frontend: tabla, consolidado, semÃ¡foro CPI/SPI, grÃ¡fica | `feature/frontend-dashboard` | 50 min | PENDIENTE |
| 7 | Verificar que los nÃºmeros tienen sentido (cÃ¡lculos a mano vs sistema) | (sin cÃ³digo) | 15 min | PENDIENTE |
| 8 | Release: `release/1.0.0`, merge a `main`, tag | `release/1.0.0` | 15 min | PENDIENTE |
| 9 | README, AI_PROCESS.md, guion del video, checklist final | `feature/documentation` | 60 min | PENDIENTE |

## Detalle por fase

### Fase 0 â€” Repo y Gitflow
- Objetivo: tener el repositorio listo con la estructura de ramas del PDF.
- Se entrega: `git init`, `.gitignore`, `.env.example`, `README.md` inicial, `CLAUDE.md`, `PROMPTS_LOG.md`, `AI_PROCESS.md` (esqueleto), `docs/`; ramas `main` y `develop`; repo en GitHub.
- Pruebas: ninguna.
- Checkpoint: quÃ© es `develop` frente a `main` y por quÃ© cada feature entra por Pull Request.

### Fase 1 â€” Entender EVM (sin cÃ³digo)
- Objetivo: aprender PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC con un ejemplo numÃ©rico; el usuario calcula uno a mano.
- Decisiones del usuario (con pros y contras): divisiÃ³n por cero (CPI con AC=0, EAC con CPI=0, SPI con PV=0), consolidaciÃ³n (sumar y recalcular vs promediar), Decimal vs float, porcentajes 0â€“100 vs 0â€“1, cÃ¡lculo al vuelo vs guardado.
- Se entrega: decisiones registradas en este plan; hechos en `AI_PROCESS.md`.
- Checkpoint: calcular a mano un caso completo e interpretar CPI y SPI.

### Fase 2 â€” CÃ¡lculos EVM puros
- Antes de programar: pregunta de la decisiÃ³n de arquitectura independiente (dÃ³nde viven los cÃ¡lculos, cÃ³mo se organizan las capas). El usuario responde primero.
- Objetivo: funciones puras (sin BD, sin FastAPI) que reciben nÃºmeros y devuelven indicadores e interpretaciones.
- Pruebas: unitarias con valores reales y casos borde (AC=0, sin actividades, avance real=0, avance planificado=0). Cobertura â‰¥80% con `--cov-fail-under=80`.
- Checkpoint: por quÃ© se consolida como se consolida y quÃ© devuelve el sistema con AC=0.

### Fase 3 â€” Base de datos
- Objetivo: tablas `projects` y `activities` en PostgreSQL, modelos SQLAlchemy, script `database/init.sql`, `.env` local.
- Pruebas: conexiÃ³n y creaciÃ³n de tablas.
- Checkpoint: relaciÃ³n proyecto â†’ actividades y quÃ© hace `DELETE` en cascada.

### Fase 4 â€” API
- Objetivo: CRUD de proyectos y actividades; endpoint de indicadores por actividad y consolidados con interpretaciÃ³n CPI/SPI. Capas: routers â†’ servicios â†’ repositorio/modelos. ValidaciÃ³n con Pydantic.
- DecisiÃ³n del usuario: cÃ³mo probar la API contra la BD.
- Pruebas: al menos un test de integraciÃ³n por endpoint validando el contrato y valores calculados.
- Checkpoint: quÃ© recibe y devuelve un endpoint y dÃ³nde estÃ¡ la lÃ³gica de negocio.

### Fase 5 â€” OpenAPI
- Objetivo: Swagger en `/api-docs` con descripciÃ³n, esquemas y cÃ³digos de error por endpoint.
- Pruebas: test que verifica que `/api-docs` responde y que `/openapi.json` incluye los endpoints.
- Checkpoint: quÃ© es un contrato de API.

### Fase 6 â€” Frontend
- Objetivo: React + Vite (JavaScript) + Recharts; formulario y tabla de actividades, consolidado, semÃ¡foro CPI/SPI, grÃ¡fica PV/EV/AC por actividad. Textos en espaÃ±ol.
- Pruebas: ESLint limpio; verificaciÃ³n manual de la demo (1 proyecto, 3 actividades).
- Checkpoint: de dÃ³nde salen los nÃºmeros que muestra la pantalla.

### Fase 7 â€” VerificaciÃ³n de nÃºmeros
- Objetivo: el usuario calcula a mano un proyecto con 3 actividades y lo compara con la API y la pantalla. Se anota en `AI_PROCESS.md`.

### Fase 8 â€” Release
- `release/1.0.0` desde `develop`, ajustes finales, merge a `main` (solo con confirmaciÃ³n explÃ­cita del usuario), tag `v1.0.0`, merge de vuelta a `develop`.

### Fase 9 â€” Documentos y video
- README con instrucciones para correr y el script de BD; `AI_PROCESS.md` completo (el usuario redacta sus desviaciones, razones, decisiÃ³n de arquitectura y reflexiÃ³n); guion del video; checklist final contra el PDF.

## QuÃ© se recorta si vamos tarde
1. Docker opcional (no se hace).
2. Fase 5 se fusiona con la 4.
3. La grÃ¡fica y el semÃ¡foro se hacen en su versiÃ³n mÃ¡s simple.
Lo que NO se recorta: cÃ¡lculos con pruebas, API, Gitflow con PR y release, README, `AI_PROCESS.md`, video.

## Decisiones registradas
(se completan durante la ejecuciÃ³n)
