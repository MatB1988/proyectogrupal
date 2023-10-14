import json
import os
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

data_gmaps_reviews = pd.read_parquet(
    os.path.join(folder_pipeline,'data_gmaps_reviews_norm.parquet')).rename(
    columns={"gmap_id":"business_id"}).drop(columns=["user_name"])
    
data_yelp_reviews = pd.read_parquet(
    os.path.join(folder_pipeline,'data_yelp_reviews_norm.parquet')).drop(
        columns=["review_id"])

data_business_reviews = pd.concat([data_gmaps_reviews, data_yelp_reviews]).rename(
    columns={"zcta5_geoid":"codigo_postal_zcta"})

data_business_reviews.to_parquet(
    os.path.join(folder_output,'business_metadata_filtrado.parquet'))