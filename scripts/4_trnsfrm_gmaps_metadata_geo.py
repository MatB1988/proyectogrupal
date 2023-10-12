# Liberias
import os
import json
import numpy as np
import pandas as pd
import geopandas as geopd
import pyogrio

#### ENTORNO
# Ruta de la carpeta que contiene los archivos JSON
#ruta_datos = "C:/Users/54280/Documents/GitHub/proyectogrupal/Pruebas/metadata-sitios"

# no modificar
folder_data = "1_data_extract"
folder_uscensus = "uscensus"
folder_zcta_geo = "zcta_geo"
folder_pipeline = "2_pipeline"
folder_output = "3_output"

#### DATOS
# importamos el df limpia sin filas duplicadas
data_gmaps_metadata_sindups = pd.read_parquet(
    os.path.join(folder_pipeline,'gmaps_metadata_limpio.parquet'))

# importamos df con datos de geolocalizacion
geodata_zcta = geopd.read_file(
    os.path.join(
        folder_data,folder_uscensus,folder_zcta_geo,'tl_2020_us_zcta520.shp')
    ,engine="pyogrio"
    ).iloc[:,[1,5,9]]
geodata_zcta.rename(
    columns = {"GEOID20":"zcta5_geoid",
               "ALAND20":"zcta5_arealand"},
    inplace = True)

#### GENERACION DE DATOS ESPACIALES
# generamos una columna POINT() 'geometry'
data_gmaps_metadata_geo = geopd.GeoDataFrame(
    data_gmaps_metadata_sindups, geometry = geopd.points_from_xy(
        data_gmaps_metadata_sindups.longitude, data_gmaps_metadata_sindups.latitude),
    crs="EPSG:4326"
    ).to_crs(geodata_zcta.crs) # type: ignore

# unicmos los dfs segun la interseccion de point con el polygono de zcta
data_gmaps_metadata_zcta = geopd.sjoin(
    data_gmaps_metadata_geo,
    geodata_zcta,
    how="left"
    ,op="within"
    )

#### FILTRAR POR ZONA GEOGRAFICA
# filtramos las que no pertnencen al territorio EEUU
data_gmaps_metadata_zcta_usa = data_gmaps_metadata_zcta[data_gmaps_metadata_zcta["zcta5_geoid"].notnull()].copy()

# Generamos un dummy para las zonas que estan en la zona continental de EEUU
# Defino los límites geográficos de los Estados Unidos
latitud_min = 24.396308
latitud_max = 49.384358
longitud_min = -125.000000
longitud_max = -66.934570

# Filtro lugares dentro de los límites geográficos de los Estados Unidos
# Asigno el resultado a un nuevo df
data_gmaps_metadata_zcta_usa['us_continente'] = np.where((
    (data_gmaps_metadata_zcta_usa['latitude'] >= latitud_min) &
    (data_gmaps_metadata_zcta_usa['latitude'] <= latitud_max) &
    (data_gmaps_metadata_zcta_usa['longitude'] >= longitud_min) &
    (data_gmaps_metadata_zcta_usa['longitude'] <= longitud_max)),1,0)

# Genero un df que contenga el los id y los nombres para que se puedan filtrar las rewiews
df_id_gmaps = data_gmaps_metadata_zcta_usa[['gmap_id', 'name']].copy()

# Exporto un df con los id y los name para pasar al grupo que esta trabajando con  las rewiews
df_id_gmaps.drop_duplicates(inplace=True)
df_id_gmaps.to_csv(
    os.path.join(folder_output,'df_id_gmaps.csv'))

#### EXPORTAR DF FINAL
# Exporto df_filtrado para probar union por latitud y longitud
data_gmaps_metadata_zcta_usa.to_parquet(
    os.path.join(folder_output,'gmaps_metadata_filtrado.parquet'))
####