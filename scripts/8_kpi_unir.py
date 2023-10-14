import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
business_kpi_popularidad = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_popularidad.parquet'))

business_kpi_satisfaccion = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_satisfaccion.parquet'))

business_kpi = pd.merge(
    left=business_kpi_popularidad,
    right=business_kpi_satisfaccion,
    how='left')

business_kpi.to_parquet(
    os.path.join(folder_output,'business_kpi.parquet'))