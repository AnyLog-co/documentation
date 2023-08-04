# Configuring Overlay Network with AnyLog
Deploying an overlay network onto of AnyLog allows for a unified network, even when nodes are spread across physical 
locations with different subnetworks. For testing purposes, we had used _Nebula_, an open-source overlay network 
developed by the _Slack_ team and managed under [Defined](https://www.defined.net/).

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within user-defined groups. 

**Documents**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs)
* [Defines' Website](https://www.defined.net/)
* [Installing Nebula](nebula.md)


## Deploy AnyLog with OverLay

### Manual Deployment 
When manually starting a network service (TCP, REST or Message Broker), replace the internal IP address value with the 
overlay IP address. Notice, without overlay IP the `internal_ip` parameter is set to the local/internal (**!ip**) IP 
address, where with overlay IP the `internal_ip` parameter is set to **!overlay_ip**. 

* Without Overlay IP
```anylog
# Disabled TCP bind 
anylog_server_port = 32048 
tcp_bind = false 
threads = 3 
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

# Enabled TCP bind 
anylog_server_port = 32048 
tcp_bind = true 
threads = 3 
<run tcp server where
    external_ip=!ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
```

* With Overlay IP
```anylog
# Disabled TCP bind 
anylog_server_port = 32048 
tcp_bind = false 
threads = 3 
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

# Enabled TCP bind 
anylog_server_port = 32048 
tcp_bind = true 
threads = 3 
<run tcp server where
    external_ip=!overlay_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
```


### Configuration based deployment
When deploying with an overlay network, the AnyLog [deployment scripts](https://github.com/AnyLog-co/deployment-scripts) 
will use the overlay IP address instead of the internal (or local) IP address auto generated on the node. 

1. To utilize the overlay IP address, make the following changes in the configuration file (`anylog_configs.env`):

a) `OVERLAY_IP` - the IP address of the physical machine that's associated with the overlay network

b) Make sure binding for `TCP_BIND`, `REST_BIND` and `BROKER_BIND` to **true**. Otherwise, the AnyLog instance is accessible
from outside the _overlay network_. If your query node(s) communicating with a business intelligence program (ex. 
_Microsoft PowerBI_, _Grafana_, _Lookr_) that's not part of the overlay network, then the `REST_BIND` for the query node
should be set to **false** in the configuration.

```dotenv
# --- Networking ---
# By default, a node will connect to the (TCP, REST and Message Broker - if declared) based on its associated policy.
#
# If a user disables policy-based option (`POLICY_BASED_NETWORKING=false`) then network connectivity is based on information
# in the configuration file.
#
# For policy-based configuration networking will be set as follows:
#   1. A user is able to decide whether the TCP connectivity is set to bind or not. If bind is enabled - then AnyLog
#       will use either the local or overlay IP address.
#        * If an overlay is declared, then the overlay IP address will replace the local IP address
#        * If binding is enabled, then AnyLog will only utilize the local or overlay IP address. Whereas if
#          binding is disabled, the blockchain will use both the external and local (or overlay) IP addresses of the
#          physical machine.
#
#    2. For REST and Message Broker, the (default) binding value is False. This is because data and/or GET requests
#       coming-in may come from machines/devices outside the network.#
#
#    3. Regarding the relation between blockchain policy and AnyLog networking - AnyLog only cares about policy keys `ip`,
#       `local_ip` and port values. All other networking information, such as `proxy_ip` and `external_ip` (if binding is
#       True), are more of an FYI regarding the network configurations of the actual machine.

# Connect to TCP, REST and Message Broker (if configured) based on correlating node policy
POLICY_BASED_NETWORKING=true
# Declare Policy name
#CONFIG_POLICY_NAME=<NETWORKING_CONFIG_POLICY_NAME>
# External IP address of the machine
#EXTERNAL_IP=<NETWORKING_EXTERNAL_IP>
# Local network IP address of the machine
#LOCAL_IP=<NETWORKING_LOCAL_IP>
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=192.168.100.1
# Configurable (local) IP address that can be used when behind a proxy, or using Kubernetes for static IP
#PROXY_IP=<NETWORKING_PROXY_IP>
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32048
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32049
# Port value to be used as an MQTT broker, or some other third-party broker
#ANYLOG_BROKER_PORT=<NETWORKING_ANYLOG_BROKER_PORT>
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=true
# The number of concurrent threads supporting HTTP requests.    
TCP_THREADS=6
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=true
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=20
# The number of concurrent threads supporting HTTP requests.    
REST_THREADS=6
# Boolean value to determine if messages are send over HTTPS with client certificates.
REST_SSL=False
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
BROKER_BIND=false
# The number of concurrent threads supporting broker requests.  
BROKER_THREADS=6
```

