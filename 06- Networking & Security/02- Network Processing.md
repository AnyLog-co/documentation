---
title: "Network Processing"
description: How AnyLog nodes exchange REST and TCP messages, the three network services, and how NETWORK_TYPE/NIC_TYPE/binding determine whether a node is actually reachable in the network.
layout: page
source_path: "01 Network Exchanges.md"
---
<!---
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Fixed grammar throughout (subject/verb agreement, "srvice" typo, the garbled
   "allowing to manage" and "can reside as one of the EDF" sentences, inconsistent spacing/capitalization).
   Filled in the previously-empty [message broker] link, since the actual doc's location is now known.
   Cross-linked the default port table (Master/Operator/Query/Publisher/Generic) from the Networking & Security
   intro doc, since this document only shows bracketed placeholders. Added a table of contents given the length.
   Left the Edge Data Fabric section's content as-is (it reads as already-polished) — flagging that it may
   duplicate ground already covered in the Introduction to AnyLog doc; worth a check for overlap rather than
   something I'm resolving here.
--->

# Network Processing

## Contents

1. <a href="#overview" target="_blank">Overview</a>
2. <a href="#edge-data-fabric-a-quick-explanation" target="_blank">Edge Data Fabric: A Quick Explanation</a>
3. <a href="#network-services" target="_blank">Network Services</a>
4. <a href="#network-types--binding" target="_blank">Network Types & Binding</a>
5. <a href="#binding" target="_blank">Binding</a>
6. <a href="#configuring-it" target="_blank">Configuring It</a>

## Overview

Networking is a critical component of AnyLog — it's the part that connects agents together to form the Edge Data
Fabric (EDF), the network layer of the product.

When setting up new AnyLog instances to join the EDF, choosing the correct internal/external network interface (NIC)
is critical.

Equally important is deciding how reachable each agent should be to other instances in the network. While the NIC
determines the IP address an instance identifies itself by, binding determines how other AnyLog instances can
actually connect to it — whether it listens on one specific address, or on all available interfaces.

AnyLog is a peer-to-peer (P2P) network of nodes that facilitates data management across distributed nodes. These
nodes appear to users and applications as a single machine. This document describes the low-level networking
configurations and operations that make that possible — combined with a shared metadata layer, they let the
network's nodes and the data they host appear as a single machine managing one unified collection of data.

The AnyLog Network Protocol deploys 2 layers of messaging:

* **Messages between users/applications and the network.** These are REST-based ("REST messages"), delivered to
  one node in the network. When a REST message arrives, the AnyLog protocol on that node transforms it into a TCP
  message (see <a href="#network-services" target="_blank">Network Services</a> below) and delivers it to the proper nodes; if a reply is
  needed, it's returned to the user or application over that same REST connection.

* **Messages between nodes that are members of the network.** A member node is any instance running the AnyLog
  software. These are TCP-based ("TCP messages"), using the AnyLog messaging protocol to communicate between
  instances. TCP messages support two kinds of functionality:
  1. **Maintaining the network itself** — transparent to users and applications, these messages manage the
     network and its processes. Examples: heartbeat messages, metadata sync messages, recovery messages.
  2. **User messages** — supporting user and application requests. Users can log into a node and message any
     available peer directly, or issue REST requests that get translated into a message exchange between nodes.
     Examples: querying data, querying metadata, retrieving node status, copying data.

## Edge Data Fabric: A Quick Explanation

The Edge Data Fabric (EDF) is our proprietary name for the architecture connecting nodes on the AnyLog network.

Rather than pulling operational data into a central repository, EDF leaves that data where it's generated — on each
node — and instead virtualizes access to it, so applications, administrators, and AI tools all see one coherent
environment rather than a collection of disconnected machines. This virtualization happens through three layers:

- **Virtual Data Lake** — lets applications query distributed data across nodes using standard SQL, without needing
  to know which node actually holds the data.
- **Unified Namespace(s)** — presents industrial assets and their relationships as logical objects, independent of
  which physical database they're stored in. Multiple namespaces can coexist for different operational views over
  the same underlying data.
- **Single System Image** — gives administrators one operational view across every node, regardless of physical
  location, rather than requiring them to manage each machine independently.

