---
title: "Intro to Networking and Security"
description: How AnyLog nodes select IPs/ports, the default port scheme per node type, and the layered security options available.
layout: page
source_path: ""
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-25 | Ori Shadmon | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Fixed grammar throughout (subject/verb agreement, the garbled "work simpleness"
   sentence, "complimentary" → "complementary"). Clarified the NIC/overlay explanation. Fixed a logical
   inconsistency in the Security list — username/password was labeled "the least secure" option, which
   contradicts the list's own first entry (no authentication is trivially less secure than any credential).
 | 2026-07-25 | Ori Shadmon | Rewrote the Networking and Security sections now that the two deep-dive docs
   (Network Processing, Securing the Network) actually exist to check against, rather than guessing at what
   they'd cover. Networking section now links to Network Processing directly instead of only listing default
   ports. Security section rewritten to match what Securing the Network actually documents — three real
   mechanisms (overlay network, key-based node/user authentication, certificate-based auth for third-party
   apps) plus a distinct "local password" concept (protects a node's stored private key at rest) that the old
   version didn't mention at all. Flagged the unconfirmed "TPM" bullet rather than deleting or restating it.
 | 2026-07-25 | Ori Shadmon | Confirmed TPM is real, current, and documented at software%20tpm.md (fetched
   directly). It's a software-emulated TPM (`swtpm` + a REST API, via the AnyLog-TPM project) that optionally
   backs node keys for the existing key-based authentication mechanism — not a separate 4th mechanism, and not
   hardware-backed by default despite the name (the doc's own operational notes say so explicitly). Folded
   this into the key-based authentication bullet and added it to See also, replacing the earlier "to verify"
   callout now that it's been checked against source.
--->

At its core, AnyLog allows distributed data to be accessible from a single point.

To accomplish this, network accessibility and security are just as critical as database access.

## Networking

Network configuration is critical within AnyLog: nodes must have their ports open to the rest of the network's
nodes in order to communicate at all.

The way AnyLog selects its IPs and ports is based on the NIC type a user specifies — meaning AnyLog works with
both standard network interfaces (e.g. `eth0`) and overlay interfaces (e.g. `nebula1`, from the Nebula overlay
network).

Finally, when deploying a node, the default ports are as follows:

| Node Type | TCP Port | REST Port | Broker Port |
| :---: | :---: | :---: | :---: |
| Master | 32048 | 32049 | |
| Operator | 32148 | 32149 | 32150 |
| Query | 32348 | 32349 | |
| Publisher | 32248 | 32249 | 32250 |
| Generic (Sandbox) | 32548 | 32549 | 32550 |

> **Worth confirming:** the port scheme increments by 100 per node type (Master `0xx` → Operator `1xx` → Publisher
> `2xx` → Query `3xx` → Generic `5xx`), but `4xx` doesn't appear for any node type in this table. Worth checking
> whether that range is reserved for a node type not covered here, or simply unused.

For the full picture — how these ports are actually used (TCP/REST/Broker services), and how `NETWORK_TYPE`,
`NIC_TYPE`, and binding determine whether a node is actually reachable — see **Network Processing**.

## Security

AnyLog secures the network through three real mechanisms, which can be combined:

* **Overlay network** — a third-party overlay (e.g. <a href="https://nebula.defined.net/docs/" target="_blank">Nebula</a>) that authorizes
  which nodes can participate, gives each member a stable IP:port identity, resolves routing issues, and encrypts
  messaging between members. Configured via the third-party vendor's own tooling, not AnyLog directly.
* **Key-based authentication (node/user)** — each node or user is assigned a private/public key pair. Messages are
  signed with the private key; the receiving peer authenticates the sender with the public key, then checks that
  sender's permissions against the network's policies before processing the message. Node keys can optionally be
  backed by a **software TPM** (`swtpm` + a REST API, via the <a href="https://github.com/royshadmon/AnyLog-TPM" target="_blank">`AnyLog-TPM`</a>
  project) rather than stored as plain files — configured with `tpm set`, `tpm enabled = on`, and
  `tpm set node key password`. Despite the name, this is a software emulation, not a physical TPM chip — it doesn't
  provide hardware isolation, per the TPM doc's own operational notes. See **Software TPM for AnyLog** for the full
  setup.
* **Certificate-based authentication (third-party apps)** — AnyLog acts as its own Certificate Authority, issuing
  client certificates so external applications (a REST client, Grafana, etc.) can authenticate the same way a node
  or user would — via a public key tied to a member policy, rather than a raw username/password.

Separately, REST requests can also use plain **username/password** (basic authentication) — the simplest option,
and the one most third-party BI tools default to when they don't support certificates.

A related but distinct concept: each node's own private key is stored locally and protected by a **local password**,
which must be supplied again whenever the node restarts — this protects the key at rest, independent of how that
key is later used to authenticate messages.

See **Securing the Network** for the full mechanics and a worked deployment example (generating keys, defining
member/permission/assignment policies, and testing permitted vs. denied messages across two Operator nodes).

## See also

* **Network Processing** — the TCP/REST/Broker services, and how `NETWORK_TYPE`/`NIC_TYPE`/binding determine
  reachability.
* **Securing the Network** — overlay networks, key-based authentication, and certificate-based authentication for
  third-party applications, in full detail with a worked example.
* **Software TPM for AnyLog** — optional software-emulated TPM backing for node keys (`swtpm` + REST API), as an
  alternative to plain on-disk key storage.
* **Authentication** — SSL certificates and basic (username/password) authentication setup, referenced throughout
  this doc set as `authentication.md`.
* **DNP3 TLS Test Certificates** — generating a local CA chain for TLS testing on DNP3 connections.