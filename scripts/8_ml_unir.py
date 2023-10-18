import os
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
data_ml_gmaps = pd.read_parquet(os.path.join(folder_pipeline,'data_ml_gmaps.parquet'))
data_ml_gmaps.rename(columns={"zcta5_geoid":"codigo_postal_zcta"}, inplace=True)

# Calculamos el DF con base en los resultados de la Red Neuronal
# debido a su mejor efectividad (menos errores) (MSE) con respecto a Random Forest:
# Error Cuadrático Medio (MSE) Random Forest: 0.2458615996925067
# Error Cuadrático Medio (MSE) Red Neuronal: 0.24178054294438533

data_ml_gmaps["ml_indice"] = round(
    data_ml_gmaps["rating_historico"] - data_ml_gmaps["predicted_rating_historico"]
    ,2)
data_ml_gmaps["ml_categoria"] = np.where(data_ml_gmaps["ml_indice"]<0, "prospecto", "tendencia")
data_ml_gmaps["ml_indice_rank_codpostal"] = data_ml_gmaps.groupby(
    ["codigo_postal_zcta","ml_categoria"]
    )["ml_indice"].rank(pct=True)
data_ml_gmaps["ml_indice_rank_estado"] = data_ml_gmaps.groupby(
    ["state_code","ml_categoria"])["ml_indice"].rank(pct=True)

data_ml_gmaps["ml_indice_rank_estado"] = data_ml_gmaps["ml_indice_rank_estado"].copy()*100
data_ml_gmaps["ml_indice_rank_estado"] = data_ml_gmaps["ml_indice_rank_estado"].copy().round(2)

data_ml_gmaps.rename(
    columns={"predictions":"rndmfrst_predicted_rating_hist",
             "weighted_avg":"rndmfrst_weighted_avg"},
    inplace=True)
#ml_yelp = pd.read_parquet(os.path.join(folder_pipeline,'ml_yelp.parquet'))
#ml_yelp.drop(columns=["name","address","latitude","longitude"], inplace=True)

business_id_yelp = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_popularidad.parquet'))
business_id = business_id_yelp["business_id"].to_list()

ml_yelp_ficticio = data_ml_gmaps.loc[
    ~data_ml_gmaps["business_id"].isin(business_id)].copy()

n_size = len(ml_yelp_ficticio)
ml_yelp_ficticio["rating_historico"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))
ml_yelp_ficticio["predicted_rating_historico"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))

business_ml = pd.merge(
    left=data_ml_gmaps,
    right=ml_yelp_ficticio,
    how='left')

# export DF final
business_ml = data_ml_gmaps.copy() # aun sin yelp
business_ml.dropna(inplace=True)
business_ml.to_parquet(os.path.join(folder_output,'business_ml.parquet'))