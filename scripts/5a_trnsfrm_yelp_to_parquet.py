import pandas as pd
import pickle
import json
import os
import pyarrow as pa
import pyarrow.parquet as pq
#import fastparquet as fp # edit manuel: no usado
#import numpy as np # edit manuel: no usado

# Ruta a la carpeta Yelp
#yelp_folder = 'yelp'

# no modificar
folder_data = "1_data_extract"
folder_pipeline = "2_pipeline"
folder_output = "3_output"
yelp_folder = "yelp"

file_to_df = 'business.pkl'

# edit manuel: echo en linux
os.system("Proceso iniciado")

# Leer el archivo business.pkl
df_business = pd.read_pickle(
    os.path.join(folder_data,yelp_folder,file_to_df))

business_df = df_business.iloc[:, :14]

# Verificar si el directorio 'parquet' existe, y si no, crearlo
if not os.path.exists(os.path.join(folder_pipeline,yelp_folder,'parquet')):
    os.makedirs(os.path.join(folder_pipeline,yelp_folder,'parquet'))

# Obtener el nombre del archivo original sin la extensión
df_2_file_name = 'business.pkl'.split('.')[0]

# Guardar el DataFrame en formato Parquet en el directorio 'parquet' con el nombre del archivo original
file_path = os.path.join(folder_pipeline,yelp_folder,'parquet', f'{df_2_file_name}.parquet')

# Guardar el DataFrame en formato Parquet usando fastparquet
business_df.to_parquet(file_path, engine='fastparquet')


# checkin.json to parquet
# Ruta al archivo checkin.json dentro de la carpeta Yelp
checkin_path = os.path.join(folder_data,yelp_folder, 'checkin.json')

# Lista para almacenar los DataFrames
checkin_dfs = []

# Leer el archivo línea por línea y convertir cada línea en un DataFrame
with open(checkin_path, 'r') as checkin_file:
    for line in checkin_file:
        data = eval(line)  # Convertir la línea en un diccionario
        df = pd.DataFrame([data])  # Crear un DataFrame a partir del diccionario
        checkin_dfs.append(df)

# Concatenar los DataFrames en uno solo
checkin_df = pd.concat(checkin_dfs, ignore_index=True)

# Verificar si el directorio 'parquet' existe, y si no, crearlo
# edit manuel: ya se hizo arriba
#if not os.path.exists(os.path.join(folder_pipeline,yelp_folder,'parquet')):
#    os.makedirs(os.path.join(folder_pipeline,yelp_folder,'parquet'))

# Obtener el nombre del archivo original sin la extensión
df_2_file_name = 'checkin.json'.split('.')[0]

# Guardar el DataFrame en formato Parquet en el directorio 'parquet' con el nombre del archivo original
file_path = os.path.join(folder_pipeline,yelp_folder,'parquet', f'{df_2_file_name}.parquet')

# A continuación, se guarda el DataFrame en formato Parquet usando fastparquet
checkin_df.to_parquet(file_path, engine='fastparquet')

#tip.json to parquet
# Ruta al archivo tip.json dentro de la carpeta Yelp
tip_path = os.path.join(folder_data,yelp_folder,'tip.json')

# Lista para almacenar los DataFrames
tip_df = []

# Leer el archivo línea por línea y convertir cada línea en un DataFrame
with open(tip_path, 'r', encoding='utf-8') as tip_file:
    for line in tip_file:
        data = json.loads(line)  # Convertir la línea en un diccionario
        df = pd.DataFrame([data])  # Crear un DataFrame a partir del diccionario
        tip_df.append(df)

# Concatenar los DataFrames en uno solo
tip_df = pd.concat(tip_df, ignore_index=True)

# Transformar columna 'date' a formato datetime
tip_df['date'] = pd.to_datetime(tip_df['date'])

