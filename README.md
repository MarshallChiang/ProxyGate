## ProxyGate
A proxy with lambda integrated function to consolidate and transit HTTP requests from {myProxy+} on API Gateway.
<img src=https://marshallchiang.github.io/assets/img/portfolio/fullsize/ProxyGate_image_1.png>

## Environment Setup

```bash
$ cd path/to/project
$ pip install -r requirements.txt -t .
```

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

## Example

Input and Output 

```javascript
// POST request as input.
{
   "amount":"1000",
   "session_id":"b3ceaf8f58ad0f",
   "order_number":"0035454",
   "shop":"TEST_STORE",
   "datetime":"2021-08-03 20:32:04",
   "order_list":[
      {
         "product":{
            "product_name":"itemA",
            "product_type":"normal",
            "product_id":"23067710-aa3e",
            "product_amount":"200"
         }
      },
      {
         "product":{
            "product_name":"itemB",
            "product_type":"normal",
            "product_id":"23352710-d3fd",
            "product_amount":"300"
         }
      },
      {
         "product":{
            "product_name":"itemC",
            "product_type":"normal",
            "product_id":"23395710-cedd",
            "product_amount":"250"
         }
      },
      {
         "product":{
            "product_name":"itemD",
            "product_type":"normal",
            "product_id":"04b86690-4ca5",
            "product_amount":"250"
         }
      }
   ]
}
```

Configuration starts iterating with defined path and extracting.

```javascript
// Multiple payloads as output.
{
    'order_number' : '0035454',
    'amount' :  '200',
    'product_id' : '23067710-aa3e',
    'datetime' : '2021-08-03 20:32:04',
    'session_id' : 'b3ceaf8f58ad0f'
    'type' : 'normal'
}
{
    'order_number' : '0035454',
    'amount' :  '300',
    'product_id' : '23352710-d3fd',
    'datetime' : '2021-08-03 20:32:04',
    'session_id' : 'b3ceaf8f58ad0f'
    'type' : 'normal'
}
{
    'order_number' : '0035454',
    'amount' :  '250',
    'product_id' : '23395710-cedd',
    'datetime' : '2021-08-03 20:32:04',
    'session_id' : 'b3ceaf8f58ad0f'
    'type' : 'normal'
}
{
    'order_number' : '0035454',
    'amount' :  '250',
    'product_id' : '04b86690-4ca5',
    'datetime' : '2021-08-03 20:32:04',
    'session_id' : 'b3ceaf8f58ad0f'
    'type' : 'normal'
}

```
