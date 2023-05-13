import requests
import json

url = 'https://api-eu.restb.ai/vision/v2/multipredict'
payload = {
    # Add your client key
    'client_key': '2593c868c3e81326f28f6eab1c97191f70017da8908b0dec17d8e60cfc690e49',
    'model_id': 're_roomtype_global_v2',
    # Add the image URL you want to classify
    'image_url': 'https://santos.es/wp-content/uploads/2022/01/cocina-gris-abierta-con-isla-santos.jpg'
}

# Make the classify request
response = requests.get(url, params=payload)

# The response is formatted in JSON
json_response = response.json()


print(json_response['error'])