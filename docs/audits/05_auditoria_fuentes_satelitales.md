

## 1. Objetivo de la auditoría

Antes de utilizar las variables satelitales para predecir el rendimiento de cebada, se revisaron las fuentes disponibles para conocer:

- qué sensores están disponibles;
- qué periodo cubre cada fuente;
- qué variables contiene cada una;
- cuántas observaciones existen;
- qué porcentaje de datos está disponible;
- cómo se comportan los datos faltantes;
- si existen valores fuera de rango o inconsistentes;
- y qué información debe conservarse para su evaluación posterior.

La auditoría se realizó por fuente y sensor. **No se asumió que variables con el mismo nombre provenientes de diferentes fuentes son equivalentes.**

---

# 2. Fuentes satelitales disponibles

Se identificaron tres fuentes principales:

| Fuente | Sensor | Periodo | Variables principales |
|---|---|---|---|
| BÁSICO | Sentinel-2 | 2022–2025 | NDVI, EVI, LAI, FAPAR, NDWI, MSI, entre otros |
| BÁSICO | Landsat | 2022–2025 | Principalmente VI6T |
| PRO | Planet | 2025 | NDVI, EVI, LAI, MSAVI |

Los datos están organizados por parcela y fecha. Sin embargo, para el modelo final no se utilizarán directamente estas observaciones individuales. Posteriormente se deberán transformar en variables temporales y agregadas para obtener **una fila por parcela**.

---

# 3. Auditoría BÁSICO

## 3.1 Estructura general

El archivo BÁSICO contiene:

- **107,666 registros**
- **197 parcelas**
- información de Sentinel-2 y Landsat;
- observaciones entre 2022 y 2025;
- estadísticas por fecha de diferentes índices de vegetación y condición de la superficie.

Cada observación contiene estadísticas como:

- promedio;
- desviación estándar;
- mínimo;
- máximo;
- porcentaje de nubosidad.

---

## 3.2 Sentinel-2

Sentinel-2 representa la mayor cantidad de información dentro del conjunto BÁSICO.

Se encontraron:

- **59,040 observaciones**
- **197 parcelas**
- **301 fechas**
- cobertura para las 197 parcelas durante cada año de 2022–2025.

La disponibilidad de los índices depende de las condiciones de observación.

Para NDVI, por ejemplo, se encontraron:

- 44,877 observaciones con información disponible;
- 14,163 observaciones sin información de índice.

Las observaciones sin índices presentan nubosidad del 100%, mientras que también existen observaciones con índices disponibles bajo diferentes niveles de nubosidad.

### Decisión

No se estableció todavía un umbral arbitrario de nubosidad.

La razón es que eliminar automáticamente todas las observaciones con nubosidad elevada podría eliminar información útil. El efecto de diferentes filtros de calidad deberá evaluarse posteriormente mediante experimentos de validación.

También se verificó que, en las observaciones válidas de los principales índices:

- mínimo ≤ promedio ≤ máximo;
- desviación estándar ≥ 0;
- no existen duplicados por parcela, fecha y sensor.

Se detectaron algunos valores que requieren interpretación, especialmente valores negativos en variables como LAI, pero **no se eliminaron automáticamente** durante esta auditoría.

---

# 4. Landsat

Dentro de BÁSICO se encontraron:

- **48,626 observaciones Landsat**.

La estructura de Landsat es diferente a Sentinel-2.

La mayoría de las variables del archivo BÁSICO no presentan información para Landsat. La variable que aparece de manera estructurada es principalmente **VI6T**, con sus estadísticas de promedio, desviación estándar, mínimo y máximo.

Por lo tanto, no se debe tratar a Landsat como si tuviera la misma disponibilidad de variables que Sentinel-2.

### Decisión

Se conserva Landsat como una fuente independiente.

No se eliminará únicamente por tener menos variables. Su utilidad predictiva se determinará posteriormente mediante experimentos controlados.

---

# 5. Auditoría PRO — Planet

El archivo PRO contiene:

- **47,804 observaciones**
- **197 parcelas**
- **311 fechas**
- periodo 2025
- sensor Planet.

Las variables principales son:

- NDVI
- EVI
- LAI
- MSAVI

Cada variable contiene promedio, desviación estándar, mínimo y máximo, además del porcentaje de nubosidad.

Se encontraron **35,747 observaciones con los cuatro índices disponibles** y **12,057 observaciones sin índices disponibles**.

En las observaciones sin índices, la nubosidad es del 100%.

---

## 5.1 Relación entre nubosidad e información disponible

La nubosidad mostró un comportamiento importante:

- con 100% de nubosidad, los índices están ausentes;
- también existen observaciones con índices disponibles bajo nubosidad elevada;
- por lo tanto, nubosidad e información disponible están relacionadas, pero no pueden utilizarse todavía para definir un umbral sin evaluar su impacto sobre el modelo.

En las observaciones disponibles se verificó:

- mínimo ≤ promedio ≤ máximo;
- desviación estándar ≥ 0;
- NDVI, EVI y MSAVI dentro de rangos razonables;
- no existen duplicados por parcela y fecha.

---

# 6. Observación sospechosa

Se identificó una observación que requiere especial atención:

**Parcela:** AGC_148  
**Fecha:** 24/05/2025  
**Nubosidad:** 94.179%

Valores registrados:

- NDVI = 0.007
- EVI = 0.038
- LAI = -0.112
- MSAVI = 0.010

Esta observación resulta sospechosa porque presenta valores muy bajos bajo una nubosidad elevada y posteriormente la serie temporal vuelve a valores compatibles con las observaciones cercanas.

Sin embargo, **no se puede confirmar que sea un error únicamente con esta evidencia**.

### Decisión

La observación no se elimina en esta etapa.

Se considera una observación de calidad sospechosa que deberá evaluarse cuando se construyan las variables temporales y se comparen diferentes estrategias de filtrado.

---

# 7. Decisiones generales de la auditoría

A partir de la revisión realizada se establecen las siguientes reglas:

1. **Las fuentes satelitales se mantienen separadas.**
2. No se consideran equivalentes los índices con el mismo nombre provenientes de diferentes sensores.
3. Los datos RAW no se modificarán ni eliminarán.
4. Los valores faltantes no se imputarán automáticamente durante esta etapa.
5. No se establecerán umbrales arbitrarios de nubosidad.
6. Las observaciones sospechosas se documentan antes de decidir si se excluyen.
7. La utilidad de cada fuente se evaluará mediante experimentos con la misma estrategia de validación.
8. La información temporal será aprovechada posteriormente mediante variables agregadas y características fenológicas.
9. El dataset final para modelado deberá tener **una fila por parcela**.
10. Las decisiones de filtrado y transformación se documentarán para garantizar reproducibilidad.

---

# 8. Conclusión

La auditoría muestra que las fuentes satelitales presentan diferencias importantes en cobertura, variables disponibles y calidad de observación.

**Sentinel-2** proporciona la mayor variedad de variables dentro de BÁSICO, mientras que **Landsat** presenta una disponibilidad mucho más limitada. **Planet** proporciona información de mayor frecuencia temporal durante 2025, pero también presenta observaciones afectadas por nubosidad y datos faltantes.

Por ahora, ninguna fuente se elimina.

La siguiente etapa será integrar las fuentes después de terminar las auditorías restantes y evaluar mediante validación experimental qué combinación de información aporta mayor capacidad predictiva para el rendimiento de cebada.