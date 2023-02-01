# Kubernetes Networking

Kubernetes Orchestrator generates a unique virtual IP each time a node is deployed. Since communication between nodes is 
policy based, AnyLog cannot have a new virtual IP each time a node is deployed. As such, the configuration file, for
Kubernetes, has a configuration called `KUBERNETES_SERVICE_IP` which should be set to the service name of the deployment.
When using the [deployment scripts](deploying_node.md), this step is done automatically. Once set, the network 
connectivity will be done with the virtual IP address for local IP. However, on the blockchain the local_ip will be set 
to the service name; which other members on the Kubernetes cluster can utilize.

Farther details regarding things like binding and thread count can be found in our [networking section](../../network%20configuration.md)

When deploying with Kubernetes we recommend using [Nginx](https://www.nginx.com/) or other proxy service, as well as our
[configuration policy](../../policies.md).

### Sample Node Policy for Kubernetes
The following provides a basic example of both the configuration policy, as-well-as a (master) node policy. 
Notice that the values for the configuration policy are relatively set, that way when a deployment is restarted there
won't be a need to declare a new policy for the node due to the changing virtual IP address.

```json 
{"config" : {
  "name" : "master-configs",
  "company" : "New Company",
  "port" : "!anylog_server_port.int",
  "external_ip" : "!external_ip",
  "ip" : "!ip",
  "rest_port" : "!anylog_rest_port.int"
}},
{"master" : {
  "name" : "anylog-master",
  "company" : "New Company",
  "hostname" : "anylog-master-pod", 
  "loc" : "0.0, 0.0",
  "country" : "Unknown",
  "state" : "Unknown",
  "city" : "Unknown",
  "port" : 32048,
  "external_ip" : "73.222.38.13",
  "ip" : "anylog-master-service",
  "proxy_ip" : "10.0.0.183",
}}
```

