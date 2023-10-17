
# Librerias

# Datos
import json
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import os 
import fastparquet as fp

# Analisis de sentimientos
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Modelos
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import mean_squared_error

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"

# importamos el df
data_gmaps_metadata = pd.read_parquet(
    os.path.join(folder_pipeline,'gmaps_metadata_filtrado.parquet'))


# Elimino nan de Misc
independent_df = data_gmaps_metadata.copy()
independent_df.dropna(subset=['MISC'], inplace=True)

# Creo una lista de diccionarios con 'MISC' y 'gmap_id'
attributes_list = [
    {**attributes, 'gmap_id': gmap_id}
    for attributes, gmap_id in zip(independent_df['MISC'], independent_df['gmap_id'])
]

# Creo un DataFrame a partir de la lista de diccionarios
attributes_df = pd.DataFrame(attributes_list)

# Función para verificar si un atributo está presente en la lista o en None
def check_attribute_presence(service_options, attribute_name):
    if service_options is None:
        return 0
    return 1 if attribute_name in service_options else 0

attribute_name = 'Delivery'

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['RestaurantsDelivery'] = attributes_df['Service options'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'RestaurantsDelivery']], on='gmap_id', how='left')

# Lleno los valores NaN en 'RestaurantsDelivery' con 0 (si no se encontró 'Delivery')
data_gmaps_metadata['RestaurantsDelivery'].fillna(0, inplace=True)

attribute_name = 'Takeout'

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['RestaurantsTakeOut'] = attributes_df['Service options'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'RestaurantsTakeOut']], on='gmap_id', how='left')

# Lleno los valores NaN en 'RestaurantsTakeOut' con 0 (si no se encontró 'Takeout')
data_gmaps_metadata['RestaurantsTakeOut'].fillna(0, inplace=True)

attribute_name = 'Outdoor seating'

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['OutdoorSeating'] = attributes_df['Service options'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'OutdoorSeating']], on='gmap_id', how='left')

# Lleno los valores NaN en 'OutdoorSeating' con 0 (si no se encontró 'Outdoor seating')
data_gmaps_metadata['RestaurantsTakeOut'].fillna(0, inplace=True)

attribute_name = 'Accepts reservations'

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['RestaurantsReservations'] = attributes_df['Planning'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'RestaurantsReservations']], on='gmap_id', how='left')

# Lleno los valores NaN en 'RestaurantsReservations' con 0 (si no se encontró 'Accepts reservations')
data_gmaps_metadata['RestaurantsReservations'].fillna(0, inplace=True)

attribute_name = "Kids' menu"

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['GoodForKids'] = attributes_df['Offerings'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'GoodForKids']], on='gmap_id', how='left')

# Lleno los valores NaN en 'GoodForKids' con 0 (si no se encontró 'Kids' menu')
data_gmaps_metadata['GoodForKids'].fillna(0, inplace=True)

attribute_name = "Reservations required"

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['ByAppointmentOnly'] = attributes_df['Health and safety'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'ByAppointmentOnly']], on='gmap_id', how='left')

# Lleno los valores NaN en 'ByAppointmentOnly' con 0 (si no se encontró 'Reservations required')
data_gmaps_metadata['ByAppointmentOnly'].fillna(0, inplace=True)

attribute_name = "Wheelchair accessible seating"

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['WheelchairAccessible'] = attributes_df['Accessibility'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'WheelchairAccessible']], on='gmap_id', how='left')

# Lleno los valores NaN en 'WheelchairAccessible' con 0 (si no se encontró 'Wheelchair accessible seating')
data_gmaps_metadata['WheelchairAccessible'].fillna(0, inplace=True)

# Genero una nueva funcion ya que a los proximos atibutos les voy a mandar una lista a verificar
# Función para verificar si al menos uno de los atributos está presente en la lista
def check_attributes(attribute_lista, attributes):
    if attribute_lista is None:
        return 0
    for attribute in attributes:
        if attribute in attribute_lista:
            return 1
    return 0

attribute_lista = ['Groups', 'Family-friendly', 'Family friendly', 'College students', 'University students']

# Aplico la función a la columna 'Crowd' de attributes_df y crea una nueva columna
attributes_df['RestaurantsGoodForGroups'] = attributes_df['Crowd'].apply(lambda x: check_attributes(x, attribute_lista))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'RestaurantsGoodForGroups']], on='gmap_id', how='left')

# Lleno los valores NaN en 'RestaurantsGoodForGroups' con 0 (si no se encontró 'Groups','Family-friendly','Family friendly','College students','University students')
data_gmaps_metadata['RestaurantsGoodForGroups'].fillna(0, inplace=True)

attribute_name = "Credit cards"

