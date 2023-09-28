## Diccionario de Datos

### **Google Maps**

#### metadata_sitios
La carpeta contiene 11 archivos .json que contienen información sobre comercios, incluyendo su ubicación, atributos y categorías.

- 🏢 **name**: 'Walgreens Pharmacy'
- 📍 **address**: 'Walgreens Pharmacy, 124 E North St, Kendallville, IN 46755'
- 🆔 **gmap_id**: '0x881614ce7c13acbb:0x5c7b18bbf6ec4f7e'
- 📝 **description**: 'Sucursal de la cadena Walgreens que ofrece medicamentos con receta y otros artículos relacionados con la salud.'
- 🌐 **latitude**: 41.45186
- 🌐 **longitude**: -85.2666757
- 🏷️ **category**: ['Farmacia']
- ⭐ **avg_rating**: 4.2
- 📊 **num_of_reviews**: 5
- 💲 **price**: '$$'
- 🕒 **hours**: 
  - ['Thursday', '8AM–1:30PM']
  - ['Friday', '8AM–1:30PM']
  - ['Saturday', '9AM–1:30PM']
  - ['Sunday', '10AM–1:30PM']
  - ['Monday', '8AM–1:30PM']
  - ['Tuesday', '8AM–1:30PM']
  - ['Wednesday', '8AM–1:30PM']
- 🛒 **MISC**: 
  - 🛍️ **Service options**: ['Recogida en la acera', 'Drive-through', 'Recogida en la tienda', 'Compras en la tienda']
  - 🌡️ **Salud y seguridad**: ['Se requiere mascarilla', 'El personal usa mascarillas', 'El personal se toma la temperatura']
  - ♿ **Accesibilidad**: ['Entrada accesible para sillas de ruedas', 'Estacionamiento accesible para sillas de ruedas']
  - 🚀 **Planificación**: ['Visita rápida']
  - 💳 **Pagos**: ['Cheques', 'Tarjetas de débito']
- 🕒 **state**: 'Cierra pronto ⋅ 1:30 PM ⋅ Abre a las 2 PM'
- 🔗 **url**: [Ver en Google Maps](https://www.google.com/maps/place//data=!4m2!3m1!1s0x881614ce7c13acbb:0x5c7b18bbf6ec4f7e?authuser=-1&hl=en&gl=us)

#### review-estados
Los archivos que contienen las reseñas de los usuarios se dividen en 51 carpetas, una por cada estado de los EE. UU., y cada una contiene varios archivos .json con la siguiente estructura:

- 👤 **user_id**: '101463350189962023774'
- 👤 **name**: 'Jordan Adams'
- 🕒 **time**: 1627750414677
- ⭐ **rating**: 5
- 💬 **text**: 'Lugar genial, gente estupenda, ¡dentista increíble!'
- 📷 **pics**: 
  - '📸 url': ['[Enlace a la imagen](https://lh5.googleusercontent.com/p/AF1QipNq2nZC5TH4_M7h5xRAd61hoTgvY1o9lozABguI=w150-h150-k-no-p)']
- 💬 **resp**: 
  - 🕒 **time**: 1628455067818
  - 💬 **text**: '¡Gracias por tu reseña de cinco estrellas! -Dr. Blake'
- 📍 **gmap_id**: '0x87ec2394c2cd9d2d:0xd1119cfbee0da6f3'

### **Dataset de Yelp!**

#### business.pkl

Contiene información del comercio, incluyendo localización, atributos y categorías.

- ⭐ **business_id**: "tnhfDv5Il8EaGSXZGiuQGg"
- 🏢 **name**: "Garaje"
- 🏡 **address**: "475 3rd St"
- 🏙️ **city**: "San Francisco"
- 🇺🇸 **state**: "CA"
- 📯 **postal code**: "94107"
- 🌍 **latitude**: 37.7817529521
- 🌍 **longitude**: -122.39612197
- ⭐ **stars**: 4.5
- 💬 **review_count**: 1198
- 🔓 **is_open**: 1
- ⚙️ **attributes**:
  - "RestaurantsTakeOut": true
  - "BusinessParking":
    - "garage": false
    - "street": true
    - "validated": false
    - "lot": false
    - "valet": false
- 📑 **categories**: ["Mexican", "Burgers", "Gastropubs"]
- 🕙 **hours**:
  - "Monday": "10:00-21:00"
  - "Tuesday": "10:00-21:00"
  - "Friday": "10:00-21:00"
  - "Wednesday": "10:00-21:00"
  - "Thursday": "10:00-21:00"
  - "Sunday": "11:00-18:00"
  - "Saturday": "10:00-21:00"

#### review.json

Contiene las reseñas completas, incluyendo el user_id que escribió el review y el business_id por el cual se escribe la reseña.

- 📝 **review_id**: "zdSx_SD6obEhz9VrW9uAWA"
- 👤 **user_id**: "Ha3iJu77CxlrFm-vQRs_8g"
- ⭐ **business_id**: "tnhfDv5Il8EaGSXZGiuQGg"
- ⭐ **stars**: 4
- 📅 **date**: "2016-03-09"
- 💬 **text**: "Great place to hang out after work: the prices are decent, and the ambiance is fun. It's a bit loud, but very lively. The staff is friendly, and the food is good. They have a good selection of drinks."
- 👍 **useful**: 0
- 😂 **funny**: 0
- 😎 **cool**: 0

#### user.parquet

Data del usuario incluyendo referencias a otros usuarios amigos y a toda la metadata asociada al usuario.

- 👤 **user_id**: "Ha3iJu77CxlrFm-vQRs_8g"
- 👤 **name**: "Sebastien"
- 📝 **review_count**: 56
- 📆 **yelping_since**: "2011-01-01"
- 👥 **friends**: ["wqoXYLWmpkEH0YvTmHBsJQ", "KUXLLiJGrjtSsapmxmpvTA", "6e9rJKQC3n0RSKyHLViL-Q"]
- 👍 **useful**: 21
- 😂 **funny**: 88
- 😎 **cool**: 15
- ⭐ **fans**: 1032
- 🏆 **elite**: [2012, 2013]
- ⭐ **average_stars**: 4.31
- 🔥 **compliment_hot**: 339
- 🔥 **compliment_more**: 668
- 🔥 **compliment_profile**: 42
- 😍 **compliment_cute**: 62
- 📋 **compliment_list**: 37
- 💌 **compliment_note**: 356
- 📋 **compliment_plain**: 68
- 😎 **compliment_cool**: 91
- 😂 **compliment_funny**: 99
- ✏️ **compliment_writer**: 95
- 📷 **compliment_photos**: 50

#### checkin.json

Registros en el negocio.

- ⭐ **business_id**: "tnhfDv5Il8EaGSXZGiuQGg"
- 📅 **date**: "2016-04-26 19:49:16, 2016-08-30 18:36:57, 2016-10-15 02:45:18, 2016-11-18 01:54:50, 2017-04-20 18:39:06, 2017-05-03 17:58:02"

#### tip.json

Tips (consejos) escritos por el usuario. Los tips son más cortos que las reseñas y tienden a dar sugerencias rápidas.

- 📝 **text**: "Secret menu - fried chicken sando is da bombbbbbb. Their zapatos are good too."
- 📅 **date**: "2013-09-20"
- 👍 **compliment_count**: 172
- ⭐ **business_id**: "tnhfDv5Il8EaGSXZGiuQGg"
- 👤 **user_id**: "49JhAJh8vSQ-vM4Aourl0g"
