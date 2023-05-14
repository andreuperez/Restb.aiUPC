import sys
import json
import joblib
import requests
import pandas as pd

city = 0
square_meters = 0
bedrooms = 0
bathrooms = 0
property = 1
kitchen = 1
bathroom_r1r6 = 1
bedrooms_r1r6 = 1
interior = 1

def jsonFormat():
    data = {
        "city": city,
        "square_meters": square_meters,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "image_data": {
            "r1r6": {
                "property": property,
                "kitchen": kitchen,
                "bathroom": bathroom_r1r6,
                "interior": interior,
                "bedrooms": bedrooms_r1r6
            }
        }
    }

    with open("datos.json", "w") as outfile:
        json.dump(data, outfile)


def api():
    global json_response
    url = 'https://property.restb.ai/v1/multianalyze'
    payload = {
    # Add your client key
    'client_key': '2593c868c3e81326f28f6eab1c97191f70017da8908b0dec17d8e60cfc690e49'
    }
    urls = sys.argv[3].split(",")
    request_body = {
    "image_urls": urls,
    "solutions": {"roomtype": 1.0, "roomtype_reso": 1.0, "style": 1.0, "r1r6": None, "c1c6": None, "features": 4.0, "features_reso": 1.0, "compliance": 2.0, "caption": None}
    }
    
    # Make the classify request
    response = requests.post(url, params=payload, json=request_body)
   
    # The response is formatted in JSON
    json_response = response.json()


def readJson():
    global city, bedrooms_r1r6, neighborhood, region, square_meters, bedrooms, bathrooms, property, kitchen, bathroom_r1r6, interior
    city = sys.argv[1]
    square_meters = sys.argv[2]
    try:
        bedrooms = json_response["response"]["solutions"]["roomtype"]["summary"]["count"]["room-bedroom"]
        if(bedrooms == None):
            bedrooms = 0
    except:
        bedrooms = 0
    
    try:
        bathrooms = json_response["response"]["solutions"]["roomtype"]["summary"]["count"]["bathroom"]
        if(bathrooms == None):
            bathrooms = 0
    except:
        bathrooms = 0

    try:
        property = json_response["response"]["solutions"]["r1r6"]["property"]["score"]
        if(property == None):
            property = 1
    except:
        property = 1

    try:
        kitchen = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["kitchen"]
        if(kitchen == None):
            kitchen = 1
    except:
        kitchen = 1

    try:
        bathroom_r1r6 = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["bathroom"]
        if(bathroom_r1r6 == None):
            bathroom_r1r6 = 1
    except:
        bathroom_r1r6 = 1

    try:
        bedrooms_r1r6 = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["bedrooms"]
        if(bedrooms_r1r6 == None):
            bedrooms_r1r6 = 1
    except:
        bedrooms_r1r6 = 1
    
    try:
        interior = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["interior"]
        if(interior == None):
            interior = 1
    except:
        interior = 1


def formatJoblib():
    modelo = joblib.load('random_forest_v2.joblib')

    # Cargar los datos de entrada desde un archivo JSON
    with open('datos.json', 'r') as archivo_json:
        datos = json.load(archivo_json)
    
    df = pd.DataFrame(columns=['square_meters', 'bedrooms', 'bathrooms','property_rating', 'kitchen_rating', 'bathroom_rating', 'interior_rating', 'zipcode'])

    property_dict = {}
    property_dict['square_meters'] = datos['square_meters']
    property_dict['bedrooms'] = datos['bedrooms']
    property_dict['bathrooms'] = datos['bathrooms']
    property_dict['property_rating'] = datos['image_data']['r1r6']['property'] 
    property_dict['kitchen_rating'] = datos['image_data']['r1r6']['kitchen'] 
    property_dict['bathroom_rating'] = datos['image_data']['r1r6']['bathroom']
    property_dict['interior_rating'] = datos['image_data']['r1r6']['interior']
    property_dict['zipcode'] = datos['city']

    df = df._append(property_dict, ignore_index=True)

    # Preprocesar los datos si es necesario
    # ...

    # Aplicar el modelo a los datos
    resultados = modelo.predict(df)

    # Procesar los resultados si es necesario
    # ...

    # Guardar los resultados en un archivo de salida
    print(str(resultados[0])+" €")

def main():
    try:
        api()
        readJson()
        jsonFormat()
        formatJoblib()
    except Exception as e:
        print(e)
    


if __name__ == '__main__':
    main()

