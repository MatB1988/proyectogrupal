import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"


# importamos el df
data_gmaps_reviews = pd.read_parquet(
    os.path.join(folder_output,'data_gmaps_reviews_norm.parquet'))

# filtramos nuestro df
columns_interes = [
    "state_name","state_code","zcta5_geoid",
    "gmap_id",
    "user_time_year","user_time_month","user_time_day",
    "rating"]

gmaps_kpi_popularidad = data_gmaps_reviews[
    columns_interes].sort_values(
        by=[
            "state_name","state_code","zcta5_geoid","gmap_id",
            "user_time_year","user_time_month","user_time_day"]
        ).copy() # type: ignore


# por restaurante: gmap_id
gmaps_kpi_popularidad_rating_gmap_id = gmaps_kpi_popularidad.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "gmap_id","user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"gmap_id_rating_size"})
gmaps_kpi_popularidad_rating_gmap_id["gmap_id_size_pctchange"] = gmaps_kpi_popularidad_rating_gmap_id.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "gmap_id","user_time_year"
        ],
    dropna=False
    )["gmap_id_rating_size"].pct_change(1)*100

# por zona: zcta5_geoid
gmaps_kpi_popularidad_rating_zcta5_geoid = gmaps_kpi_popularidad.groupby(
     by=[
        "state_name","state_code","zcta5_geoid",
        "user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"zcta5_geoid_rating_size"})
gmaps_kpi_popularidad_rating_zcta5_geoid["zcta5_geoid_size_pctchange"] = gmaps_kpi_popularidad_rating_zcta5_geoid.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "user_time_year"
        ],
    dropna=False
    )["zcta5_geoid_rating_size"].pct_change(1)*100

# calculo del KPI segun crecimiento relativo
gmaps_kpi_popularidad_crecimiento = pd.merge(
    left=gmaps_kpi_popularidad_rating_gmap_id.drop(columns=["gmap_id_rating_size"]),
    right=gmaps_kpi_popularidad_rating_zcta5_geoid.drop(columns=["zcta5_geoid_rating_size"]),
    how='left'
    ).dropna()

gmaps_kpi_popularidad_crecimiento["kpi_popularidad_crecimiento"] = gmaps_kpi_popularidad_crecimiento[
    "gmap_id_size_pctchange"] - gmaps_kpi_popularidad_crecimiento["zcta5_geoid_size_pctchange"]
gmaps_kpi_popularidad_crecimiento.drop(
    columns=["gmap_id_size_pctchange","zcta5_geoid_size_pctchange"], inplace=True)

#### EXPORTAR DF FINAL
gmaps_kpi_popularidad_crecimiento.to_parquet(
    os.path.join(folder_pipeline,'gmaps_kpi_popularidad_crecimiento.parquet'))

# calculo del KPI segun parte del total
gmaps_kpi_popularidad_parte = pd.merge(
    left=gmaps_kpi_popularidad_rating_gmap_id.drop(columns=["gmap_id_size_pctchange"]),
    right=gmaps_kpi_popularidad_rating_zcta5_geoid.drop(columns=["zcta5_geoid_size_pctchange"]),
    how='left'
).dropna()
gmaps_kpi_popularidad_parte["kpi_popularidad_parte"] = (
    gmaps_kpi_popularidad_parte["gmap_id_rating_size"] / gmaps_kpi_popularidad_parte["zcta5_geoid_rating_size"]
    )*100
gmaps_kpi_popularidad_parte.drop(
    columns=["gmap_id_rating_size","zcta5_geoid_rating_size"], inplace=True)

#### EXPORTAR DF FINAL
gmaps_kpi_popularidad_parte.to_parquet(
    os.path.join(folder_pipeline,'gmaps_kpi_popularidad_parte.parquet'))

