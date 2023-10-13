# **Tercer Sprint** 📌

En este tercer sprint, se completó la limpieza de la base de datos y se realizó un análisis de sentimientos, que posteriormente se integrará en el modelo de Machine Learning Random Forest. El objetivo es identificar los atributos más influyentes en la efectividad de un restaurante, basándose en las revisiones de los usuarios.

También se finalizó la definición de cómo medir los KPIs de satisfacción de los clientes, la tasa de cumplimiento de atributos, la tasa de crecimiento mensual y el ranking de Machine Learning.

Se exploró la posibilidad de utilizar Looker directamente con el almacenamiento, pero debido a las limitaciones que esto implicaba, se optó por combinar el almacenamiento con BigQuery. A partir de esta instancia, se conectará con Looker. Una dificultad que surgió al utilizar Looker es que solo permite unir un máximo de 5 columnas y 5 métricas con la misma cantidad de otra tabla. Buscamos ampliar este límite, ya que resultaba insuficiente para nuestros análisis. Al no poder superar esta limitación de Looker, consideramos la creación de diferentes data frames para cada gráfico. Finalmente, concluimos que la mejor opción era la conexión de BigQuery con Power BI, ya que nos permite relacionar tablas y acceder a todos los datos necesarios.

La conexión se realizó a través de DirectQuery, lo que tiene la limitación de no permitir transformaciones de datos, como la eliminación de duplicados. Por lo tanto, estas tareas deberán llevarse a cabo en Python según las necesidades de los analistas de datos.

## KPIs

Vamos a desarrollas los KPIs a utilizar en el tablero para medir los mismos: