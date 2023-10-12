import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
gmaps_kpi_popularidad = pd.read_parquet(
    os.path.join(folder_pipeline,'gmaps_kpi_popularidad.parquet'))

gmaps_kpi = gmaps_kpi_popularidad
#gmaps_kpi = pd.merge(left=gmaps_kpi_popularidad,right=gmaps_kpi_satisfaccion, how='left')

gmaps_kpi.to_parquet(
    os.path.join(folder_output,'gmaps_kpi_popularidad.parquet'))