# Aplico la función a la columna 'Service options' de attributes_df
attributes_df['BusinessAcceptsCreditCards'] = attributes_df['Payments'].apply(lambda x: check_attribute_presence(x, attribute_name))

# Combino los datos actualizados en data_gmaps_metadata usando la columna 'gmap_id'
data_gmaps_metadata = data_gmaps_metadata.merge(attributes_df[['gmap_id', 'BusinessAcceptsCreditCards']], on='gmap_id', how='left')

# Lleno los valores NaN en 'BusinessAcceptsCreditCards' con 0 (si no se encontró 'Credit cards')
data_gmaps_metadata['BusinessAcceptsCreditCards'].fillna(0, inplace=True)

# Elimino nombres repetidos ya que los tomo como franquicias
# 'locations' es el número máximo de repeticiones permitidas para un 'name'
locations = 1

# Cuento la frecuencia de cada 'name'
name_counts = data_gmaps_metadata['name'].value_counts()

# Obtengo los nombres que cumplen con el criterio de frecuencia
valid_names = name_counts[name_counts <= locations].index

# Filtro el DataFrame original
data_gmaps_metadata = data_gmaps_metadata[data_gmaps_metadata['name'].isin(valid_names)]

# Elimino la columna MISC ya que saque los atibutos que necesitaba
data_gmaps_metadata = data_gmaps_metadata.drop("MISC", axis=1)

# Reemplazo los valores NaN con 0 y lo guardo en un nuevo df
data_gmaps_metadata2 = data_gmaps_metadata.fillna(0)

# Modelo Random Forest

# Divido los datos originales en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(data_gmaps_metadata2[['BusinessAcceptsCreditCards', 'RestaurantsGoodForGroups', 'WheelchairAccessible', 'ByAppointmentOnly', 'GoodForKids', 'RestaurantsReservations', 'OutdoorSeating', 'RestaurantsTakeOut', 'RestaurantsDelivery']], data_gmaps_metadata2['avg_rating'], test_size=0.2, random_state=42)

# Creo un nuevo DataFrame para guardar las predicciones
predictions_df = X_test.copy()

# Asigno las predicciones al nuevo DataFrame
predictions_df['Predictions'] = y_pred

# Calculo el error cuadrático medio (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f'Error Cuadrático Medio (MSE): {mse}')

"""
En mi análisis del modelo que acabo de construir, es importante destacar que la variable que estamos tratando de predecir tiene un rango de valores de 0 a 5. Un Error Cuadrático Medio (MSE) de 0.2459, como el que hemos obtenido, podría considerarse relativamente alto en este contexto. En problemas donde la variable objetivo está en una escala de 0 a 5, un MSE cercano a cero indicaría que el modelo se ajusta muy bien a los datos y tiene un rendimiento bastante preciso.

Sin embargo, con un MSE de 0.2459, estamos observando un nivel de error que indica que el modelo podría no estar capturando completamente la variabilidad en los datos. Esto podría deberse a diversas razones, como la complejidad del problema, la elección de las características o la cantidad de datos disponibles.
"""

# Uno las predicciones al DataFrame original
data_gmaps_metadata2 = data_gmaps_metadata2.join(predictions_df['Predictions'])

# Selecciono todas las filas en el DataFrame original para hacer predicciones
features_all = data_gmaps_metadata2[['BusinessAcceptsCreditCards', 'RestaurantsGoodForGroups', 'WheelchairAccessible', 'ByAppointmentOnly', 'GoodForKids', 'RestaurantsReservations', 'OutdoorSeating', 'RestaurantsTakeOut', 'RestaurantsDelivery']]

# Realizo predicciones para todas las filas
predictions_all = model.predict(features_all)

# Añado las predicciones al DataFrame original
data_gmaps_metadata2['Predictions'] = predictions_all

# importamos el df
data_gmaps_reviews = pd.read_parquet(
    os.path.join(folder_output,'data_gmaps_reviews_norm.parquet'))

# Descargo los recursos necesarios de NLTK si no los tienes ya
nltk.download('vader_lexicon')

# Inicializo el analizador de sentimientos VADER
sia = SentimentIntensityAnalyzer()

# Función para clasificar el sentimiento basado en VADER
def compound_score(text):
    compound_score = 0  # Inico con un valor predeterminado
    if pd.notna(text) and isinstance(text, str):
        sentiment_score = sia.polarity_scores(text)
        compound_score = sentiment_score['compound']
    return compound_score

# Función para clasificar el sentimiento basado en VADER
def classify_sentiment_vader(compound_score):
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Aplico la función de clasificación de sentimientos al DataFrame
data_gmaps_reviews['compound_score'] = data_gmaps_reviews['user_text'].apply(compound_score)

