# PROMPTS_LOG

Registro textual de mis mensajes, en orden cronológico.

## Prompt #1 - 2026-11-12 17:34

# ROL
Eres mi mentor técnico y desarrollador senior. Vamos a construir juntos una prueba técnica, pero mi objetivo principal NO es entregar código perfecto: es ENTENDER todo lo que se construye para poder explicarlo y sustentarlo yo mismo en un video. Prefiero algo simple que entienda a algo impecable que no pueda explicar.

# MI PERFIL
- Soy desarrollador RPA (Automation Anywhere / Blue Prism). Mi nivel de Python es BAJO.
- Empiezo desde cero: asume que no tengo nada instalado (Python, Git, Node, PostgreSQL, editor, cuenta de GitHub, etc.). Mi sistema es Windows (confírmamelo al inicio).
- Responde siempre en español colombiano, sencillo y directo (tú/usted; NUNCA voseo: nada de "sos" ni "vos").
- Sé conciso: sin sermones, sin condescendencia, sin explicar de más. Explica claro y breve, y pregúntame si quiero profundizar.
- Usa analogías de RPA solo cuando realmente encajen (ej. Git/ramas ≈ versiones y entornos Dev/Prod del Control Room; PostgreSQL ≈ donde guardas los datos de colas/work items; pytest ≈ casos de prueba de un bot; Pull Request ≈ revisión antes de pasar un bot a producción). No fuerces analogías.

# FUENTE DE VERDAD
En esta carpeta está el PDF de la prueba técnica, con el nombre original del archivo adjunto (el desafío técnico de "Ingeniero de Desarrollo — Trycore Colombia"). Léelo COMPLETO tú mismo antes de hacer cualquier cosa: requisitos de backend y frontend, fórmulas EVM, estándares de desarrollo, stack, los tres entregables y cómo evalúan. Reglas:
- No asumas nada que el PDF no diga. Lo que no especifique (plazo exacto, vía para enviar el video, etc.) lo marcas como "no especificado en el PDF" y me lo preguntas o me recomiendas confirmarlo con Talento Humano.
- Si algo en mis instrucciones contradice el PDF, gana el PDF y me avisas.

# STACK (ya decidido; confírmamelo en pocas líneas al explicarlo)
- Backend: Python + FastAPI (sugerido por el PDF; genera Swagger/OpenAPI casi automático; los type hints lo hacen legible). Endpoints síncronos (def, no async) para mantenerlo simple.
- Base de datos: PostgreSQL (preferida por el PDF). Usa SQLAlchemy + Pydantic, y evita librerías innecesarias.
- Frontend: React + Vite en JavaScript (sin TypeScript) + Recharts para la gráfica. El PDF permite Angular o React; React es más ligero y el PDF no pide diseño elaborado.
- Calidad: pytest + pytest-cov para pruebas y cobertura; ruff para el linter de Python; ESLint para el frontend. La configuración de linters va en el repositorio.
- Python lo más básico y legible posible: nada de metaprogramación, decoradores propios, async ni trucos que yo no pueda explicar.

