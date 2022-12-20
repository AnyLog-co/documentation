# EdgeX
The demo is using [EdgeX](https://www.edgexfoundry.org/) random data generator, with data being sent over their  
_app-service-mqtt_. The contents that  changes are set to **BOLD**. For general information of Edgex, in terms of AnyLog,
please review [EdgeX Usage](../../using%20edgex.md).

### Steps 
1. Clone [lfedge-code](https://github.com/AnyLog-co/lfedge-code)
```shell
git clone https://github.com/AnyLog-co/lfedge-code 
cd lfedge-code/edgex 
```

2. Update configurations in [.env](https://github.com/AnyLog-co/lfedge-code/blob/main/edgex/.env) file
   1. Update the MQTT params to match the credentials in _anylgo-operator-node1_
   ```dotenv
    MQTT_TOPIC=anylogedgex
    MQTT_IP_ADDRESS=139.162.200.15
    MQTT_PORT=32150
    MQTT_USER=""
    MQTT_PASSWORD=""
    ```
   2. If you're using update the `ARCH` value in _line 27_. Sample ARCH value for ARM64: `ARCH=-arm64`
   ```dotenv
    # default amd64 machine 
   ARCH=""
    # update to arm64 machine 
   ARCH=-arm64
   ```
3. Start EdgeX instance 
```shell
cd lfedge-code/edgex 
docker-compose up -d
```

## Validate Deployment
1. Make sure nothing crashed: `docker ps -a | grep edgex`
```shell
root@edgex-operator2:~# docker ps -a | grep edgex
a13b169023b7   emqx/kuiper:1.1.1-alpine                                                   "/usr/bin/docker-ent…"   45 hours ago   Up 44 hours             127.0.0.1:20498->20498/tcp, 9081/tcp, 127.0.0.1:48075->48075/tcp                       edgex-kuiper
56a3482bdfc8   edgexfoundry/docker-sys-mgmt-agent-go:1.3.1                                "/sys-mgmt-agent -cp…"   45 hours ago   Up 44 hours             127.0.0.1:48090->48090/tcp                                                             edgex-sys-mgmt-agent
2740875f17a4   edgexfoundry/docker-app-service-configurable:1.3.1                         "/app-service-config…"   45 hours ago   Up 44 hours             48095/tcp, 127.0.0.1:48101->48101/tcp                                                  edgex-app-service-configurable-mqtt
32b749bbd104   edgexfoundry/docker-device-random-go:1.3.1                                 "/device-random --cp…"   45 hours ago   Up 44 hours             127.0.0.1:49988->49988/tcp                                                             edgex-device-random
e960f5ff00c5   edgexfoundry/docker-app-service-configurable:1.3.1                         "/app-service-config…"   45 hours ago   Up 44 hours             48095/tcp, 127.0.0.1:48100->48100/tcp                                                  edgex-app-service-configurable-rules
e50c8de4b879   edgexfoundry/docker-device-modbus-go:1.3.1                                 "/device-modbus --cp…"   45 hours ago   Up 44 hours             127.0.0.1:49991->49991/tcp                                                             edgex-device-modbus
e91cd4ad63fa   edgexfoundry/docker-core-command-go:1.3.1                                  "/core-command -cp=c…"   45 hours ago   Up 44 hours             127.0.0.1:48082->48082/tcp                                                             edgex-core-command
59464a3a976d   edgexfoundry/docker-core-data-go:1.3.1                                     "/core-data -cp=cons…"   45 hours ago   Up 44 hours             127.0.0.1:5563->5563/tcp, 127.0.0.1:48080->48080/tcp                                   edgex-core-data
b706d9584413   edgexfoundry/docker-core-metadata-go:1.3.1                                 "/core-metadata -cp=…"   45 hours ago   Up 44 hours             127.0.0.1:48081->48081/tcp                                                             edgex-core-metadata
13abb3559d2a   edgexfoundry/docker-support-notifications-go:1.3.1                         "/support-notificati…"   45 hours ago   Up 44 hours             127.0.0.1:48060->48060/tcp                                                             edgex-support-notifications
ff7d350ca3ba   edgexfoundry/docker-support-scheduler-go:1.3.1                             "/support-scheduler …"   45 hours ago   Up 44 hours             127.0.0.1:48085->48085/tcp                                                             edgex-support-scheduler
0346e264f6d6   edgexfoundry/docker-edgex-consul:1.3.0                                     "edgex-consul-entryp…"   45 hours ago   Up 44 hours             8300-8302/tcp, 8400/tcp, 8301-8302/udp, 8600/tcp, 8600/udp, 127.0.0.1:8500->8500/tcp   edgex-core-consul
fab7cbdcc29f   redis:6.0.9-alpine                                                         "docker-entrypoint.s…"   45 hours ago   Up 44 hours             127.0.0.1:6379->6379/tcp                                                               edgex-redis
f135b724626e   nexus3.edgexfoundry.org:10003/edgex-devops/edgex-modbus-simulator:latest   "/simulator"             45 hours ago   Up 44 hours             127.0.0.1:1502->1502/tcp                                                               edgex-modbus-simulator
```
2. Data is coming in: `curl http://127.0.0.1:48080/api/v1/reading 2> /dev/null`
```json
[
  {
    "id": "000767a3-61bb-49e1-93ff-be4695eb5b43",
    "created": 1659412501505,
    "origin": 1659412501498780400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int16",
    "value": "10380",
    "valueType": "Int16"
  },
  {
    "id": "000797b4-736b-48b9-bbe5-09594be7099f",
    "created": 1659403221133,
    "origin": 1659403221133020700,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int32",
    "value": "771919435",
    "valueType": "Int32"
  },
  {
    "id": "00079ae9-340a-4d70-9e0b-9a5a8b48e216",
    "created": 1659412541467,
    "origin": 1659412541463869400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "27",
    "valueType": "Int8"
  },
  {
    "id": "0008d23e-7640-4974-aaeb-179e375566cb",
    "created": 1659425642023,
    "origin": 1659425642019472400,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "-87",
    "valueType": "Int8"
  },
  {
    "id": "000f547c-25b7-4d96-b862-67467345a74c",
    "created": 1659461623534,
    "origin": 1659461623530927000,
    "device": "Random-Integer-Generator01",
    "name": "RandomValue_Int8",
    "value": "-49",
    "valueType": "Int8"
  },
  ...
]
```
