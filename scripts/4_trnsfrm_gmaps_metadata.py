# Liberias
import os
import json
import numpy as np
import pandas as pd

# Ruta de la carpeta que contiene los archivos JSON
#ruta_datos = "C:/Users/54280/Documents/GitHub/proyectogrupal/Pruebas/metadata-sitios"

# no modificar
folder_data = "1_data_extract"
folder_pipeline = "2_pipeline"
folder_output = "3_output"
folder_gmaps = "gmaps"
folder_metadata = "metadata-sitios"

# Lista para almacenar los DataFrames de datos JSON
data_frames = []

# Itero sobre los archivos JSON en la carpeta
for filename in os.listdir(os.path.join(folder_data,folder_gmaps,folder_metadata)):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_data,folder_gmaps,folder_metadata, filename)
        # Leo el archivo JSON y creo un DataFrame
        with open(file_path, 'r', encoding='utf-8') as file:
            data = pd.read_json(file, lines=True)
        data_frames.append(data)

# Combino todos los DataFrames de datos JSON en uno
df_gmaps = pd.concat(data_frames, ignore_index=True)

# Saco la lista que compone category y la dejo como texto para explorarla
df_exploded = df_gmaps.explode('category')

# Lista de palabras clave
palabras_clave = ["restaurant", "food", "cafe", "diner", "bakery", "lunch", "brunch"]

# Combino palabras clave en un patrón de búsqueda con '|'
patron_busqueda = '|'.join(palabras_clave)

# Eliminar registros con valores faltantes en la columna "category"
df_exploded = df_exploded.dropna(subset=['category'])

# Convertir la columna "category" a minúsculas y eliminar espacios en blanco
df_exploded['category'] = df_exploded['category'].str.lower().str.strip()

# Filtrar los registros que contienen cualquier parte de las palabras clave en la columna "category"
df_filtrado = df_exploded[df_exploded['category'].str.contains(patron_busqueda, case=False)]

# Genero un df que contenga el los id y los nombres para que se puedan filtrar las rewiews
df_id_gmaps = df_filtrado[['gmap_id', 'name']].copy()

# Exporto un df con los id y los name para pasar al grupo que esta trabajando con  las rewiews
df_id_gmaps.to_csv(
    os.path.join(folder_output,'df_id_gmaps.csv'))

# Creo una nueva columna 'estado_categoria' en función de las etiquetas existentes
def categorizar_estado(row):
    if pd.notna(row) and ('Open' in row or '24 hours' in row):
        return 'Open'
    elif pd.notna(row) and 'Temporarily closed' in row:
        return 'Temporarily closed'
    elif pd.notna(row) and 'Permanently closed' in row:
        return 'Permanently closed'
    else:
        return 'Specific Hours'

df_filtrado['estado_categoria'] = df_filtrado['state'].copy().apply(categorizar_estado)

# Exporto df_filtrado para probar union por latitud y longitud con la base de yeld
df_filtrado.to_pickle(
    os.path.join(folder_output,'gmaps_metadata_filtrado.pkl'))