import os
import requests
import json
from partner import parse_lib
from urllib.parse import parse_qs

def proxy_handler(even, config) : 
    response_message = ""
    try : 
        method = even['httpMethod']
        path_params = even['pathParameters']['myProxy']
        if method == 'GET' :
            payload = even['queryStringParameters']
        else :
            try : 
                payload = json.loads(even['body'])
            except Exception :
                payload = { k : v[0] for k, v in parse_qs(even['body']).items() }
        assert payload, ""
        params = parse_lib(path_params, payload)
        if params : 
            r = requests.get(os.environ['api_url'], params=params)
            response_message = r.text
        else :
            response_message = "undefined path parameter : %s"%path_params
    except Exception as e :
        response_message = str(e) 
    finally :
        return HttpsResponse(200, response_message)
    
def HttpsResponse(statusCode, Message) :
    return {
        'statusCode' : statusCode,
        "headers": {
            "content-type": "application/json"
        },
        'body' : json.dumps({
            'message' : Message
        })
    }
    
        
        
