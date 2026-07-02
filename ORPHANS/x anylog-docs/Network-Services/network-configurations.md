---
title: Network Configuration
description: Configure IP addresses, ports, NAT, bind settings, and overlay networks for AnyLog nodes.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

AnyLog nodes communicate over a peer-to-peer TCP network. Correctly configuring IP addresses and ports ensures nodes are discoverable, reachable, and able to participate in the network — whether they sit on a local LAN, behind NAT, or across an overlay network.

---

## IP address concepts

When an AnyLog node starts, it automatically detects two IP addresses and stores them in the local dictionary:

| Key | Description |
|---|---|
| `!ip` | The local/internal IP — accessible within the private network |
| `!external_ip` | The external IP — accessible from the Internet |

These are used as defaults when starting the TCP and REST services. You can override them explicitly in your configuration.

```anylog
get !ip
get !external_ip
get ip list     # all IPs available on the node
```

---

## Single IP vs dual IP setup

### Single IP (simple deployment)
If the node has one IP that is reachable by all peers, use the same IP for both `external_ip` and `internal_ip`:

```anylog
run tcp server where external_ip = !ip and external_port = 32048 and threads = 6
```

### Dual IP (NAT / cloud / edge)
When the node is behind a router or NAT — with a private LAN IP and a public Internet IP — configure both:

```anylog
<run tcp server where
  external_ip = !external_ip and external_port = 32048 and
  internal_ip = !ip and internal_port = 32048 and
  bind = false and threads = 6>
```

The node will **listen** on the internal IP but **publish** the external IP to the blockchain, making it discoverable to peers across the Internet.

---

## The bind parameter

`bind` controls which IPs the service actually listens on:

| Value | Behaviour |
|---|---|
| `true` | Binds to the single specified IP only |
| `false` | Listens on **all** available IPs on the specified port |

Use `bind = false` when you want the node to accept connections from both local and external interfaces on the same port.

---

## Port forwarding (NAT traversal)


If your node is behind a home router or corporate firewall, configure 
<a href="https://en.wikipedia.org/wiki/Port_forwarding" target="_blank">port forwarding</a> on the router to redirect 
incoming traffic:

```
External IP:Port  →  Internal IP:Port
e.g. 203.0.113.5:32048  →  192.168.1.10:32048
```

Set `internal_ip` and `internal_port` to the LAN-side values. AnyLog will publish the external address to the blockchain so peers know where to connect.

---

## Connecting to an existing network

When a node starts for the first time, it needs to pull the current metadata from the network:

```anylog
blockchain pull to json [ip:port]
```

Where `[ip:port]` is any existing member node. This syncs the local blockchain file and lets the node discover all peers.

Then start the blockchain sync service to keep the local copy updated automatically:

```anylog
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node
```

---

## Switching networks

A node can be associated with different network configurations — useful for switching between testnet and mainnet, or different deployments on the same machine:

```anylog
blockchain switch network where master = [IP:Port]
```

To associate a node with a different root directory:
```anylog
set anylog root [path]
```

---

## Testing connectivity

After configuring the network services, validate connectivity:

```anylog
get connections         # confirm listening IPs and ports
test node               # validate local TCP and REST services
test network            # ping all nodes published on the metadata layer
```

Target a specific peer:
```anylog
test node 10.0.0.78:32048
run client 10.0.0.78:32048 get status
```

See <a href="{{ '/docs/Reference/troubleshooting' | relative_url }}">CLI — test node and test network</a> for full details.

---

## Overlay networks

For deployments where nodes are on isolated networks or across cloud providers, an overlay network creates a virtual 
private network across all nodes. AnyLog supports <a href="https://github.com/slackhq/nebula" target="_blank">Nebula</a> 
as an overlay layer.

In an overlay setup:
- Each node is assigned a virtual overlay IP (e.g. `192.168.100.x`)
- AnyLog's `internal_ip` is set to the overlay IP
- Peer communication travels over the encrypted overlay tunnel

```anylog
<run tcp server where
  external_ip = !overlay_ip and external_port = 32048 and
  internal_ip = !overlay_ip and internal_port = 32048 and
  bind = false and threads = 6>
```

---

## Common port assignments

By convention, AnyLog deployments use the following port ranges:

| Service | Default port range |
|---|---|
| TCP (peer messaging) | 32048, 32148, 32248, … |
| REST (external API) | 32049, 32149, 32249, … |
| Message broker (MQTT) | 32550 |

Ports are fully configurable — the convention exists to make multi-node deployments on the same host easier to manage.

---

## Configuring via environment variables

When using Docker or deployment scripts, network settings are typically passed as environment variables:

```env
ANYLOG_SERVER_PORT=32048
ANYLOG_REST_PORT=32049
ANYLOG_BROKER_PORT=32550
OVERLAY_IP=192.168.100.5
```

These are mapped to dictionary keys and referenced in the node's startup script:

```anylog
run tcp server where external_ip = !ip and external_port = !anylog_server_port and threads = 6
run rest server where external_ip = !ip and external_port = !anylog_rest_port and timeout = 20
```

See <a href="{{ '/docs/Getting-Started/deployment-scripts/' | relative_url }}">Deployment Scripts</a> for the full configuration workflow.