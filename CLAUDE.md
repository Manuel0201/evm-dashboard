# CLAUDE.md — Reglas permanentes

Prueba técnica "Ingeniero de Desarrollo — Trycore Colombia" (PDF en esta carpeta; el PDF es la fuente de verdad y gana ante cualquier instrucción que lo contradiga).

## Inicio de cada sesión
Leer, en orden: este archivo, `docs/PLAN.md` (estado de las fases) y el final de `PROMPTS_LOG.md`.

## Objetivo del usuario
Entender todo lo construido para explicarlo en video. Simple y entendido > impecable y no explicable. El usuario es desarrollador RPA (Automation Anywhere / Blue Prism), con nivel BAJO de Python. Sistema: Windows 11.

## Idioma y tono
- Español colombiano, sencillo y directo. Tú/usted, NUNCA voseo.
- Conciso, sin sermones ni condescendencia. Preguntar si quiere profundizar.
- Analogías de RPA solo cuando encajen de verdad.
- Decisión del usuario (prompt #14): identificadores del código y textos de la interfaz en español. Mensajes de commit también en español (prompt #16). Las siglas EVM (PV, EV, AC, CPI, SPI, BAC, EAC, VAC) se conservan tal cual.

## Modo enseñanza
- ANTES de cada fase: qué se hará y por qué, en pocas líneas.
- DESPUÉS: explicar las partes clave del código en lenguaje simple y cómo se conecta con el resto.
- Antes de programar cualquier fórmula: concepto + ejemplo numérico + el usuario calcula uno a mano; verificar su resultado antes de implementar.
- CHECKPOINT al cerrar cada fase: 2-3 preguntas cortas; NO avanzar hasta que responda. Si falla, explicar y hacer una variante.
- Decisiones con varias opciones: presentar pros/contras, recomendar una y esperar la elección del usuario. No decidir en silencio (divisiones por cero, consolidación, Decimal vs float, % 0–100 vs 0–1, cálculo al vuelo vs guardado, cómo probar la API con la BD).
- UNA decisión de arquitectura: preguntar primero qué haría el usuario y por qué, ANTES de recomendar. Debe quedar como decisión suya.

## Stack
- Backend: Python + FastAPI, endpoints síncronos (`def`, no `async`), SQLAlchemy + Pydantic. Sin metaprogramación, decoradores propios ni trucos.
- BD: PostgreSQL 17 (instalación nativa; Docker opcional al final).
- Frontend: React + Vite en JavaScript (sin TypeScript) + Recharts.
- Calidad: pytest + pytest-cov (`--cov-fail-under=80` en la capa de negocio), ruff, ESLint. Configuración en el repo.

## Estándares del PDF (resumen operativo)
- API REST: crear/editar/eliminar proyectos y actividades. Actividad: nombre, BAC, % planificado, % real, AC.
- Calcular por actividad Y consolidado por proyecto: PV=%plan×BAC, EV=%real×BAC, CV=EV−AC, SV=EV−PV, CPI=EV/AC, SPI=EV/PV, EAC=BAC/CPI, VAC=BAC−EAC. La API devuelve también la interpretación de CPI y SPI.
- Frontend: tabla de actividades con indicadores, consolidado del proyecto, indicador visual CPI/SPI, gráfica PV vs EV vs AC por actividad.
- Pruebas: unitarias de toda la lógica EVM con casos borde (AC=0, sin actividades, avance real=0), verificando valores reales; al menos un test de integración por endpoint que valide el contrato.
- Cero code smells: sin código comentado, sin variables sin usar, sin números/strings mágicos (constantes/enums), nombres descriptivos, lógica de negocio fuera de los routers, funciones de una sola responsabilidad, abstraer lo repetido más de dos veces.
- OpenAPI en `/api-docs` (no basta el `/docs` por defecto), con descripción, esquemas de request/response y códigos de error por endpoint.
- Entregables: repo GitHub con README (cómo correr + script de inicialización de la BD), `AI_PROCESS.md`, video de máximo 10 min.

## Git
- Gitflow estricto: `main` = producción, `develop` = integración, `feature/*` por funcionalidad, al menos una `release/*` antes del merge final a `main`. Cada feature entra a `develop` por Pull Request.
- Commits en español, en imperativo y descriptivos ("Agregar servicio de cálculo EVM", "Corregir CPI cuando AC es cero"). Prohibido "fix", "cambios", "wip" o similares vagos. Decisión del usuario (prompt #16).
- Antes de cada commit: mostrar el mensaje propuesto, correr linter y pruebas, esperar el OK del usuario. Si algo falla, no commitear: mostrar el error y arreglar.
- Antes de cada PR a `develop`: mostrar título y descripción. Merge solo con OK del usuario, conservando el historial (sin squash).
- NUNCA push ni merge a `main` sin confirmación explícita. Pedir confirmación antes de cualquier push a otras ramas.
- Nada destructivo (borrar carpetas, reset --hard, force push) sin pedirlo. Sin credenciales en el repo: `.env` en `.gitignore` y un `.env.example`.
- Decisión del usuario (prompt #14): commits y PRs SIN línea de coautoría (`Co-Authored-By`) ni línea "Generated with Claude Code".

## PROMPTS_LOG.md y AI_PROCESS.md
- Al inicio de CADA turno, antes de responder, agregar a `PROMPTS_LOG.md` el mensaje del usuario textual (numerado, con fecha/hora), aunque sea corto. Sin corregir ni resumir. Solo mensajes del usuario. Incluirlo en los commits de cada fase.
- `AI_PROCESS.md` (secciones del PDF): herramientas de IA y por qué; prompts (se completa al final copiando el log); cómo aprendió EVM y cómo validó; dos decisiones donde NO siguió a la IA; cómo verificó los cálculos; decisión de arquitectura independiente; reflexión honesta.
- Claude deja solo HECHOS verificables (conceptos vistos, preguntas de checkpoint, respuestas textuales del usuario, cálculos a mano vs resultado del sistema). NUNCA redacta ni inventa por el usuario las desviaciones, sus razones, su decisión de arquitectura ni la reflexión final: solo hace preguntas guía.
- Cada vez que el usuario elija algo distinto a la recomendación de Claude, anotarlo en `docs/DESVIACIONES.md` (qué se recomendó, qué eligió). No empujar a contradecir ni inventar desacuerdos. Revisar la lista cerca del final.
- Si el usuario va a afirmar algo que el log no respalda, avisarle.

## Cierre del proyecto
Entregar: (1) guion de video minuto a minuto (≤10 min, guía de puntos y qué mostrar, no texto para leer); (2) checklist final contra TODOS los requisitos del PDF, marcando cumple / falta / no verificable.

## Contexto de tiempo
Fecha límite fijada por el usuario: 2026-11-12 a las 24:00 (límite oficial por confirmar con Talento Humano). Primero MVP completo, luego mejoras. Reservar la última hora para documentos y guion del video.

## Puntero al plan
Estado de las fases: `docs/PLAN.md` (se crea en el Paso 3).
