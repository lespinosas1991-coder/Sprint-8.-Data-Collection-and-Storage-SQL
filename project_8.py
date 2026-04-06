# Importas librerías:

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from scipy import stats as st

companies = pd.read_csv('/datasets/project_sql_result_01.csv')
neighborhoods = pd.read_csv('/datasets/project_sql_result_04.csv')
ohare = pd.read_csv('/datasets/project_sql_result_07.csv')

# Para el DF companies:
# Revisión inicial:
print(companies.head())

print()

# Revisar dataset por valores ausentes:
print(companies.isna().sum())

print()

# Revisar tipos de datos:
companies.info()

print()

# Describir DataFrame:
companies.describe()

# Para el DF neighborhoods:
# Revisión inicial:
print(neighborhoods.head())

print()

# Revisar dataset por valores ausentes:
print(neighborhoods.isna().sum())

print()

# Revisar tipos de datos:
neighborhoods.info()

print()

# Describir DataFrame:
neighborhoods.describe()

# Voy a redondear hacia arriba average_trips porque los viajes deben ser un número entero. 
neighborhoods['average_trips'] = np.ceil(neighborhoods['average_trips'])

top_10_neighborhoods = neighborhoods.sort_values(by='average_trips', ascending=False).head(10)

print(top_10_neighborhoods)

# Verificamos que haya nombres de empresas distintos.

len(companies['company_name'].unique())

# Ordenamos el DataFrame por número de viajes por cada compañía de taxis.

ordered_comp = companies.sort_values('trips_amount', ascending = False).head(35)

# Crea un gráfico de barras que muestre el número de viajes por lugar de entrega.

ordered_comp.plot(x = 'company_name'
                      , y = 'trips_amount'
                      , title = 'Las 35 principales compañías de taxis por número de viajes los días 15 y 16 de noviembre de 2017.'
                      , xlabel = 'Nombre de la empresa de taxis'
                      , ylabel = 'Número de viajes los días 15 y 16 de noviembre de 2017.'
                      , kind = 'bar'
                      , rot = 45
                      , figsize=(25,10)
                      )

# Mostrar gráfico de barras:
plt.show()

# Crear un dataframe con los 10 barrios principales por número promedio de viajes.

top_ten_dropoffs = neighborhoods.sort_values('average_trips', ascending = False).head(10)

# Crea un gráfico de barras que muestre el número de viajes por lugar de entrega.
top_ten_dropoffs.plot(x = 'dropoff_location_name'
                      , y = 'average_trips'
                      , title = 'Número promedio de viajes por lugar de destino en 2017'
                      , xlabel = 'Lugar de entrega'
                      , ylabel = 'Número promedio de viajes'
                      , kind = 'bar'
                      , rot = 45
                      , figsize=(25,10)
                      )

# Mostrar gráfico de barras:
plt.show()

# Prueba de hipótesis:

# Hipótesis Nula: "No hay diferencia en la duración promedio del viaje desde el Loop hasta el Aeropuerto Internacional O'Hare entre los sábados lluviosos y los sábados sin lluvia."
# Hipótesis Alternativa: "Existe una diferencia en la duración promedio del viaje desde Loop hasta el Aeropuerto Internacional O'Hare entre los sábados lluviosos y los sábados sin lluvia."

# Crea un conjunto de datos sobre buen y mal tiempo.
bad_weather = ohare[ohare['weather_conditions'] == 'Bad']['duration_seconds']
good_weather = ohare[ohare['weather_conditions'] != 'Bad']['duration_seconds']

# Imprime el número de valores en cada lista para ver si hay un tamaño de muestra similar y suficientemente grande.
print('El número de viajes en sábados lluvioso es:', len(bad_weather))
print('El número de viajes en sábados sin lluvia es:', len(good_weather))

print('')

print('La duración promedio de los viajes en sábados lluviosos es:',round(bad_weather.mean(),2))
print('La duración promedio de los viajes en sábados sin lluvia es:',round(good_weather.mean(),2))

# Nivel de significancia estadística crítica.
# Si el valor p es menor que alfa, rechazamos la hipótesis.
alpha = 0.05  

# Para comprobar la hipótesis de que las medias de las dos poblaciones estadísticas son iguales, basándose en muestras tomadas de ellas, se aplica la prueba t independiente.
results = st.ttest_ind(bad_weather, good_weather)

print('')

print('p-value: ', results.pvalue)

print('')

if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula: existe una diferencia en la duración promedio del viaje desde Loop hasta el Aeropuerto Internacional O'Hare entre los sábados lluviosos y los sábados sin lluvia.")
else:
    print("No podemos rechazar la hipótesis nula: no hay diferencia en la duración promedio del viaje desde Loop hasta el Aeropuerto Internacional O'Hare entre los sábados lluviosos y los sábados sin lluvia.") 