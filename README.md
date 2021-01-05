# IBMMQ-Browser-v1 
Restful service exposing messages on ibmmq  
Supports all major clients (JAVA, POSTMAN, PYTHON, etc)

## [USE THE UI at http://example.com:<port>/](http://example.com:<port>/)  
  
### Supported Methods  
base url: http://example.com:<port>
##### GET: / (Only applicable when using UI)
returns apps landing page
##### POST : /search
All post requests will be made to this endpoint

### Parameters
| param | description | Required | example |
| ------ | ------ | ------ | ----- |
| searchParam | all messages that include this string will be returned    | YES | "searchParam": "type"
| queue<#> | name of queues that will be included in search..   NOTE: keys will be ignored, values must be in ALL CAPS | YES, unless using allQueues feature | "queue1": "QUEUE.NAME"
| queueSuffix | name of queue alias, default is EXAMPLE.ENV.SUFFIX | NO | "queueSuffix": "EXAMPLE.ENV.SUFFIX"
| includeDelimiter | If true, results will include delimiter between messages | NO | "includeDelimiter": "false"
| notBefore | Result set will only include messages with a timestamp after the date provided.  Required formatting, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")  | NO | "notBefore": "2019-12-10 20:08:11"
| allQueues | if true, search all queues | NO | "allQueues": "true"
| BASE.QUEUE | if true, search base queues.  Will be useful if message scripts are down or queues are backed up | NO | "BASE.QUEUE": "true"

### Making Requests (examples)

#### Java (Rest Assured)
build JSON body
```
String url = "http://example.com:<port>/search"
JSONObject jsonObject = new JSONObject();  
jsonObject.put("searchParam", "type");  
jsonObject.put("que1", "queue_name1");  
jsonObject.put("que2", "queue_name2");  
String postRequestBody = jsonObject.toString()

Response response = RestAssured.given().config(RestAssured.config().sslConfig(config)).contentType(ContentType.JSON).body(postRequestBody).post(url);  

JSONObject result = new JSONObject(response.body().asString());  
```

#### POSTMAN  
Supports form-data, x-www-form-urlencoded, and raw JSON body requests  
Example Raw JSON body request:
```
{  
	"searchParam": "type",  
	
	"queName": "queue_name"  	
} 
```

NOTE: Unless your intention is to send the request via x-www-form-urlencoded, please ensure Content-Type -- application/x-www-form-urlencoded is unchecked, under the 'Headers' tab.  
Sometimes postman will save this setting even though you have selected another content-type option.

#### Python
Using requests library
```
import requests

URL = "http://example.com:<port>/search"  
PARAMS = {'searchParam': 'type', 'que1': 'queue_name1'}  
response = requests.post(URL, PARAMS)  
data = response.json()
```

# Response
List of JSON message objects for each queue included in the search
