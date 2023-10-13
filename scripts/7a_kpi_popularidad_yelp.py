import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"


# importamos el df
data_yelp_reviews = pd.read_parquet(
    os.path.join(folder_output,'data_yelp_reviews_norm.parquet'))

# filtramos nuestro df
columns_interes = [
    "state_name","state_code","zcta5_geoid",
    "business_id",
    "user_time_year","user_time_month","user_time_day",
    "rating"]

yelp_kpi_popularidad = data_yelp_reviews[
    columns_interes].sort_values(
        by=[
            "state_name","state_code","zcta5_geoid","business_id",
            "user_time_year","user_time_month","user_time_day"]
        ).copy() # type: ignore


# por restaurante: business_id
yelp_kpi_popularidad_rating_business_id = yelp_kpi_popularidad.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "business_id","user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"business_id_rating_size"})
yelp_kpi_popularidad_rating_business_id["business_id_size_pctchange"] = yelp_kpi_popularidad_rating_business_id.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "business_id","user_time_year"
        ],
    dropna=False
    )["business_id_rating_size"].pct_change(1)*100

# por zona: zcta5_geoid
yelp_kpi_popularidad_rating_zcta5_geoid = yelp_kpi_popularidad.groupby(
     by=[
        "state_name","state_code","zcta5_geoid",
        "user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"zcta5_geoid_rating_size"})
yelp_kpi_popularidad_rating_zcta5_geoid["zcta5_geoid_size_pctchange"] = yelp_kpi_popularidad_rating_zcta5_geoid.groupby(
    by=[
        "state_name","state_code","zcta5_geoid",
        "user_time_year"
        ],
    dropna=False
    )["zcta5_geoid_rating_size"].pct_change(1)*100

# calculo del KPI segun crecimiento relativo
yelp_kpi_popularidad_crecimiento = pd.merge(
    left=yelp_kpi_popularidad_rating_business_id.drop(columns=["business_id_rating_size"]),
    right=yelp_kpi_popularidad_rating_zcta5_geoid.drop(columns=["zcta5_geoid_rating_size"]),
    how='left'
    ).dropna()

yelp_kpi_popularidad_crecimiento["kpi_popularidad_crecimiento"] = yelp_kpi_popularidad_crecimiento[
    "business_id_size_pctchange"] - yelp_kpi_popularidad_crecimiento["zcta5_geoid_size_pctchange"]
yelp_kpi_popularidad_crecimiento.drop(
    columns=["business_id_size_pctchange","zcta5_geoid_size_pctchange"], inplace=True)


# calculo del KPI segun parte del total
yelp_kpi_popularidad_parte = pd.merge(
    left=yelp_kpi_popularidad_rating_business_id.drop(columns=["business_id_size_pctchange"]),
    right=yelp_kpi_popularidad_rating_zcta5_geoid.drop(columns=["zcta5_geoid_size_pctchange"]),
    how='left'
).dropna()
yelp_kpi_popularidad_parte["kpi_popularidad_parte"] = (
    yelp_kpi_popularidad_parte["business_id_rating_size"] / yelp_kpi_popularidad_parte["zcta5_geoid_rating_size"]
    )*100
yelp_kpi_popularidad_parte.drop(
    columns=["business_id_rating_size","zcta5_geoid_rating_size"], inplace=True)

#### EXPORTAR DF FINAL
yelp_kpi_popularidad = pd.merge(
    left=yelp_kpi_popularidad_parte,
    right=yelp_kpi_popularidad_crecimiento,
    how='left')

yelp_kpi_popularidad.to_parquet(
    os.path.join(folder_pipeline,'yelp_kpi_popularidad.parquet'))

