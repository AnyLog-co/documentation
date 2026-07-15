---
title: Networking
description: How an AnyLog node determines its identity on the network, how to point it at a specific interface or overlay, and how binding controls reachability.
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
- 2026-07-14 | Created document.
- 2026-07-14 (rev 2) | Grammar/typo pass; removed dangling NETWORK_TYPE reference.
- 2026-07-14 (rev 3) | Condensed into a one-pager: cut the full EDF bullet breakdown down to two
  sentences, merged the three near-identical TCP/REST/Broker syntax blocks into one shared pattern,
  dropped the get nics list sample output and the reply/self-messaging section (kept as a pointer to
  Network Processing instead), and trimmed Binding/Verifying to their essentials.
-->

# Networking

Networking connects AnyLog agents into the Edge Data Fabric (EDF) — a distributed architecture that leaves data at 
the edge while giving applications, admins, and AI tools one coherent view across every node, coordinated by a 
shared metadata layer.

Every agent needs two things configured correctly to actually participate: **which address it identifies as**, and 
**how exposed that address is** to the rest of the network.

## How a connection gets opened

TCP (peer-to-peer between nodes), REST (users/apps/BI tools), and Message Broker (e.g. MQTT, Kafka) all follow the 
same pattern:

```anylog
<run [tcp server|rest server|message broker] where
    external_ip = [ip] and external_port = [port] and
    internal_ip = [local_ip] and internal_port = [local_port] and
    bind = [true/false] and threads = [count]>
```

REST additionally takes `timeout` and `ssl`. When deploying via [deployment-scripts](../09-%20Integrations/deployment-scripts.md), 
this is generated for you from the [configuration policy](../09-%20Integrations/deployment-scripts.md#how-policies-and-scripts-actually-communicate) — 
worth knowing what it does under the hood regardless.

## A node's identity: three IP variables

| Variable | What it is |
|---|---|
| `!ip` | Private/internal IP, resolved from whichever NIC is recognized as default |
| `!external_ip` | The public IP of the router |
| `!overlay_ip` | An additional identity, typically via a secondary NIC (e.g. an overlay network) |

Check what's actually available with `get nics list`. If `!ip` isn't what you expect, AnyLog has picked a different 
default NIC than you intended.

**`NIC_TYPE`** sets `!ip` explicitly — equivalent to running `set internal ip with [interface_name]` (e.g. `nebula1` 
for an overlay interface). A valid choice must be (1) visible to the AnyLog process and (2) hold an IP other nodes 
can actually reach.

**`OVERLAY_IP`** sets `!overlay_ip` as a *second, independent* identity — a node can hold both a LAN identity and an 
overlay identity at once, not one or the other.

## Binding: how exposed is that identity

- **`bind=false`** — listens on every available IP (`0.0.0.0` in `get connections`).
- **`bind=true`** — listens only on the one IP passed as `internal_ip`.

Use `false` for broadly-reachable nodes (sandbox, generic); use `true` to restrict a node to one known path (e.g. 
LAN-only production nodes).

Since `!ip` and `!overlay_ip` are independent, running two separate server processes on the same port — one bound to 
each — gives "reachable via LAN + overlay, not externally" without a third binding mode. This is standard socket 
behavior but hasn't been confirmed against AnyLog's specific implementation; test before relying on it.

## Verifying it

```anylog
get connections                     # active connections + bind state
test node                           # this node's REST/TCP status
run client (host:port) get status   # connectivity to a specific peer
```

## Where to go next

- **[Overlay Networking](../05-%20Networking%20&%20Security/B-%20Networking/overlay-network.md)** — Nebula as a worked example, lighthouse/host roles, certificate trust.
- **[Securing the Network](../05-%20Networking%20&%20Security/Securing%20the%20Network.md)** — key-based node auth, certificate-based auth for third-party apps.
- **[NGINX Configuration](../05-%20Networking%20&%20Security/NGINX%20Configuration.md)** — reverse proxy for static-IP routing.
- **[Network Processing](../05-%20Networking%20&%20Security/Network%20Processing.md)** — message routing, `run client` targeting, reply/self-messaging addresses, the `subset` flag.