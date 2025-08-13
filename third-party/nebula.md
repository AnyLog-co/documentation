# Overlay Networks

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within user-defined groups. 

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs)
* [Defines' Website](https://www.defined.net/)
* [Configuring Overlay with AnyLog](Configuring%20Overlay%20with%20AnyLog.md)

## Terminology 
_Nebula's_ overlay network requires a minimum of 2 nodes: _lighthouse_ and regular nodes, nicknamed _host_, as well as 
authentication certificates for the nodes to be associated with one another.  

* **Lighthouse**: A _Nebula_ host that is responsible for keeping track of other Nebula hosts, and helping them find each 
other within a Nebula network. In order to eliminate centralization, Nebula offers advanced configuration to support 
[multiple lighthouses](https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses).

* **Host**: A _Nebula_ host is simply any single node in the network, e.g. a server, laptop, phone, tablet. Each host will 
have its own private key, which is used to validate the identity of that host when Nebula tunnels are created.

* **Certificate Authority**: Nebula Certificate Authority (CA) consists of two files, a CA certificate, and an associated 
private key. CA certificate is distributed to, and trusted by, every host on the network. The CA private key should not be 
distributed, and can be kept offline when not being used to add hosts to a Nebula network.

## Preparing 
For simplicity, the following will demonstrate deploying a _Nebula_ overlay network between an 2 physical machines. 

The following steps are all done on the same machine, unless stated otherwise

## Prepare Keys for Nebula Node
0. Make a directory called `nebula` - which will be used for all necessary files, unless stated otherwise 
```shell
cd $HOME
mkdir nebula 
cd $HOME/nebula
```
1. Downloading Nebula & Untar the Nebula software - the example below uses the latest version of Nebula (for Linux amd64), other version can be found [here](https://github.com/slackhq/nebula/releases)   
```shell
wget https://github.com/slackhq/nebula/releases/download/v1.7.2/nebula-linux-amd64.tar.gz
tar -xzvf nebula-linux-amd64.tar.gz 

<< COMMENT
root@anylog-master:~/nebula# ls -l 
total 39360
-rwxr-xr-x 1 1001  123 18811965 Jun  1 15:21 nebula
-rwxr-xr-x 1 1001  123  7664823 Jun  1 15:21 nebula-cert
-rw-r--r-- 1 root root 13820988 Jun  1 15:29 nebula-linux-amd64.tar.gz
<< COMMENT
```

2. Creating your certificate authority - certificate authority is used to create credentials that prove a host should be trusted by your organization
```shell
./nebula-cert ca -name "AnyLog Co."

<< COMMENT
root@anylog-master:~/nebula# ls -l 
total 39368
-rw------- 1 root root      243 Aug  3 01:36 ca.crt # <-- new file 
-rw------- 1 root root      174 Aug  3 01:36 ca.key # <-- new file 
-rwxr-xr-x 1 1001  123 18811965 Jun  1 15:21 nebula
-rwxr-xr-x 1 1001  123  7664823 Jun  1 15:21 nebula-cert
-rw-r--r-- 1 root root 13820988 Jun  1 15:29 nebula-linux-amd64.tar.gz
<< COMMENT
```

3. Creating Keys and Certificates - we are creating a Nebula network that uses the subnet `192.168.100.x/24`, and will assign 
IP addresses to each host from within this subnet.

a) Create keys for _Lighthouse_ node
```shell
mkdir lighthouse 

# create certificate & key  
./nebula-cert sign -name "lighthouse1" -ip "192.168.100.1/24"

# move certificate and key into lighthouse directory 
mv lighthouse1.crt lighthouse/host.crt 
mv lighthouse1.key lighthouse/host.key
cp ca.crt lighthouse/

<< COMMENT 
root@anylog-master:~/nebula# ls -l lighthouse/
total 8
-rw------- 1 root root 304 Aug  3 01:43 host.crt
-rw------- 1 root root 127 Aug  3 01:43 host.key
<< COMMENT 
 ```

b) Create keys for _Host_ 1 
```shell
mkdir host1 

# create certificate & key  
./nebula-cert sign -name "host1" -ip "192.168.100.5/24"

# move certificate and key into host1 directory 
mv host1.crt host1/host.crt 
mv host1.key host1/host.key
cp ca.crt host1/

<<COMMENT 
root@anylog-master:~/nebula# ls -l host1/
total 8
-rw------- 1 root root 304 Aug  3 01:43 host.crt
-rw------- 1 root root 127 Aug  3 01:43 host.key
<< COMMENT 
 ```

