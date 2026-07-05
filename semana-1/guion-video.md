# Guion del video — Semana 1 (duración objetivo: 4 minutos)

> Rúbrica cubierta: comprensión del desafío, uso de literatura científica,
> explicación de soluciones, reflexión crítica, comunicación oral.
> Citar explícitamente los artículos durante la exposición.

## Escena 1 — Presentación y desafío (0:00–0:50)

«Hola, mi nombre es [nombre]. En este video analizaré un desafío abierto en el
ámbito de los sistemas ciberfísicos: la **seguridad y la privacidad en sistemas de
videovigilancia con reconocimiento facial**.

Un CPS acopla cómputo, comunicación y procesos físicos. Ese acoplamiento hace que
un ataque lógico tenga consecuencias físicas: en un control de acceso, engañar al
reconocimiento facial equivale a abrir la puerta. Y hay un agravante: el dato que
sensamos es **biométrico**. Una contraseña filtrada se cambia; un rostro filtrado,
no.»

## Escena 2 — Por qué es un problema de CPS (0:50–1:30)

«Según la encuesta de **Humayed y colegas, publicada en 2017 en IEEE Internet of
Things Journal**, las contramedidas tradicionales de TI no se trasladan bien a los
CPS por tres razones: los nodos tienen recursos restringidos, los requisitos de
tiempo real desaconsejan criptografía pesada, y existe una gran heterogeneidad de
protocolos. A esto se suma la escala —miles de cámaras replican una misma
vulnerabilidad— y una regulación creciente sobre datos biométricos.»

## Escena 3 — Soluciones en la literatura (1:30–3:00)

«¿Qué propone la comunidad? Destaco dos líneas.

Primera: el **reconocimiento facial con preservación de privacidad**. **Erkin y
colegas, en PETS 2009**, demostraron que se puede ejecutar el algoritmo de
eigenfaces sobre datos **cifrados homomórficamente**: el servidor identifica el
rostro sin ver nunca la imagen. La ventaja es que ofrece garantías formales; la
limitación, su costo: es impracticable en un microcontrolador y su latencia se mide
en segundos, incompatible con el tiempo real de un CPS.

Segunda: el **procesamiento en el borde**. **Chen y Ran, en Proceedings of the IEEE
2019**, muestran que ejecutar la inferencia en el propio nodo reduce la latencia y
minimiza la exposición: la imagen no viaja por la red, solo se transmite el
resultado. Es factible hoy con hardware de bajo costo, pero desplaza el problema:
la base biométrica queda en el dispositivo y exige protección física y
actualizaciones seguras.»

## Escena 4 — Reflexión crítica y cierre (3:00–4:00)

«Mi reflexión: estas soluciones son **complementarias, pero insuficientes por sí
solas**. Siguen abiertos la verificación de extremo a extremo, la detección de
suplantación con recursos de borde, y una tensión de diseño entre trazabilidad y
minimización de datos.

Las líneas que considero más prometedoras son la inferencia eficiente en el borde,
la biometría cancelable y, sobre todo, tratar la privacidad y la oportunidad de la
respuesta como **atributos de calidad modelados desde el diseño temprano**, tal
como propone la orientación a agentes. Esa es precisamente la aproximación que
seguiré en el caso de estudio del curso: un sistema de videovigilancia con
identificación facial desarrollado con un proceso dirigido por modelos.

Muchas gracias.»
