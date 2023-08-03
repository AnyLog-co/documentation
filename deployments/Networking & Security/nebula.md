# Overlay Networks

AnyLog uses overlay networks in order to have nodes that are distributed on separated subnetworks to act as if they're all
under the same network. For demonstration purposes we use Nebula, an open-source overlay network developed by the _Slack_ 
team and managed under [Defined](https://www.defined.net/). 

_Nebula_ is a mutually authenticated peer-to-peer overlay network, based on [Noise Protocol Framework](https://noiseprotocol.org/). 
This means that Nebula's overlay network uses certificates to assert a node's IP address, name, and membership within user-defined groups. 

**Documentation**
* [GitHub](https://github.com/slackhq/nebula)
* [Documentation](https://nebula.defined.net/docs/)

## Terminology 
A _Nebula_ overlay network requires a minimum of 2 nodes: _lighthouse_ and regular nodes, nicknamed _host_. 

* **Lighthouse**: A _Nebula_ host that is responsible for keeping track of other Nebula hosts, and helping them find each 
other within a Nebula network. In order to eliminate centralization, Nebula offers advanced configuration to support 
[multiple lighthouses](https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses).

* **Host**: A _Nebula_ host is simply any single node in the network, e.g. a server, laptop, phone, tablet. Each host will 
have its own private key, which is used to validate the identity of that host when Nebula tunnels are created.

* **Certificate Authority**: Nebula Certificate Authority (CA) consists of two files, a CA certificate, and an associated 
private key. CA certificate is distributed to, and trusted by, every host on the network. The CA private key should not be 
distributed, and can be kept offline when not being used to add hosts to a Nebula network.

