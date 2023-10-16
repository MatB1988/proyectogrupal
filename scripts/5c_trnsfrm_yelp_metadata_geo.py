# Liberias
import os
import json
import numpy as np
import pandas as pd
import geopandas as geopd
#import pyogrio
import warnings
warnings.filterwarnings('ignore', message='.*initial implementation of Parquet.*')

#### ENTORNO
# Ruta de la carpeta que contiene los archivos JSON
#ruta_datos = "C:/Users/54280/Documents/GitHub/proyectogrupal/Pruebas/metadata-sitios"

# no modificar
folder_data = "1_data_extract" 
folder_uscensus = "uscensus"
folder_zcta_geo = "zcta_geo"
folder_pipeline = "2_pipeline"
folder_yelp = "yelp"
folder_output = "3_output"

#### DATOS
# importamos el df limpia sin filas duplicadas
data_yelp_business = pd.read_pickle(
    os.path.join(folder_data,folder_yelp, 'business.pkl')
    ).convert_dtypes().iloc[:, :14].drop(
        columns=["city","state","postal_code","is_open"]
    )#.dropna(subset=['categories'])

# filatramos
# lista de palabras clave relacionadas con comida
palabras_clave = [
    "Restaurant", "restaurant",
    "Food", "food",
    "Cafe", "cafe",
    "Diner", "diner",
    "Bakery", "bakery",
    "Lunch", "lunch",
    "Brunch", 'brunch']

# Filtrar los registros que contienen al menos una de las palabras clave en la columna 'category'
data_yelp_business_filtrado = data_yelp_business.loc[
    data_yelp_business['categories'].str.contains('|'.join(palabras_clave))]

# importamos df con datos de geolocalizacion
geodata_zcta = geopd.read_file(
    os.path.join(
        folder_data,folder_uscensus,folder_zcta_geo,'tl_2020_us_zcta520.shp')
    #,engine="pyogrio"
    ).iloc[:,[1,5,9]]
geodata_zcta.rename(
    columns = {"GEOID20":"zcta5_geoid",
               "ALAND20":"zcta5_arealand"},
    inplace = True)

#### GENERACION DE DATOS ESPACIALES
# generamos una columna POINT() 'geometry'
data_yelp_business_filtrado_geo = geopd.GeoDataFrame(
    data_yelp_business_filtrado, geometry = geopd.points_from_xy(
        data_yelp_business_filtrado.longitude, data_yelp_business_filtrado.latitude),
    crs="EPSG:4326"
    ).to_crs(geodata_zcta.crs) # type: ignore

# unicmos los dfs segun la interseccion de point con el polygono de zcta
data_yelp_business_filtrado_zcta = geopd.sjoin(
    data_yelp_business_filtrado_geo,
    geodata_zcta,
    how="left"
    ,op="within"
    )

data_yelp_business_filtrado_zcta["geo_looker"] = data_yelp_business_filtrado_zcta[
    "latitude"].astype(str)+","+data_yelp_business_filtrado_zcta["longitude"].astype(str)

#### FILTRAR POR ZONA GEOGRAFICA
# filtramos las que no pertnencen al territorio EEUU
data_yelp_business_filtrado_zcta_usa = data_yelp_business_filtrado_zcta[
    data_yelp_business_filtrado_zcta["zcta5_geoid"].notnull()].copy()

# Generamos un dummy para las zonas que estan en la zona continental de EEUU
# Defino los límites geográficos de los Estados Unidos
latitud_min = 24.396308
latitud_max = 49.384358
longitud_min = -125.000000
longitud_max = -66.934570

# Filtro lugares dentro de los límites geográficos de los Estados Unidos
# Asigno el resultado a un nuevo df
data_yelp_business_filtrado_zcta_usa ['us_continente'] = np.where((
    (data_yelp_business_filtrado_zcta_usa ['latitude'] >= latitud_min) &
    (data_yelp_business_filtrado_zcta_usa ['latitude'] <= latitud_max) &
    (data_yelp_business_filtrado_zcta_usa ['longitude'] >= longitud_min) &
    (data_yelp_business_filtrado_zcta_usa ['longitude'] <= longitud_max)),1,0)

data_zcta_varsxarea = pd.read_csv(
    os.path.join(folder_data,folder_uscensus,'data_zcta_varsxarea.csv'),
    dtype = {'zcta5_geoid': str}).rename(columns={
        "state_usps":"state_code"}).iloc[:,[0,11,12]].drop_duplicates()

data_yelp_business_filtrado_zcta_usa_census = pd.merge(
    data_yelp_business_filtrado_zcta_usa,
    data_zcta_varsxarea,
    on="zcta5_geoid",
    how="left"
    ).drop(columns=["index_right","zcta5_arealand"]).rename(
        columns={"geometry":"geo_point"}
    )

# Genero un df que contenga el los id y los nombres para que se puedan filtrar las rewiews
df_id_yelp = data_yelp_business_filtrado_zcta_usa_census[['business_id', 'name']].copy()

# Exporto un df con los id y los name para pasar al grupo que esta trabajando con  las rewiews
df_id_yelp.drop_duplicates(inplace=True)
df_id_yelp.to_csv(
    os.path.join(folder_output,'df_id_yelp.csv'))

data_yelp_geoloc = data_yelp_business_filtrado_zcta_usa_census[[
    "business_id","state_name","state_code","zcta5_geoid"]].drop_duplicates().copy()
data_yelp_geoloc.to_csv(
    os.path.join(folder_output, "data_yelp_geoloc.csv")
    ,index=False
    )

#### EXPORTAR DF FINAL
# Exporto df_filtrado para probar union por latitud y longitud
data_yelp_business_filtrado_zcta_usa_census.to_parquet(
    os.path.join(folder_pipeline,'yelp_metadata_filtrado.parquet'))
####