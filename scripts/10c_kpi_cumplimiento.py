import os
import json
import numpy as np
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"


# importamos el df
data_ml_gmaps = pd.read_parquet(
    os.path.join(folder_pipeline,'data_ml_gmaps.parquet'))

data_ml_gmaps["ml_indice"] = data_ml_gmaps["rating_historico"] - data_ml_gmaps["predicted_rating_historico"]
data_ml_gmaps["ml_categoria"] = np.where(data_ml_gmaps["ml_indice"]<0, "prospecto", "tendencia")
data_ml_gmaps["ml_indice_rank_codpostal"] = data_ml_gmaps.groupby(
    ["zcta5_geoid","ml_categoria"])["ml_indice"].rank(pct=True)
data_ml_gmaps["ml_indice_rank_estado"] = data_ml_gmaps.groupby(
    ["state_code","ml_categoria"])["ml_indice"].rank(pct=True)


columnas_atributos = [
    'business_id','zcta5_geoid','state_code',
    'RestaurantsDelivery','RestaurantsTakeOut', 'OutdoorSeating',
    'RestaurantsReservations','GoodForKids', 'ByAppointmentOnly',
    'WheelchairAccessible','RestaurantsGoodForGroups', 'BusinessAcceptsCreditCards'
]

data_ml_gmaps_cumplimiento = data_ml_gmaps[columnas_atributos].copy()
data_ml_gmaps_cumplimiento["atributos_business_sum"] = data_ml_gmaps_cumplimiento.sum(
    axis=1, numeric_only=True)

data_ml_gmaps_cumplimiento_cp = data_ml_gmaps_cumplimiento.groupby(
    ["zcta5_geoid"]).max(
        ["atributos_business_sum"]).reset_index()[ # type: ignore
            ["zcta5_geoid","atributos_business_sum"]]
data_ml_gmaps_cumplimiento_cp.rename(
    columns={"atributos_business_sum":"atributos_cp_max"}, inplace=True)

data_ml_gmaps_cumplimiento_state = data_ml_gmaps_cumplimiento.groupby(
    ["state_code"]).max(
        ["atributos_business_sum"]).reset_index()[ # type: ignore
            ["state_code","atributos_business_sum"]]
data_ml_gmaps_cumplimiento_state.rename(
    columns={"atributos_business_sum":"atributos_state_max"}, inplace=True)

data_ml_gmaps_cumplimiento_business = data_ml_gmaps_cumplimiento[
    ["business_id","zcta5_geoid","state_code","atributos_business_sum"]].copy()
data_kpi_gmaps_cumplimiento = pd.merge(
    right=pd.merge(
        right=data_ml_gmaps_cumplimiento_business,
        left=data_ml_gmaps_cumplimiento_cp,
        how='left'),
    left=data_ml_gmaps_cumplimiento_state,
    how='left')
data_kpi_gmaps_cumplimiento["kpi_cumplimiento_cp"] = (
    data_kpi_gmaps_cumplimiento["atributos_business_sum"] / data_kpi_gmaps_cumplimiento["atributos_cp_max"]) * 100
data_kpi_gmaps_cumplimiento["kpi_cumplimiento_state"] = (
    data_kpi_gmaps_cumplimiento["atributos_business_sum"] / data_kpi_gmaps_cumplimiento["atributos_state_max"]) * 100


# Guardar el DataFrame final como un archivo parquet
data_kpi_gmaps_cumplimiento.to_parquet(
    os.path.join(folder_pipeline,'data_kpi_gmaps_cumplimiento.parquet'),
    index=False)