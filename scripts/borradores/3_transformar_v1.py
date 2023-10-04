import os
import json
import numpy as np
import pandas as pd

folder_data = "1_external"
folder_pipeline = "2_pipeline"
folder_output = "3_output"

folder_yelp = "Yelp"

data_checkin_json = []
with open(os.path.join(folder_data,folder_yelp, "checkin.json"), "r") as file:
    for line in file:
        data_checkin_json.append(json.loads(line))

df_checkin_yelp = pd.DataFrame(data_checkin_json)
df_checkin_yelp.to_pickle(os.path.join(folder_output, 'df_checkin_yelp.pkl'))

#desanidar = []
#for _, row in df_checkin_yelp.iterrows():
#    business_id = row['business_id']
#    dates = row['date'].split(', ')
#    for date in dates:
#        time, date = date.split(' ')
#        desanidar.append([business_id, time, date])
#df_desa_checkin_yelp = pd.DataFrame(desanidar, columns=['business_id', 'fecha', 'hour'])
#df_desa_checkin_yelp.to_parquet(os.path.join(folder_output, 'yelp_checkin.parquet'))