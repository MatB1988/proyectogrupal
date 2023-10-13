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
yelp_reviews = pd.DataFrame(data)

yelp_reviews.to_parquet(
    os.path.join(folder_output,'yelp_reviews.parquet'))