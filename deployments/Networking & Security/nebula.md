# Overlay Networks

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within user-defined groups. 

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs/d
* [Defines Website](https://www.defined.net/)

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
For simplicity, the following will demonstrate deploying a _Nebula_ overlay network between an AnyLog _Master_, _Operator_
and _Query_ node respectively on linux machines 

**On Master Node**: 
0. Make a directory called Nebula - which will be used for all necessary files, unless stated otherwise 
```shell
cd $HOME
mkdir nebula 
cd $HOME/nebula
```
1. Downloading Nebula & Untar Nebula software - the example below uses the latest version of Nebula, other version can be found [here](https://github.com/slackhq/nebula/releases)   
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
<< 
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

<< comment 
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
mv host1.crt lighthouse/host.crt 
mv host1.key lighthouse/host.key

<<COMMENT 
root@anylog-master:~/nebula# ls -l host1/
total 8
-rw------- 1 root root 304 Aug  3 01:43 host.crt
-rw------- 1 root root 127 Aug  3 01:43 host.key
<< COMMENT 
 ```

c) Create keys for _Host_ 2
```shell
mkdir host2

# create certificate & key  
./nebula-cert sign -name "host2" -ip "192.168.100.9/24"

# move certificate and key into host2 directory 
mv host2.crt host2/host.crt 
mv host2.key host2/host.key

<<COMMENT 
root@anylog-master:~/nebula# ls -l host2/
total 8
-rw------- 1 root root 304 Aug  3 01:43 host.crt
-rw------- 1 root root 127 Aug  3 01:43 host.key
<< COMMENT 
 ```