# Verificar si el directorio 'parquet' existe, y si no, crearlo
# edit manuel: ya se hizo arriba
#if not os.path.exists(os.path.join(folder_pipeline,yelp_folder,'parquet')):
#    os.makedirs(os.path.join(folder_pipeline,yelp_folder,'parquet'))

# Obtener el nombre del archivo original sin la extensión
df_2_file_name = 'tip.json'.split('.')[0]

# Guardar el DataFrame en formato Parquet en el directorio 'parquet' con el nombre del archivo original
file_path = os.path.join(folder_pipeline,yelp_folder,'parquet', f'{df_2_file_name}.parquet')

# A continuación, se guarda el DataFrame en formato Parquet usando fastparquet
tip_df.to_parquet(file_path, engine='fastparquet')

# Ruta del archivo original
archivo_original = os.path.join(folder_data,yelp_folder,'review.json')

# Número de líneas por archivo parquet
lineas_por_archivo = 1000000
numero_archivo = 1
linea_actual = 0
df_actual = []
lista_df_reviews = []  # Lista para almacenar DataFrames

# Crear el directorio parquet y pq_review si no existen
if not os.path.exists(os.path.join(folder_pipeline,yelp_folder,'parquet','pq_review')):
    os.makedirs(os.path.join(folder_pipeline,yelp_folder,'parquet','pq_review'))

# Leer el archivo original y escribir archivos Parquet
with open(archivo_original, 'r', encoding='utf-8') as original_file:
    for line in original_file:
        # Cargar la línea como un objeto JSON
        linea = json.loads(line)

        # Agregar la línea al DataFrame actual
        df_actual.append(linea)
        linea_actual += 1

        # Si se alcanza el número de líneas por archivo parquet
        if linea_actual == lineas_por_archivo:
            # Crear un DataFrame
            df = pd.DataFrame(df_actual)

            # Agregar el DataFrame a la lista
            lista_df_reviews.append(df)

            # Nombre del archivo parquet
            nombre_archivo = f'2_pipeline/yelp/parquet/pq_review/review_{str(numero_archivo).zfill(2)}.parquet'

            # Guardar el DataFrame como archivo parquet
            df.to_parquet(nombre_archivo, index=False)

            # Reiniciar el contador de líneas y el DataFrame actual
            linea_actual = 0
            df_actual = []
            numero_archivo += 1

# Si quedan líneas en el último DataFrame
if df_actual:
    df = pd.DataFrame(df_actual)

    # Agregar el último DataFrame a la lista
    lista_df_reviews.append(df)

    nombre_archivo = f'2_pipeline/yelp/parquet/pq_review/review_{str(numero_archivo).zfill(2)}.parquet'
    df.to_parquet(nombre_archivo, index=False)

#user.parquet to pq_user(parquet)
# Ruta al archivo Parquet original
input_parquet_file = os.path.join(folder_data,yelp_folder,'user.parquet')

# Directorio para guardar los archivos Parquet resultantes
output_dir = os.path.join(folder_pipeline,yelp_folder,'pq_user')
os.makedirs(output_dir, exist_ok=True)

# Tamaño del lote (número de filas por archivo Parquet)
batch_size = 1000000

# Inicializamos un contador para el nombre de archivo
file_counter = 1

while True:
    # Lee un lote del archivo Parquet original
    start_row = (file_counter - 1) * batch_size
    end_row = start_row + batch_size
    user_table = pq.read_table(input_parquet_file, columns=None, use_threads=False)
    user_df = user_table.to_pandas()
    user_df = user_df.iloc[start_row:end_row]

    # Verifica si se han leído todas las filas
    if user_df.empty:
        break

    # Genera el nombre del archivo Parquet
    output_file = os.path.join(output_dir, f'user_{file_counter:02d}.parquet')

    # Guarda el lote actual en un archivo Parquet
    table = pa.Table.from_pandas(user_df)
    pq.write_table(table, output_file)

    # Incrementa el contador de archivos
    file_counter += 1

#print("Proceso completado")
# edit manuel: echo en linux
os.system("Proceso completado")