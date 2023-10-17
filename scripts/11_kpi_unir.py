import os
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
business_kpi_popularidad = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_popularidad.parquet'))

business_kpi_satisfaccion = pd.read_parquet(
    os.path.join(folder_pipeline,'business_kpi_satisfaccion.parquet'))

business_kpi_satisfaccion.drop(
    columns=["kpi_satisfaccion_rating","kpi_satisfaccion_sentimiento"],
    inplace=True)

business_kpi_sindefinir = business_kpi_popularidad[
    ["state_name","state_code","codigo_postal_zcta","business_id"]].copy()
business_kpi_sindefinir.drop_duplicates(inplace=True)

n_size = len(business_kpi_sindefinir)
business_kpi_sindefinir["kpi_3i_sindefinir"] = np.random.normal(loc=60, scale=15.0, size=(n_size))

business_kpi = pd.merge(
    left=pd.merge(
        left=business_kpi_popularidad,
        right=business_kpi_satisfaccion,
        how='left'),
    right=business_kpi_sindefinir,
    how='left')

business_kpi.to_parquet(
    os.path.join(folder_output,'business_kpi.parquet'))