## Preparing Configuration 
1. Download _Nebula_ [configuration file](https://github.com/slackhq/nebula/blob/master/examples/config.yml)
```shell
cd $HOME/nebula 
wget https://raw.githubusercontent.com/slackhq/nebula/master/examples/config.yml
```

2. Copy configuration file into _lighthouse_ directory
```shell
cp config.yml lighthouse/
```

3. In the _lighthouse_ configuration file ($HOME/nebula/lighthouse/config.yml) make the following changes:

a) Under the _static_host_map_ section, ensure there are no associating IP addresses 

b) Under the _lighthouse_ section, set `am_lighthouse` to **true**, and ensure there are no IP addresses under `hosts` parameter.

c) Under the _firewall_ section, make sure the overlay is able to communicate over _TCP_

**Subset of configuration file with relevant changes for _lighthouse_**:

```yaml
...

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

    # Allow icmp between any nebula hosts
    - port: any
      proto: tcp
      host: any
```

4. Copy the configuration file into _host1_
```shell
cp $HOME/nebula/lighthouse/config.yml $HOME/nebula/host1/
```

5. In the _host1_ configuration file ($HOME/nebula/host1/config.yml) make the following changes:

a) Under the _static_host_map_ section, ensure the lighthouse is defined in terms of **both** external IP (for AWS, the 
external IP is the _Elastic IP_) and overlay IP address 

b) Under the _lighthouse_ section, set `am_lighthouse` to **false**, and ensure lighthouse (overlay IP) is added to the `hosts` parameter.

c) Under the _firewall_ section, make sure the overlay is able to communicate over _TCP_

**Subset of configuration file with relevant changes for _host_**:
```yaml
...

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

    # Allow icmp between any nebula hosts
    - port: any
      proto: tcp
      host: any
```

## Preparing Other Nodes
In order to deploy a _Nebula_ overlay network, the following files need to be copied from their current directory into
the other nodes that'll be part of the network: 
* $HOME/nebula/nebula - into both nodes
* $HOME/nebula/host1 - into node1

**Copy Into node1**: 
1. On one of the two other nodes, create a directory called nebula 
```shell
mkdir $HOME/nebula 
```
2. From the node where the keys and configuration were generated, copy the following file and directory: 
* $HOME/nebula/nebula
* $HOME/nebula/host1
```shell
scp -r $HOME/nebula/nebula ubuntu@host1:~/nebula/ 
scp -r $HOME/nebula/host1 ubuntu@host1:~/nebula/
```

## Deploy Overlay Network 

### Lighthouse 
1. Create a nebula directory under `/etc/`
```shell
sudo mkdir /etc/nebula
```

2. Copy content from `$HOME/nebula/lighthouse` into  `/etc/nebula`
```shell
sudo cp -r $HOME/nebula/lighthouse/* /etc/nebula
```

3. Deploy Nebula inside a screen  
```shell
screen -Sd nebula -m bash -c "cd $HOME/nebula ; sudo ./nebula -config /etc/nebula/config.yml"

<< COMMENT 
# Sample Output 
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:outgoing endPort:0 groups:[] host:any ip: localIp: proto:0 startPort:0]"
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:incoming endPort:0 groups:[] host:any ip: localIp: proto:1 startPort:0]"
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:incoming endPort:0 groups:[] host:any ip: localIp: proto:6 startPort:0]"
INFO[0000] Firewall started                              firewallHash=5ce47917b3e8b8c3fe4d75838dfb76cac018d96000b9e999982b00d9e0d94586
INFO[0000] Main HostMap created                          network=192.168.100.1/24 preferredRanges="[]"
INFO[0000] punchy enabled
INFO[0000] Loaded send_recv_error config                 sendRecvError=always
INFO[0000] Nebula interface is active                    boringcrypto=false build=1.7.2 interface=nebula1 network=192.168.100.1/24 udpAddr="0.0.0.0:4242"
<< COMMENT
```

### Host 1 
1. Create a nebula directory under `/etc/`
```shell
sudo mkdir /etc/nebula
```