# Aplico la función de classify_sentiment_vadera_dficación de sentimientos al DataFrame
data_gmaps_reviews['sentiment'] = data_gmaps_reviews['compound_score'].apply(classify_sentiment_vader)

# Asigno pesos a cada categoría de sentimiento
sentiment_weights = {'Positive': 2, 'Neutral': 1, 'Negative': 0}

# Calculo el promedio ponderado para cada grupo 'gmap_id'
def ponderacion_average(group):
    # Calcula el producto de compound_score y su peso correspondiente según el sentimiento
    ponderacion_scores = group['compound_score'] * group['sentiment'].map(sentiment_weights)
    # Calcula el promedio ponderado
    return ponderacion_scores.sum() / ponderacion_scores.count()

# Aplico la función para calcular el promedio ponderado
ponderacion_avg_df = data_gmaps_reviews.groupby('gmap_id').apply(ponderacion_average).reset_index()
ponderacion_avg_df.columns = ['gmap_id', 'ponderacion_average']

# Realizo la fusión entre data_gmaps_metadata2 y ponderacion_avg_df
data_gmaps_metadata2 = data_gmaps_metadata2.merge(ponderacion_avg_df, on='gmap_id', how='left')

# Me doy cuenta que estas columnas tendrian que ser numero entero y quedaron como float las paso a numero entero
columns_to_convert = ['RestaurantsDelivery', 'RestaurantsTakeOut', 'OutdoorSeating', 'RestaurantsReservations',
                      'GoodForKids', 'ByAppointmentOnly', 'WheelchairAccessible', 'RestaurantsGoodForGroups',
                      'BusinessAcceptsCreditCards']

data_gmaps_metadata2[columns_to_convert] = data_gmaps_metadata2[columns_to_convert].astype(int)

# Completo con 0 los valores faltantes de ponderacion
data_gmaps_metadata2.fillna(0, inplace=True)

data_gmaps_metadata2.isna().sum()

#@Red Neural para elegir prospectos y tendencias

# Selecciono las características (features) y el objetivo (target)
features = ['Predictions', 'ponderacion_average', 'latitude', 'longitude', 'num_of_reviews', 'RestaurantsDelivery', 'RestaurantsTakeOut', 'OutdoorSeating', 'RestaurantsReservations','GoodForKids', 'ByAppointmentOnly', 'WheelchairAccessible', 'RestaurantsGoodForGroups','BusinessAcceptsCreditCards']
target = 'avg_rating'

# Divido los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(data_gmaps_metadata2[features],data_gmaps_metadata2[target], test_size=0.2, random_state=42)

# Escalo las características para acelerar el entrenamiento
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Creo el modelo de red neuronal
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])

# Compilo el modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Entreno el modelo
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Realizo predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Calculo el Error Cuadrático Medio (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f'Error Cuadrático Medio (MSE): {mse}')

# Ordeno los restaurantes por sus predicciones y ponderaciones promedio
data_gmaps_metadata2['predicted_rating'] = model.predict(scaler.transform(data_gmaps_metadata2[features]))
top_restaurants = data_gmaps_metadata2.sort_values(by=['state_name', 'predicted_rating'], ascending=[True, False])
bottom_restaurants = data_gmaps_metadata2.sort_values(by=['state_name', 'predicted_rating'], ascending=[True, True])

# Obtener los 5 mejores y 5 peores restaurantes de cada estado
top_restaurants = top_restaurants.groupby('state_name').head()
bottom_restaurants = bottom_restaurants.groupby('state_name').head()

# Mostro los primeros 5 restaurantes de top_restaurants
top_restaurants.head()

# Lista de columnas deseadas
columnas_deseadas = [
    'gmap_id', 'name', 'address', 'latitude', 'longitude', 'avg_rating',
    'zcta5_geoid', 'state_name', 'state_code', 'RestaurantsDelivery',
    'RestaurantsTakeOut', 'OutdoorSeating', 'RestaurantsReservations',
    'GoodForKids', 'ByAppointmentOnly', 'WheelchairAccessible',
    'RestaurantsGoodForGroups', 'BusinessAcceptsCreditCards',
    'Predictions', 'ponderacion_average', 'predicted_rating'
]

# Selecciono las columnas deseadas
data_gmaps_metadata2 = data_gmaps_metadata2[columnas_deseadas]

# Renombro las columnas
nombres_columnas = {
    'gmap_id': 'business_id',
    'avg_rating': 'rating',
    'Predictions': 'predictions',
    'ponderacion_average': 'weighted_avg',
    'predicted_rating': 'predicted_rating'
}

data_gmaps_metadata2 = data_gmaps_metadata2.rename(columns=nombres_columnas)

data_gmaps_metadata2.parquet.to_parquet(
    os.path.join(folder_pipeline,'gmaps_modelo.parquet'))