import sys
import json
import requests

city = ""
neighborhood = ""
region = ""
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
        "neighborhood": neighborhood,
        "region": region,
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
    print("--------------------------------------------------------")
    print("(LOG): DATA:")
    print(data)

    with open("datos.json", "w") as outfile:
        json.dump(data, outfile)


def api():        
    print("--------------------------------------------------------")
    print("(LOG): Init API call")
    global json_response
    url = 'https://property.restb.ai/v1/multianalyze'
    payload = {
    # Add your client key
    'client_key': '2593c868c3e81326f28f6eab1c97191f70017da8908b0dec17d8e60cfc690e49'
    }
    print("------------------")
    print(sys.argv[5:])
    request_body = {
    "image_urls": sys.argv[5:],
    "solutions": {"roomtype": 1.0, "roomtype_reso": 1.0, "style": 1.0, "r1r6": None, "c1c6": None, "features": 4.0, "features_reso": 1.0, "compliance": 2.0, "caption": None}
    }
    
    # Make the classify request
    response = requests.post(url, params=payload, json=request_body)
    print("--------------------------------------------------------")
    print("(LOG): Waiting API answer")

    # The response is formatted in JSON
    json_response = response.json()
    print("--------------------------------------------------------")
    print("(LOG): API answer recived:")
    print(json_response)


def readJson():
    global city, bedrooms_r1r6, neighborhood, region, square_meters, bedrooms, bathrooms, property, kitchen, bathroom_r1r6, interior
    city = sys.argv[1]
    neighborhood = sys.argv[2]
    region = sys.argv[3]
    square_meters = sys.argv[4]
    try:
        bedrooms = json_response["response"]["solutions"]["roomtype"]["summary"]["count"]["room-bedroom"]
    except:
        bedrooms = 0
    
    try:
        bathrooms = json_response["response"]["solutions"]["roomtype"]["summary"]["count"]["bathroom"]
    except:
        bathrooms = 0

    try:
        property = json_response["response"]["solutions"]["r1r6"]["property"]["score"]
    except:
        property = 1

    try:
        kitchen = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["kitchen"]
    except:
        kitchen = 1

    try:
        bathroom_r1r6 = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["bathroom"]
    except:
        bathroom_r1r6 = 1

    try:
        bedrooms_r1r6 = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["bedrooms"]
    except:
        bedrooms_r1r6 = 1
    
    try:
        interior = json_response["response"]["solutions"]["r1r6"]["summary"]["score"]["interior"]
    except:
        interior = 1


def main():
    print("--------------------------------------------------------")
    print("(LOG): Init restb.aiAPI.py")
    print("--------------------------------------------------------")
    print("(LOG): Parameters:")
    print(sys.argv)
    api()
    readJson()
    jsonFormat()


if __name__ == '__main__':
    main()

