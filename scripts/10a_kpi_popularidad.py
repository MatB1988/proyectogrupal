import os
import pandas as pd

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"


# importamos el df
data_business_reviews = pd.read_parquet(
    os.path.join(folder_output,'business_reviews_norm.parquet'))

# filtramos nuestro df
columns_interes = [
    "state_name","state_code","codigo_postal_zcta",
    "business_id",
    "user_time_year","user_time_month","user_time_day",
    "rating"]

business_kpi_popularidad = data_business_reviews[
    columns_interes].sort_values(
        by=[
            "state_name","state_code","codigo_postal_zcta","business_id",
            "user_time_year","user_time_month","user_time_day"]
        ).copy() # type: ignore


# por restaurante: business_id
business_kpi_popularidad_rating_business_id = business_kpi_popularidad.groupby(
    by=[
        "state_name","state_code","codigo_postal_zcta",
        "business_id","user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"business_id_rating_size"})
business_kpi_popularidad_rating_business_id["business_id_size_pctchange"] = business_kpi_popularidad_rating_business_id.groupby(
    by=[
        "state_name","state_code","codigo_postal_zcta",
        "business_id","user_time_year"
        ],
    dropna=False
    )["business_id_rating_size"].pct_change(1)*100

# por zona: zcta5_geoid
business_kpi_popularidad_rating_codigo_postal_zcta = business_kpi_popularidad.groupby(
     by=[
        "state_name","state_code","codigo_postal_zcta",
        "user_time_year","user_time_month"
        ],
    dropna=False
    )["rating"].size().reset_index().rename(columns={"rating":"codigo_postal_zcta_rating_size"})
business_kpi_popularidad_rating_codigo_postal_zcta["codigo_postal_zcta_size_pctchange"] = business_kpi_popularidad_rating_codigo_postal_zcta.groupby(
    by=[
        "state_name","state_code","codigo_postal_zcta",
        "user_time_year"
        ],
    dropna=False
    )["codigo_postal_zcta_rating_size"].pct_change(1)*100

# calculo del KPI segun crecimiento relativo
business_kpi_popularidad_crecimiento = pd.merge(
    left=business_kpi_popularidad_rating_business_id.drop(columns=["business_id_rating_size"]),
    right=business_kpi_popularidad_rating_codigo_postal_zcta.drop(columns=["codigo_postal_zcta_rating_size"]),
    how='left'
    ).dropna()
business_kpi_popularidad_crecimiento["kpi_popularidad_crecimiento"] = business_kpi_popularidad_crecimiento[
    "business_id_size_pctchange"] - business_kpi_popularidad_crecimiento["codigo_postal_zcta_size_pctchange"]
business_kpi_popularidad_crecimiento.drop(
    columns=["business_id_size_pctchange","codigo_postal_zcta_size_pctchange"], inplace=True)

# calculo del KPI segun parte del total
business_kpi_popularidad_parte = pd.merge(
    left=business_kpi_popularidad_rating_business_id.drop(columns=["business_id_size_pctchange"]),
    right=business_kpi_popularidad_rating_codigo_postal_zcta.drop(columns=["codigo_postal_zcta_size_pctchange"]),
    how='left'
    ).dropna()
business_kpi_popularidad_parte["kpi_popularidad_parte"] = (
    business_kpi_popularidad_parte["business_id_rating_size"] / business_kpi_popularidad_parte["codigo_postal_zcta_rating_size"]
    )*100
business_kpi_popularidad_parte.drop(
    columns=["business_id_rating_size","codigo_postal_zcta_rating_size"], inplace=True)

#### DF FINAL
business_kpi_popularidad = pd.merge(
    left=business_kpi_popularidad_parte,
    right=business_kpi_popularidad_crecimiento,
    how='left')

#### EXPORTAR
business_kpi_popularidad.to_parquet(
    os.path.join(folder_pipeline,'business_kpi_popularidad.parquet'),
    index=False)

