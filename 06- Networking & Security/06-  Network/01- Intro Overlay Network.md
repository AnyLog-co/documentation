---
title: "Overlay Networking"
description: What an overlay network is, why AnyLog uses Nebula as a worked example, how it differs from a reverse proxy like NGINX, and how OVERLAY_IP/NIC_TYPE/binding tie an overlay into AnyLog's own networking.
layout: page
visibility: public
version: open source
tags:
- networking
- security
- nebula
- third-party
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-13 |  | created document | 2.0.2606 |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Created as a general "what and why" companion to the Nebula-specific how-to doc.
   Pulled the conceptual framing from "03 overlay-network.md" and the AnyLog-integration mechanics (OVERLAY_IP,
   binding, policy examples) from "03 Configuring Overlay with AnyLog.md" — resolving that file's unresolved git
   merge conflict on its "Installing Nebula" link by pointing at the new Nebula doc directly. Fixed typos
   ("onto of" → "on top of," "Defines'" → "Defined's," "modifoed" → "modified," "phyical"/"addrress"/"aaddress" →
   "physical"/"address," a duplicated "without overlay" label that should have read "with overlay"). Anonymized
   the real public IP (`172.105.4.104`) used throughout the connection examples.
 | 2026-07-25 | Ori Shadmon | Added a "Not the same as a reverse proxy" section distinguishing overlay networking
   from NGINX (also documented in this section) — the two solve related but different reachability problems, and
   nothing previously here explained when to reach for which. Matched frontmatter (`visibility`, `version`,
   `tags`) to the Nebula/NGINX docs' convention now that this page sits alongside them as an index.
--->

An overlay network is a virtual network built on top of an existing physical network, allowing logical communication 
channels and connections between devices that may be geographically dispersed or belong to separate physical 
networks.

From an AnyLog / EdgeLake perspective, overlay networks are valuable because they allow remote connectivity between 
nodes without exposing the broader infrastructure network those nodes are part of.

