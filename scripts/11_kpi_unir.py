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

business_kpi_cumplimiento = pd.read_parquet(
    os.path.join(folder_pipeline,'data_kpi_gmaps_cumplimiento.parquet'))

business_kpi_cumplimiento.rename(
    columns={"zcta5_geoid":"codigo_postal_zcta"}, inplace=True)
business_kpi_cumplimiento.drop(
    columns=["atributos_business_sum","atributos_cp_max","atributos_state_max"],
    inplace=True)

# datos ficticios
# business_kpi_satisfaccion.drop(columns=["kpi_satisfaccion_rating","kpi_satisfaccion_sentimiento"],inplace=True)
#business_kpi_sindefinir = business_kpi_popularidad[["state_name","state_code","codigo_postal_zcta","business_id"]].copy()
#business_kpi_sindefinir.drop_duplicates(inplace=True)
#n_size = len(business_kpi_sindefinir)
#business_kpi_sindefinir["kpi_3i_sindefinir"] = np.random.normal(loc=60, scale=15.0, size=(n_size))

business_kpi = pd.merge(
    left=pd.merge(
        left=business_kpi_popularidad,
        right=business_kpi_satisfaccion,
        how='left'),
    right=business_kpi_cumplimiento,
    how='left')

business_kpi_cumplimiento.rename(
    columns={"zcta5_geoid":"codigo_postal_zcta"}, inplace=True)
business_kpi_cumplimiento.drop(
    columns=["atributos_business_sum","atributos_cp_max","atributos_state_max",
             "codigo_postal_zcta","state_code"],
    inplace=True)

business_kpi = pd.merge(
    left=pd.merge(
      left=business_kpi_popularidad,
      right=business_kpi_satisfaccion,
      how='left'),
    right=business_kpi_cumplimiento,
    how='left')
business_kpi.drop(
    columns=["kpi_popularidad_crecimiento","kpi_satisfaccion_rating","kpi_satisfaccion_sentimiento"],
    inplace=True)
business_kpi.dropna(inplace=True)

business_kpi.to_parquet(
    os.path.join(folder_output,'business_kpi.parquet'))