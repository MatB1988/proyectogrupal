import os
import glob
import json
import pandas as pd

# no modificar
folder_data = "1_data_extract"
folder_pipeline = "2_pipeline"
folder_gmaps = "gmaps"
folder_output = "3_output"

# obtenemos una lista de los archivos en pipeline
list_files_gmaps_state_norm = glob.glob(
    os.path.join(folder_pipeline,folder_gmaps,"review-*_norm.parquet"))
list_files_gmaps_state_norm.sort()

# aplicamos read_parquet a todos los archivos de la lista
# generamos una lista de archivos parquet
list_dfs_gmaps_state_norm = [
    pd.read_parquet(f) for f in list_files_gmaps_state_norm
    ]

# unimos los df de la lista de archivos parquet
data_gmaps_reviews_norm = pd.concat(
    list_dfs_gmaps_state_norm, ignore_index=True)

df_id_gmaps = pd.read_csv(
    os.path.join(folder_output,'df_id_gmaps.csv'))

data_gmaps_reviews_norm_filtrado = data_gmaps_reviews_norm.loc[
    data_gmaps_reviews_norm['gmap_id'].isin(df_id_gmaps['gmap_id'].to_list())
    ].drop(columns=["state"])

# geo referenciamos

data_gmaps_geoloc = pd.read_csv(
    os.path.join(folder_output,'data_gmaps_geoloc.csv'))

data_gmaps_reviews_norm_filtrado_zcta = pd.merge(
    left=data_gmaps_reviews_norm_filtrado,
    right=data_gmaps_geoloc,
    how='left'
    )

# guardamos el archivo grande en pipeline
data_gmaps_reviews_norm_filtrado_zcta.to_parquet(
    os.path.join(folder_pipeline, "data_gmaps_reviews_norm.parquet")
    )