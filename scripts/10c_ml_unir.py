import os
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
ml_gmaps = pd.read_parquet(os.path.join(folder_pipeline,'ml_gmaps.parquet'))
#ml_gmaps.drop(columns=["name","address","latitude","longitude"], inplace=True)

#ml_yelp = pd.read_parquet(os.path.join(folder_pipeline,'ml_yelp.parquet'))
#ml_yelp.drop(columns=["name","address","latitude","longitude"], inplace=True)

business_id_yelp = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_popularidad.parquet'))
business_id = business_id_yelp["business_id"].to_list()

ml_yelp_ficticio = ml_gmaps.loc[
    ~ml_gmaps["business_id"].isin(business_id)].copy()

n_size = len(ml_yelp_ficticio)
ml_yelp_ficticio["rating_historico"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))
ml_yelp_ficticio["predictions"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))
ml_yelp_ficticio["weighted_avg"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))
ml_yelp_ficticio["predicted_rating_historico"] = np.random.normal(loc=3.5, scale=0.3, size=(n_size))

business_ml = pd.merge(
    left=ml_gmaps,
    right=ml_yelp_ficticio,
    how='left')

business_ml.to_parquet(
    os.path.join(folder_output,'business_ml.parquet'))