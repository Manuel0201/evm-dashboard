# AI_PROCESS

Documento de proceso de la prueba técnica.

## 1. Herramientas de IA usadas y por qué

Para este ejercicio utilicé **Claude Code** como herramienta de inteligencia artificial. La elegí porque es con la que más he trabajado y con la que más cómodo me siento. Además, considero que es la que me entrega mejores resultados, y valoro la facilidad con la que se integra con los sistemas del proyecto y la ayuda que ofrece para organizarlo.

Mis expectativas eran claras. Esperaba que Claude Code me apoyara en la organización del proyecto, que me permitiera ser más eficiente y que me ayudara en la ejecución. Por mi parte, esperaba encargarme de la toma de decisiones sobre el proyecto y de definir la idea general de cómo hacerlo.

No utilicé ninguna otra herramienta de IA en este ejercicio.

## 2. Cómo aprendí EVM y cómo validé que entendí las fórmulas

Hechos registrados (Fase 1):

- Ejemplo 1: actividad con BAC=1000, avance planificado 50%, avance real 40%, AC=600. Cálculo a mano del usuario, antes de implementar: PV=500, EV=400, CV=-200, SV=-100, CPI=0.67, SPI=0.8; interpretación del usuario: sobre presupuesto y atrasado. Resultado esperado según las fórmulas del PDF: PV=500, EV=400, CV=-200, SV=-100, CPI=0.6667, SPI=0.8. Coincide.

- Ejemplo 1, continuación: el usuario calculó a mano EAC=1500 y VAC=-500 (BAC=1000, CPI=0.6667). Coincide con las fórmulas del PDF (EAC=BAC/CPI=1500; VAC=BAC-EAC=-500). El usuario preguntó cuánto se iba a pasar del presupuesto; la respuesta es el VAC: 500 sobre el presupuesto.

- Ejemplo 2, checkpoint de la Fase 1: actividad con BAC=2000, planificado 30%, real 45%, AC=800. El usuario calculó a mano PV=600, EV=900, CPI=1.125, SPI=1.5 (correcto). Al pedirle la interpretación y qué devuelve el sistema con AC=0, indicó que no conocía las definiciones; la IA le explicó las reglas (CPI/SPI mayor o menor que 1; null con AC=0) y luego el usuario interpretó correctamente el resultado (bajo presupuesto y adelantado) e indicó que con AC=0 el sistema devuelve null. Es decir: los cálculos los hizo solo; la interpretación la acertó después de la explicación.
- Checkpoint de la Fase 2: consolidado con A (BAC 500, EV 100, AC 200) y B (BAC 1500, EV 600, AC 400). Al inicio el usuario no supo responder y pidió una explicación; la IA explicó el método (sumar EV y AC y dividir) y el usuario calculó 700/600 ≈ 1,1666 (el sistema redondea half-up a 4 decimales: 1,1667). A la pregunta de por qué las fórmulas no dependen de la base de datos ni de la web, respondió que así las funciones se pueden reutilizar y el código se simplifica.
- Checkpoint de la Fase 3: ante "una actividad con 150% de avance real, ¿dónde se rechaza?", el usuario respondió que se rechaza, sin indicar dónde (la IA aclaró que hoy lo rechaza la base de datos con una restricción CHECK y que en la Fase 4 lo detendrá antes la validación del API). Ante "borras un proyecto con 3 actividades", respondió que se borran en cascada y que la decisión busca no dejar datos remanentes (correcto: evita actividades huérfanas).
- Checkpoint de la Fase 4: ante "indicadores de un proyecto que no existe", el usuario respondió 404 (correcto). Ante "dónde vive la lógica de consolidar", no supo responder la segunda parte; la IA explicó el recorrido router → servicio → cálculos. En la variante (si cambia la regla a promediar, qué capa se toca) indicó el archivo de cálculos evm.py (correcto; sin explicar el porqué).
- Checkpoint de la Fase 5: sobre qué significa que la documentación OpenAPI sea "un artefacto de comunicación", el usuario respondió que permite interactuar con la aplicación vía API más que solo documentar, y que es una página interactiva con funcionalidades. La IA aclaró que la parte correcta es que es interactiva (Try it out) y faltó la idea de contrato: define qué envía y qué recibe cada endpoint y qué errores puede dar, para que frontend y backend se pongan de acuerdo sin leer el código.
- Checkpoint de la Fase 6: el usuario corrigió a la IA (el número del CPI no se ve en rojo; lo rojo es la etiqueta) y ubicó correctamente que el texto "Sobre presupuesto" sale de la función de cálculo. A "cómo se enteran las tarjetas y la gráfica de un cambio" respondió que no sabía (la IA explicó que el frontend vuelve a pedir los datos al API). En la variante "si cambia una fórmula, ¿se toca el frontend?" respondió primero que el frontend tendría que modificar el cálculo (incorrecto: el frontend no calcula) y, tras la aclaración, indicó que la fórmula está en evm.py (correcto en el archivo; no explicó el porqué).
- Checkpoint de la Fase 8: ante "por qué hizo falta un segundo PR hacia develop" y "qué diferencia hay entre la rama release y el tag", el usuario respondió que no sabía en ambos casos; la IA explicó (develop quedaría atrasado respecto a main; la rama es de trabajo y el tag es una etiqueta fija sobre un commit). En la variante "para obtener exactamente lo entregado en 1.0.0, ¿rama o tag?" respondió que el tag v1.0.0 (correcto, sin explicar el porqué).
- Decisiones de negocio y de diseño tomadas durante el desarrollo: consolidar el proyecto sumando los montos y recalculando los índices; devolver `null` ("No calculable") en las divisiones por cero; usar `Decimal` para el dinero; manejar los porcentajes en escala 0 a 100; calcular los indicadores al vuelo sin guardarlos; organizar el backend en tres capas; y probar la API contra una base PostgreSQL de pruebas.

