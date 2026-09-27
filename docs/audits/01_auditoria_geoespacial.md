# 01 — Auditoría de Datos Geoespaciales

## 1. Objetivo de la auditoría

El objetivo de esta auditoría fue validar la integridad espacial, los sistemas de referencia de coordenadas (CRS), la calidad de las geometrías, la cobertura espacial y la compatibilidad entre los datos geoespaciales proporcionados para el reto AgroCebada FIRA 2026.

La auditoría se enfocó en:

- Validar las geometrías de las parcelas.
- Verificar los identificadores de las parcelas.
- Revisar los sistemas de referencia de coordenadas.
- Revisar la cobertura espacial de los datos topográficos.
- Verificar la resolución y metadatos de los rasters de elevación y pendiente.
- Evaluar la compatibilidad entre las parcelas y las cuadrículas raster.
- Analizar inicialmente diferentes estrategias de extracción espacial.

El objetivo final fue asegurar que los datos geoespaciales pudieran integrarse correctamente en un pipeline de machine learning a nivel parcela, evitando inconsistencias espaciales y transformaciones no documentadas.

---

# 2. Fuentes de datos

Durante la auditoría se revisaron las siguientes fuentes geoespaciales.

## 2.1 Polígonos de parcelas

**Archivo:**

`Parcelas_Reto_AGC_CONJUNTO.shp`

El archivo contiene los polígonos georreferenciados de las parcelas agrícolas consideradas en el reto.

Los principales atributos identificados fueron:

| Campo | Descripción |
|---|---|
| `ID_POLIGON` | Identificador único de la parcela en el Shapefile |
| `área_ha` | Área de la parcela en hectáreas |
| `Municipio` | Municipio al que pertenece la parcela |
| `Estado` | Estado al que pertenece la parcela |
| `CONJUNTO` | Partición del conjunto de datos |
| `Cultivo` | Cultivo registrado |
| `geometry` | Geometría poligonal de la parcela |

El Shapefile utiliza el campo `ID_POLIGON` debido a las limitaciones de longitud de nombres de campos del formato Shapefile.

El archivo tabular de rendimiento utiliza el campo:

`ID_POLIGONO`

Ambos campos representan el mismo identificador de parcela y fueron comparados durante la auditoría.

---

## 2.2 Elevación

**Archivo:**

`Elevacion_INEGI_CEM4_120m.tif`

Principales metadatos:

| Propiedad | Valor |
|---|---|
| CRS | EPSG:6372 |
| Resolución | 120 × 120 m |
| Ancho | 2900 píxeles |
| Alto | 3362 píxeles |
| Tipo de dato | float32 |
| NoData | -9999 |
| Variable | Elevación |
| Unidad | metros sobre el nivel del mar |

Los metadatos identifican a INEGI CEM como fuente de los datos.

El raster representa la elevación del terreno con una resolución espacial de 120 metros.

---

## 2.3 Pendiente

**Archivo:**

`Pendiente_INEGI_CEM4_120m_grados.tif`

Principales metadatos:

| Propiedad | Valor |
|---|---|
| CRS | EPSG:6372 |
| Resolución | 120 × 120 m |
| Tipo de dato | float32 |
| NoData | -9999 |
| Variable | Pendiente |
| Unidad | grados |
| Método indicado en metadatos | Horn 3 × 3 |

El raster de pendiente utiliza el mismo CRS, resolución y extensión espacial que el raster de elevación.

---

# 3. Validación de las geometrías de las parcelas

El archivo de parcelas fue inspeccionado utilizando GeoPandas.

El conjunto contiene:

- **197 parcelas**
- **197 geometrías poligonales válidas**
- **197 identificadores únicos**
- Ningún identificador de parcela duplicado.

La extensión espacial aproximada del conjunto de parcelas es:

- Longitud mínima: -98.613
- Longitud máxima: -98.197
- Latitud mínima: 19.524
- Latitud máxima: 19.984

El sistema de referencia de coordenadas de las parcelas es:

