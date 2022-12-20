# Overlay Networks

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/).

* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs/)


## Deploying Nebula 
A _Nebula_ overlay network requires a minimum of 2 nodes: lighthouse node and regular nodes. Lighthouse is a Nebula 
hosts that is responsible for keeping track of other Nebula hosts, and helping them find each other within a Nebula 
network. 

### Prepare Keys & Configurations  
1. Make directory nebula and store configs and [software](https://github.com/slackhq/nebula/releases) into it
```shell
cd $HOME
mkdir nebula 
cd $HOME/nebula 

wget https://github.com/slackhq/nebula/releases/download/v1.6.1/nebula-linux-amd64.tar.gz
tar -xzvf nebula-linux-amd64.tar.gz
```
2. Create a [certificate authority](https://nebula.defined.net/docs/guides/quick-start/#creating-your-first-certificate-authority) 
for your organization - this will create `ca.crt` & `ca.key`. The CA certificate is distributed to, and trusted by, 
every host on the network. The CA private key should not be distributed, and can be kept offline when not being used to 
add hosts to a Nebula network.
```shell
# Feel free to replace 'AnyLog co.' with any other value 
./nebula-cert ca -name "AnyLog co."
```
3. Create [node specific keys](https://nebula.defined.net/docs/guides/quick-start/#creating-keys-and-certificates) - 
You can name the hosts any way you'd like, including FQDN. Make sure the nebula IP address(es) are on a different subnet 
from the  
```shell
./nebula-cert sign -name lighthouse -ip 10.0.0.1/24
./nebula-cert sign -name node1 -ip 10.0.0.2/24 
```
Note - Each non-lighthouse node should have its own IP address and configuration files. 

4. Download configuration file(s)
```shell
curl -o config.yml https://raw.githubusercontent.com/slackhq/nebula/master/examples/config.yml
cp config.yml config-lighthouse.yaml
```
5. Update `config-lighthouse.yaml` 
   * Update `static_host_map` -- `"${NEBULA_IP}": ["${NEBULA_NODE_EXTERNAL_IP}:4242"]`
   * Set `am_lighthouse` to **`true`**
   * `hosts` value(s) should be commented out
   * Under `inbound` make sure everything is accessible
```yaml
inbound:
# Allow icmp between any nebula hosts
- port: any
  proto: any
  host: any

6. Copy the lighthouse configuration file to create nebula node configuration file
```shell
cp config-lighthouse.yaml config-node.yaml
```

7. Update `config-node.yaml`
    * Set `am_lighthouse` to **`false`**
    * Uncomment `hosts` value(s) and set the value to the lighthouse Nebula IP address 

### Deploy Lighthouse
1. Assuming you created the configurations and keys on a different machine, copy the relevant content into the node
    * ca.crt 
    * config-lighthouse.yaml
    * lighthouse.crt 
    * lighthouse.key
    * nebula 
```shell
# on nebula node create nebula directory 
mkdir $HOME/nebula ; cd $HOME/nebula 

# copy from original node into nebula lighthouse node   
scp $HOME/nebula/ca.crt user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula
scp $HOME/nebula/config-lighthouse.yaml user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/config.yml
scp $HOME/nebula/lighthouse.crt user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/host.crt 
scp $HOME/nebula/lighthouse.key user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/host.key
scp $HOME/nebula/nebula user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/
```

2. On the lighthouse node create `/etc/nebula` and move all files (except nebula) into the new directory 
```shell
sudo mkdir /etc/nebula 
cd $HOME/nebula 
for FILE in ca.crt config.yml host.crt host.key ; do sudo cp ${FILE} /etc/nebula ; done  
```

3. Start lighthouse node
```shell
screen -Sd nebula -m bash -c "cd $HOME/nebula ; sudo ./nebula -config /etc/nebula/config.yml"
```

### Deploy Node
1. Assuming you created the configurations and keys on a different machine, copy the relevant content into the node
    * ca.crt 
    * config-node.yaml
    * node1.crt 
    * node1.key
    * nebula 
```shell
# on nebula node create nebula directory 
mkdir $HOME/nebula ; cd $HOME/nebula 

# copy from original node into nebula lighthouse node   
scp $HOME/nebula/ca.crt user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula
scp $HOME/nebula/config-lighthouse.yaml user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/config.yml
scp $HOME/nebula/node1.crt user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/host.crt 
scp $HOME/nebula/node1.key user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/host.key
scp $HOME/nebula/nebula user@${NEBULA_NODE_EXTERNAL_IP}:$HOME/nebula/
```

2. On the lighthouse node create `/etc/nebula` and move all files (except nebula) into the new directory 
```shell
sudo mkdir /etc/nebula 
cd $HOME/nebula 
for FILE in ca.crt config.yml host.crt host.key ; do sudo cp ${FILE} /etc/nebula ; done  
```

3. Start lighthouse node
```shell
screen -Sd nebula -m bash -c "cd $HOME/nebula ; sudo ./nebula -config /etc/nebula/config.yml"
```