All three are coordinated by the **Distributed Metadata Layer** — the shared "index" that tracks which nodes exist,
what data each one holds, what services are available, and what security policies apply. This is the layer that
lets a query submitted anywhere in the network get routed to the right node(s) automatically, and lets new nodes
become discoverable as soon as they join.

Note: EdgeLake and AnyLog nodes can coexist within the same EDF.

**Why this matters for networking specifically:** every one of these virtualization layers depends on nodes being
able to actually reach each other over the network. A Virtual Data Lake query can't route to the node that holds
the data if that node isn't reachable at the address it's advertising; a Single System Image can't show an
administrator a node's status if metadata from that node never arrives. This is exactly the layer this document is
about — `NETWORK_TYPE`, `NIC_TYPE`, and binding determine whether a node is actually a reachable participant in the
EDF, or just an isolated machine that happens to run the software.

## Network Services

AnyLog uses 3 major ports for communication between nodes. These ports are defined in both the config policy and
node policy. For the default ports assigned per node type (Master, Operator, Query, Publisher, Generic), see
<a href="./01-%20Networking%20&%20Security.md" target="_blank">Intro to Networking and Security</a> — the examples below use
bracketed placeholders since the actual values depend on your deployment.

### TCP Service

The TCP service is used to communicate between nodes on the network. It's probably the most critical of the three,
since it's what allows a node to actually be part of the network. This port is used to transfer:
1. A copy of the blockchain when doing `blockchain sync`
2. A request and response when executing `run client ()`
3. File/data transfer from a Publisher to an Operator node, or a query response between the Query node and an Operator

```anylog
<run tcp server where 
    external_ip = [ip] and external_port = [port] and 
    internal_ip = [local_ip] and internal_port = [local_port] and 
    bind = [true/false] and threads = [threads count]>
```

Sets a TCP server listening on the specified IP and port. The first IP/port pair is used by the listener process to
receive messages from members of the network. The second (optional) pair indicates the IP and port accessible from
a local network. `threads` is optional — the number of worker threads processing requests sent to the given
IP/port; default is `6`.

### REST Service

The REST service is the one most commonly used by end users. It's where applications send requests to the network
from a single point and get a reply — either from a specific node, or without needing to know where the data
actually resides.

```anylog
<run rest server where 
    external_ip = [external_ip ip] and external_port = [external port] and 
    internal_ip = [internal ip] and internal_port = [internal port] and 
    timeout = [timeout] and ssl = [true/false] and bind = [true/false]>
```

Enables a REST service listening on the specified IP and port. `timeout` is the max wait time in seconds — `0`
means no wait limit; default is `20` seconds. If `ssl` is set to `true`, the connection uses HTTPS.

### Broker Service

The Broker service port is a TCP-based connection that acts as AnyLog's built-in <a href="./05-%20Message%20Broker.md" target="_blank">message broker</a>.
This port can accept data from different sources (e.g. Kafka, MQTT, Modbus) from a single point, and understands
how to interpret it based on a correlating message client service.

```anylog
<run message broker where 
    external_ip = [ip] and external_port = [port] and 
    internal_ip = [local_ip] and internal_port = [local_port] and 
    bind = [true/false] and threads = [threads count]>
```

## Network Types & Binding

Getting a node reachable in the EDF is really two separate questions, each controlled by its own setting: where does
the container itself sit on the network (`NETWORK_TYPE`), and which of the container's interfaces does the agent
identify itself by (`NIC_TYPE`)? Binding then determines how exposed that identified address is to incoming
connections. The three subsections below walk through each in turn.

### `NETWORK_TYPE` — where the container sits

By default, Docker places a container on its own isolated bridge network — reachable only from the Docker host
itself, not from other physical machines on the same subnet. For an AnyLog agent to actually participate in the
EDF, it needs to reside on an address that other physical machines can reach directly, not an address trapped
inside Docker's internal networking.

`NETWORK_TYPE` controls how the container opts out of that isolation:

