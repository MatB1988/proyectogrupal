import json
import os
import numpy as np
import pandas as pd

# no modificar
folder_data = "1_data_extract"
folder_pipeline = "2_pipeline"
folder_output = "3_output"
yelp_folder = "yelp"

data = []
with open(os.path.join(
    folder_data,yelp_folder, "review.json"), "r") as file:
        for line in file:
            data.append(json.loads(line))
data_yelp_reviews = pd.DataFrame(data)

data_yelp_reviews['user_time_year'] = pd.to_datetime(data_yelp_reviews['date']).dt.year
data_yelp_reviews['user_time_month'] = pd.to_datetime(data_yelp_reviews['date']).dt.month
data_yelp_reviews['user_time_day'] = pd.to_datetime(data_yelp_reviews['date']).dt.day
data_yelp_reviews['user_time_hms'] = pd.to_datetime(data_yelp_reviews['date']).dt.time

data_yelp_reviews_norm = data_yelp_reviews.loc[
    (data_yelp_reviews['user_time_year'] >= 2020) &
    (data_yelp_reviews['user_time_month'] >= 7)].copy().sort_values(
        ["user_time_year","user_time_month"]).drop(
            columns=["useful","funny","cool"]).rename(columns={
                "stars":"rating",
                "text":"user_text",
                "date":"user_time"
            })

df_id_yelp = pd.read_csv(
    os.path.join(folder_output,'df_id_yelp.csv'))

data_yelp_reviews_norm_filtrado = data_yelp_reviews_norm.loc[
    data_yelp_reviews_norm['business_id'].isin(df_id_yelp['business_id'].to_list())
    ]#.drop(columns=["state"])

# geo referenciamos

data_yelp_geoloc = pd.read_csv(
    os.path.join(folder_output,'data_yelp_geoloc.csv'))

data_yelp_reviews_norm_filtrado_zcta = pd.merge(
    left=data_yelp_reviews_norm_filtrado,
    right=data_yelp_geoloc,
    how='left'
    )

# guardamos el archivo grande en output
data_yelp_reviews_norm_filtrado_zcta.to_parquet(
    os.path.join(folder_pipeline, "data_yelp_reviews_norm.parquet")
    )