2. Copy content from `$HOME/nebula/host1` into  `/etc/nebula`
```shell
sudo cp -r $HOME/nebula/host1/* /etc/nebula
```

3. Deploy Nebula inside a screen
```shell
screen -Sd nebula -m bash -c "cd $HOME/nebula ; sudo ./nebula -config /etc/nebula/config.yml"

<< COMMENT 
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:outgoing endPort:0 groups:[] host:any ip: localIp: proto:0 startPort:0]"
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:incoming endPort:0 groups:[] host:any ip: localIp: proto:1 startPort:0]"
INFO[0000] Firewall rule added                           firewallRule="map[caName: caSha: direction:incoming endPort:0 groups:[] host:any ip: localIp: proto:6 startPort:0]"
INFO[0000] Firewall started                              firewallHash=5ce47917b3e8b8c3fe4d75838dfb76cac018d96000b9e999982b00d9e0d94586
INFO[0000] Main HostMap created                          network=192.168.100.5/24 preferredRanges="[]"
INFO[0000] punchy enabled
INFO[0000] Loaded send_recv_error config                 sendRecvError=always
INFO[0000] Nebula interface is active                    boringcrypto=false build=1.7.2 interface=nebula1 network=192.168.100.5/24 udpAddr="0.0.0.0:4242"
INFO[0000] Handshake message sent                        handshake="map[stage:1 style:ix_psk0]" initiatorIndex=3984236087 localIndex=3984236087 remoteIndex=0 udpAddrs="[172.105.4.104:4242]" vpnIp=192.168.100.1
INFO[0000] Handshake message received                    certName=lighthouse1 durationNs=88321353 fingerprint=895d2ceeaeb01a3b7ca0c69c3341fb6d2796f14de9eb9ddb34bb474f04fd843b handshake="map[stage:2 style:ix_psk0]" initiatorIndex=3984236087 issuer=962964ccb25b15d31b28e6569ac8a563d86291d590ea3062bace377d0a422f92 remoteIndex=3984236087 responderIndex=1655575412 sentCachedPackets=1 udpAddr="172.105.4.104:4242" vpnIp=192.168.100.1
<< COMMENT 
```

### Validate 
* Ping from _Host_ to _Lighthouse_ 
```shell
root@localhost:~# ping 192.168.100.1 -c 10 
PING 192.168.100.1 (192.168.100.1) 56(84) bytes of data.
64 bytes from 192.168.100.1: icmp_seq=1 ttl=64 time=86.3 ms
64 bytes from 192.168.100.1: icmp_seq=2 ttl=64 time=86.3 ms
64 bytes from 192.168.100.1: icmp_seq=3 ttl=64 time=86.2 ms
64 bytes from 192.168.100.1: icmp_seq=4 ttl=64 time=86.3 ms
64 bytes from 192.168.100.1: icmp_seq=5 ttl=64 time=86.1 ms
64 bytes from 192.168.100.1: icmp_seq=6 ttl=64 time=86.4 ms
64 bytes from 192.168.100.1: icmp_seq=7 ttl=64 time=86.2 ms
64 bytes from 192.168.100.1: icmp_seq=8 ttl=64 time=86.2 ms
64 bytes from 192.168.100.1: icmp_seq=9 ttl=64 time=86.2 ms
64 bytes from 192.168.100.1: icmp_seq=10 ttl=64 time=86.2 ms

--- 192.168.100.1 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9014ms
rtt min/avg/max/mdev = 86.137/86.225/86.399/0.080 ms
```

* Ping from _Lighthouse_ to _Host_
```shell
root@anylog-master:~/nebula# ping 192.168.100.5 -c 10 
PING 192.168.100.5 (192.168.100.5) 56(84) bytes of data.
64 bytes from 192.168.100.5: icmp_seq=1 ttl=64 time=86.2 ms
64 bytes from 192.168.100.5: icmp_seq=2 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=3 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=4 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=5 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=6 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=7 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=8 ttl=64 time=86.1 ms
64 bytes from 192.168.100.5: icmp_seq=9 ttl=64 time=86.3 ms
64 bytes from 192.168.100.5: icmp_seq=10 ttl=64 time=86.1 ms

--- 192.168.100.5 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9011ms
rtt min/avg/max/mdev = 86.050/86.137/86.257/0.050 ms
```