| Value | Behavior |
|---|---|
| `""` (empty) | Auto-detect: `host` mode on Linux/WSL, port-mapped on Windows/macOS |
| `network` | Force `network_mode: host` (Linux/WSL only) |
| `ports` | Force explicit port-mapped mode (Windows, macOS, or Linux) |
| `<custom-name>` | Attach to a pre-existing external Docker network (`external: true`) — the user must define this network themselves beforehand |

A custom overlay network (e.g. Nebula) is one instance of the `<custom-name>` case — see
<a href="06-%20%20Network/01-%20Intro%20Overlay%20Network.md" target="_blank">Overlay Networking</a> for a full worked example.

### `NIC_TYPE` — which interface identifies this agent

A physical machine may have more than one Network Interface Card. A common edge deployment pattern is one NIC
connected 1:1 to a piece of equipment (e.g. a PLC) and a second NIC (e.g. `eth1`) connected to the router/broader
network. In this situation, AnyLog cannot safely guess which NIC represents the agent's identity to the rest of the
EDF — the user must specify it.

A valid `NIC_TYPE` must satisfy two conditions:

1. **It's reachable via Docker** — i.e., it's actually exposed given the `NETWORK_TYPE` chosen above. A NIC that
   Docker can't see is not a usable choice, regardless of whether it exists on the host machine.
2. **It has an IP (internal or external) that other nodes in the network can reach.** A NIC connected only to a
   private point-to-point link (e.g. edge device ↔ PLC) has no path to the rest of the EDF and is not a valid
   choice, even if Docker can see it.

`NIC_TYPE` is what ends up published as the agent's `local_ip` — the address other AnyLog instances use to route
requests back to it. Choosing the wrong NIC doesn't cause a startup failure; it causes the agent to advertise an
address nobody else can actually use.

If the agent is joined to an overlay network, `NIC_TYPE` is typically set to the overlay's virtual interface (e.g.
`nebula1`) rather than a physical NIC — see <a href="06-%20%20Network/01-%20Intro%20Overlay%20Network.md" target="_blank">Overlay Networking</a> for how that interface
gets created.

**`NIC_TYPE` vs. `OVERLAY_IP`:** with only `bind=true`/`false` available today, `OVERLAY_IP` doesn't add much beyond
what `NIC_TYPE=nebula1` already gives you — the NIC already resolves to the overlay address. `OVERLAY_IP` becomes
genuinely useful once `bind=explicit` exists (see <a href="#binding" target="_blank">Binding</a> below): that's the field that would let an
agent bind to its internal IP *and* its overlay IP together, rather than being restricted to `NIC_TYPE`'s single
address.

### Binding

Once `NIC_TYPE` determines *which* address the agent identifies as, binding (`TCP_BIND`, `REST_BIND`, `BROKER_BIND`)
determines *how exposed* that address actually is to incoming connections.

- **`bind=false`** — the agent listens on all IPs available to it. `get connections` reports this as `0.0.0.0:[PORT]`
  under Bind Address.
- **`bind=true`** — the agent listens on exactly one specific IP, based on `NIC_TYPE` (almost always the internal
  address).

**Choosing between them:**

Use `bind=false` for nodes that need to be reachable broadly — a sandbox/generic node, where restricting access
isn't the goal.

Use `bind=true` for nodes that should be reachable only from a single, known network path — e.g. a production node
that should never be reachable from outside its local LAN.

**Pending: `bind=explicit`.** Today there's no middle ground between "one address" and "all addresses" — you can't
bind to, say, the internal IP and the overlay IP while excluding the external IP. A `bind=explicit` mode covering
this case is proposed but not yet implemented. This section will be updated with usage details once it ships.

## Configuring It

Putting the above together, a node's advanced configs would include:

```env
#--- Networking ---
NETWORK_TYPE=""          # empty = auto-detect; "network" or "ports" to force a mode
NIC_TYPE=""              # e.g. eth0, eth1 — required if the machine has multiple NICs
OVERLAY_IP=""            # set only if using an overlay network (see Overlay Networking doc)

#--- Bind Settings ---
TCP_BIND=true
REST_BIND=false
BROKER_BIND=false
```

Which combination is correct depends entirely on the two questions this document covers: which NIC represents this
agent to the rest of the EDF, and how exposed that address should be to other participants.