## 3. Dos decisiones donde no seguí lo que la IA sugirió

**Decisión 1: lenguaje del código.**
La IA me sugirió combinar idiomas en el proyecto. Decidí mantener un lenguaje único, claro y fácil de entender, para conservar la coherencia entre el frontend y el backend.

**Decisión 2: momento de la verificación de los resultados.**
La IA me recomendó hacer la verificación manual de los cálculos antes de publicar la primera versión. Decidí aplazarla hasta que el producto estuviera terminado, porque quería concentrarme primero en completar la aplicación. Cuando llegó el momento, calculé a mano un proyecto de tres actividades y comparé mis resultados con los del sistema.

## 4. Cómo verifiqué que los cálculos son correctos

Hechos de la verificación (Fase 7):

- Datos de la prueba: proyecto con tres actividades. A: BAC 1.500, planificado 60 %, real 50 %, AC 900. B: BAC 2.500, planificado 40 %, real 55 %, AC 1.200. C: BAC 1.000, planificado 20 %, real 0 %, AC 150.
- Antes del ejercicio, el usuario pidió la hoja de siglas y fórmulas y la IA se la entregó.
- Primer intento del usuario, calculado sin ver el resultado del sistema: BAC total 5000 y AC total 2250 correctos; PV y EV de cada actividad 100 veces más pequeños de lo correcto (por ejemplo, PV de A = 9 en vez de 900); y totales de PV y EV calculados sumando porcentajes (120 % y 105 %) y multiplicando por el BAC total (PV total 60, EV total 52,5), lo cual es incorrecto.
- La IA señaló los dos errores sin dar los resultados. Segundo intento del usuario: PV/EV por actividad 900/750, 1.000/1.375 y 200/0; totales PV 2.100, EV 2.125, AC 2.250; CPI 0,9444; SPI 1,0119; EAC 5.294,12; VAC -294,12; interpretación: sobre presupuesto y ligeramente adelantado. Ante la pregunta de la IA sobre cómo obtuvo esa respuesta, el usuario respondió que lo calculó él mismo; la IA no tiene forma de comprobarlo.
- Comparación con el sistema: se cargaron las mismas tres actividades en la API real y se consultó el consolidado. Resultado del sistema: PV 2100, EV 2125, CV -125, SV 25, CPI 0,9444, SPI 1,0119, EAC 5294,12, VAC -294,12, "Sobre presupuesto" y "Adelantado". Coinciden con el cálculo del usuario en todos los valores.
- Otras verificaciones automáticas: 103 pruebas del backend con valores calculados a mano (incluyen el consolidado del ejemplo y los casos AC=0, avance real=0, avance planificado=0 y proyecto sin actividades) y una verificación manual en el navegador con 3 actividades (Fase 6).

## 5. Una decisión de arquitectura tomada de forma independiente

Hechos (Fase 2): antes de recibir ninguna recomendación de la IA, se le preguntó al usuario cómo organizaría el código (recibir peticiones, calcular EVM, base de datos). Su respuesta fue que lo mejor era separar la lógica para facilitar el mantenimiento y el entendimiento, y que la lógica de cada indicador podía ser independiente, porque un cambio en uno podría afectar a los demás; por eso convenía mantener las fórmulas por separado.

Después de oír dos alternativas (dos capas o tres capas), el usuario eligió tres capas, que coincide con la recomendación de la IA.

Mi decisión fue separar la lógica del proyecto en tres capas: routers, servicios y cálculos. Consideré que era la mejor opción para mantener un código limpio y reutilizable, fácil de mantener y de corregir cuando sea necesario. Además, quise que la lógica de negocio no viviera en los controladores, para evitar que se complicara, y por eso separé las funciones de los servicios.

## 6. Reflexión honesta: qué haría diferente

Si repitiera el ejercicio, dedicaría más tiempo a la presentación del producto, porque considero que es importante de cara a lo que se quiere entregar. El plazo de la prueba es adecuado; sin embargo, por mis labores, ya que actualmente trabajo, no pude aprovecharlo completo y tuve que limitar el alcance a unas pocas horas en la noche para poder cumplir con el entregable.

De haber contado con el plazo completo, habría hecho un diseño más robusto, con validaciones más amplias, y una interfaz visual más agradable, completa e intuitiva.
