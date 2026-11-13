# AI_PROCESS

Documento de proceso de la prueba técnica. Las secciones marcadas "lo escribe el usuario" las redacta Manuel con sus propias palabras.

## 1. Herramientas de IA usadas y por qué

Hechos: se usó Claude Code (modelo Claude Sonnet 5.5) dentro de la app de escritorio de Claude, como mentor y asistente de programación.

Por qué elegí esta herramienta: _lo escribe el usuario_.

## 2. Prompts enviados

Se completa al final copiando textualmente `PROMPTS_LOG.md`, en orden cronológico.

## 3. Cómo aprendí EVM y cómo validé que entendí las fórmulas

Hechos registrados (Fase 1):

- Ejemplo 1 (prompt #23): actividad con BAC=1000, avance planificado 50%, avance real 40%, AC=600. Cálculo a mano del usuario, antes de implementar: PV=500, EV=400, CV=-200, SV=-100, CPI=0.67, SPI=0.8; interpretación del usuario: "sobrepresupuesto y atrasado". Resultado esperado según las fórmulas del PDF: PV=500, EV=400, CV=-200, SV=-100, CPI=0.6667, SPI=0.8. Coincide.

- Ejemplo 1, continuación (prompt #24): el usuario calculó a mano EAC=1500 y VAC=-500 (BAC=1000, CPI=0.6667). Coincide con las fórmulas del PDF (EAC=BAC/CPI=1500; VAC=BAC-EAC=-500). El usuario preguntó "cuánto me voy a terminar pasando"; la respuesta es el VAC: 500 sobre el presupuesto.

- Ejemplo 2, checkpoint de la Fase 1 (prompts #30 y #31): actividad con BAC=2000, planificado 30%, real 45%, AC=800. El usuario calculó a mano PV=600, EV=900, CPI=1.125, SPI=1.5 (correcto). Al pedirle la interpretación y qué devuelve el sistema con AC=0, respondió que no sabía las definiciones; la IA le explicó las reglas (CPI/SPI mayor o menor que 1; null con AC=0) y luego el usuario respondió "Bajo presupuesto y adelantado; con AC=0 devuelve null" (correcto). Es decir: los cálculos los hizo solo; la interpretación la acertó después de la explicación.
- Checkpoint de la Fase 2 (prompts #37 y #38): consolidado con A (BAC 500, EV 100, AC 200) y B (BAC 1500, EV 600, AC 400). El usuario no supo responder al inicio ("No sé la respuesta, explícame"); la IA explicó el método (sumar EV y AC y dividir) y el usuario calculó 700/600 = "1.1666" (el sistema redondea half-up a 4 decimales: 1.1667). A la pregunta de por qué las fórmulas no dependen de la base de datos ni de la web, respondió: "las funciones se pueden reutilizar y simplifica el codigo".
- Checkpoint de la Fase 3 (prompt #45): ante "una actividad con 150% de avance real, ¿dónde se rechaza?", el usuario respondió "lo rechaza" (sin indicar dónde; la IA aclaró que hoy lo rechaza la base de datos con una restricción CHECK y que en la Fase 4 lo detendrá antes la validación del API). Ante "borras un proyecto con 3 actividades", respondió "se borran en cascada y la decicion es para no dejar remanentes?" (correcto: evita actividades huérfanas).
- Checkpoint de la Fase 4 (prompts #50 y #51): ante "indicadores de un proyecto que no existe", el usuario respondió "404" (correcto). Ante "dónde vive la lógica de consolidar", respondió "la segunda no sé"; la IA explicó el recorrido router → servicio → cálculos. En la variante (si cambia la regla a promediar, qué capa se toca) respondió "En cálculos evm.py." (correcto; sin explicar el porqué).
- Decisiones de negocio tomadas en la Fase 1: ver `docs/PLAN.md`, sección "Decisiones registradas" (consolidación, división por cero, Decimal, escala 0–100, cálculo al vuelo).

## 4. Dos decisiones donde no seguí lo que la IA sugirió

_Lo escribe el usuario. Insumo: `docs/DESVIACIONES.md`._

## 5. Cómo verifiqué que los cálculos son correctos

_Pendiente (Fase 7)._

## 6. Una decisión de arquitectura tomada de forma independiente

Hechos (Fase 2): antes de recibir ninguna recomendación de la IA, se le preguntó al usuario cómo organizaría el código (recibir peticiones, calcular EVM, base de datos). Su respuesta textual (prompt #32): "Ok, lo mejor es hacer lógica separada para un fácil mantenimiento y fácil entendimiento también de las situaciones. Em, La lógica de negocio por cada indicador puede ser independiente, teniendo en cuenta que si cambian algún punto, esto puede afectar a los demás. Entonces es mejor mantener la lógica, las fórmulas por separado. Las pondría, ¿dónde las pondría? Ni siquiera sé dónde se ponen las cosas. O sea, estoy tan perdido que no sé ni dónde van las cosas, dónde va cada cosa."

Después de oír dos alternativas (dos capas o tres capas), el usuario eligió "Tres capas" (prompt #33), que coincide con la recomendación de la IA. _La decisión final y sus razones las escribe el usuario._

## 7. Reflexión honesta: qué haría diferente

_Lo escribe el usuario._