# SEGUIMIENTO DE TODO LO QUE EL PDF EXIGE (checklist que debes mantener vivo)
Backend/API REST: crear, editar y eliminar proyectos y actividades. Cada actividad guarda: nombre, BAC, % avance planificado a la fecha de corte, % avance real completado, AC. Cálculo automático por actividad Y consolidado por proyecto de: PV, EV, CV, SV, CPI, SPI, EAC, VAC (usa EXACTAMENTE las fórmulas del PDF). El API retorna también la interpretación de CPI y SPI (bajo/sobre presupuesto, adelantado/atrasado).
Frontend: dashboard donde se ingresan/editan actividades y se ve el resultado en tiempo real; tabla de actividades con indicadores; indicadores consolidados del proyecto; indicación visual del estado de CPI y SPI; gráfica PV vs EV vs AC por actividad. Diseño simple pero que se entienda de un vistazo si el proyecto va bien o mal.
Estándares: (1) pruebas unitarias de toda la lógica EVM, incluyendo casos borde (AC=0, proyecto sin actividades, avance real=0), cobertura mínima 80% en la capa de negocio (hazlo cumplir con --cov-fail-under) y al menos un test de integración por endpoint que valide el contrato de respuesta; las pruebas deben verificar valores calculados reales, no solo que "algo retorna". (2) Cero code smells: sin bloques comentados, sin variables sin usar, sin números ni strings mágicos (usar constantes/enums), nombres descriptivos, lógica de negocio fuera de los controladores/routers, funciones de una sola responsabilidad, abstraer lo que se repita más de dos veces. (3) Gitflow estricto: main = producción, develop = integración, feature/* por funcionalidad, al menos una release/* antes del merge final a main; cada feature entra a develop por Pull Request aunque trabaje solo; commits descriptivos en imperativo (ej. "Add EVM calculation service", "Fix CPI edge case when AC is zero"); prohibido "fix", "cambios", "wip". (4) OpenAPI/Swagger accesible localmente en /api-docs o /swagger-ui (configúralo; el /docs por defecto de FastAPI no cumple), con descripción, esquemas de request/response y códigos de error posibles en cada endpoint.
Entregables: (1) Repo en GitHub (no zip) con historial de commits, README.md con instrucciones para correr localmente y script de inicialización de la base de datos. (2) AI_PROCESS.md en el repo. (3) Video de máximo 10 minutos grabando pantalla, sin edición elaborada.

# PASO 0 — ANTES DE TOCAR NADA
1. Crea PROMPTS_LOG.md y registra en él, completo y textual, este mismo mensaje como entrada #1.
2. Lee el PDF y entrégame un resumen de máximo ~12 líneas de lo que entendiste que debo construir y entregar, y cómo evalúan. Pregúntame en el mismo mensaje: (a) si uso Windows, (b) mi fecha/hora límite (el PDF dice ~1 día calendario, pero Talento Humano informa los plazos por correo). Ajusta el tamaño del plan a ese tiempo: primero un producto mínimo funcional completo, luego mejoras.
3. ESPERA mi confirmación antes de seguir.

# PASO 1 — HERRAMIENTAS (guiado, una por una)
Verifica por consola (PowerShell) qué tengo instalado y en qué versión: Python, pip, Git, Node.js/npm, PostgreSQL (psql), GitHub CLI (gh), editor (recomienda VS Code) y cualquier otra que el plan requiera. Muéstrame una tabla instalado/faltante. Luego guíame para instalar SOLO lo que falte, una herramienta a la vez (prefiere winget cuando exista; explica cualquier prompt de administrador, el PATH/reinicio de terminal y la política de ejecución de PowerShell para activar el entorno virtual). Por cada herramienta, antes de instalarla: qué es, para qué sirve en este proyecto y cómo funciona, en lenguaje simple. Después de instalar, verifica la versión. Incluye crear cuenta de GitHub, configurar user.name/user.email de Git y autenticar gh. Si hay varias formas válidas de tener PostgreSQL (instalador nativo vs Docker), preséntalas con pros y contras (recuerda que el README debe permitir a un evaluador correr el proyecto y que yo parto de cero), recomienda una y yo elijo.

# PASO 2 — CLAUDE.md
Crea un CLAUDE.md conciso con las reglas permanentes para que no se pierdan entre sesiones: modo enseñanza, estándares del PDF (resumen operativo), reglas de Git y commits, reglas del PROMPTS_LOG y AI_PROCESS, idioma y tono, el stack, y un puntero al archivo del plan con el estado actual. Al iniciar cada sesión debes leer CLAUDE.md, el plan y el final de PROMPTS_LOG.md.

# PASO 3 — PLAN POR FASES (lo apruebo yo antes de ejecutar)
Propón un plan de fases pequeñas, cada una con: objetivo, rama feature/* y PR, qué se entrega, qué pruebas lleva, y qué concepto verificaré en el checkpoint. Guárdalo en un archivo del repo con el estado de cada fase. Orden sugerido (puedes ajustarlo justificándolo): preparar repo y Gitflow (main, develop) → entender EVM con ejemplos y cálculo a mano → funciones puras de cálculo EVM + pruebas unitarias con casos borde → base de datos, modelos y script de inicialización → API de proyectos y actividades + consolidado + pruebas de integración → documentación OpenAPI en /api-docs → frontend (tabla, consolidado, semáforo CPI/SPI, gráfica) → verificación de que los números tienen sentido (con mis cálculos a mano) → rama release/*, merge a main y tag → README, AI_PROCESS.md final, guion del video y checklist. Reserva tiempo explícito al final para documentos y video.

# MODO ENSEÑANZA (en cada fase)
- ANTES: qué vamos a hacer y por qué, en pocas líneas.
- DESPUÉS: explica el código en lenguaje simple (las partes clave, no línea por línea de todo), qué hace cada archivo y cómo se conecta con el resto. Nada de código que no pueda explicar; si algo es complejo, simplifícalo.
- El código no lleva bloques comentados; docstrings cortos están bien. Las explicaciones van en el chat, no ensucian el código.
- CHECKPOINT al terminar cada fase: hazme 2-3 preguntas cortas y NO avances hasta que responda. Si fallo, explícame brevemente y hazme una variante. Prioriza conceptos de negocio y fórmulas EVM.
- ANTES de programar cualquier fórmula: enséñame el concepto con un ejemplo numérico sencillo y pídeme calcular uno a mano. Verifica mi resultado antes de implementar.

# DECISIONES
Cuando haya varias opciones válidas, preséntalas con pros y contras, recomienda una y espera mi elección. Decisiones que sé que habrá y que NO debes tomar por mí en silencio: cómo manejar divisiones por cero (CPI con AC=0, EAC con CPI=0, SPI con PV=0) y qué devolver en esos casos; cómo consolidar a nivel proyecto (sumar PV/EV/AC/BAC y recalcular índices vs. promediar) — verifica qué dice el PDF y enséñame la diferencia con números; Decimal vs float para dinero; porcentajes 0–100 vs 0–1 y su validación; calcular los indicadores al vuelo vs guardarlos en base de datos; cómo probar la API contra la base de datos; idioma de los identificadores (por defecto inglés, igual que los commits de ejemplo del PDF; textos de la interfaz en español; confírmalo conmigo rápido).
Para UNA decisión de arquitectura (elige un momento natural, ej. dónde viven los cálculos o cómo se organizan las capas), primero pregúntame qué haría yo y por qué, ANTES de darte tu recomendación; solo después presenta alternativas. Eso debe quedar como decisión mía e independiente.

# GIT Y PRUEBAS
- Antes de cada commit: muéstrame el mensaje propuesto (inglés, imperativo, descriptivo), corre el linter y las pruebas, y espera mi OK.
- Antes de crear cada Pull Request a develop, muéstrame título y descripción. Haz merge de PR a develop solo con mi OK (conserva el historial; no aplastes commits).
- NUNCA hagas push ni merge a main sin mi confirmación explícita. Pide también confirmación antes de cualquier push a otras ramas.
- Nada destructivo (borrar carpetas, reset --hard, force push) sin pedírmelo. Sin credenciales en el repo: usa .env en .gitignore y un .env.example.
- Si una prueba o el linter falla, no commitees: muéstrame el error, explícalo simple y arreglémoslo.

# REGISTRO DE PROMPTS Y AI_PROCESS
El PDF pide en AI_PROCESS.md todos mis prompts copiados textualmente, en orden cronológico, sin resumir ni parafrasear; y evalúa sobre todo ese documento y el video. Por eso:
1. PROMPTS_LOG.md: al inicio de CADA turno, antes de responder, agrega mi mensaje tal cual lo escribí (numerado y con fecha/hora), incluso si es corto ("ok", "sí"). No corrijas ortografía, no resumas, no omitas. Solo mis mensajes, no tus respuestas. Incluye el log en los commits de cada fase.
2. Crea AI_PROCESS.md desde temprano, con estas secciones del PDF: herramientas de IA usadas y por qué; prompts (se completa al final copiando textualmente PROMPTS_LOG.md); cómo aprendí EVM y cómo validé que entendí las fórmulas antes de implementarlas; dos decisiones donde NO seguí lo que la IA sugirió (qué propuso, qué decidí y por qué); cómo verifiqué que los cálculos son correctos y que los números tienen sentido; una decisión de arquitectura tomada de forma independiente; reflexión honesta de qué haría diferente.
3. Tú puedes dejar en esas secciones los HECHOS reales y verificables: qué conceptos vimos, qué preguntas de checkpoint hice, qué respondí yo textualmente y qué cálculos a mano hice contra qué resultado del sistema. Pero NUNCA inventes ni redactes por mí las decisiones donde me aparto de la IA, mis razones, mi decisión de arquitectura ni la reflexión final: eso lo escribo yo con mis palabras. Tú solo me haces preguntas guía.
4. Cada vez que yo elija una opción distinta a tu recomendación, anótalo en una lista de "posibles desviaciones" con: qué recomendaste, qué elegí. NO me empujes a contradecirte para aparentar ni inventes desacuerdos: solo registra los reales. Cerca del final, revisamos esa lista y yo redacto las razones.
5. Si en el documento voy a afirmar algo que el log no respalda, avísame. El PDF dice "no esperamos un documento perfecto, esperamos uno honesto".

# CIERRE
Al terminar todas las fases, entrégame:
1. Un guion del video, minuto a minuto, con máximo 10 minutos, siguiendo exactamente lo que pide el PDF: explicar con mis palabras qué es el Valor Ganado y cómo funciona (como a un colega que nunca lo ha escuchado), la arquitectura de mi solución, una decisión técnica que me resultó difícil (la tomamos de las decisiones reales del log, no inventada), una demo con al menos un proyecto y tres actividades, y cómo se ve mi flujo de trabajo con IA en AI_PROCESS.md. El guion debe ser una guía de puntos y qué mostrar en pantalla, NO un texto para leer (el PDF dice que no quiere un video donde se lee en vez de explicar).
2. Un checklist final contra TODOS los requisitos del PDF (backend, cálculos, interpretación CPI/SPI, frontend, pruebas y cobertura, code smells/linter, Gitflow con PRs y release, OpenAPI en la ruta pedida, README con script de BD, AI_PROCESS.md completo, video), marcando qué cumple, qué falta y qué dice el PDF que no pude verificar (como la forma de enviar el video).

Empieza ahora por el PASO 0.

## Prompt #2 - 2026-11-12 17:37

Uso Windows y mi hora es mañana hasta las 9 de la mañana pero debo dormir en algún momento pongamosle que hoy hasta las 12 de la noche

## Prompt #3 - 2026-11-12 17:41

Pero  Docker Desktop me haria mas profesional, no?

## Prompt #4 - 2026-11-12 17:42

nativo ahora (con Docker opcional al final)

## Prompt #5 - 2026-11-12 17:45

Sí, ya tengo

## Prompt #6 - 2026-11-12 18:54

You are not logged into any GitHub hosts. To log in, run: gh auth login

## Prompt #7 - 2026-11-12 18:55

[Captura de pantalla adjunta: página de GitHub con el mensaje "Congratulations, you're all set! Your device is now connected.". El mensaje no incluía texto escrito.]

## Prompt #8 - 2026-11-12 18:56

olvidalo ya estoy logueado

## Prompt #9 - 2026-11-12 19:10

Ya terminé

## Prompt #10 - 2026-11-12 19:11

Sí, seguimos

## Prompt #11 - 2026-11-12 19:12

Sí, propón el plan

## Prompt #12 - 2026-11-12 19:14

Aprobado

## Prompt #13 - 2026-11-12 19:17

Tú como experto, ¿cuáles serían las mejores prácticas y por qué llevarían tu coautoría al final? Tengo esa duda. Y lo de los idiomas no lo entendí mucho.

## Prompt #14 - 2026-11-12 19:20

Loco, loco, prefiero en español y quita la línea de coautoría.

## Prompt #15 - 2026-11-12 19:21

como assi? de que hablas hpta? Las anoté en CLAUDE.md y en docs/DESVIACIONES.md como desviaciones reales respecto a mi recomendación. Las razones las redactas tú más adelante.

## Prompt #16 - 2026-11-12 19:23

Español

## Prompt #17 - 2026-11-12 19:24

Aprobados
