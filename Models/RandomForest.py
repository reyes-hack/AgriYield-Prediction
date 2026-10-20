import pandas as pd
import numpy as np
import joblib
import sklearn
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor


def random_forest_model():
    return make_pipeline(SimpleImputer(strategy='median'), 
                         RandomForestRegressor(n_estimators=300, min_samples_leaf=5, max_features=0.4, random_state=42, n_jobs=-1))
    

REPS = 20
K = 5
min_parcelas_mun = 8 #Los munucipios con menos parcelas se agrupan en eotros
META = ["ID_POLIGON", "CONJUNTO", "Municipio"]
target = 'rendimiento_t_ha'

#Load Data
df = pd.read_csv('../Dataset/NewDataset/dataset_final_entrenamiento.csv')
y = df[target].to_numpy()

features = [c for c in df.columns if c not in META + [target]]
best_cols = ["precipitacion_acumulada_abril_octubre", "Tmin_media_abril_octubre",
    "elevacion_media", "pendiente_media", "área_ha",
    "s2_ndvi_mes_05", "s2_ndvi_mes_06", "s2_ndvi_max", "s2_ndvi_auc"]
cols = [c for c in best_cols if c in df.columns]

model_features = cols + [c for c in df.columns if c.startswith("mun_")]

#MODEL
model = random_forest_model()
model.fit(df[model_features], df[target])

#Save Model
joblib.dump({
    'modelo': model,
    'variables': model_features,
    'version_sklearn': sklearn.__version__
}, '../Models/RandomForestModel.joblib')
 