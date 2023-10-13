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

data_yelp_reviews.to_parquet(
    os.path.join(folder_output,'yelp_reviews.parquet'))