```text
EPSG:4326

Este CRS representa coordenadas geográficas expresadas en longitud y latitud.

4. Distribución de las parcelas

Las 197 parcelas se encuentran distribuidas entre tres estados:

Estado	Número de parcelas
Puebla	100
Hidalgo	51
Tlaxcala	46
Total	197

Los municipios representados son:

Municipio	Número de parcelas
Chignahuapan	100
Calpulalpan	44
Singuilucan	23
Almoloya	14
Cuautepec de Hinojosa	9
Emiliano Zapata	3
Nanacamilpa	2
Tepeapulco	1
Apan	1

También se revisó el campo Cultivo.

Se identificó una inconsistencia de capitalización entre valores como:

CEBADA
Cebada

Esta diferencia no afecta las geometrías espaciales, pero deberá considerarse para una posible estandarización posterior si el campo se utiliza como variable durante el modelado.

5. Consistencia de los identificadores de parcela

Se compararon los identificadores de las parcelas entre el Shapefile y el archivo CSV de rendimiento.

El Shapefile utiliza:

ID_POLIGON

mientras que el CSV utiliza:

ID_POLIGONO

Después de considerar esta diferencia en el nombre del campo:

Se encontraron 197 IDs en el Shapefile.
Se encontraron 197 IDs en el CSV.
Los 197 IDs coincidieron.
No se encontraron IDs duplicados.

Esto confirma que la geometría espacial y la información tabular de rendimiento pueden relacionarse mediante el identificador de parcela.

6. Consistencia de la partición del conjunto de datos

El archivo de rendimiento contiene 197 parcelas divididas en:

138 parcelas de entrenamiento
59 parcelas de predicción

La capa espacial fue comparada contra esta partición.

Los mismos 197 identificadores están presentes espacialmente, por lo que cada parcela puede asociarse correctamente con su correspondiente conjunto.

Las 59 parcelas de predicción no deben utilizarse como observaciones etiquetadas durante el entrenamiento del modelo.

7. Sistemas de referencia de coordenadas

Durante la auditoría se identificó una diferencia entre el CRS de las parcelas y el CRS de los rasters topográficos.

Las parcelas utilizan:

EPSG:4326

mientras que los rasters topográficos utilizan:

EPSG:6372

Esta diferencia no representa un error.

EPSG:4326 es un sistema geográfico basado en longitud y latitud, mientras que EPSG:6372 es un sistema de coordenadas proyectadas adecuado para realizar operaciones espaciales métricas en la zona de estudio.

8. Estrategia de transformación de CRS

Para realizar operaciones espaciales con los rasters topográficos, las geometrías de las parcelas fueron transformadas de EPSG:4326 a EPSG:6372.

El archivo original de parcelas no fue modificado.

La transformación se realizó sobre una copia de trabajo:

parcels_projected = parcels.to_crs("EPSG:6372")

Se adoptó este procedimiento porque los rasters topográficos ya se encuentran en EPSG:6372.

Reproyectar los rasters a EPSG:4326 introduciría una transformación innecesaria de la cuadrícula raster y podría alterar su estructura espacial original.

Por lo tanto, se adoptó el siguiente principio:

Cuando sea necesario realizar operaciones métricas sobre un raster, se transforman las geometrías vectoriales al CRS del raster, preservando el raster original.

9. Compatibilidad espacial con los datos topográficos

Después de transformar las parcelas a EPSG:6372, se evaluó su intersección espacial con los rasters de elevación y pendiente.

Los resultados mostraron que:

197 de 197 parcelas intersectan la cobertura espacial de los rasters.
No existen parcelas completamente fuera de la cobertura topográfica.
No es necesario utilizar una fuente adicional para cubrir espacialmente las parcelas.

Por lo tanto, los datos topográficos pueden ser potencialmente extraídos para las 197 parcelas.

10. Resolución espacial e implicaciones

Los rasters topográficos tienen una resolución de:

120 × 120 metros

Por lo tanto, cada píxel representa aproximadamente:

120 m × 120 m = 14,400 m²

equivalentes aproximadamente a:

1.44 hectáreas

Esta resolución es importante debido a que algunas parcelas son relativamente pequeñas respecto al tamaño de un píxel.

Las áreas de las parcelas presentan aproximadamente:

Estadístico	Área
Mínimo	0.35 ha
Mediana	5.46 ha
Media	6.60 ha
Máximo	64.30 ha

Por esta razón, el método utilizado para extraer las variables topográficas debe considerar la relación entre el tamaño de la parcela y la resolución espacial del raster.

11. Evaluación de cobertura de píxeles para parcelas pequeñas

Se realizó una evaluación preliminar utilizando los centros de los píxeles del raster.

Con este enfoque, 17 parcelas no contenían ningún centro de píxel del raster.

Estas parcelas son relativamente pequeñas, con áreas inferiores aproximadamente a 3 hectáreas.

Este resultado no significa que dichas parcelas carezcan de información topográfica.

Significa que, debido a la resolución del raster, utilizar únicamente los centros de los píxeles puede fallar cuando una parcela es pequeña respecto al tamaño de la celda raster.

Este resultado motivó la evaluación de diferentes estrategias de extracción espacial.

12. Métodos candidatos de extracción espacial

Se consideraron tres métodos principales para convertir la información raster en una variable a nivel parcela.

12.1 Extracción mediante centroide
 
En este método se identifica el píxel que contiene el centroide de la parcela y se asigna su valor a toda la parcela.

Ventajas
Es sencillo.
Es computacionalmente eficiente.
Es fácil de reproducir.
Genera una única observación por parcela.
Limitaciones
Utiliza únicamente un píxel.
Puede no representar la heterogeneidad de una parcela.
Puede ser sensible cuando el tamaño de la parcela es pequeño respecto a la resolución del raster.

12.2 Extracción all_touched

En este método se consideran todos los píxeles que tienen alguna intersección con la geometría de la parcela.

Ventajas
Permite utilizar información de todos los píxeles que intersectan la parcela.
Evita el problema de parcelas pequeñas cuyo centroide no coincide con un centro de píxel.
Limitaciones

Los píxeles se consideran sin ponderación por superficie.

Por lo tanto, un píxel que apenas toca la parcela puede recibir el mismo peso que un píxel que está casi completamente cubierto por ella.

12.3 Extracción ponderada por área

En este método se calcula cuánto del área de cada píxel pertenece realmente a la parcela.

Para cada píxel se calcula:

peso_i =
área_intersección_i / área_parcela

Posteriormente, el valor de la parcela se calcula mediante:

valor_parcela =
Σ(valor_i × peso_i)

De esta manera, un píxel contribuye proporcionalmente a la superficie que realmente ocupa dentro de la parcela.

Este método resulta especialmente relevante cuando:

Una parcela atraviesa varios píxeles.
Existen diferencias importantes entre píxeles vecinos.
El tamaño de la parcela es comparable o menor que la resolución del raster.
13. Consideraciones sobre los métodos de extracción

Los tres métodos no representan exactamente la misma interpretación espacial.

Cada uno responde a una pregunta diferente:

Método	Interpretación
Centroide	Valor representativo del punto central de la parcela
all_touched	Promedio de todos los píxeles que intersectan la parcela
Ponderado por área	Promedio considerando cuánto del área de cada píxel pertenece realmente a la parcela

Por esta razón, no se considera metodológicamente correcto simplemente promediar los resultados de los tres métodos.

Antes de seleccionar el método definitivo para elevación y pendiente, se realizará una comparación cuantitativa de los resultados obtenidos mediante cada estrategia.

14. Principios de integridad aplicados

Durante la auditoría se siguieron los siguientes principios:

Los archivos originales no fueron modificados.
Las transformaciones de CRS se realizaron sobre copias de trabajo.
Los metadatos de los rasters fueron revisados antes de realizar extracciones.
Las operaciones espaciales utilizaron CRS explícitos.
No se eliminaron valores únicamente por ser altos o bajos.
Los valores NoData se distinguieron de mediciones válidas.
Los identificadores originales de las parcelas fueron preservados.
Se mantuvo la estructura de 197 parcelas.
Las parcelas de predicción no fueron utilizadas como observaciones etiquetadas para entrenamiento.
Las decisiones relacionadas con extracción espacial se documentarán antes de entrar a la etapa de modelado.
15. Estado de la auditoría
Validado
 Geometrías de las parcelas.
 197 registros de parcelas.
 Identificadores únicos.
 Correspondencia entre IDs espaciales y tabulares.
 Consistencia de la partición entrenamiento/predicción.
 CRS de las parcelas.
 CRS y resolución del raster de elevación.
 CRS y resolución del raster de pendiente.
 Cobertura espacial de las 197 parcelas por los rasters topográficos.
 Identificación del problema de resolución espacial para parcelas pequeñas.
 Evaluación inicial de métodos de extracción espacial.
Pendiente
 Comparar cuantitativamente los tres métodos para elevación.
 Comparar cuantitativamente los tres métodos para pendiente.
 Seleccionar el método definitivo de extracción topográfica.
 Integrar las variables topográficas seleccionadas a la tabla de variables a nivel parcela.

Estas decisiones deberán finalizarse antes de la etapa de ingeniería de características y entrenamiento de modelos.

16. Conclusión

La auditoría geoespacial confirma que las geometrías de las parcelas y los datos topográficos son espacialmente compatibles y pueden integrarse en el pipeline de modelado del reto AgroCebada FIRA 2026.

El principal aspecto técnico identificado es la diferencia entre el tamaño de las parcelas y la resolución espacial de 120 metros de los rasters topográficos.

Esta diferencia puede afectar la representación de la información cuando una parcela es pequeña respecto al tamaño del píxel o cuando atraviesa los límites de varias celdas raster.

Por lo tanto, la metodología de extracción espacial debe considerarse explícitamente como una decisión del pipeline y no como una operación automática sin justificación.

La auditoría deja los datos topográficos listos para una evaluación comparativa de los métodos de extracción antes de su incorporación al modelo predictivo.

