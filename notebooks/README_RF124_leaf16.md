# RF124 leaf16 — reconstrucción limpia

## Archivos requeridos

Este notebook utiliza dos archivos históricos que deben estar dentro del proyecto `AgroCebada-FIRA-2026`:

1. `notebooks/data/interim/tabular/exp38_c_matriz_maestra.csv`
2. `notebooks/EXP24_predicciones_oof.csv`

La matriz maestra se creó en EXP38-C integrando siete tablas: `planet_features`, `chirps_ancho`, `tmax_ancho`, `tmin_ancho`, `tmedia_ancho`, `clima_resumen` y `topo_features`. El notebook de reconstrucción no recrea desde cero esas siete tablas; usa la matriz maestra ya producida y preserva las asignaciones espaciales de folds históricas.

## Ejecución

1. Coloca `RF124_leaf16_reconstruccion_limpia.ipynb` dentro de la carpeta `notebooks/` del proyecto.
2. Confirma que existan los dos archivos requeridos.
3. Instala las dependencias si hacen falta:

   ```bash
   pip install numpy pandas scikit-learn joblib jupyter
   ```

4. Abre Jupyter desde la carpeta del proyecto y ejecuta el notebook de arriba hacia abajo.

## Salidas generadas

- `models/reconstruccion_rf124_leaf16/RF124_leaf16_final.joblib`
- `models/reconstruccion_rf124_leaf16/RF124_leaf16_predicciones_59.csv`
- `models/reconstruccion_rf124_leaf16/metadata.json`
- `reports/metrics/rf124_leaf16_comparacion_oof.csv`
- `reports/tables/rf124_leaf16_metricas_por_fold.csv`
- `reports/tables/rf124_leaf16_predicciones_oof.csv`

## Configuración

- Algoritmo: `RandomForestRegressor`
- `n_estimators=500`
- `min_samples_leaf=16`
- `max_features=1.0`
- `random_state=2026`
- 124 variables predictoras
- 138 parcelas con rendimiento observado
- 59 parcelas para predecir
- 5 folds espaciales originales (38, 25, 25, 25, 25 parcelas)

## Nota de reproducibilidad

La validación OOF y el entrenamiento final son procesos diferentes. Las métricas se calculan con las predicciones fuera de muestra por fold; el modelo final se vuelve a ajustar con las 138 parcelas etiquetadas antes de predecir las 59 parcelas restantes.

Para reproducir la construcción de la matriz desde los archivos de origen, también deben entregarse los pasos previos que generan las siete tablas fuente y sus datos originales. Los notebooks revisados documentan la integración y el modelado, pero no incluyen una secuencia autónoma completa que reconstruya todas esas fuentes desde sus datos crudos.
