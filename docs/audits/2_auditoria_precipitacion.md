# 02 — Auditoría de Precipitación CHIRPS

## 1. Objetivo de la auditoría

El objetivo de esta auditoría fue revisar, validar y transformar los datos mensuales de precipitación del producto CHIRPS para obtener una representación consistente de la precipitación a nivel de parcela.

La auditoría tuvo como objetivos específicos:

- Verificar la integridad temporal de los archivos CHIRPS.
- Revisar el sistema de referencia de coordenadas.
- Validar la resolución espacial y extensión de los rasters.
- Revisar los valores NoData.
- Comprobar la cobertura espacial de las 197 parcelas.
- Evaluar la presencia de valores cero.
- Comparar diferentes métodos de extracción espacial.
- Seleccionar una metodología reproducible para obtener precipitación mensual a nivel parcela.
- Generar una tabla estructurada de precipitación parcela-mes para su posterior utilización en ingeniería de características.

---

# 2. Fuente de datos

La fuente utilizada corresponde a archivos raster mensuales de precipitación CHIRPS.

Los archivos fueron organizados en:

```text
data/raw/climate/precipitation/
├── 2022/
├── 2023/
├── 2024/
└── 2025/

Cada archivo representa un mes específico y sigue el patrón:

PREC_YYYY_MM.tif

donde:

YYYY corresponde al año.
MM corresponde al mes.
3. Cobertura temporal

Se identificaron 48 archivos raster mensuales.

La cobertura corresponde a:

Enero 2022 — Diciembre 2025

Distribución:

Año	Archivos
2022	12
2023	12
2024	12
2025	12
Total	48

No se identificaron meses faltantes.

La primera observación corresponde a:

2022-01

y la última a:

2025-12

Por lo tanto, la serie temporal mensual está completa para el periodo disponible.

4. Metadatos espaciales

Se inspeccionó el primer raster de la serie y posteriormente se verificó la consistencia de los metadatos entre los 48 archivos.

Ejemplo:

PREC_2022_01.tif

Principales características:

Propiedad	Valor
CRS	EPSG:4326
Resolución	~0.05° × 0.05°
Dimensiones	65 × 72 píxeles
Bandas	1
Tipo de dato	float32
NoData	-9999

Los 48 archivos presentaron:

El mismo CRS.
La misma resolución.
Las mismas dimensiones.
El mismo valor NoData.
La misma extensión espacial.

No se identificaron inconsistencias estructurales entre los rasters mensuales.

5. Interpretación de la resolución espacial

La resolución de los rasters CHIRPS es aproximadamente:

0.05° × 0.05°

Debido a que el raster se encuentra en EPSG:4326, esta resolución está expresada angularmente y no representa exactamente la misma distancia en metros en todas las ubicaciones.

Para el área de estudio, esta escala corresponde aproximadamente a varios kilómetros por píxel.

Por lo tanto, CHIRPS proporciona una representación climática regional y no una medición puntual de precipitación dentro de cada parcela.

Esta consideración es importante al interpretar posteriormente las variables de precipitación como predictores del rendimiento.

6. Cobertura espacial

Se comparó la extensión espacial de los rasters CHIRPS con la extensión de las parcelas.

Las 197 parcelas se encuentran dentro de la cobertura espacial de CHIRPS.

Resultado:

Parcelas dentro de cobertura: 197
Parcelas fuera de cobertura: 0

Por lo tanto, no fue necesario utilizar otra fuente de precipitación para cubrir alguna parcela.

7. Revisión de valores NoData

Los archivos CHIRPS utilizan:

NoData = -9999

Estos valores no representan precipitación y fueron tratados como valores ausentes durante la extracción.

Los valores NoData no fueron interpretados como cero.

Esta distinción es importante:

NoData ≠ 0 mm

Un valor de 0 mm representa una precipitación válida de cero, mientras que -9999 representa ausencia de información válida.

8. Validación de cobertura por parcela

Para comprobar que la extracción pudiera realizarse para todas las parcelas, se evaluó la disponibilidad de valores válidos dentro de cada geometría.

Se revisaron los 48 meses.

En todos los meses:

Parcelas con datos válidos: 197
Parcelas sin datos válidos: 0

Por lo tanto:

Ninguna parcela quedó sin información durante la serie temporal.
No existen meses con pérdida completa de información para alguna parcela.
La tabla final puede construirse para las 197 parcelas durante los 48 meses.
9. Valores cero de precipitación

Durante la auditoría se identificaron valores de precipitación exactamente iguales a cero.

Inicialmente se verificó la distribución de ceros en la tabla parcelaria.

Posteriormente, se realizó una comprobación directamente sobre los rasters originales para determinar si los ceros provenían del procesamiento o de la fuente de datos.

Se verificaron tres meses representativos:

Enero 2023
Mínimo válido: 0.0 mm
Máximo válido: 50.13238 mm
Píxeles exactamente iguales a 0: 983
Píxeles válidos: 2032
Porcentaje de ceros: 48.38 %
Febrero 2023
Mínimo válido: 0.0 mm
Máximo válido: 57.64569 mm
Píxeles exactamente iguales a 0: 1194
Píxeles válidos: 2032
Porcentaje de ceros: 58.76 %
Marzo 2024
Mínimo válido: 0.0 mm
Máximo válido: 60.782063 mm
Píxeles exactamente iguales a 0: 662
Píxeles válidos: 2032
Porcentaje de ceros: 32.58 %

La comprobación confirmó que los valores cero existen directamente en los rasters CHIRPS originales.

Por lo tanto, los valores cero encontrados a nivel de parcela no son producto de un error de extracción.

Decisión

Los valores de:

0 mm

se conservaron como mediciones válidas.

No se realizó:

Eliminación de ceros.
Reemplazo por NaN.
Imputación.
Sustitución por otro valor.
Filtrado arbitrario de meses secos.
10. Métodos de extracción evaluados

Para convertir la información raster mensual en variables a nivel de parcela se evaluaron tres métodos.

10.1 Centroide

Se asigna a la parcela el valor del píxel donde se encuentra su centroide.

Este método representa la precipitación del píxel correspondiente al punto central de la parcela.

Ventajas
Simple.
Rápido.
Fácil de reproducir.
Limitaciones
Utiliza solamente un píxel.
Puede ignorar variabilidad espacial dentro de la parcela.
Puede ser sensible cuando la parcela cruza límites entre píxeles.


10.2 all_touched

Se consideran todos los píxeles que intersectan la geometría de la parcela.

Los valores de esos píxeles se promedian sin ponderarlos según el porcentaje de superficie que ocupan dentro de la parcela.

Ventajas
Considera todos los píxeles que intersectan la parcela.
Evita depender exclusivamente del centroide.
Limitaciones
Un píxel que apenas toca la parcela puede tener el mismo peso que uno que cubre una superficie mucho mayor.
No representa directamente la superficie real de intersección entre parcela y píxel.


10.3 Ponderación por área

Se calculó la superficie de intersección entre cada píxel y la parcela.

Para cada píxel se definió:

peso_i =
área_intersección_i / área_parcela

La precipitación parcelaria se calculó como:

P_parcela =
Σ(P_i × peso_i)

donde:

P_i es la precipitación del píxel.
peso_i representa la proporción de la superficie de la parcela cubierta por dicho píxel.

Los pesos deben cumplir:

Σ peso_i ≈ 1

Este método permite que cada píxel contribuya proporcionalmente a la superficie que realmente ocupa dentro de la parcela.

11. Comparación de métodos

Se compararon los tres métodos para septiembre de 2025 en las 197 parcelas.

El objetivo fue identificar si las diferentes estrategias producían resultados equivalentes o si la elección metodológica podía modificar la variable resultante.

Para la mayoría de las parcelas las diferencias fueron pequeñas o nulas, pero se identificaron casos donde la diferencia fue relevante.

Un ejemplo representativo fue la parcela:

AGC_145

Para septiembre de 2025:

Método	Precipitación
Centroide	196.586 mm
all_touched	264.105 mm
Ponderado por área	242.015 mm

La parcela intersectaba dos píxeles con valores:

196.586 mm
331.624 mm

El área de la parcela estaba distribuida aproximadamente de la siguiente manera:

Píxel	Precipitación	Peso
1	196.586 mm	0.663586
2	331.624 mm	0.336414

El resultado ponderado fue:

242.015 mm

Esto demuestra que los tres métodos pueden producir valores diferentes cuando una parcela atraviesa varios píxeles con distinta precipitación.

12. Validación geométrica de la ponderación

Para validar la metodología de ponderación por área se verificó que la suma de las áreas de intersección coincidiera con el área real de la parcela.

Para el caso AGC_145:

Área de la parcela:
82796.14639335373 m²

Suma de áreas de intersección:
82796.14639335312 m²

La diferencia fue:

≈ 6.11 × 10⁻¹⁰ m²

La diferencia corresponde a error numérico de punto flotante y es despreciable.

También se verificó que:

Σ pesos = 1

y que el resultado ponderado se encontrara dentro del rango de valores de los píxeles involucrados.

13. Comparación estadística de los métodos

Para septiembre de 2025 se calcularon las diferencias absolutas entre los métodos.

Centroide vs. ponderado por área
Estadístico	Diferencia absoluta
Media	1.160 mm
Desviación estándar	4.699 mm
Mediana	0 mm
Máximo	45.429 mm
all_touched vs. ponderado por área
Estadístico	Diferencia absoluta
Media	1.329 mm
Desviación estándar	4.613 mm
Mediana	0 mm
Máximo	35.020 mm
Centroide vs. all_touched
Estadístico	Diferencia absoluta
Media	2.489 mm
Desviación estándar	8.466 mm
Mediana	0 mm
Máximo	67.519 mm

Estos resultados muestran que las diferencias no son necesariamente grandes para todas las parcelas, pero pueden ser relevantes en casos donde una parcela atraviesa varios píxeles.

14. Número de píxeles intersectados

Para septiembre de 2025 se evaluó cuántos píxeles intersectaban cada parcela.

La distribución fue:

Número de píxeles	Parcelas
1	167
2	28
3	2
Total	197

Por lo tanto:

167 parcelas (84.8 %) intersectaron un único píxel.
30 parcelas (15.2 %) intersectaron más de un píxel.

Las diferencias entre métodos aparecen principalmente cuando una parcela intersecta múltiples píxeles con diferentes valores de precipitación.

15. Selección del método de extracción

Después de comparar las estrategias, se seleccionó la extracción ponderada por área para generar la precipitación mensual a nivel parcela.

La decisión se basa en que este método:

Utiliza la geometría completa de la parcela.
Considera todos los píxeles que intersectan la parcela.
Pondera cada píxel según la superficie real que aporta a la parcela.
Evita asignar el mismo peso a píxeles con diferentes grados de cobertura.
Mantiene una interpretación espacial clara.
Es reproducible.
Permite validar geométricamente que los pesos cubren la totalidad de la parcela.

Los métodos de centroide y all_touched se conservaron como métodos de referencia para auditoría y comparación, pero no se combinaron mediante un promedio arbitrario.

16. Optimización computacional

La extracción inicial mediante intersección directa de geometrías fue utilizada como referencia.

Posteriormente se construyó una estructura espacial STRtree para acelerar la búsqueda de los píxeles candidatos que intersectan cada parcela.

La cuadrícula CHIRPS contiene:

65 × 72 = 4680 píxeles

Las geometrías de estos píxeles fueron construidas una sola vez y transformadas al CRS métrico utilizado para calcular las áreas de intersección.

Esto permitió realizar la extracción de forma mucho más eficiente sin cambiar el resultado numérico.

17. Validación de la implementación optimizada

La implementación optimizada fue comparada contra la implementación de referencia para septiembre de 2025.

Resultados:

Parcelas comparadas: 197

Máxima diferencia:
≈ 0 mm para centroide

Máxima diferencia:
≈ 0 mm para all_touched

Máxima diferencia:
5.68 × 10⁻¹⁴ mm para ponderación por área

Las diferencias corresponden a precisión numérica de punto flotante.

Posteriormente, la función reutilizable de extracción ponderada por área fue validada nuevamente:

Máxima diferencia respecto a referencia:
1.58 × 10⁻¹⁰ mm

Diferencia media:
4.10 × 10⁻¹² mm

Por lo tanto, la optimización computacional no modificó de forma significativa los resultados.

18. Dataset final de precipitación

Después de procesar los 48 rasters mensuales se generó una tabla a nivel:

parcela × mes

El dataset contiene:

197 parcelas × 48 meses = 9456 observaciones

Dimensiones finales:

9456 filas × 8 columnas

Las columnas son:

Columna	Descripción
ID_POLIGON	Identificador de parcela
area_weighted_mm	Precipitación mensual ponderada por área
n_pixeles	Número de píxeles intersectados
suma_pesos	Suma de los pesos espaciales
area_intersecciones_m2	Área total de intersección
area_parcela_m2	Área de la parcela
year	Año
month	Mes

La variable principal para posteriores etapas de ingeniería de características es:

area_weighted_mm

y representa la precipitación mensual promedio espacialmente ponderada dentro de la parcela.

No representa el volumen total de agua recibido por la parcela.

19. Validación estructural del dataset final

Después de guardar el dataset se realizó una segunda lectura desde disco para comprobar que el archivo generado conservara su integridad.

Resultados:

Shape:
(9456, 8)

Duplicados parcela-mes:
0

Valores nulos:
0

Parcelas únicas:
197

Periodos únicos:
48

Además:

Cada parcela tiene exactamente 48 meses.
Cada mes contiene exactamente 197 parcelas.
No existen combinaciones parcela-mes duplicadas.
No existen meses faltantes.
No existen parcelas faltantes.
20. Auditoría de valores de precipitación

Sobre las 9,456 observaciones finales se obtuvieron los siguientes estadísticos:

Estadístico	Precipitación (mm/mes)
Media	69.514
Desviación estándar	71.653
Mínimo	0.000
Percentil 1	0.000
Percentil 5	5.757
Percentil 25	14.562
Mediana	38.220
Percentil 75	111.911
Percentil 95	227.132
Percentil 99	302.371
Máximo	392.024

No se identificaron:

Valores negativos.
Valores superiores a 500 mm/mes a nivel de parcela.
Valores superiores a 800 mm/mes.
Valores superiores a 1000 mm/mes.

No se eliminaron valores extremos automáticamente.

21. Valores cero a nivel parcela

En el dataset final se identificaron:

222 observaciones exactamente iguales a 0 mm

Estas observaciones fueron conservadas.

Los ceros fueron validados directamente contra los rasters originales, confirmando que no fueron generados por el proceso de extracción.

Por lo tanto, se consideran observaciones válidas y no valores faltantes.

22. Comportamiento mensual

Como revisión exploratoria, se calculó la climatología mensual utilizando las observaciones disponibles de los cuatro años.

El patrón interno observado muestra:

Valores relativamente bajos durante invierno y principios de primavera.
Incremento de precipitación durante mayo.
Mayores valores durante junio-septiembre.
Reducción durante octubre.
Descenso adicional durante noviembre y diciembre.

Los valores medios mensuales obtenidos fueron:

Mes	Media (mm)
Enero	12.417
Febrero	15.500
Marzo	13.006
Abril	23.970
Mayo	75.483
Junio	129.170
Julio	155.636
Agosto	140.137
Septiembre	129.883
Octubre	88.768
Noviembre	35.578
Diciembre	14.617

Esta revisión se utilizó como control de consistencia interna de los datos.

No se utilizó este comportamiento por sí solo como evidencia causal sobre el rendimiento agrícola.

23. Auditoría de meses con muchos ceros

Se revisaron específicamente los meses que presentaron mayor cantidad de valores cero en la tabla parcelaria.

Enero 2023
Parcelas con 0 mm: 48
Media: 4.981 mm
Mediana: 6.341 mm
Febrero 2023
Parcelas con 0 mm: 167
Media: 0.644 mm
Mediana: 0 mm
Marzo 2024
Parcelas con 0 mm: 7
Media: 4.875 mm
Mediana: 5.757 mm

Los valores cero de estos meses fueron previamente comprobados directamente contra los rasters originales.

Por lo tanto, no se consideraron errores de procesamiento.

24. Principios de integridad aplicados

Durante la auditoría se siguieron los siguientes principios:

Los rasters originales no fueron modificados.
Los valores NoData fueron tratados como ausencia de información.
Los valores cero válidos fueron conservados.
No se eliminaron valores extremos de manera arbitraria.
No se realizó interpolación espacial para aumentar artificialmente la resolución.
Las geometrías de las parcelas fueron preservadas.
Los cálculos de área se realizaron utilizando un CRS métrico.
La suma de pesos fue validada.
La cobertura espacial fue validada para los 48 meses.
La estructura parcela-mes fue validada después de guardar el resultado.
La implementación optimizada fue comparada contra una implementación de referencia.
Todas las decisiones metodológicas fueron mantenidas explícitas y reproducibles.
25. Archivo generado

El dataset procesado fue almacenado en:

data/interim/climate/chirps_parcel_month_area_weighted.csv

Este archivo representa la versión intermedia validada de precipitación mensual a nivel parcela.

El archivo original CHIRPS permanece sin modificaciones.

26. Estado de la auditoría
Validado
 48 archivos CHIRPS identificados.
 Cobertura enero 2022 — diciembre 2025.
 12 meses por año.
 Sin meses faltantes.
 CRS consistente.
 Resolución consistente.
 Dimensiones consistentes.
 NoData identificado.
 Cobertura espacial de las 197 parcelas.
 Disponibilidad de datos para todas las parcelas y meses.
 Valores cero validados contra los rasters originales.
 Comparación de métodos de extracción.
 Validación geométrica de la ponderación por área.
 Validación de la implementación optimizada.
 9456 observaciones finales.
 197 parcelas.
 48 periodos.
 0 duplicados parcela-mes.
 0 valores nulos.
 0 valores negativos.
 Dataset guardado y verificado después de su escritura.
Decisión metodológica

La precipitación mensual a nivel parcela se representará mediante:

Extracción raster ponderada por área (area-weighted zonal extraction).

Los métodos de centroide y all_touched se conservarán como referencias de auditoría y comparación, pero no se combinarán arbitrariamente con el método seleccionado.

27. Conclusión

La auditoría confirma que los datos mensuales de precipitación CHIRPS proporcionados para el reto son temporal y espacialmente consistentes para las 197 parcelas del estudio.

La transformación de los datos raster a información a nivel parcela se realizó mediante una extracción ponderada por área, utilizando la superficie real de intersección entre cada píxel y cada parcela.

La metodología permite conservar la información espacial disponible sin introducir una precisión artificial mediante interpolación.

El resultado final es una tabla de 9,456 observaciones parcela-mes correspondiente a 197 parcelas y 48 meses, sin duplicados, sin valores nulos y sin meses o parcelas faltantes.

Este dataset queda disponible como entrada intermedia para la siguiente etapa del proyecto: la integración de precipitación con temperatura y posteriormente la construcción de variables climáticas y agronómicas temporalmente alineadas con el ciclo de cultivo de cebada.


### Y aquí sí cerramos algo importante

Con este documento tenemos oficialmente:

```text
01_auditoria_geoespacial.md
        ↓
Geometrías + CRS + topografía
        ↓
02_auditoria_precipitacion.md
        ↓
CHIRPS + extracción ponderada
        ↓
chirps_parcel_month_area_weighted.csv

Y no vamos todavía a hacer features climáticas. Primero quiero que estos dos documentos estén guardados en Git y que dejemos registrado el estado del proyecto.

El siguiente paso, después de que guardes este .md, será revisar qué archivos están modificados/no trackeados con git status y hacer un commit limpio de toda esta etapa de auditoría.