# Auditoría de Topografía

## 1. Objetivo

Evaluar la calidad, consistencia espacial y comportamiento de las variables topográficas derivadas de los productos de elevación y pendiente proporcionados para el proyecto.

La auditoría busca verificar:

- Sistema de referencia y alineación espacial.
- Resolución y dimensiones de los rasters.
- Valores NoData.
- Cobertura espacial dentro de las parcelas.
- Métodos de extracción de valores por parcela.
- Presencia de valores físicamente inválidos.
- Diferencias entre métodos de extracción.
- Comportamiento general de elevación y pendiente.

El objetivo final es definir una metodología reproducible para obtener variables topográficas a nivel de parcela sin introducir valores artificiales ni perder información innecesariamente.

---

# 2. Fuentes de datos

## 2.1 Elevación

Archivo:

`Elevacion_INEGI_CEM4_120m.tif`

Características verificadas:

| Característica | Valor |
|---|---|
| CRS | EPSG:6372 |
| Resolución | 120 × 120 m |
| Dimensiones | 2900 × 3362 |
| Unidad | metros sobre el nivel del mar |
| Tipo de dato | float32 |
| NoData | -9999 |

Estadísticos del raster completo:

- Mínimo: 8 m
- Máximo: 5608 m
- Media: 1828.26 m
- Mediana: 1979 m

---

## 2.2 Pendiente

Archivo:

`Pendiente_INEGI_CEM4_120m_grados.tif`

Características verificadas:

| Característica | Valor |
|---|---|
| CRS | EPSG:6372 |
| Resolución | 120 × 120 m |
| Dimensiones | 2900 × 3362 |
| Unidad | grados |
| Tipo de dato | float32 |
| NoData | -9999 |
| Método indicado en metadatos | Horn 3×3 |

Estadísticos del raster completo:

- Mínimo: 0°
- Máximo: 70.63786°
- Media: 10.171154°
- Mediana: 7.143111°

No se encontraron valores negativos ni valores superiores a 90°.

---

# 3. Verificación espacial

Los polígonos de las 197 parcelas fueron comparados con ambos rasters.

Se verificó que los productos de elevación y pendiente presentan:

- Las mismas dimensiones.
- El mismo sistema de referencia.
- La misma transformación espacial.
- La misma extensión espacial.

Por lo tanto, ambos rasters se encuentran correctamente alineados espacialmente entre sí.

---

# 4. Métodos de extracción evaluados

Para cada parcela se evaluaron tres métodos:

### 4.1 Centroide

Se obtiene el valor del píxel que contiene el centroide de la parcela.

Ventaja:

- Método sencillo y computacionalmente económico.

Limitación:

- Utiliza únicamente un píxel.
- Puede no representar la variabilidad espacial de una parcela.

---

### 4.2 Promedio de píxeles intersectados

Se calcula el promedio de los valores de los píxeles que intersectan espacialmente con la parcela.

Este método permite utilizar más información espacial que el centroide, pero no pondera cada píxel según la superficie exacta que ocupa dentro del polígono.

---

### 4.3 Promedio ponderado por área

Se calcula un promedio en el que cada píxel recibe un peso proporcional al área de intersección entre el píxel y la parcela.

Este método fue seleccionado como metodología principal porque representa directamente el promedio espacial de la variable dentro de la geometría de la parcela.

Para los píxeles NoData, no se asignaron valores artificiales. Solamente se utilizaron las áreas de intersección correspondientes a valores válidos.

---

# 5. Cobertura válida

La cobertura válida se definió como:

