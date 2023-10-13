import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
yelp_kpi_popularidad = pd.read_parquet(
    os.path.join(folder_pipeline,'yelp_kpi_popularidad.parquet'))

yelp_kpi = yelp_kpi_popularidad
#yelp_kpi = pd.merge(left=yelp_kpi_popularidad,right=yelp_kpi_satisfaccion, how='left')

yelp_kpi.to_parquet(
    os.path.join(folder_output,'yelp_kpi.parquet'))