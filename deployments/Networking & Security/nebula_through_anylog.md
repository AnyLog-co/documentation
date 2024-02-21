# Nebula Through AnyLog

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within 
user-defined groups. 

By default, AnyLog is provided with pre-set certification. This allows the user to just declare Nebula configuration file 
and configure the desired `OVERLAY_IP` value in order to deploy AnyLog with Nebula. Please note, using this tactic means 
your nodes can be accessed by people using the pre-set certifications.

In order to resolve the issue mentioned above, users can do 2 things:  
* [Personalize Nebula](nebula.md) & [Updating Docker for Nebula](#personalized-nebula)  
* Directions to secure your network with AnyLog can be found [here](../../secure%20network.md)

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs)
* [Defines' Website](https://www.defined.net/)
* [Configuring Overlay with AnyLog](Configuring%20Overlay%20with%20AnyLog.md)

## Deploying with pre-set Nebula 
1. Download Nebula [configuration file](https://raw.githubusercontent.com/slackhq/nebula/master/examples/config.yml)
```shell
wget https://raw.githubusercontent.com/slackhq/nebula/master/examples/config.yml
```

2. Update configuration file for either _lighthouse_ or _node_ 
* Lighthouse 
```yaml
# This is the nebula example configuration file. You must edit, at a minimum, the static_host_map, lighthouse, and firewall sections
# Some options in this file are HUPable, including the pki section. (A HUP will reload credentials from disk without affecting existing tunnels)

# PKI defines the location of credentials for this node. Each of these can also be inlined by using the yaml ": |" syntax.
pki:
  # The CAs that are accepted by this node. Must contain one or more certificates created by 'nebula-cert ca'
  ca: /app/nebula/ca.crt
  cert: /app/nebula/host.crt
  key: /app/nebula/host.key
  # blocklist is a list of certificate fingerprints that we will refuse to talk to
  #blocklist:
  #  - c99d4e650533b92061b09918e838a5a0a6aaee21eed1d12fd937682865936c72
  # disconnect_invalid is a toggle to force a client to be disconnected if the certificate is expired or invalid.
  #disconnect_invalid: true

# The static host map defines a set of hosts with fixed IP addresses on the internet (or any network).
# A host can have multiple fixed IP addresses defined here, and nebula will try each when establishing a tunnel.
# The syntax is:
#   "{nebula ip}": ["{routable ip/dns name}:{routable port}"]
# Example, if your lighthouse has the nebula IP of 192.168.100.1 and has the real ip address of 100.64.22.11 and runs on port 4242:
static_host_map:
  #  "192.168.100.1": ["100.64.22.11:4242"]

...

lighthouse:
  # am_lighthouse is used to enable lighthouse functionality for a node. This should ONLY be true on nodes
  # you have configured to be lighthouses in your network
  am_lighthouse: true
  # serve_dns optionally starts a dns listener that responds to various queries and can even be
  # delegated to for resolution
  #serve_dns: false
  #dns:
    # The DNS host defines the IP to bind the dns listener to. This also allows binding to the nebula node IP.
    #host: 0.0.0.0
    #port: 53
  # interval is the number of seconds between updates from this node to a lighthouse.
  # during updates, a node sends information about its current IP addresses to each node.
  interval: 60
  # hosts is a list of lighthouse hosts this node should report to and query from
  # IMPORTANT: THIS SHOULD BE EMPTY ON LIGHTHOUSE NODES
  # IMPORTANT2: THIS SHOULD BE LIGHTHOUSES' NEBULA IPs, NOT LIGHTHOUSES' REAL ROUTABLE IPs
  hosts:
    #    - "192.168.100.1"

... 

firewall: 
  outbound:
    # Allow all outbound traffic from this node
    - port: any
      proto: any
      host: any

  inbound:
    # Allow icmp between any nebula hosts
    - port: any
      proto: icmp
      host: any
    # AnyLog Server port
    - port: 32048
      proto: tcp
      host: any
    # AnyLog REST port
    - port: 32049
      proto: tcp
      host: any
```
* Node 
```yaml
# This is the nebula example configuration file. You must edit, at a minimum, the static_host_map, lighthouse, and firewall sections
# Some options in this file are HUPable, including the pki section. (A HUP will reload credentials from disk without affecting existing tunnels)

# PKI defines the location of credentials for this node. Each of these can also be inlined by using the yaml ": |" syntax.
pki:
  # The CAs that are accepted by this node. Must contain one or more certificates created by 'nebula-cert ca'
  ca: /app/nebula/ca.crt
  cert: /app/nebula/host.crt
  key: /app/nebula/host.key
  # blocklist is a list of certificate fingerprints that we will refuse to talk to
  #blocklist:
  #  - c99d4e650533b92061b09918e838a5a0a6aaee21eed1d12fd937682865936c72
  # disconnect_invalid is a toggle to force a client to be disconnected if the certificate is expired or invalid.
  #disconnect_invalid: true

# The static host map defines a set of hosts with fixed IP addresses on the internet (or any network).
# A host can have multiple fixed IP addresses defined here, and nebula will try each when establishing a tunnel.
# The syntax is:
#   "{nebula ip}": ["{routable ip/dns name}:{routable port}"]
# Example, if your lighthouse has the nebula IP of 192.168.100.1 and has the real ip address of 100.64.22.11 and runs on port 4242:
static_host_map:
    "192.168.100.1": ["100.64.22.11:4242"]

...

lighthouse:
  # am_lighthouse is used to enable lighthouse functionality for a node. This should ONLY be true on nodes
  # you have configured to be lighthouses in your network
  am_lighthouse: false
  # serve_dns optionally starts a dns listener that responds to various queries and can even be
  # delegated to for resolution
  #serve_dns: false
  #dns:
    # The DNS host defines the IP to bind the dns listener to. This also allows binding to the nebula node IP.
    #host: 0.0.0.0
    #port: 53
  # interval is the number of seconds between updates from this node to a lighthouse.
  # during updates, a node sends information about its current IP addresses to each node.
  interval: 60
  # hosts is a list of lighthouse hosts this node should report to and query from
  # IMPORTANT: THIS SHOULD BE EMPTY ON LIGHTHOUSE NODES
  # IMPORTANT2: THIS SHOULD BE LIGHTHOUSES' NEBULA IPs, NOT LIGHTHOUSES' REAL ROUTABLE IPs
  hosts:
    - "192.168.100.1"

... 

firewall: 
  outbound:
    # Allow all outbound traffic from this node
    - port: any
      proto: any
      host: any

  inbound:
    # Allow icmp between any nebula hosts
    - port: any
      proto: icmp
      host: any
    # AnyLog Server port
    - port: 32148
      proto: tcp
      host: any
    # AnyLog REST port
    - port: 32149
      proto: tcp
      host: any
  # AnyLog Message Broker port
    - port: 32150
      proto: tcp
      host: any
```

3. Enable [TUN/TAP driver](https://docs.kernel.org/networking/tuntap.html) to provide packet reception and transmission 
for user space programs. 
```shell
sudo modprobe tun
```
4. In advance_configurations.al on the AnyLog node, update the following parameters: 
   * ENABLE_NEBULA 
   * OVERLAY_IP
   * NEBULA_CONFIG_FILE - local Nebula configuration file path

```dotenv
...
#--- Networking ---
# Declare Policy name
CONFIG_NAME=""
# Overlay IP address - if set, will replace local IP address when connecting to network 
OVERLAY_IP="" # <--- update this value 
# Configurable (local) IP address that can be used when behind a proxy, or using Kubernetes for static IP
PROXY_IP=""
...
#--- Nebula ---
# Whether to enable nebula overlay or not (by default set  
ENABLE_NEBULA=true 
# Nebula configuration file - path should be the local path on the machine of the user
NEBULA_CONFIG_FILE=/root/deployments/nebula/config_lighthouse.yml
```

5. Start Node

**Notes**: 
1. It is recommended to begin with lighthouse(s) and then slowly add in more nodes.
2. When using Nebula, no 2 nodes can seat on the same physical machine due to the dependecy on _tun_ driver

## Personalized Nebula
While AnyLog does have default certifications for Nebula, users can easily change those out to use their own certifications.

1. Using the directions in the generic [nebula document](nebula.md), complete the following steps: 
   1. [Prepare personalized keys](nebula.md#prepare-keys-for-nebula-node)
      1. Downloading Nebula & Untar the Nebula software
      2. Creating your own certificate authority
      3. Create keys for lighthouse and nodes -- each set of keys (_host.crt_ and _host.key_) should be in its own directory 
      that'll be associated with an AnyLog Node 
   2. [Prepare Configuration](nebula.md#preparing-configuration-) 
      1. Download [configuration file](https://github.com/slackhq/nebula/blob/master/examples/config.yml)
      2. make a copy of the configurations into each of the directories associated with AnyLog Node(s)
      3. Update the configuration file as either [lighthouse](./nebula_through_anylog.md#L59) or [node](./nebula_through_anylog.md#L102)
2. For the docker-compose.yml file update the volumes
    * remove `${NEBULA_CONFIG_FILE}:${ANYLOG_PATH}/nebula/config.yml`
    * remove `anylog-master-nebula-configs:${ANYLOG_PATH}/nebula/`
    * manually include new files
```yaml
# before
version: "3"
services:
  anylog-master:
    image: anylogco/anylog-network:${TAG}
    privileged: true
    restart: always
    env_file:
      - anylog_configs.env
      - advance_configs.env
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: host
    environment:
      - INIT_TYPE=${INIT_TYPE}
    volumes:
      - anylog-master-anylog:/app/AnyLog-Network/anylog
      - anylog-master-blockchain:/app/AnyLog-Network/blockchain
      - anylog-master-data:/app/AnyLog-Network/data
      - anylog-master-local-scripts:/app/deployment-scripts
      - ${NEBULA_CONFIG_FILE}:${ANYLOG_PATH}/nebula/config.yml
      - anylog-master-nebula-configs:${ANYLOG_PATH}/nebula/
volumes:
  anylog-master-anylog:
  anylog-master-blockchain:
  anylog-master-data:
  anylog-master-local-scripts:
  anylog-master-nebula-configs:

# updated
version: "3"
services:
  anylog-master:
    image: anylogco/anylog-network:${TAG}
    privileged: true
    restart: always
    env_file:
      - anylog_configs.env
      - advance_configs.env
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: host
    environment:
      - INIT_TYPE=${INIT_TYPE}
    volumes:
      - anylog-master-anylog:/app/AnyLog-Network/anylog
      - anylog-master-blockchain:/app/AnyLog-Network/blockchain
      - anylog-master-data:/app/AnyLog-Network/data
      - anylog-master-local-scripts:/app/deployment-scripts
      - /home/anyloguser/lighthouse:/app/nebula/
volumes:
  anylog-master-anylog:
  anylog-master-blockchain:
  anylog-master-data:
  anylog-master-local-scripts:
```  
3. start node 
```shell
bash /home/anyloguser/deployments/run.sh docker master up
```