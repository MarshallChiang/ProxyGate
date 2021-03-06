## ProxyGate
A proxy as lambda integrated function to consolidate and transit HTTP requests from {myProxy+} on API Gateway
<img src=https://marshallfiles.s3-ap-northeast-1.amazonaws.com/github-static/component_image_1_proxygate.png>

## Environment Setup

```bash
$ cd path/to/project
$ pip install -r requirements.txt -t .
```
<img src=https://marshallfiles.s3-ap-northeast-1.amazonaws.com/github-static/component_image_2_proxygate.png width=60% height=60%>

After implement to AWS lambda and integrated with API Gateway, setup os environment of server endpoint and configuration source.

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
#### pathName
   Wildcard value of {myProxy+} on API Gateway as a key to respective configuration.
#### mapping
   To indicate the value in client request payload and transit into the defined key.
#### constant
   Fixed key-value pair to append to the payload.
#### condition
   Each `if` statement is bind to their `then` action, as long as the clause(s) in `if` are satisfied, the payload will be rendered according to the value in `then`.
#### formatting
   Manipulate the payload by evaling the lambda expression.
