---
marp: true
theme: default
paginate: true
size: 16:9
header: "EMI305 · Producción de Software — Sistemas Ciberfísicos"
footer: "Semana 1 · Desafíos abiertos en CPS"
---

<!-- Exportable a PDF/PPTX con Marp: `marp presentacion.md --pdf` -->

# Seguridad y privacidad en CPS de videovigilancia con reconocimiento facial

**Actividad Semana 1 — Desafíos abiertos en Sistemas Ciberfísicos**

EMI305 · Producción de Software
UFRO, 2026

---

## El desafío

- Los CPS acoplan **cómputo + comunicación + proceso físico**: un ataque lógico
  produce **consecuencias físicas** (abrir una puerta, silenciar una alarma).
- Las contramedidas de TI tradicionales no bastan (Humayed et al., 2017):
  - nodos con **recursos restringidos**,
  - requisitos de **tiempo real** que desaconsejan criptografía pesada,
  - **heterogeneidad** de protocolos y dispositivos.
- En videovigilancia facial el dato sensado es **biométrico**:
  identifica de forma única y **no es revocable** (un rostro filtrado no se cambia).

**Problema abierto:** proteger el CPS *y* la privacidad biométrica sin violar las
restricciones temporales y de energía del nodo.

---

## ¿Por qué es relevante para los CPS?

- **Consecuencia física directa:** una identificación falsificada (*spoofing* con
  una fotografía) equivale a una intrusión física.
- **Tensión seguridad ↔ tiempo real:** cifrar y anonimizar cuesta cómputo;
  el entorno dicta el plazo de respuesta (Lee, 2006).
- **Regulación y confianza:** datos biométricos crecientemente regulados
  (GDPR; Ley 19.628 en Chile).
- **Escala:** una vulnerabilidad se replica en miles de cámaras desplegadas
  (Zanero, 2017).

---

## Soluciones en la literatura (1/2)

**Caracterización del desafío — Humayed et al. (2017), *IEEE IoT Journal***

- Encuesta sistemática de seguridad CPS: tres ejes (información, control,
  infraestructura) × dominios de aplicación.
- Contramedidas organizadas por capa: percepción, transmisión, aplicación.
- *Ventaja:* visión integral. *Limitación:* marco de análisis, no solución operativa.

**Reconocimiento facial con preservación de privacidad — Erkin et al. (2009), PETS**

- *Eigenfaces* sobre datos **cifrados homomórficamente**: el servidor identifica
  sin ver la imagen; el cliente no aprende la base de datos.
- *Ventaja:* garantías formales. *Limitación:* costo computacional impracticable
  en microcontroladores; latencia de segundos.

---

## Soluciones en la literatura (2/2)

**Procesamiento en el borde — Chen & Ran (2019), *Proceedings of the IEEE***

- Inferencia de aprendizaje profundo **en el propio nodo**:
  - la imagen **no viaja por la red**; solo se transmite el resultado mínimo
    (minimización de datos),
  - latencia acotada, factible en hardware de bajo costo.
- *Limitación:* la base biométrica reside en el nodo → seguridad física,
  actualización segura, modelos de menor capacidad.

---

## Reflexión crítica

- Las soluciones actuales son **complementarias, no suficientes** por sí solas.
- Sin resolver:
  - **verificación** extremo a extremo de propiedades de seguridad/privacidad,
  - **anti-spoofing** con recursos de borde,
  - tensión **trazabilidad ↔ minimización de datos**.
- Líneas prometedoras:
  - inferencia eficiente en el borde (aceleradores de bajo consumo),
  - **biometría cancelable** (plantillas revocables),
  - atributos de calidad modelados **desde etapas tempranas** (softgoals en
    orientación a agentes) — enfoque que aplicaremos en el caso SVIF del curso.

---

## Referencias

- Chen, J., & Ran, X. (2019). Deep learning with edge computing: A review.
  *Proceedings of the IEEE, 107*(8), 1655–1674.
- Erkin, Z., Franz, M., Guajardo, J., Katzenbeisser, S., Lagendijk, I., & Toft, T.
  (2009). Privacy-preserving face recognition. *PETS 2009*, LNCS 5672, 235–253.
- Humayed, A., Lin, J., Li, F., & Luo, B. (2017). Cyber-physical systems security —
  A survey. *IEEE Internet of Things Journal, 4*(6), 1802–1831.
- Lee, E. A. (2006). Cyber-physical systems — Are computing foundations adequate?
  *NSF Workshop on CPS*.
- Zanero, S. (2017). Cyber-physical systems. *Computer, 50*(4), 14–16.
