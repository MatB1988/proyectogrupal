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

#business_kpi.to_parquet(os.path.join(folder_output,'business_kpi.parquet'))

#### TABLAS AJUSTADAS PARA DASHBOARD
business_kpi.drop(columns=["kpi_cumplimiento_state"], inplace=True)

business_ml = pd.read_parquet(
    os.path.join(folder_output,'business_ml.parquet')).convert_dtypes()

business_ml_simple = business_ml.drop(
    columns=["RestaurantsDelivery", "RestaurantsTakeOut", "OutdoorSeating",
             "RestaurantsReservations", "GoodForKids", "ByAppointmentOnly",
             "WheelchairAccessible", "RestaurantsGoodForGroups", "BusinessAcceptsCreditCards"]
    ).copy()


# TABLAS CON DATOS DE CONTACTO: DF 1
business_contacto = business_ml_simple[
    ["business_id","name","address","codigo_postal_zcta","state_code"]
    ].drop_duplicates().copy()
business_contacto.to_parquet(os.path.join(folder_output,'business_contacto.parquet'))


#### METRICAS PARA EL DASHBOARD POR CATEGORIA DE ML

# insumos
business_contacto_2join = business_contacto[["business_id","name"]].copy()

business_ml_dashboard = business_ml_simple[
    ["business_id","rating_historico","predicted_rating_historico","ml_indice","ml_categoria"
    #,"rndmfrst_predicted_rating_hist","rndmfrst_weighted_avg"
    ]].drop_duplicates().copy()
business_ml_dashboard.to_parquet(os.path.join(folder_output,'business_ml_dashboard.parquet'))

# union
business_metricas_dashboard = pd.merge(
    right=business_kpi,
    left=business_ml_dashboard)
business_metricas_dashboard = business_metricas_dashboard.merge(business_contacto_2join, how='left')
columns_first = ["ml_categoria","business_id","name",
                 "codigo_postal_zcta","state_name","state_code",
                 "user_time_year","user_time_month",
                 "kpi_popularidad_parte","kpi_satisfaccion_suma","kpi_cumplimiento_cp"]
business_metricas_dashboard = business_metricas_dashboard.reindex(
    columns=columns_first + list(business_metricas_dashboard.columns.difference(columns_first, sort=False)))
columns_float = business_metricas_dashboard.select_dtypes(include=[float]).columns.tolist() # type: ignore
business_metricas_dashboard[columns_float] = business_metricas_dashboard[columns_float].round(2)

# DF 2
business_metricas_dashboard.to_parquet(os.path.join(folder_output,'business_metricas_dashboard_todos.parquet'))

# TABLAS SEPARADAS POR CATEGORIA DE ML

# DF 3
business_metricas_dashboard_prospecto = business_metricas_dashboard.loc[
    business_metricas_dashboard["ml_categoria"].isin(["prospecto"])].drop_duplicates().copy()
business_metricas_dashboard_prospecto.to_parquet(os.path.join(folder_output,'business_metricas_dashboard_prospecto.parquet'))

# DF 4
business_metricas_dashboard_tendencia = business_metricas_dashboard.loc[
    business_metricas_dashboard["ml_categoria"].isin(["tendencia"])].drop_duplicates().copy()
business_metricas_dashboard_tendencia.to_parquet(os.path.join(folder_output,'business_metricas_dashboard_tendencia.parquet'))
