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


