06 — Auditoría temporal de clima y relación con topografía
1. Objetivo

Esta auditoría tiene como objetivo evaluar la estructura temporal y espacial de las variables climáticas disponibles para las 197 parcelas del reto AgroCebada FIRA 2026, así como verificar su consistencia y explorar su relación con variables topográficas previamente auditadas.

La auditoría se concentra principalmente en:

precipitación mensual CHIRPS;
temperatura mínima mensual (Tmin);
temperatura máxima mensual (Tmax);
diferencia térmica mensual (DTR);
elevación;
pendiente.

El objetivo de esta etapa no es determinar todavía qué variables son las mejores predictoras del rendimiento. Esa decisión se realizará posteriormente mediante experimentos de modelado y validación fuera de muestra.

La finalidad de esta auditoría es asegurar que las variables sean:

estructuralmente consistentes;
completas o correctamente caracterizadas respecto a sus faltantes;
temporalmente coherentes;
espacialmente interpretables;
adecuadas para posteriormente construir variables predictoras a nivel parcela.
2. Fuentes utilizadas

Se utilizaron los resultados ya auditados de las siguientes fuentes.

Precipitación

Archivo:

data/interim/climate/chirps_parcel_month_area_weighted.csv

Fuente:

CHIRPS

Características de los datos originales:

periodo: enero 2022 – diciembre 2025;
frecuencia: mensual;
resolución: 0.05°;
CRS: EPSG:4326;
variable: precipitación acumulada mensual;
unidad: mm/mes.

La extracción a nivel parcela se realizó previamente mediante promedio ponderado por área de intersección entre cada parcela y los píxeles del raster.

Temperatura mínima

Archivo:

data/interim/climate/chirts_era5_tmin_parcel_month_area_weighted.csv

Fuente:

CHIRTS-ERA5

Características:

periodo: enero 2022 – diciembre 2025;
frecuencia: mensual;
resolución: 0.05°;
unidad: °C;
extracción espacial ponderada por área.
Temperatura máxima

Archivo:

data/interim/climate/chirts_era5_tmax_parcel_month_area_weighted.csv

Características equivalentes a Tmin:

enero 2022 – diciembre 2025;
frecuencia mensual;
resolución 0.05°;
unidad °C;
extracción ponderada por área.
Topografía

Archivo generado a partir de la auditoría topográfica:

data/interim/topography/topografia_parcelas.csv

Variables:

ID_POLIGON
slope_deg
slope_coverage
elevation_m
elevation_coverage

La elevación y la pendiente fueron extraídas previamente mediante estadísticas ponderadas por área y se conservaron variables de cobertura para representar la calidad de la extracción.

3. Estructura temporal de la precipitación
3.1 Integridad temporal

La tabla de precipitación contiene:

9,456 registros
197 parcelas
48 periodos mensuales
periodo: enero 2022 – diciembre 2025.

La cantidad esperada de registros es:

197 parcelas × 48 meses = 9,456 registros

Se verificó que cada parcela cuenta exactamente con los 48 meses y que no existen registros duplicados por parcela y periodo.

Resultado

La estructura temporal de CHIRPS es completa para las 197 parcelas.

4. Control de calidad de precipitación

Se verificaron:

valores nulos;
valores infinitos;
valores negativos;
valores exactamente iguales a cero.

Resultados globales:

Estadístico	Precipitación (mm/mes)
Media	69.51
Desviación estándar	71.65
Mínimo	0.00
P25	14.56
Mediana	38.22
P75	111.91
Máximo	392.02

No se encontraron valores negativos ni faltantes.

Se identificaron 222 valores exactamente iguales a cero.

Estos ceros fueron revisados directamente contra los raster originales y corresponden a valores presentes en la fuente, por lo que no fueron eliminados ni tratados como errores.

Decisión

Los valores cero de precipitación se conservan como observaciones válidas.

No se realiza imputación ni eliminación arbitraria de valores extremos.

5. Comportamiento mensual de precipitación

La climatología 2022–2025 muestra una marcada variación estacional.

Mes	Media mm
Enero	12.42
Febrero	15.50
Marzo	13.01
Abril	23.97
Mayo	75.48
Junio	129.17
Julio	155.64
Agosto	140.14
Septiembre	129.88
Octubre	88.77
Noviembre	35.58
Diciembre	14.62

La precipitación aumenta claramente a partir de mayo, alcanza sus valores medios más elevados durante junio–septiembre y disminuye posteriormente.

Esto demuestra que utilizar únicamente una precipitación anual podría perder información temporal relevante.

6. Precipitación durante el ciclo productivo 2025

Para una descripción inicial del periodo abril–octubre de 2025 se calculó la precipitación acumulada:

abril + mayo + junio + julio + agosto + septiembre + octubre

Resultados entre las 197 parcelas:

Estadístico	Precipitación abril–octubre 2025 (mm)
Media	962.61
Desviación estándar	171.30
Mínimo	702.79
P25	816.23
Mediana	961.35
P75	1006.24
Máximo	1459.14

Existe, por tanto, una variación espacial considerable en la cantidad acumulada de precipitación durante el periodo.

Sin embargo, este resultado por sí mismo no demuestra un efecto sobre el rendimiento.

Decisión

La precipitación acumulada abril–octubre queda como variable candidata para los experimentos de modelado.

También queda abierta la posibilidad de utilizar acumulaciones por ventanas temporales más específicas, siempre que estas sean justificadas agronómicamente y evaluadas mediante validación.

7. Variabilidad espacial de la precipitación

Durante 2025 se calculó la desviación estándar entre parcelas para cada mes.

Dentro del periodo abril–octubre:

junio presentó la mayor desviación estándar absoluta: aproximadamente 51.4 mm;
septiembre presentó el mayor coeficiente de variación: aproximadamente 0.324.

Esto demuestra que la precipitación no solamente cambia temporalmente, sino también espacialmente entre parcelas.

No obstante, una mayor variabilidad espacial no implica automáticamente mayor capacidad predictiva.

8. Integridad temporal de temperatura

Tanto Tmin como Tmax contienen:

9,456 registros;
197 parcelas;
48 meses;
enero 2022 – diciembre 2025.

Se realizó una unión mediante:

ID_POLIGON + año + mes

La validación de la unión fue uno-a-uno.

Posteriormente se calculó:

DTR = Tmax - Tmin

donde DTR representa la diferencia térmica entre temperatura máxima y mínima mensual.

9. Control de consistencia térmica

Para las 9,456 observaciones:

no se encontraron valores nulos;
no existen duplicados por parcela-periodo;
no se encontraron casos donde:
Tmin > Tmax

Por lo tanto, la relación básica entre ambas variables es consistente en todo el periodo analizado.

10. Distribución general de temperatura
Tmin 2022–2025
Estadístico	°C
Media	11.23
Desviación estándar	2.54
Mínimo	5.42
Mediana	11.55
P95	14.94
Máximo	16.26
Tmax 2022–2025
Estadístico	°C
Media	23.49
Desviación estándar	2.18
Mínimo	18.76
Mediana	23.35
P95	27.15
Máximo	30.16
DTR
Estadístico	°C
Media	12.26
Desviación estándar	2.35
Mínimo	7.45
Mediana	12.42
Máximo	17.81
11. Temperatura durante abril–octubre 2025

Para cada parcela se calculó la media de Tmin, Tmax y DTR durante abril–octubre de 2025.

Variable	Media	Std	Mín	Máx
Tmin	12.88 °C	0.57	11.42	13.48
Tmax	23.67 °C	0.16	23.25	24.01
DTR	10.79 °C	0.57	10.19	11.83

Se observa que Tmin presenta mayor variabilidad espacial que Tmax durante el periodo.

Sin embargo, esta variabilidad no debe confundirse con importancia predictiva.

12. Relación entre temperatura y elevación

Se integraron los datos climáticos del ciclo abril–octubre 2025 con la tabla topográfica de las 197 parcelas.

La tabla resultante tuvo:

197 parcelas
8 variables
0 duplicados
0 valores nulos

Las variables utilizadas fueron:

Tmin_media_abr_oct
Tmax_media_abr_oct
DTR_media_abr_oct
elevation_m
slope_deg
elevation_coverage
slope_coverage

Se calcularon correlaciones de Pearson y Spearman entre temperatura y elevación.

Relación	Pearson	Spearman
Elevación – Tmin	0.210	0.022
Elevación – Tmax	-0.673	-0.680
Elevación – DTR	-0.393	-0.359
13. Interpretación de la relación temperatura–elevación
Tmax

La relación entre elevación y Tmax fue:

Pearson  = -0.673
Spearman = -0.680

La similitud entre ambas medidas indica una asociación negativa consistente entre elevación y Tmax en las 197 parcelas.

En términos descriptivos:

