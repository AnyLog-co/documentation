# Adding Data

## Adding Data 
**cURL Format**: 
<pre>
curl --location --request POST '192.168.50.159:2051' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'Content-Type: text/plain' \
--data-raw ' [{"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
 {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
 {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}]'
</pre>

**Python Format**: 
<pre> 
import json 
import requests

# REST connection information (IP + Port) 
conn = '192.168.50.159:2051' 

# Header for POST data 
headers = {
    'command': 'data',
    'User-Agent': 'AnyLog/1.23',
    'Content-Type': 'text/plain'
}

# data to POST 
data = [
    {"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
    {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
    {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}
]

# Convert to JSON 
jdata = json.dumps(data) 

# POST proces 
try:
    r = requests.post('http://%s' % conn, headers=headers, data=jdata)
except Exception as e: 
    print('Failed to POST data to %s (Error: %s)' % (conn, e))
else: 
    if r.status_code != 200: 
        print('Failed to POST data to %s due to network error: %s' % (conn, r.status_code))
    else:
        print('Success') 
</pre> 
