# **Primer Sprint** 📌

El primer Sprint duró dos semanas, en las cuales nos enfocamos en conocernos con los miembros del equipo, definir nuestra estrategia para abordar el desafío planteado y comenzar a trabajar en él.

Tuvimos varias conversaciones en las que nos conocimos mejor y exploramos cómo encajarían nuestros diferentes perfiles.

Una de las primeras cosas que acordamos fue establecer un flujo de trabajo y realizar reuniones diarias mientras cada uno de nosotros investigaba el proyecto.

El desafío que se nos presentó fue el siguiente:

> "La opinión de los usuarios es un dato muy valioso que crece día a día gracias a plataformas de reseñas. Yelp es una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios, entre otros. Los usuarios utilizan el servicio y luego publican reseñas basadas en su experiencia. Esta información es sumamente valiosa para las empresas, ya que les permite conocer la percepción de los usuarios sobre los diferentes lugares y servicios que ofrecen. Asimismo, Google cuenta con una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios, etc., integrada en su servicio de localización y mapas, Google Maps. Los usuarios utilizan el servicio y comparten reseñas de acuerdo a sus experiencias. Muchos usuarios leen estas reseñas antes de tomar decisiones sobre dónde comprar, comer, alojarse o reunirse. Esta información es de gran valor para las empresas, ya que les permite conocer la imagen que los usuarios tienen de sus locales y servicios, y es muy útil para evaluar su desempeño y utilidad, así como para identificar áreas de mejora en el servicio."

## Enfoque del Proyecto

En calidad de consultora de análisis de datos, hemos sido seleccionadas por la productora de entretenimiento de un influyente conglomerado mediático para colaborar en el reality show "Restaurant Rescue". Este programa se enfoca en áreas específicas con la misión fundamental de rescatar restaurantes que atraviesan dificultades y convertirlos en negocios exitosos.

### Definición del Alcance

Nuestro enfoque se centra en medir la satisfacción, lealtad y popularidad de los clientes como indicadores clave para ayudar a mejorar los restaurantes. No consideramos aspectos financieros u operativos en nuestra análisis, sino que nos concentramos en evaluar la perspectiva del cliente. 👥🍽️📈

### Investigacion de estar tecnologico

Como parte del primer Sprint, nos enfrentamos al desafío de decidir si debíamos adoptar una estrategia basada en la nube (Cloud) o en Big Data. Nuestra primera decisión fue optar por un modelo en la nube, lo que nos llevó a investigar las principales opciones disponibles, como Google Cloud, Azure y AWS.

Después de un análisis exhaustivo, optamos por Google Cloud, ya que nos ofrecía la posibilidad de aprovechar al máximo los recursos disponibles para todos los participantes del proyecto, lo que mejor se adaptaba a nuestros requerimientos. Esto también influyó en nuestra elección de utilizar Python, ya que Google Cloud no admite Spark.

**Resumen de la Elección**
- 🌐 Plataforma Cloud: Google Cloud Platform (GCP)
  - Almacenamiento: 
    - GC storage
    - GC big query
  - Procesamiento: 
    - GC Compute Engine
  - Visualizacion: 
    - GC Looker
- 🐍 Lenguaje de Programación: Python
   - Librerias: 
      - Pandas
      - Numpy
      - Matplotlib
      - Seaborn
  - Modelos de machine learning:
    -  Scikit-learn
    -  Redes Neurales
    -  Lenguaje Natural

### Definicion de roles:

Para esta etapa, debimos asignar roles a cada miembro, lo cual logramos mediante una discusión conjunta en la que consensuamos en qué rol nos sentíamos más cómodos.

Data Engineer:
 - Matías Basso
 - Javier de la Fuente
  
Data Analytics:
 - Alfonzo Rubianes

Data Science:
 - Javier Melo
 - Manuel Valderrama

### Esquema de trabajo GANTT:

Tras una conversación entre todos, se planteó un plan de trabajo para abordar las tareas asignadas en el primer sprint, que abarca un período de 15 días. A continuación, se presenta una imagen que ilustra el esquema de trabajo propuesto.

<p align="center">
  <img src="https://i.ibb.co/nBN6G2n/flujo-de-trabajo.png" height="300">
</p>

### Pruebas Google Cloud:

Comenzamos a explorar las diferentes instancias de Google Cloud, cargamos los archivos de la base de datos y examinamos cómo funciona el sistema de automatización y el trabajo en Compute Engine, utilizando las diversas interfaces disponibles en Google Cloud.

<p align="center">
  <img src="https://i.ibb.co/2Sws7k3/Whats-App-Image-2023-09-15-at-20-31-30.jpg" height="300">
</p>

### Planteo de los KPI y tablero final:

Se plantea que el producto final consista en un panel de control en Looker, donde cada pestaña representará un indicador clave de rendimiento general que llamaremos "atributo". Los atributos serán los siguientes:

- Atributo 1: Satisfacción
- Atributo 2: Lealtad
- Atributo 3: Popularidad

A pesar de que cada atributo será el resultado de varios análisis, incluyendo comparativas de KPI, entre los restaurantes prospectos y las tendencias, cada atributo se considera como un indicador clave de rendimiento general.

A modo de orientación, se presentó un ejemplo de lo que podría componer el primer atributo **Satisfacción**:

 *KPI Satisfacción del cliente*:

 - **Método 1** Red Neuronal: 
    + Entradas: calidad de la comida, servicio al cliente, limpieza y ambiente, precio 
    + Capa Oculta: puede consistir en varias capas intermedias de neuronas.
    +  Salida: Puntuación de satisfacción (escala de 1 a 5, por ejemplo).
  
 - **Método 2** Análisis de sentimiento:
    + Entrada: Texto de reseñas.
    + Salida: Proporción del sentimiento de reseñas: tasa de reseñas positivas vs tasa de reseñas negativas. 