Las parcelas ubicadas a mayor elevación tienden a presentar menores valores de Tmax media durante abril–octubre de 2025.

Esta afirmación describe una asociación observada en los datos.

No se interpreta como una relación causal.

Tmin

Para Tmin:

Pearson  = 0.210
Spearman = 0.022

La diferencia entre ambas medidas es considerable.

La correlación de Spearman cercana a cero indica que no existe una relación monotónica clara entre elevación y Tmin en estas parcelas durante el periodo analizado.

Por lo tanto, no se considera apropiado describir a Tmin como un simple proxy de elevación.

DTR

Para DTR:

Pearson  = -0.393
Spearman = -0.359

Se observa una asociación negativa moderada con elevación.

DTR disminuye generalmente conforme aumenta la elevación, aunque la relación es considerablemente más débil que la observada para Tmax.

14. Control de cobertura topográfica

La tabla topográfica conserva dos indicadores de calidad:

elevation_coverage
slope_coverage

Resultados:

Variable	Media	Mediana	Mínimo
Elevation coverage	99.82%	100%	75.94%
Slope coverage	98.73%	100%	2.10%

La elevación presenta una cobertura prácticamente completa para la mayoría de las parcelas.

La pendiente presenta algunos casos con cobertura considerablemente menor debido a valores NoData del raster de pendiente.

Las parcelas con cobertura parcial ya fueron identificadas durante la auditoría topográfica.

Decisión

No se eliminan parcelas por cobertura.

Los valores calculados se conservan y las variables de cobertura permanecen disponibles como posibles variables de calidad.

La inclusión de estas variables en el modelo final se decidirá posteriormente mediante validación.

15. Relación con la literatura agronómica

Los resultados obtenidos son compatibles con la idea general de que las condiciones térmicas e hídricas tienen importancia para el desarrollo y rendimiento de la cebada, pero la literatura también muestra que el efecto depende del momento del ciclo.

Un estudio reciente sobre cebada de primavera encontró que la temperatura y la radiación solar fueron factores climáticos importantes y que la disponibilidad de agua estuvo asociada con el rendimiento en diferentes ambientes.

Otros estudios reportan sensibilidad de la cebada a temperaturas elevadas durante etapas reproductivas y de llenado de grano, con efectos sobre componentes del rendimiento.

También existe evidencia experimental de que déficits hídricos antes de antesis pueden afectar el número de granos, mientras que el déficit posterior puede afectar el llenado del grano.

Estos resultados de literatura se utilizan únicamente para generar hipótesis agronómicas. No se transfieren directamente como reglas al conjunto de datos del reto.

16. Decisiones tomadas

A partir de esta auditoría se establecen las siguientes decisiones:

Precipitación
Mantener la precipitación mensual.
Mantener valores cero observados.
No realizar imputación.
No eliminar valores extremos automáticamente.
Mantener extracción ponderada por área.
Considerar acumulaciones por ventanas temporales en etapas posteriores.
Temperatura
Mantener Tmin y Tmax separadas.
Mantener DTR como variable derivada candidata.
No eliminar Tmax por su correlación con elevación.
No eliminar Tmin por su baja correlación con elevación.
Evaluar posteriormente redundancia mediante validación.
Topografía
Mantener elevation_m.
Mantener slope_deg.
Mantener elevation_coverage.
Mantener slope_coverage.
No realizar imputación general de NoData.
No eliminar parcelas únicamente por cobertura.
Modelado

Ninguna variable se declara todavía como "la más importante".

La importancia predictiva se determinará posteriormente mediante experimentos reproducibles y validación fuera de muestra.

17. Limitaciones de esta auditoría

Esta auditoría presenta varias limitaciones que deben mantenerse explícitas:

CHIRPS y CHIRTS-ERA5 tienen una resolución espacial de aproximadamente 0.05°, mucho mayor que la escala de algunas parcelas.
Las variables climáticas son agregaciones mensuales y no representan directamente condiciones diarias.
El periodo abril–octubre se utilizó como referencia inicial del ciclo, pero no implica que todas las parcelas tengan exactamente las mismas fechas fenológicas.
Las correlaciones entre clima y topografía son exploratorias.
No se ha utilizado todavía RENDIMIENTO_T_HA en estos análisis de estructura interna.
Por lo tanto, los resultados anteriores no permiten concluir qué variables predicen mejor el rendimiento.
La climatología 2022–2025 incluye 2025; por ello, las comparaciones descriptivas realizadas contra ella no deben interpretarse como anomalías independientes del año objetivo.