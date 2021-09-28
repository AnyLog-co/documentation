# AnyLog-API

AnyLog allows for executing commands via REST. 
As such, we have created a tool to easily deploy different types of AnyLog instance on any node as long as has REST and TCP are ruunning.
Additionally, this package provides different types of calls that can be used to easily connect  any app to AnyLog.     

The provided example uses Docker, however this process works on any form   
## Steps 
0. Download [AnyLog-API](https://github.com/AnyLog-co/AnyLog-API)
```buildoutcfg
git clone https://github.com/AnyLog-co/AnyLog-API
```


1. Create a personalized config file based on the type of node you want to deploy. [Sample Config File](examples/sample_config.ini)


2. Deploy a REST based AnyLog instance 
```buildoutcfg
export NODE_NAME=new-node
export SERVER_PORT=2048
export REST_PORT=2049 
export BROKER_PORT=2050 # optional

docker run --network host --name ${NODE_NAME} --rm \
    -e NODE_TYPE=rest \
    -e ANYLOG_SERVER_PORT=${SERVER_PORT} \
    -e ANYLOG_REST_PORT=${REST_PORT} \
    -e ANYLOG_BROKER_PORT=${BROKER_PORT} \ # Optional 
    -v ${NODE_NAME}-anylog:/app/AnyLog-Network/anylog:rw \ 
    -v ${NODE_NAME}-blockchain:/app/AnyLog-Network/blockchain:rw \ 
    -v ${NODE_NAME}-data:/app/AnyLog-Network/data:rw \ 
    -v ${NODE_NAME}-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -d oshadmon/anylog:predevelop
```
**Attach to Docker**: `docker attach --detach-keys="ctrl-d"  ${CONTAINER_ID}`

**Detach from Docker**: `CTRL+d`


3. Start A specific type of node based on personalized configuration

**Options**
```buildoutcfg
anylog@anylog-vm:~/AnyLog-API$ python3 ~/AnyLog-API/deployment/main.py --help
usage: main.py [-h] [-a AUTH] [-t TIMEOUT] [-l [LOCATION]] [-e [EXCEPTION]]
               rest_conn config_file

positional arguments:
  rest_conn             REST connection information
  config_file           AnyLog INI config file

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  REST authentication information (default: None)
  -t TIMEOUT, --timeout TIMEOUT
                        REST timeout period (default: 30)
  -l [LOCATION], --location [LOCATION]
                        If set to True & location not in config, add lat/long
                        coordinates for new policies (default: False)
  -e [EXCEPTION], --exception [EXCEPTION]
                        print exception errors (default: False)
```

**Sample Call**
```buildoutcfg
# Sample Call
export NODE_CONN=127.0.0.1:2049 # REST IP and PORT
export CONFIG_FILE=$HOME/AnyLog-API/config/my_node.ini  # Path of config file 
python3 $HOME/AnyLog-API/deployment/main.py ${NODE_CONN} ${CONFIG_FILE} -e -l 
```
