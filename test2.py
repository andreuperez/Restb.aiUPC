import joblib
import numpy as np
import json

# Carga el modelo de joblib
modelo = joblib.load('random_forest.joblib')

# Define el diccionario de entrada
with open('datos.json', 'r') as archivo_json:
    datos = json.load(archivo_json)


# Convierte el diccionario a un arreglo numpy
datos_array = np.array(list(datos.values())).reshape(1, -1)

# Llama a la función predict del modelo con el arreglo numpy
resultados = modelo.predict(datos_array)
print(resultados)