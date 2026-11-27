---
title: "Intro to Networking and Security"
description: "AnyLog network configuration, IP and port selection, network monitoring and diagnostics, and the layered security mechanisms available to secure distributed AnyLog networks."
layout: page
source_path: ""
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**   | **Version** |
 |------------|-------------|--------------|----------|
 | 2026-11-26 | Moshe Shadmon | Updated |          |
--->

AnyLog makes distributed data accessible as a single logical data source, regardless of the physical location of the data.

To accomplish this, network connectivity, accessibility, and security are as critical as database access. AnyLog provides mechanisms to configure, monitor, and secure communications between nodes, applications, and external services.

## Networking

AnyLog nodes communicate over a distributed network. Each node must be accessible to the nodes and applications that need to communicate with it, using the appropriate IP addresses, ports, and network routes.

AnyLog supports both standard network interfaces (e.g., `eth0`) and virtual network interfaces (e.g., `nebula1`, from the Nebula overlay network).

The network interface, IP address selection, and service binding are configurable, allowing AnyLog to operate across local networks, public networks, private networks, and secure overlay networks.

When deploying a node, the default ports are as follows:

| Node Type | TCP Port | REST Port | Broker Port |
| :---: | :---: | :---: | :---: |
| Master | 32048 | 32049 | |
| Operator | 32148 | 32149 | 32150 |
| Query | 32348 | 32349 | |
| Publisher | 32248 | 32249 | 32250 |
| Generic (Sandbox) | 32548 | 32549 | 32550 |

These are default port assignments and can be modified to accommodate specific deployment requirements.

For details on the TCP, REST, and Broker services, network interface selection, IP address configuration, and service binding, see **Network Processing**.

## Network Status and Diagnostics

AnyLog provides CLI commands to inspect the networking environment, monitor network status, and troubleshoot connectivity issues.

These commands allow users and administrators to examine the networking environment of individual nodes as well as nodes distributed across the AnyLog network.

Network monitoring and diagnostics include:

* Identifying available network interfaces and their configurations.
* Examining network connections.
* Identifying IP addresses and network service endpoints.
* Monitoring network connectivity and accessibility.
* Troubleshooting communication issues between nodes and external applications.

### Network Status Commands

AnyLog provides commands to inspect the network configuration of a node, identify available network interfaces, and troubleshoot network accessibility and service binding.

| Command           | Description |
|-------------------| --- |
| `get connections` | Displays the external, internal, and bind addresses associated with the node's TCP, REST, and Messaging services. |
| `get nics list`   | Lists the available network interfaces, their IP addresses, connection speeds, and operational status. |
| `get hostname`    | Returns the hostname assigned to the local computing environment by the operating system. |

#### Get Connections

The `get connections` command displays the network endpoints associated with the services configured on an AnyLog node.

```anylog
get connections
```

Example output:

```text
Type      External Address    Internal Address  Bind Address
---------|-------------------|-----------------|------------|
TCP      | 203.0.113.10:7448  | 10.0.0.199:7448  |0.0.0.0:7448|
REST     | 203.0.113.10:7449  | 10.0.0.199:7449  |0.0.0.0:7449|
Messaging| 203.0.113.10:7450  | 10.0.0.199:7450  |0.0.0.0:7450|
```

| Property | Description |
| --- | --- |
| `Type` | The network service (TCP, REST, or Messaging). |
| `External Address` | The IP address and port advertised for external access to the service. |
| `Internal Address` | The IP address and port associated with the service within the local network. |
| `Bind Address` | The local IP address and port to which the service is bound. An IP address of `0.0.0.0` indicates that the service listens on all available IPv4 interfaces. |

This command is particularly useful when deploying nodes behind NAT, configuring port forwarding, using overlay networks, or troubleshooting connectivity between nodes and external applications.

Note that the command displays the configured network endpoints and does not verify whether they are accessible from other machines.

#### Get NICs List

The `get nics list` command displays the Network Interface Cards (NICs) available in the computing environment in which the AnyLog node is running.

The list includes physical, virtual, wireless, overlay, and loopback network interfaces, as available on the host.

```anylog
get nics list
```

Example output:

```text
NICs List
Name                         IP              Speed Is Up
----------------------------|---------------|-----|-----|
Ethernet                    |  169.254.63.12|    0|False|
Ethernet 2                  | 169.254.144.89|    0|False|
Wi-Fi                       |     10.0.0.199| 1505|True |
vEthernet (Default Switch)  |     172.31.0.1| 4294|True |
NordLynx                    |       10.5.0.2| 4294|False|
Loopback Pseudo-Interface 1 |      127.0.0.1| 1073|True |
```