2. Redeploy AnyLog with the new configuration. 

## How AnyLog Works with Overlay Network
Using the configuration policies allows for consistent behavior against a node, even when if the IPs / Ports change, as 
it uses variable names rather than hard-codded values. As such, when re-deploying with an overlay IP address, 

The following provides example for both with and without overlay network when `TCP_BIND` is enabled and `REST_BIND` disabled 
in order to demonstrate how the change in the configuration file would reflect in the policies.

* Sample configuration without `overlay_ip` variable set
```json
{"config" : {
    "name" : "anylog-master-config",
    "company" : "New Company",
    "ip" : "!ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int"
  }
}
{"master" : {
    "name": "anylog-master",
    "company": "New Company",
    "hostname": "anylog-master",
    "loc": "43.6496,-79.3833",
    "country": "CA",
    "state": "Ontario",
    "city": "Toronto",
    "port": 32048,
    "ip": "172.105.4.104",
    "rest_port": 32049
  }
}
```

* Sample configuration with `overlay_ip` variable set
```json
{"config" : {
    "name" : "anylog-master-overlay-config",
    "company" : "New Company",
    "ip" : "!broker_ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int"
  }
}
{"master" : {
    "name": "anylog-master",
    "company": "New Company",
    "hostname": "anylog-master",
    "loc": "43.6496,-79.3833",
    "country": "CA",
    "state": "Ontario",
    "city": "Toronto",
    "port": 32048,
    "ip": "192.168.100.1",
    "rest_port": 32049
  }
}
```

You'll notice that the change in configuration changed a few parameters in both the `config` policy and `master` policy 
1. The name of the `config` policy changed from `anylog-master-config` to `anylog-master-overlay-config`
2. In the `config` policy the variable `ip` changed from **!ip** to **!overlay_ip**
3. In the `master` policy, associated with a specific master node, the `ip` variable changed from  **172.105.4.104** to 
**192.168.100.1**. 

When the node is deployed, it will utilize the new overlay IP rather than the internal or local IP of the node. This change 
would be reflected in the `get connections`, while still allowing user to view all three IP addresses `within the AnyLog 
dictionary. 

* AnyLog connections  without overlay 
```anylog
AL anylog-master +> get connections 

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |172.105.4.104:32048|172.105.4.104:32048|172.105.4.104:32048|
REST     |172.105.4.104:32049|172.105.4.104:32049|172.105.4.104:32049|
Messaging|Not declared       |Not declared       |Not declared       |
```

* AnyLog connections  without overlay 
```anylog
AL anylog-master +> get connections 

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |192.168.100.1:32048|192.168.100.1:32048|192.168.100.1:32048|
REST     |192.168.100.1:32049|192.168.100.1:32049|192.168.100.1:32049|
Messaging|Not declared       |Not declared       |Not declared       |
```

* View IP address within the AnyLog dictionary  
```anylog
AL anylog-master +> get dictionary ip 

Key                 Value                           
-------------------|-------------------------------|
deploy_local_script|false                          |
external_ip        |                  172.105.4.104| # <-- external IP addrress (autogenerated for the phyical network)
ip                 |                  172.105.4.104| # <-- local/internal IP addrress (autogenerated for the phyical network)  
ledger_ip          |                      127.0.0.1|
local_scripts      |/app/deployment-scripts/scripts|
nosql_ip           |                      127.0.0.1|
overlay_ip         |                  192.168.100.1| # <-- nebula overlay IP aaddress 
```