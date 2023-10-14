import json
import os
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
data_gmaps_metadata = pd.read_parquet(
    os.path.join(folder_pipeline,'gmaps_metadata_filtrado.parquet')).drop(
        columns=["geo_point","geo_looker","hours"]
    ).rename(
    columns={
        "gmap_id":"business_id",
        "avg_rating":"rating_historico",
        "num_of_reviews":"review_count_historico",
        "MISC":"attributes",
        "category":"categories"})
    
data_yelp_metadata = pd.read_parquet(
    os.path.join(folder_pipeline,'yelp_metadata_filtrado.parquet')).drop(
        columns=["geo_point","geo_looker","hours"]
    ).rename(columns={
        "stars":"rating_historico",
        "review_count":"review_count_historico"})

data_business_metadata = pd.concat([data_gmaps_metadata, data_yelp_metadata]).rename(
    columns={"zcta5_geoid":"codigo_postal_zcta"})

data_business_metadata.to_parquet(
    os.path.join(folder_output,'business_metadata_filtrado.parquet'))