| Property | Description |
| --- | --- |
| `Name` | The name assigned to the network interface by the operating system. |
| `IP` | The IP address associated with the network interface. |
| `Speed` | The reported interface speed in Mbps. A value of `0` indicates that the speed is unknown or unavailable. |
| `Is Up` | Indicates whether the network interface is operational (`True` or `False`). |

The command is particularly useful when:

* Identifying the network interfaces available on a node.
* Selecting an interface when configuring the `NIC_TYPE` parameter.
* Identifying the IP addresses associated with physical and virtual network interfaces.
* Verifying the status of network interfaces.
* Troubleshooting network configuration and connectivity issues.

#### Get Hostname

The `get hostname` command returns the hostname of the computing environment in which the AnyLog node is running, as reported by the operating system.

```anylog
get hostname
```

Example output:

```text
GT13_Max
```

The hostname identifies the local machine or container. It is not necessarily the AnyLog node name or a fully qualified domain name (FQDN).

The command does not verify DNS resolution or network accessibility. In a containerized deployment, the returned hostname may be that of the container rather than the host machine.

#### Monitoring Remote Nodes

Network status commands can also be issued using the `run client` command to inspect the networking environment of remote AnyLog nodes.

```anylog
run client (192.168.1.100:32148) get connections
run client (192.168.1.100:32148) get nics list
```

This allows users and administrators to inspect network configurations across a distributed AnyLog network from a single node.

For information on the computing environment of a node, including its operating system, CPU, memory, and disk resources, see **Get Node Resources** (`get node resources`).

## Security

AnyLog provides multiple complementary security mechanisms that can be combined to address the security requirements of a deployment.

### Overlay Networks

A third-party overlay network, such as [Nebula](https://nebula.defined.net/docs/), provides a secure networking infrastructure between distributed AnyLog nodes.

An overlay network can:

* Control which nodes are authorized to participate in the network.
* Provide stable virtual IP addresses to participating nodes.
* Simplify routing between nodes across different physical networks.
* Encrypt communications between participating nodes.

Overlay networks are configured using the third-party provider's tools, independently of AnyLog.

### Key-Based Authentication

Each participating node or user can be assigned a private/public key pair.

Messages are signed using the sender's private key. The receiving node authenticates the sender using the corresponding public key and validates the sender's permissions against the network's policies before processing the message.

This mechanism enables authentication and authorization across a distributed AnyLog network.

Node keys can optionally be managed using a software TPM (`swtpm` and a REST API), provided by the [AnyLog-TPM](https://github.com/royshadmon/AnyLog-TPM) project.

The software TPM is configured using commands such as:

```anylog
tpm set
tpm enabled = on
tpm set node key password
```

The software TPM provides an alternative to storing private keys as plain files. As a software-emulated TPM, it does not provide the hardware isolation of a physical TPM chip.

See **Software TPM for AnyLog** for configuration and deployment details.

### Certificate-Based Authentication

AnyLog can act as a Certificate Authority (CA), issuing client certificates to external applications, such as REST clients, Grafana, and other third-party services.

Certificates allow external applications to authenticate using a public key associated with a member policy, enabling authentication and authorization through AnyLog's policy-based security mechanisms.

### Local Private Key Protection

A node's locally stored private key is protected by a local password, which must be supplied when the node restarts.

This password protects the private key at rest and is independent of the authentication mechanisms used to secure communications between nodes.

For details on configuring network security, generating keys, defining member, permission, and assignment policies, and testing authentication and authorization between nodes, see **Securing the Network**.

## See Also

* **Network Processing** — Configuring TCP, REST, and Broker services, network interfaces, IP addresses, and service binding.
* **Network Status and Diagnostics** — Commands for monitoring network interfaces, connections, and connectivity.
* **Get Node Resources** — Retrieving hardware, operating system, CPU, memory, and disk information using the `get node resources` command.
* **Securing the Network** — Overlay networks, key-based authentication, certificate-based authentication, and policy-based permissions.
* **Software TPM for AnyLog** — Optional software-emulated TPM for managing node keys.
* **Authentication** — SSL certificates and Basic Authentication configuration.
* **DNP3 TLS Test Certificates** — Generating a local CA chain for TLS testing on DNP3 connections.