```text
cobertura_valida =
área de intersección con datos válidos
/
área total de la parcela

Esta variable permite distinguir entre una media calculada con cobertura prácticamente completa y una media calculada utilizando solamente una fracción de la parcela.

6. Auditoría de elevación

Las 197 parcelas intersectaron correctamente el raster de elevación.

La cobertura válida mínima observada fue aproximadamente:

75.94 %

Cuatro parcelas presentaron cobertura parcial:

Parcela	Cobertura válida
AGC_170	75.94 %
AGC_164	95.06 %
AGC_023	95.90 %
AGC_020	97.83 %

La reducción de cobertura se debió a valores NoData presentes dentro del raster y no a un problema de alineación espacial.

Se evaluó una estrategia de imputación mediante vecinos 3×3.

La evaluación global de esta estrategia mostró errores importantes en algunos casos, por lo que no se adoptó como método general de imputación.

Para las parcelas con cobertura parcial se decidió utilizar únicamente los valores válidos disponibles y conservar la cobertura como indicador de calidad.

7. Auditoría de pendiente

La pendiente presentó un comportamiento diferente al de la elevación.

El raster contiene:

4,047,765 píxeles válidos.
5,702,035 píxeles NoData.

Al comparar ambos rasters se obtuvo:

Elevación válida: 4,081,208 píxeles.
Pendiente válida: 4,047,765 píxeles.
Pendiente NoData donde la elevación es válida: 33,443 píxeles.
Pendiente válida donde la elevación es NoData: 0 píxeles.

Para los 33,443 píxeles donde la elevación era válida pero la pendiente era NoData, se verificó la ventana 3×3 de elevación.

Resultado:

0 píxeles sin vecinos NoData.
33,443 píxeles con al menos un vecino NoData.

Esto es consistente con la naturaleza del cálculo de pendiente mediante una ventana Horn 3×3, que requiere información de los píxeles vecinos.

Por lo tanto, no se identificó evidencia de un problema de CRS, alineación o transformación espacial.

8. Cobertura de pendiente por parcela

La cobertura de pendiente fue evaluada para las 197 parcelas.

Cobertura válida	Número de parcelas
≥ 99 %	192
≥ 95 %	193
≥ 90 %	193
≥ 75 %	193
≥ 50 %	195
< 50 %	2

Estadísticos:

Media: 98.73 %
Mediana: 100 %
Mínimo: 2.10 %
Máximo: 100 %

Las dos parcelas con cobertura inferior al 50 % fueron:

Parcela	Cobertura
AGC_170	2.10 %
AGC_023	28.64 %

También se identificaron:

Parcela	Cobertura
AGC_164	55.27 %
AGC_020	65.25 %

No se eliminaron estas parcelas.

9. Comparación de métodos de extracción de pendiente

Se compararon los valores obtenidos mediante centroide, promedio de píxeles intersectados y promedio ponderado por área.

9.1 Centroide vs. promedio ponderado por área

Diferencia absoluta:

Estadístico	Diferencia
Media	0.397°
Mediana	0.219°
P75	0.515°
P90	0.858°
P95	1.351°
P99	2.645°
Máximo	3.052°

La mayor diferencia se observó en:

Parcela	Centroide	Ponderado por área	Diferencia
AGC_120	2.151°	5.203°	3.052°
AGC_149	2.869°	5.870°	3.001°
AGC_155	2.700°	5.318°	2.618°

Estas parcelas presentaban 100 % de cobertura válida, por lo que las diferencias no se explican por valores NoData.

9.2 Promedio de píxeles intersectados vs. promedio ponderado por área

Diferencia absoluta:

Estadístico	Diferencia
Media	0.206°
Mediana	0.104°
P75	0.250°
P90	0.570°
P95	0.716°
P99	1.492°
Máximo	1.599°

La mayor diferencia se observó en AGC_149:

Promedio de píxeles intersectados: 7.469°
Promedio ponderado por área: 5.870°
Diferencia: 1.599°
10. Control de calidad de las variables extraídas

Después de la extracción mediante promedio ponderado por área se obtuvieron 197 observaciones para cada variable.

Elevación por parcela
Estadístico	Valor
Media	2667.10 m
Desviación estándar	92.28 m
Mínimo	2496.65 m
P25	2611.35 m
Mediana	2638.90 m
P75	2726.68 m
P95	2880.83 m
Máximo	2906.04 m

No se encontraron:

valores negativos;
valores NaN.
Pendiente por parcela
Estadístico	Valor
Media	2.79°
Desviación estándar	2.05°
Mínimo	0.282°
P25	1.149°
Mediana	2.126°
P75	3.891°
P95	7.275°
Máximo	9.396°

No se encontraron:

valores negativos;
valores superiores a 90°;
valores NaN.
11. Relación descriptiva entre elevación y pendiente

La correlación de Pearson entre elevación y pendiente fue:

r = 0.4496

Esta relación se utiliza únicamente como control descriptivo de los datos.

No se interpreta como evidencia de causalidad.

La presencia de parcelas con elevación elevada y pendientes moderadas, así como parcelas con pendientes relativamente altas a diferentes elevaciones, indica que ambas variables contienen información topográfica diferente.

12. Decisiones metodológicas

A partir de las pruebas realizadas se establecen las siguientes decisiones:

Elevación

Se utilizará:

elevation_m = promedio ponderado por área

No se realizará imputación general de valores NoData.

Se conservará:

elevation_coverage

como indicador de calidad de extracción.

Pendiente

Se utilizará:

slope_deg = promedio ponderado por área

No se realizará imputación general de valores NoData.

Se conservará:

slope_coverage

como indicador de calidad de extracción.

Métodos no seleccionados

El método de centroide y el promedio sin ponderación por área no se utilizarán como métodos principales.

Se conservarán únicamente como métodos de comparación y auditoría.

13. Variables topográficas candidatas

El resultado de esta auditoría genera las siguientes variables candidatas a nivel de parcela:

elevation_m
elevation_coverage
slope_deg
slope_coverage

La inclusión definitiva de estas variables en el modelo predictivo se determinará posteriormente mediante experimentación y validación cruzada.

La existencia de una variable no implica que deba incorporarse automáticamente al modelo.

14. Conclusión

La auditoría topográfica permitió verificar la consistencia espacial de los rasters de elevación y pendiente y establecer una metodología reproducible de extracción a nivel de parcela.

El promedio ponderado por área fue seleccionado como método principal debido a que utiliza la superficie de la parcela de manera explícita y evita depender de un único píxel.

La pendiente presenta algunas zonas con NoData derivadas de las condiciones necesarias para el cálculo Horn 3×3. Sin embargo, la cobertura es ≥95 % en 193 de las 197 parcelas.

No se identificaron valores físicamente inválidos en las variables finales extraídas.

No se realizará imputación general de NoData ni eliminación de parcelas por problemas de cobertura topográfica.

Las variables resultantes quedan como candidatas para la siguiente etapa del proyecto:

elevation_m
elevation_coverage
slope_deg
slope_coverage

La utilidad predictiva de estas variables será evaluada posteriormente mediante validación rigurosa y sin utilizar información del conjunto de predicción oculto.