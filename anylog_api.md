# AnyLog-API

AnyLog allows users to communicate with it via [REST](using%20rest.md), as such as long as a node is accessible via 
_REST_ users can deploy nodes remotely; in an automated fashion. The API tool allows to manage configurations of a node 
remotely, rather than needing to have the exact, and potentially unchangeable, configurations when deploying a node at 
the edge.

The [AnyLog-API](https://github.com/AnyLog-co/AnyLog-API) is a set of packages (in different languages) that can be used
as the bases for building your own deployment scripts. 

## Deployment via Anylog-API
Within the AnyLog-API directory, we've created [deployments](https://github.com/AnyLog-co/AnyLog-API/tree/main/deployments), 
which are a set of scripts that accept configurations information, and based on the configuration deploy the relevant
processes. 

```shell
anylog-node:~/ $ python3.9 ~/AnyLog-API/deployments/python_rest/deploy_node.py --help
usage: deploy_node.py [-h] [--auth AUTH] [--timeout TIMEOUT] [-e [EXCEPTION]] rest_conn config_file

positional arguments:
  rest_conn             REST connection information
  config_file           Configuration file to be utilized

optional arguments:
  -h, --help                     show this help message and exit
  --auth          AUTH           Authentication information (comma separated) [ex. username,password] (default: None)
  --timeout       TIMEOUT        REST timeout (default: 30)
  -e, --exception [EXCEPTION]    Whether to print errors (default: False)
```


## Usage
In order for AnyLog-API to work, the AnyLog instance which the API is communicating against must be running with at least
_REST_. Directions for deploying a [REST node](deployments/Docker/rest_node.md)

```shell
/home/anylog/AnyLog-API/python_rest/src
├── anylog_connector.py 
├    * base functions for GET, PUT and POST commands
├── generic_get_calls.py
├    * check node status 
├    * get AnyLog set parameters
├    * view processes
├    * view network information 
├    * get hostname 
├    * get operator / publisher 
├    * get streaming 
├    * help (for a given command) 
├── generic_post_calls.py
├    * adding key/value pairs to AnyLog dictionary
├    * network connection
├    * run scheduler 
├    * run operator / publisher
├── rest_support.py
├    * generated error message if a REST request fails 
├    * extract results if request is a GET 
├    * generate command for network connection
├── generic_data_calls.py
├    * view partitions
├    * view information comming in via `run mqtt client`
├    * PUT data 
├    * POST (data)
├    * Enable MQTT client 
├    * set partitions
├    * query data  
├── generic_data_support.py
├    * Build `run mqtt client` command
├    * Build query command 
├── blockchain_calls.py
├    * blockchain   
├    * blockchain sync
├    * prepare policy 
├    * post policy
├── blockchain_support.py
├    * build blockchain commands   
├    * build policies 
├── database_calls.py
├    * view connected logical databases
├    * view declared tables (on a given database)
├    * declare to logical database 
├    * declare table on a logical database (if table is declared)
├── database_support.py
├    * generate `connect dbms` command based on params 
├    * check whether a (specific) logical database exists 
├    * check whether a (specific) table exists  
├── find_location.py
├    * Check the geo location of a given node
└── support.py

```

### Python3
**Requirements**: 
* [ast](https://docs.python.org/3/library/ast.html)
* [json](https://docs.python.org/3/library/json.html?highlight=json#module-json)
* [os](https://docs.python.org/3/library/os.html?highlight=os#module-os)
* [requests](https://pypi.org/project/requests/)

```shell
python3.9 -m pip install -r $HOME/AnyLog-API/python_rest/requirements.txt
```
 
**Sample Utilization**: 
1. Download AnyLog-API -- we hope to have a `pip install` option in the near future 
```shell
cd $HOME
git clone https://github.com/AnyLog-co/AnyLog-API
```

2. import the AnyLog-API code into your project & declare _REST_ connection information
```pyhon
import os
import sys

ANYLOG_API_PATH = $HOME/AnyLog-API/python_rest 
sys.path.insert(0, ANYLOG_API_PATH)

from anylog_connector import AnyLogConnector

# connect to AnyLog 
anylog_conn = AnyLogConnector(conn='127.0.0.1:32049', auth='username,password', timeout=30)

"""
using methods in python_rest, easily communicate with the AnyLog node via REST 
"""
```

