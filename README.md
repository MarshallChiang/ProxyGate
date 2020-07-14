## ProxyGate
A proxy as lambda integrated function to consolidate and transit HTTP requests from {myProxy+} on API Gateway 
![Component screenshot](https://marshallfiles.s3-ap-northeast-1.amazonaws.com/ProxyGate_diagram.png)

## Environment Setup

```bash
$ cd path/to/project
$ pip install -r requirements.txt -t .
```

After implement to AWS lambda and integrated with API Gateway
```bash
$ aws lambda update-function-configuration --function-name ProxyGate \
    --environment "Variables={api_url=https://www.server.site ,resource=https://www.config.site}"
```
## Configuration Data Structure


```json
{
    "pathName": {
        "mapping": {
            "server_field1": "client_field1",
            "server_field2": "client_field2",
            "server_field3": "client_field3",
            "server_field4": "client_field4",
            "server_field5": "client_field5"
        },
        "constant": {
            "server_constant_field": "foo"
        },
        "condition": [
            {
                "if": {
                    "server_field1": [
                        "apple"
                    ]
                },
                "then": {
                    "server_field2": "red",
                    "server_field3": "fruit"
                }
            }
        ],
        "formatting": {
            "server_field6" : "lambda x : x['server_field3'] + '_' + x['server_field4']"
        }
    }
}
```
 
