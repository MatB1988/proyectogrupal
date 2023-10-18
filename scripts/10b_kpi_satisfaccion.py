import os
import json
import pandas as pd

# NLP
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# no modificar
folder_pipeline = "2_pipeline"
folder_output = "3_output"


# importamos el df
data_business_reviews = pd.read_parquet(
    os.path.join(folder_output,'business_reviews_norm.parquet'))

# 1. Promedio de rating por año-mes
data_business_reviews_average_rating = data_business_reviews.groupby(
    ["business_id","user_time_year","user_time_month"])['rating'].mean().reset_index().rename(
        columns={'rating': 'average_rating'})

# 2. Rescalar el rating promedio de 0 a 1
min_rating = 1 # valor minimo absoluto/teorico
max_rating = 5 # valor maximo absoluto/teorico
data_business_reviews_average_rating['rescaled_rating'] = (
    data_business_reviews_average_rating['average_rating'] - min_rating
    ) / (max_rating - min_rating)

# 3. Calcular el KPI de satisfacción
data_business_reviews_average_rating['kpi_satisfaccion_rating'] = data_business_reviews_average_rating[
    'rescaled_rating'] * 0.4

# Descarga los recursos necesarios de NLTK si no los tienes ya
nltk.download('vader_lexicon')

# Inicializar el analizador de sentimientos VADER
sia = SentimentIntensityAnalyzer()

# Función para clasificar el sentimiento basado en VADER
def classify_sentiment_vader(text):
    if pd.notna(text) and isinstance(text, str):
        sentiment_score = sia.polarity_scores(text)
        compound_score = sentiment_score['compound']
        return compound_score
    else:
        return None

# Calcular el valor de compound_score y agregarlo como columna
data_business_reviews['compound_score'] = data_business_reviews[
    'user_text'].apply(classify_sentiment_vader)

# Calcular el promedio del compound_score por restaurante y año-mes
data_business_reviews_avg_compound = data_business_reviews.groupby(
    ["business_id","user_time_year","user_time_month"])['compound_score'].mean().reset_index().rename(
        columns={'compound_score': 'average_compound'})

# Rescalar de 0 a 1 y luego multiplicar por 0.6 para obtener el KPI de satisfacción de sentimiento
min_compound = -1 # valor minimo absoluto/teorico
max_compound = 1 # valor maximo absoluto/teorico
data_business_reviews_avg_compound['rescaled_average_compound'] = (
    data_business_reviews_avg_compound['average_compound'] - min_compound) / (max_compound - min_compound)
data_business_reviews_avg_compound['kpi_satisfaccion_sentimiento'] = data_business_reviews_avg_compound[
    'rescaled_average_compound'] * 0.6

# Fusiona los DataFrames 'data_business_reviews_avg_compound' y 'data_business_reviews_average_rating'
# en función de la columna 'business_id'
data_business_reviews_kpi_satisfaccion = pd.merge(
    data_business_reviews_average_rating,
    data_business_reviews_avg_compound,
    how='left').drop(columns=[
        "average_compound","rescaled_average_compound",
        "average_rating","rescaled_rating"])

# Calcular el KPI de satisfacción de suma ponderada por restaurante y año-mes
data_business_reviews_kpi_satisfaccion['kpi_satisfaccion_suma'] = round((data_business_reviews_kpi_satisfaccion[
    'kpi_satisfaccion_rating'] + data_business_reviews_kpi_satisfaccion['kpi_satisfaccion_sentimiento'])*100,2)

# Guardar el DataFrame final como un archivo parquet
data_business_reviews_kpi_satisfaccion.to_parquet(
    os.path.join(folder_pipeline,'business_kpi_satisfaccion.parquet'),
    index=False)