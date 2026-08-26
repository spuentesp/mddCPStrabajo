# Actividad Semana 1 — Desafíos abiertos en Sistemas Ciberfísicos

**Desafío seleccionado:** *Seguridad y privacidad en sistemas ciberfísicos de
videovigilancia con reconocimiento facial.*

**Entregables:** video individual de 3–5 minutos (guion en `guion-video.md`) y
presentación de apoyo (`../slides/semana-1/presentacion.html` → `.pdf`; ver
`README.md` de esta carpeta para la versión canónica y las alternativas).

---

## 1. Descripción del desafío

### 1.1 ¿En qué consiste?

Los CPS acoplan estrechamente el cómputo, la comunicación y el control con procesos
físicos. Esta integración amplía la superficie de ataque respecto de los sistemas de
información tradicionales: un compromiso lógico (ciberataque) puede producir
consecuencias físicas (apertura indebida de una puerta, desactivación de una alarma),
y un compromiso físico (manipulación del sensor) puede corromper la capa lógica.
Humayed, Lin, Li y Luo (2017) sistematizan esta problemática y muestran que las
contramedidas clásicas de TI resultan insuficientes en CPS debido a tres factores:
recursos de cómputo restringidos en los nodos, requisitos de tiempo real que
desaconsejan criptografía pesada, y heterogeneidad de protocolos y dispositivos.

En el caso particular de la videovigilancia con reconocimiento facial, el desafío se
agrava porque el dato sensado es un **dato biométrico**: la imagen del rostro
identifica de manera única y permanente a una persona. A diferencia de una
contraseña, un rostro filtrado no puede revocarse. El desafío abierto es, entonces,
doble: (i) proteger el CPS frente a ataques que exploten el acoplamiento
ciber-físico y (ii) garantizar la **privacidad** de los datos biométricos que el
sistema captura, procesa y transmite.

### 1.2 ¿Por qué representa un problema relevante para los CPS?

- **Consecuencias físicas directas:** en un control de acceso, una identificación
  falsificada (p. ej., *spoofing* con una fotografía) produce una intrusión física.
- **Tensión entre seguridad y tiempo real:** cifrar y anonimizar tiene costo
  computacional, en conflicto con la restricción de responder dentro de intervalos
  dictados por el entorno (Lee, 2006).
- **Regulación y confianza social:** el tratamiento de datos biométricos está
  crecientemente regulado (p. ej., GDPR en Europa; Ley 19.628 y su actualización en
  Chile), y su vulneración erosiona la aceptación social de los CPS.
- **Escala:** las cámaras inteligentes se despliegan por miles; una vulnerabilidad
  se replica en toda la flota (Zanero, 2017).

## 2. Soluciones propuestas en la literatura

### 2.1 Enfoques

1. **Taxonomías y defensa por capas (perspectiva del desafío).** Humayed et al.
   (2017) proponen analizar la seguridad CPS desde tres ejes —seguridad de la
   información, del control y de la infraestructura— y por dominios de aplicación,
   derivando contramedidas específicas por capa (percepción, transmisión,
   aplicación).
2. **Reconocimiento facial con preservación de privacidad.** Erkin et al. (2009)
   demuestran que es posible ejecutar el algoritmo de *eigenfaces* sobre datos
   cifrados mediante cifrado homomórfico y protocolos de cómputo seguro entre dos
   partes: el servidor identifica si un rostro está en la lista de vigilancia sin
   conocer la imagen ni el resultado, y el cliente no aprende nada sobre la base de
   datos. Es la línea de *privacy-preserving face recognition*.
3. **Procesamiento en el borde (edge computing).** Chen y Ran (2019) sistematizan
   cómo ejecutar inferencia de aprendizaje profundo en el borde reduce la latencia y
   la exposición de datos: si la identificación ocurre en el propio nodo de cámara,
   la imagen no viaja por la red y solo se transmite el resultado mínimo necesario
   (principio de minimización de datos).

### 2.2 Ventajas y limitaciones

| Enfoque | Ventajas | Limitaciones |
|---|---|---|
| Defensa por capas (Humayed et al., 2017) | Visión integral; orienta contramedidas por dominio | Es un marco de análisis, no una solución operativa; no resuelve el costo de la criptografía en nodos restringidos |
| Cripto. homomórfica (Erkin et al., 2009) | Garantías formales de privacidad | Costo computacional y de comunicación elevado; impracticable hoy en microcontroladores; latencias de segundos |
| Edge computing (Chen & Ran, 2019) | Baja latencia; minimización de datos; factible en hardware de bajo costo | La base biométrica reside en el nodo: exige protección física y actualización segura; menor capacidad de modelos |

## 3. Reflexión crítica personal

Las soluciones actuales **no son suficientes por sí solas**, pero son
complementarias. La criptografía con preservación de privacidad ofrece garantías
fuertes que el borde no puede dar, pero su costo la aleja de los nodos de tiempo
real; el procesamiento en el borde es pragmático y aplicable hoy —de hecho, es la
decisión adoptada en nuestro caso de estudio SVIF—, pero desplaza el problema hacia
la seguridad física y la gestión del ciclo de vida del dispositivo (enrolamiento,
revocación, actualización de firmware).

Quedan sin resolver, a mi juicio: (i) la **verificación** de propiedades de
seguridad y privacidad de extremo a extremo en sistemas heterogéneos, (ii) la
**detección de suplantación** (*presentation attacks*) con recursos de borde, y
(iii) la conciliación entre trazabilidad (registrar quién accedió) y minimización de
datos (registrar lo menos posible), que es una tensión de diseño más que un problema
técnico.

Las líneas futuras más prometedoras me parecen la inferencia eficiente en el borde
con aceleradores de bajo consumo, los esquemas biométricos cancelables (plantillas
revocables) y la incorporación de estos atributos de calidad desde las etapas
tempranas de modelado —tal como propone la orientación a agentes con sus
*softgoals*—, de modo que privacidad y oportunidad de respuesta se analicen como
contribuciones explícitas del diseño y no como parches posteriores.

## 4. Referencias

- Chen, J., & Ran, X. (2019). Deep learning with edge computing: A review.
  *Proceedings of the IEEE, 107*(8), 1655–1674.
- Erkin, Z., Franz, M., Guajardo, J., Katzenbeisser, S., Lagendijk, I., & Toft, T.
  (2009). Privacy-preserving face recognition. *Privacy Enhancing Technologies
  Symposium (PETS 2009)*, LNCS 5672, 235–253. Springer.
- Humayed, A., Lin, J., Li, F., & Luo, B. (2017). Cyber-physical systems security —
  A survey. *IEEE Internet of Things Journal, 4*(6), 1802–1831.
- Lee, E. A. (2006). Cyber-physical systems — Are computing foundations adequate?
  *NSF Workshop on Cyber-Physical Systems*. Austin, TX.
- Zanero, S. (2017). Cyber-physical systems. *Computer, 50*(4), 14–16.
