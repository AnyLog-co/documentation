# Streaming Data into AnyLog 

Data can be sent into an AnyLog node via different forms of communication, such as: _REST_, _MQTT_ and _Kafka_.

Detailed information is available in the following documents:
* [Adding data](../adding%20data.md) - an overview on how data is added to AnyLog nodes.
* [Mapping Data](../mapping%20data%20to%20tables.md) - Mapping source data to a target format.
* [REST Calls](../using%20rest.md) - Using REST calls to deliver data to an AnyLog Node.  
* [Message Broker](../message%20broker.md) - Declaring AnyLog as a message broker.

## Sending Data
[send_data.py](Sample Python Scripts/data/send_data.py) is a python script to send timestamp & value data (see the example below) into AnyLog node via _REST_ (_POST_ or _PUT_)  or _MQTT_ publish. 
```json
{
  "timestamp": "2023-07-16T22:15:16.275270Z", 
  "value": 26.760648537459296
}
```

Other examples can be found in our [generic data generator](../training/Data%20Generator.md).

## cURL 
* The following cURL request sends data via REST _PUT_ into AnyLog node.
```shell
curl -X PUT 127.0.0.1:32149 \
  -H "type: json" \
  -H "dbms: test" \
  -H "table: sample_data" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:15:16.275270Z", "value": 26.760648537459296}, {"timestamp": "2023-07-16T22:15:16.779954Z", "value": 99.07731050408944}, {"timestamp": "2023-07-16T22:15:17.282287Z", "value": 99.28450509848346}, {"timestamp": "2023-07-16T22:15:17.786096Z", "value": 80.41027907076285}, {"timestamp": "2023-07-16T22:15:18.290123Z", "value": 32.27699391736516}, {"timestamp": "2023-07-16T22:15:18.794041Z", "value": 44.586993538065876}, {"timestamp": "2023-07-16T22:15:19.296349Z", "value": 97.49718100436169}, {"timestamp": "2023-07-16T22:15:19.796996Z", "value": 14.902283983713582}, {"timestamp": "2023-07-16T22:15:20.299712Z", "value": 85.88924631087048}, {"timestamp": "2023-07-16T22:15:20.803080Z", "value": 15.671337182852396}]'
```

* The following cURL request sends data via REST _POST_ into AnyLog node.   
  * When using REST _POST_, the accepting AnyLog node needs to enable the MQTT client service.  
  * An example can be found under [Enabling the MQTT Client Service](#enabling-the-mqtt-client-service).
```shell
curl -X POST 127.0.0.1:32149 \
  -H "command: data" \
  -H "topic: sample-data" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:01:35.531498Z", "value": 0.34818421211998407, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.036593Z", "value": 43.03195182458719, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.540271Z", "value": 2.7131214097633305, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.044805Z", "value": 60.165240674173546, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.549647Z", "value": 73.94402366511534, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.053755Z", "value": 51.633021025712786, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.558580Z", "value": 41.02022743564046, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.062021Z", "value": 52.22346461071091, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.567019Z", "value": 63.078391396022596, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:40.071045Z", "value": 52.09570154599, "db_name": "test", "table": "sample_data"}]'
```

## Python 
**Prerequisite**:
1) Python3
2) With the exception of [paho-mqtt](https://pypi.org/project/paho-mqtt/), the following libraries are pre-installed with Python3.X 
    * argparse 
    * datetime 
    * json 
    * importlib 
    * random 
    * re 
    * requests 
    * [paho-mqtt](https://pypi.org/project/paho-mqtt/) (required only if _MQTT_ publish is used)

### Example
[Python example](Sample Python Scripts/data/send_data.py) is an interactive tool to publish data into AnyLog via _REST_ or _MQTT_
* View help information
```shell
anyloguser$ python3 ~/Documentation/examples/Sample\ Python\ Scripts/data/send_data.py --help 
positional arguments:
  conn                  Either REST or MQTT connection information
options:
  -h, --help            show this help message and exit
  --db-name DB_NAME     logical database name
  --total-rows TOTAL_ROWS
                        number of rows to generate
  --insert-process {put,post,mqtt}
                        which insert process type to utilize
  --topic TOPIC         POST or MQTT topic
```

* Sample Call using POST command
```shell
anyloguser$ python3 ~/Documentation/examples/Sample\ Python\ Scripts/data/send_data.py 127.0.0.1:32149 \
  --db-name test \
  --total-rows 100 \
  --insert-process post \
  --topic sample-data
```

## Enabling the MQTT Client Service
When adding data using _POST_ or _MQTT_ publish, enable an AnyLog service that considers the published data.

The command `run mqtt client` enables the service on the AnyLog node. This service allows to map the published data to 
a target structure and is required when data is transferred to the node with REST POST or data is published on the node 
(as if the AnyLog node is a message broker).  

The example below enables the MQTT Client service whereas:
1. If data is transferred using REST, the IP and Port are using the REST address of the service enabled on the node.
    * In the example use: `!external_ip` for !ip and `!anylog_rest_port` for !port
2. If data is Published, the IP and Port (by default are using the Message Broker address of the service enabled on the node.
    * In the example use: `!external_ip` for !ip and `!anylog_broker_port` for !port
3. DBMS - provides the mapping to retrieve the database name from the source data.
4. Table - provides the mapping to retrieve the table name from the source data.
5. column.timestamp.timestamp - provides the mapping to retrieve the timestamp value from the source data.
6. column.value.float - provides the mapping to retrieve the value from the source data.

```anylog
<run mqtt client where broker = !ip and port = !port and user-agent=anylog and log=false and topic=(
    name=sample-data and
    dbms="bring [db_name]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]"
)>
```



