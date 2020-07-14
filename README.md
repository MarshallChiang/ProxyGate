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


 