**A general networking note, independent of any specific node's config:** overlay networks like Nebula still rely on 
ordinary IP networking underneath — they don't bypass firewalls, they tunnel through them. Nebula's peer-to-peer 
traffic uses UDP, and by default on port `4242`. Whatever network the lighthouse and hosts sit on, that port needs to 
be open (or forwarded, in NAT'd setups) between the machines that need to discover and reach each other — otherwise 
the overlay has no path to establish tunnels in the first place, regardless of how the AnyLog-side config is set.

For a concrete, worked example, see **[Nebula](G-%20Nebula.md)** — the overlay technology we use for testing and
demos. Nothing below is Nebula-specific; it applies to whatever overlay technology sits underneath.

---

## Not the Same as a Reverse Proxy

This doc set also covers **[NGINX](03-%20NGINX.md)**, which solves a related but genuinely different problem —
worth being clear on which one you actually need:

* **Overlay networking (Nebula)** solves cross-network reachability: nodes on *separate physical networks or
  locations* need to discover and securely reach each other, as if they were on one LAN. It's a mesh — every
  member gets a stable, authenticated address, and traffic between any two members can flow directly.
* **NGINX (reverse proxy)** solves address *instability within a single deployment* — specifically, Kubernetes
  assigning a new virtual IP to a pod every time it's redeployed. NGINX sits in front and gives callers one static
  address to hit, forwarding to whatever the pod's current address happens to be. It doesn't connect separate
  networks together; it just hides churn on one side of a single connection.

They're not mutually exclusive — a node could sit behind an NGINX proxy for local stability *and* be a member of a
Nebula mesh for cross-location reachability, addressing two different problems at once. But reach for NGINX only if
your actual pain point is "my pod's IP keeps changing," and reach for an overlay only if it's "these nodes are on
different networks entirely." Using the wrong one won't solve the other problem.

---

## How AnyLog Integrates with an Overlay

AnyLog doesn't run the overlay itself — it just needs to know to use the overlay's IP address instead of its
default local/internal one when advertising itself to the network.

### Manual deployment

When manually starting a network service (TCP, REST, or Message Broker), replace the `internal_ip` value with the
overlay IP instead of the local IP (`!ip`):

**Without overlay IP:**
```anylog
anylog_server_port = 32048
tcp_bind = false
threads = 3
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
```

**With overlay IP:**
```anylog
anylog_server_port = 32048
tcp_bind = false
threads = 3
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
```

### Configuration-based deployment

If deploying via the [deployment-scripts](https://github.com/AnyLog-co/deployment-scripts), the overlay IP is used
automatically once configured. In `node_configs.env`:

1. Set **`OVERLAY_IP`** to the physical machine's overlay address.
2. Set **`TCP_BIND`**, **`REST_BIND`**, and **`BROKER_BIND`** to `true`. Otherwise the instance remains reachable
   from *outside* the overlay too. Exception: if a query node needs to talk to a BI tool (PowerBI, Grafana, Looker,
   etc.) that isn't part of the overlay, set that query node's `REST_BIND` to `false` instead.

```dotenv
# --- Networking ---
# By default, a node connects to TCP/REST/Message Broker based on its associated policy.
# If POLICY_BASED_NETWORKING=false, network connectivity is based on this config file directly instead.
#
# For policy-based configuration:
#   1. TCP connectivity can be set to bind or not. If bind is enabled, AnyLog uses either the local or overlay IP
#      (overlay, if one is declared, replaces the local IP). If binding is disabled, the blockchain records both
#      the external and local/overlay IPs of the machine.
#   2. REST and Message Broker default to bind=false, since incoming GET/data requests may come from machines or
#      devices outside the network entirely.
#   3. AnyLog's networking only cares about the policy keys `ip`, `local_ip`, and port values — other fields like
#      `proxy_ip` and `external_ip` (when binding is true) are informational only.

POLICY_BASED_NETWORKING=true
#CONFIG_POLICY_NAME=<NETWORKING_CONFIG_POLICY_NAME>
#EXTERNAL_IP=<NETWORKING_EXTERNAL_IP>
#LOCAL_IP=<NETWORKING_LOCAL_IP>
OVERLAY_IP=192.168.100.1
#PROXY_IP=<NETWORKING_PROXY_IP>
ANYLOG_SERVER_PORT=32048
ANYLOG_REST_PORT=32049
#ANYLOG_BROKER_PORT=<NETWORKING_ANYLOG_BROKER_PORT>
TCP_BIND=true
TCP_THREADS=6
REST_BIND=true
REST_TIMEOUT=20
REST_THREADS=6
REST_SSL=False
BROKER_BIND=false
BROKER_THREADS=6
```

Redeploy after making these changes.

---

## What Changes in the Policies

Because AnyLog uses variable names (`!ip`, `!overlay_ip`) rather than hard-coded values internally, re-deploying
with an overlay IP set changes what gets published to the blockchain — without touching anything else in the
node's configuration.

**Without `OVERLAY_IP` set:**
```json
{"config" : {
    "name" : "anylog-master-config",
    "company" : "New Company",
    "ip" : "!ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int"
  }
}
{"master" : {
    "name": "anylog-master",
    "company": "New Company",
    "hostname": "anylog-master",
    "loc": "43.6496,-79.3833",
    "country": "CA",
    "state": "Ontario",
    "city": "Toronto",
    "port": 32048,
    "ip": "10.0.0.101",
    "rest_port": 32049
  }
}
```

**With `OVERLAY_IP` set:**
```json
{"config" : {
    "name" : "anylog-master-overlay-config",
    "company" : "New Company",
    "ip" : "!overlay_ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int"
  }
}
{"master" : {
    "name": "anylog-master",
    "company": "New Company",
    "hostname": "anylog-master",
    "loc": "43.6496,-79.3833",
    "country": "CA",
    "state": "Ontario",
    "city": "Toronto",
    "port": 32048,
    "ip": "192.168.100.1",
    "rest_port": 32049
  }
}
```

What changed:
1. The `config` policy's name changed to reflect it's an overlay config (`anylog-master-overlay-config`).
2. Its `ip` field switched from `!ip` to `!overlay_ip`.
3. The `master` policy's actual `ip` value switched from the machine's real address (`10.0.0.101`) to the overlay
   address (`192.168.100.1`).

This is reflected in `get connections`, while all three addresses remain visible in the AnyLog dictionary:

**Without overlay:**
```anylog
AL anylog-master +> get connections 

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |10.0.0.101:32048   |10.0.0.101:32048   |10.0.0.101:32048   |
REST     |10.0.0.101:32049   |10.0.0.101:32049   |10.0.0.101:32049   |
Messaging|Not declared       |Not declared       |Not declared       |
```

**With overlay:**
```anylog
AL anylog-master +> get connections 

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |192.168.100.1:32048|192.168.100.1:32048|192.168.100.1:32048|
REST     |192.168.100.1:32049|192.168.100.1:32049|192.168.100.1:32049|
Messaging|Not declared       |Not declared       |Not declared       |
```

**Viewing all three addresses in the dictionary:**
```anylog
AL anylog-master +> get dictionary ip 

Key                 Value                           
-------------------|-------------------------------|
deploy_local_script|false                          |
external_ip        |                     10.0.0.101| # <-- external IP (autogenerated for the physical network)
ip                 |                     10.0.0.101| # <-- local/internal IP (autogenerated for the physical network)
ledger_ip          |                      127.0.0.1|
local_scripts      |/app/deployment-scripts/scripts|
nosql_ip           |                      127.0.0.1|
overlay_ip         |                  192.168.100.1| # <-- overlay IP (e.g. Nebula)
```

---

## Related

* **[Nebula](G-%20Nebula.md)** — the overlay technology we use for testing and demos, including how to deploy it.
* **[NGINX](03-%20NGINX.md)** — the reverse-proxy approach to a related-but-different problem (see
  "Not the Same as a Reverse Proxy" above).
* **[Network Processing](B-%20Network%20Processing.md)** — `NETWORK_TYPE`, `NIC_TYPE`, and binding in full, including
  how `NIC_TYPE=nebula1` fits alongside `OVERLAY_IP`.