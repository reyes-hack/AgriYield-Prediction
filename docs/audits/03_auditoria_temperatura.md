# Auditoría de Temperatura — CHIRTS-ERA5

## 1. Objetivo

Auditar, validar y transformar los datos mensuales de temperatura mínima (Tmin) y temperatura máxima (Tmax) del producto CHIRTS-ERA5 para obtener información climática consistente a nivel de parcela.

La auditoría busca verificar:

- Integridad de los archivos raster.
- Consistencia espacial y temporal.
- Cobertura de las 197 parcelas.
- Calidad de los valores de temperatura.
- Consistencia física entre Tmin y Tmax.
- Comparación de diferentes métodos de extracción espacial.
- Selección de un método reproducible para obtener una observación por parcela y mes.

---

## 2. Fuente de datos

La fuente climática utilizada es CHIRTS-ERA5.

Se trabajó con dos variables:

- Tmin: temperatura mínima mensual.
- Tmax: temperatura máxima mensual.

Los archivos se encuentran organizados en:

```text
data/raw/climate/temperature/
├── Tmin/
│   ├── 2022/
│   ├── 2023/
│   ├── 2024/
│   └── 2025/
└── Tmax/
    ├── 2022/
    ├── 2023/
    ├── 2024/
    └── 2025/
Cobertura temporal

La información comprende:

Enero 2022 — Diciembre 2025

Se verificaron:

48 archivos Tmin.
48 archivos Tmax.
48 meses únicos para cada variable.
Ningún mes faltante.

3. Auditoría de metadatos raster
3.1 Tmax

El archivo Tmax_2022_01.tif fue utilizado como referencia inicial.

Características:

Propiedad	Valor
CRS	EPSG:4326
Resolución	~0.05° × 0.05°
Dimensiones	65 × 72
Bandas	1
Tipo de dato	float32
NoData	-9999
Unidad	°C
3.2 Tmin

El archivo Tmin_2022_01.tif presentó la misma estructura:

Propiedad	Valor
CRS	EPSG:4326
Resolución	~0.05° × 0.05°
Dimensiones	65 × 72
Bandas	1
Tipo de dato	float32
NoData	-9999
Unidad	°C
3.3 Consistencia entre archivos

Se verificó la consistencia de los 48 archivos de cada variable.

Para Tmax:

CRS consistente.
Resolución consistente.
Dimensiones consistentes.
NoData consistente.
Tipo de dato consistente.
Extensión espacial consistente.

Para Tmin se obtuvo el mismo resultado.

No fue necesario reproyectar los raster climáticos, ya que tanto los raster de temperatura como las parcelas utilizan EPSG:4326.

4. Cobertura espacial

Las parcelas del proyecto utilizan:

CRS: EPSG:4326

Los raster de Tmin y Tmax utilizan igualmente:

CRS: EPSG:4326

Por lo tanto, no fue necesario reproyectar los raster.

Para la extracción espacial se utilizaron las geometrías de las parcelas y los píxeles del raster.

La metodología permitió obtener información climática para las 197 parcelas durante los 48 meses.

Por variable:

197 parcelas × 48 meses = 9,456 observaciones

5. Método de extracción espacial

Se evaluaron tres métodos:

5.1 Centroid

Se obtiene el valor del píxel donde se encuentra el centroide de la parcela.

Ventaja:

Simple y rápido.

Limitación:

Utiliza únicamente un punto para representar toda la parcela.
5.2 All touched

Se consideran todos los píxeles que intersectan la geometría de la parcela y se calcula su promedio.

Ventaja:

Considera más de un píxel cuando la parcela atraviesa límites de celdas raster.

Limitación:

Los píxeles intersectados reciben el mismo peso independientemente del área real de intersección.
5.3 Area-weighted

Se calcula el área de intersección entre cada píxel y la parcela.

Para cada píxel:

peso = área de intersección / área total de la parcela

Posteriormente:

valor de parcela =
Σ(valor del píxel × peso)

Este método permite representar la contribución espacial de cada píxel de acuerdo con la superficie real de la parcela que ocupa.

6. Comparación de métodos — Tmax

Se compararon los métodos para las 9,456 observaciones de Tmax.

Centroid vs Area Weighted
Estadístico	Diferencia (°C)
Media	0.004672
Mediana	0
P90	0.007350
P95	0.031673
P99	0.110269
Máximo	0.196105
All Touched vs Area Weighted
Estadístico	Diferencia (°C)
Media	0.005762
Mediana	0
P90	0.015823
P95	0.042373
P99	0.110540
Máximo	0.220203
Centroid vs All Touched
Estadístico	Diferencia (°C)
Media	0.010434
Mediana	0
P90	0.032154
P95	0.069530
P99	0.192559
Máximo	0.271256

No se observaron diferencias superiores a 0.5 °C entre los métodos evaluados.

7. Comparación de métodos — Tmin

Para Tmin también se compararon los tres métodos utilizando las 9,456 observaciones.

Centroid vs Area Weighted
Estadístico	Diferencia (°C)
Media	0.007514
Mediana	0
P90	0.018508
P95	0.056189
P99	0.145883
Máximo	0.267989
All Touched vs Area Weighted
Estadístico	Diferencia (°C)
Media	0.010741
Mediana	0
P90	0.035564
P95	0.082823
P99	0.178577
Máximo	0.286772
Centroid vs All Touched
Estadístico	Diferencia (°C)
Media	0.018254
Mediana	0
P90	0.073679
P95	0.136271
P99	0.279617
Máximo	0.370688

Las diferencias fueron pequeñas en relación con el rango de las temperaturas observadas.

8. Método seleccionado

Se seleccionó area-weighted como método principal para la extracción de temperatura a nivel de parcela.

La decisión se basa en criterios geométricos y de consistencia metodológica.

El método utiliza el área real de intersección entre cada parcela y los píxeles del raster, evitando representar toda una parcela mediante un único punto o asignar el mismo peso a píxeles con diferentes áreas de intersección.

Además, este método es consistente con el tratamiento utilizado para la extracción de precipitación CHIRPS.

Los métodos centroid y all_touched se conservaron durante la auditoría para evaluar la sensibilidad del resultado ante la metodología de extracción.

9. Auditoría de valores — Tmin

Los valores de Tmin obtenidos mediante extracción area-weighted presentaron:

Estadístico	Valor
Mínimo	5.416 °C
Máximo	16.260 °C
Media	11.231 °C
Mediana	11.551 °C
P1	5.955 °C
P5	7.026 °C
P25	9.089 °C
P75	13.344 °C
P95	14.940 °C
P99	15.868 °C

Se encontraron:

0 valores negativos.
0 valores exactamente iguales a cero.
0 valores nulos después de la extracción.

No se eliminaron observaciones por criterios arbitrarios.

10. Auditoría de valores — Tmax

Durante la auditoría de los raster Tmax se identificaron los siguientes extremos globales:

Mínimo global: 17.059 °C
Máximo global: 41.973 °C

El valor mínimo global se presentó en:

Tmax_2022_09.tif

y el máximo global en:

Tmax_2024_05.tif

Los valores no fueron eliminados automáticamente. Los extremos se conservaron para mantener la trazabilidad de los datos originales.

11. Integridad de la extracción

Para Tmin:

Filas: 9,456
Parcelas: 197
Periodos: 48
Duplicados parcela-mes: 0
Nulos: 0

Para Tmax:

Filas: 9,456
Parcelas: 197
Periodos: 48
Duplicados parcela-mes: 0
Nulos: 0

La suma de los pesos de intersección presentó un error máximo de:

1.11 × 10⁻¹⁶

lo cual corresponde a error numérico de punto flotante.

12. Validación física Tmax vs Tmin

Se unieron los resultados de Tmin y Tmax utilizando:

ID_POLIGON
year
month

Se obtuvieron:

9,456 observaciones
197 parcelas
48 periodos

Se verificó la condición física:

Tmax >= Tmin

Resultado:

Casos Tmax < Tmin: 0

Por lo tanto, no se encontraron inconsistencias físicas entre las dos variables después de la extracción espacial.

13. Diferencia térmica diaria aproximada (DTR)

Como validación descriptiva se calculó:

DTR = Tmax - Tmin

La distribución obtenida fue:

Estadístico	DTR (°C)
Mínimo	7.453
P1	7.617
P5	8.408
P25	10.178
Mediana	12.422
P75	14.140
P95	15.827
P99	17.392
Máximo	17.810

DTR fue calculado únicamente como validación y exploración inicial.

No se ha incorporado todavía como variable definitiva del modelo.

14. Climatología mensual 2022–2025

Se calculó el promedio de Tmin y Tmax por mes considerando el periodo 2022–2025.

Mes	Tmin media (°C)	Tmax media (°C)	DTR medio (°C)
Enero	7.575	21.272	13.697
Febrero	8.424	23.128	14.704
Marzo	10.255	25.614	15.359
Abril	12.121	26.114	13.993
Mayo	13.472	26.726	13.254
Junio	14.013	24.664	10.651
Julio	13.686	23.532	9.846
Agosto	13.563	23.633	10.070
Septiembre	13.128	22.671	9.543
Octubre	11.400	21.897	10.496
Noviembre	9.204	22.487	13.282
Diciembre	7.936	20.155	12.219

La climatología muestra una variación estacional clara de las temperaturas durante el año.

Esta observación es descriptiva y no implica por sí misma una relación causal con el rendimiento.

15. Archivos procesados

Los datos finales a nivel parcela-mes se guardaron en:

data/interim/climate/
├── chirts_era5_tmin_parcel_month_area_weighted.csv
└── chirts_era5_tmax_parcel_month_area_weighted.csv

Cada archivo contiene:

9,456 filas
197 parcelas
48 periodos
Estructura final

Tmin:

ID_POLIGON
year
month
TMIN_C
n_pixeles
suma_pesos

Tmax:

ID_POLIGON
year
month
TMAX_C
n_pixeles
suma_pesos

n_pixeles y suma_pesos se mantienen como metadatos de auditoría y no como variables predictoras.

16. Decisiones metodológicas
Decisión 1 — Mantener los datos mensuales

Se conserva la resolución mensual original de CHIRTS-ERA5.

No se agregaron inicialmente los datos a una escala temporal diferente.

Decisión 2 — Utilizar area-weighted

Se seleccionó extracción ponderada por área después de comparar:

centroid,
all_touched,
area-weighted.
Decisión 3 — Mantener Tmin y Tmax separadas

No se combinaron permanentemente las dos variables durante esta etapa.

Las variables derivadas, como DTR, temperatura media o acumulaciones térmicas, se evaluarán posteriormente durante feature engineering.

Decisión 4 — No eliminar extremos automáticamente

Los valores extremos se conservaron.

Cualquier transformación, filtrado o tratamiento posterior deberá estar respaldado por evidencia y validación.

17. Limitaciones

La resolución espacial del producto es aproximadamente 0.05°, equivalente a varios kilómetros.

Por lo tanto:

La temperatura representa condiciones climáticas a una escala relativamente gruesa.
Parcelas diferentes pueden compartir los mismos píxeles climáticos.
La extracción area-weighted mejora la representación espacial de la parcela dentro del raster, pero no aumenta la resolución real del producto.
No debe interpretarse la precisión numérica de los valores como precisión espacial equivalente.

La información climática deberá combinarse posteriormente con información satelital, topográfica y otras variables disponibles para evaluar su utilidad predictiva.

18. Estado de la auditoría

Estado: COMPLETADA

Se considera que los datos de temperatura han pasado las validaciones iniciales de integridad, consistencia espacial, consistencia temporal y consistencia física.

Los archivos procesados quedan disponibles en:

data/interim/climate/

La construcción de variables climáticas derivadas y su evaluación como predictores se realizará posteriormente durante la etapa de feature engineering y modelado.