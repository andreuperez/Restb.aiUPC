import requests
import json
import sys

def api():
    global json_response
    url = 'https://property.restb.ai/v1/multianalyze'
    payload = {
    # Add your client key
    'client_key': '2593c868c3e81326f28f6eab1c97191f70017da8908b0dec17d8e60cfc690e49'
    }
    request_body = {
    "image_urls": args,
    "solutions": {"roomtype": 1.0, "roomtype_reso": 1.0, "style": 1.0, "r1r6": None, "c1c6": None, "features": 4.0, "features_reso": 1.0, "compliance": 2.0, "caption": None}
    }

    # Make the classify request
    response = requests.post(url, params=payload, json=request_body)

    # The response is formatted in JSON
    json_response = response.json()
    print(json_response)
    
def main():
    global args
    args = sys.argv[1:]
    api()

if __name__ == '__main__':
    main()
