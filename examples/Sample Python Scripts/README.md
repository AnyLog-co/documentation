# REST via Python

Data can be sent into an AnyLog node via different forms of communication, such as: _REST_, _MQTT_ and _Kafka_.
Our [adding data](../../adding%20data.md) document provides an explanation for how to add data into an AnyLog node.

## Sending Data
### MQTT Client
As the [adding data](../../adding%20data.md#using-a-post-command) explains, a `run mqtt client` command is required when
sending data in any form but _REST PUT_ command. This is because all other formats (such as _REST POST_, _MQTT_, _Kafka_,
etc.) require data to be mapped to a destination format. For the sample data used both the cURL and [python](data/send_data.py)
examples, the `run mqtt client` is as follows: 

```anylog
# Sending data via POST 
<run mqtt client where broker = !ip and port = !anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=sample-data and 
    dbms="bring [db_name]" and 
    table="bring [table]" and 
    column.timestamp.timestamp="bring [timestamp]" and 
    column.value.float="bring [value]"
)>

# Sending data via MQTT 
<run mqtt client where broker = !ip and port = !anylog_broker_port and log=false and topic=(
    name=sample-data and 
    dbms="bring [db_name]" and 
    table="bring [table]" and 
    column.timestamp.timestamp="bring [timestamp]" and 
    column.value.float="bring [value]"
)>
```


### Examples
* Send data via REST _PUT_ using cURL
```shell
curl -X PUT 127.0.0.1:32149 \
  -H "type: json" \
  -H "dbms: test" \
  -H "table: sample_data" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:15:16.275270Z", "value": 26.760648537459296}, {"timestamp": "2023-07-16T22:15:16.779954Z", "value": 99.07731050408944}, {"timestamp": "2023-07-16T22:15:17.282287Z", "value": 99.28450509848346}, {"timestamp": "2023-07-16T22:15:17.786096Z", "value": 80.41027907076285}, {"timestamp": "2023-07-16T22:15:18.290123Z", "value": 32.27699391736516}, {"timestamp": "2023-07-16T22:15:18.794041Z", "value": 44.586993538065876}, {"timestamp": "2023-07-16T22:15:19.296349Z", "value": 97.49718100436169}, {"timestamp": "2023-07-16T22:15:19.796996Z", "value": 14.902283983713582}, {"timestamp": "2023-07-16T22:15:20.299712Z", "value": 85.88924631087048}, {"timestamp": "2023-07-16T22:15:20.803080Z", "value": 15.671337182852396}]'
```

* Send Data via REST _POST_ using cURL - reminder that for _POST_ the accepting AnyLog node needs to have a corresponding [MQTT client](#mqtt-client).
```shell
curl -X POST 127.0.0.1:32149 \
  -H "command: data" \
  -H "topic: sample-data" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:01:35.531498Z", "value": 0.34818421211998407, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.036593Z", "value": 43.03195182458719, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.540271Z", "value": 2.7131214097633305, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.044805Z", "value": 60.165240674173546, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.549647Z", "value": 73.94402366511534, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.053755Z", "value": 51.633021025712786, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.558580Z", "value": 41.02022743564046, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.062021Z", "value": 52.22346461071091, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.567019Z", "value": 63.078391396022596, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:40.071045Z", "value": 52.09570154599, "db_name": "test", "table": "sample_data"}]'
```

* [Python example](data/send_data.py) is an interactive tool to publish data into AnyLog via _REST_ or _MQTT_
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

anyloguser$ python3 ~/Documentation/examples/Sample\ Python\ Scripts/data/send_data.py 127.0.0.1:32149 \
  --db-name test \
  --total-rows 100 \
  --insert-process post \
  --topic sample-data
```


## Sending Blockchain Policies
The [blockchain](blockchain) directory provides examples to send into AnyLog. Unlike data, in which you declare 
only the Operator REST connection information, for data to be sent via REST, users need to also specify the correlating 
master (or ledger) TCP connection information. Farther details regarding blockchain can be found: 
* [Blockchain Configuratio](../../blockchain%20configuration.md)
* [Blockchain Commands](../../blockchain%20commands.md)

```shell
anyloguser$ python3 ~/Documentation/examples/Sample\ Python\ Scripts/blockchain/blockchain_add_policy_simple.py 127.0.0.1:32149 127.0.0.1:32048
```



