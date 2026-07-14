---
title: AnyLog Networking
description: How to choose NETWORK_TYPE and NIC_TYPE, and how binding controls which addresses an AnyLog agent accepts connections from.
layout: page
visibility: public
version: open source
tags:
- networking
- configuration
- getting-started
---
 
<!--
## Changelog
- 2026-07-13 | Created document
-->
# AnyLog Networking

Networking is a critical component of AnyLog, as it's the part that connects agents together to form the Edge Data 
Fabric (EDF) — the network layer of the product.

When setting up new AnyLog instances to join the EDF, choosing the correct internal/external network interface (NIC) 
is critical.

Equally important is deciding how reachable each agent should be to other instances in the network. While the NIC 
determines the IP address an instance identifies itself by, binding determines how other AnyLog instances can 
actually connect to it — whether it listens on one specific address, or on all available interfaces.

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

Note: EdgeLake + AnyLog nodes can reside as one of the EDF.

**Why this matters for networking specifically:** every one of these virtualization layers depends on nodes being 
able to actually reach each other over the network. A Virtual Data Lake query can't route to the node that holds 
the data if that node isn't reachable at the address it's advertising; a Single System Image can't show an 
administrator a node's status if metadata from that node never arrives. This is exactly the layer this document is 
about — NETWORK_TYPE, NIC_TYPE, and binding determine whether a node is actually a reachable participant in the 
EDF, or just an isolated machine that happens to run the software.

## Choosing NETWORK & NIC Type

### `NETWORK_TYPE` — where the container sits

By default, Docker places a container on its own isolated bridge network — reachable only from the Docker host itself, 
not from other physical machines on the same subnet. For an AnyLog agent to actually participate in the EDF, it needs 
to reside on an address that other physical machines can reach directly, not an address trapped inside Docker's 
internal networking.

`NETWORK_TYPE` controls how the container opts out of that isolation:

| Value | Behavior |
|---|---|
| `""` (empty) | Auto-detect: `host` mode on Linux/WSL, port-mapped on Windows/macOS |
| `network` | Force `network_mode: host` (Linux/WSL only) |
| `ports` | Force explicit port-mapped mode (Windows, macOS, or Linux) |
| `<custom-name>` | Attach to a pre-existing external Docker network (`external: true`) — the user must define this network themselves beforehand |

A custom overlay network (e.g. Nebula) is one instance of the `<custom-name>` case — see 
[Overlay Networking](overlay-network.md) for a full worked example.

### `NIC_TYPE` — which interface identifies this agent

A physical machine may have more than one Network Interface Card. A common edge deployment pattern is one NIC 
connected 1:1 to a piece of equipment (e.g. a PLC) and a second NIC (e.g. `eth1`) connected to the router / broader 
network. In this situation, AnyLog cannot safely guess which NIC represents the agent's identity to the rest of the 
EDF — the user must specify it.

A valid `NIC_TYPE` must satisfy two conditions:

1. **It's reachable via Docker** — i.e., it's actually exposed given the `NETWORK_TYPE` chosen above. A NIC that Docker 
   can't see is not a usable choice, regardless of whether it exists on the host machine.
2. **It has an IP (internal or external) that other nodes in the network can reach.** A NIC connected only to a 
   private point-to-point link (e.g. edge device ↔ PLC) has no path to the rest of the EDF and is not a valid choice, 
   even if Docker can see it.

`NIC_TYPE` is what ends up published as the agent's `local_ip` — the address other AnyLog instances use to route 
requests back to it. Choosing the wrong NIC doesn't cause a startup failure; it causes the agent to advertise an 
address nobody else can actually use.

If the agent is joined to an overlay network, `NIC_TYPE` is typically set to the overlay's virtual interface (e.g. 
`nebula1`) rather than a physical NIC — see [Overlay Networking](overlay-network.md) for how that interface gets 
created.

**`NIC_TYPE` vs. `OVERLAY_IP`:** with only `bind=true`/`false` available today, `OVERLAY_IP` doesn't add much beyond 
what `NIC_TYPE=nebula1` already gives you — the NIC already resolves to the overlay address. `OVERLAY_IP` becomes 
genuinely useful once `bind=explicit` exists (see below): that's the field that would let an agent bind to its 
internal IP *and* its overlay IP together, rather than being restricted to `NIC_TYPE`'s single address.

## Binding

Once `NIC_TYPE` determines *which* address the agent identifies as, binding (`TCP_BIND`, `REST_BIND`, `BROKER_BIND`) 
determines *how exposed* that address actually is to incoming connections.

- **`bind=false`** — the agent listens on all IPs available to it. `get connections` reports this as `0.0.0.0:[PORT]` 
  under Bind Address.
- **`bind=true`** — the agent listens on exactly one specific IP, based on `NIC_TYPE` (almost always the internal 
  address).

**Choosing between them**:

Use`bind=false` for nodes that need to be reachable broadly — a sandbox/generic node, where restricting access isn't the goal. 

Use `bind=true` for nodes that should be reachable only from a  single, known network path — e.g. a production node that should never be reachable from outside its local LAN.

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