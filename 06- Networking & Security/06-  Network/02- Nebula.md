---
title: "Nebula"
description: What Nebula is, why we use it as AnyLog's example overlay network, and how to deploy it as a lighthouse or host.
layout: page
visibility: public
tags:
- networking
- security
- nebula
- third-party
---

<!---
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-13 |  | created document | 2.0.2606 |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Split from the general overlay-networking concept doc (now
   **<a href="01-%20Intro%20Overlay%20Network.md" target="_blank">Overlay Networking</a>**) — this file is Nebula-specific. Kept the Docker-based
   deployment (via `oshadmon/nebula-anylog`) as the primary how-to, since it's the current, actively-maintained
   approach. A second, older raw-binary/manual method exists ("04 Nebula Configuration.md" — `wget` the Nebula
   binary directly, hand-edit YAML, run inside `screen`) but predates the Docker workflow and looks superseded;
   summarized rather than reproduced in full, flagged for a decision on whether to keep, update, or retire it.
--->

<a href="https://github.com/slackhq/nebula" target="_blank">Nebula</a> is a mutually authenticated peer-to-peer overlay network, originally
built for Slack and now managed by <a href="https://www.defined.net/" target="_blank">Defined</a>, based on the
<a href="https://noiseprotocol.org/" target="_blank">Noise Protocol Framework</a>. Nodes use certificates — not shared secrets — to assert
their IP address, name, and membership in user-defined groups. It's the overlay technology we use as a working
example for AnyLog deployments; see **<a href="01-%20Intro%20Overlay%20Network.md" target="_blank">Overlay Networking</a>** for the general concept
this fits into.

**Documentation:** <a href="https://github.com/slackhq/nebula" target="_blank">GitHub</a> · <a href="https://nebula.defined.net/docs" target="_blank">Docs</a> ·
<a href="https://www.defined.net/" target="_blank">Defined's website</a>

---

## Why Nebula as the Example Overlay

- **Certificate-based trust, not shared secrets.** Every node authenticates using a signed certificate rather than a
  shared VPN key, so onboarding a new node is just signing and distributing a cert — a good match for AnyLog's
  config-driven, largely automated deployment model.
- **No dedicated VPN server or centralized relay.** Once nodes discover each other through the lighthouse, traffic
  flows directly between them (often through NAT hole-punching), rather than through a single choke point that has
  to scale with the whole network.
- **Lightweight enough for edge hardware.** Nebula runs as a single small binary with modest resource needs, which
  matters for nodes deployed on gateways, industrial computers, or other constrained edge devices rather than
  full servers.
- **Open source and free to self-host**, avoiding licensing costs or vendor lock-in for something as foundational
  as node-to-node connectivity.
- **Runs cleanly in Docker**, matching how AnyLog itself is deployed — Nebula becomes just another container in the
  same docker-compose stack rather than a separate piece of infrastructure to manage.

None of this makes Nebula a requirement — it's presented as a working example of the pattern, and any overlay
technology that gives nodes a stable, authenticated address to reach each other by would satisfy the same need.

## Terminology

Nebula's overlay requires a minimum of two node types, plus certificates to associate them:

* **Lighthouse** — a Nebula node responsible for discovery: other nodes register with it and query it. When Node A
  wants to reach Node B, it asks the lighthouse "where is 10.10.1.5 right now?" and gets back B's real, routable
  location. Once discovered, traffic between A and B flows directly — the lighthouse is a directory service, not a
  relay sitting in the data path.

  > Relying on a single lighthouse creates a single point of failure for *discovery* specifically (existing tunnels
  > keep working, but new nodes can't join and existing nodes can't find new peers if it goes down). Nebula
  > supports <a href="https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses" target="_blank">multiple lighthouses</a>
  > to eliminate this. **Note:** this is a Nebula capability in theory, not something we've applied in an AnyLog
  > deployment — treat it as a known option to investigate if single-lighthouse availability becomes a real
  > concern, not as a documented, ready-to-use path today.

* **Host** — any other node in the mesh (server, laptop, container, etc.). Each host has its own signed certificate
  and private key, used to prove its identity when establishing tunnels with peers. A host doesn't perform
  discovery for anyone else — it registers with the lighthouse(s) and queries them to find other hosts.

* **Certificate Authority (CA)** — two files: a CA certificate (distributed to and trusted by every host) and its
  private key (never distributed; can be kept offline except when signing new hosts in). See
  **<a href="./02-1%20Nebula%20Certifications.md" target="_blank">Certificate Authority</a>** for why this is a separate concern from the
  lighthouse, and how to handle the CA key more safely than this doc's own quick-start default.

### Where Should the Lighthouse Live?

Should the lighthouse be one of the actual EDF nodes (an operator or query node doing double duty), or a separate,
dedicated instance that exists purely to run Nebula?

**Running it as a separate, dedicated instance is the better default:**

- **Decoupled lifecycle** — if the lighthouse is also a working EDF node, restarting or troubleshooting that node's
  AnyLog software risks taking discovery down for the entire mesh, even though the two concerns are unrelated.
- **Smaller blast radius** — a dedicated lighthouse can be minimal and purpose-built, with less attack surface than
  a full node also handling operational data, queries, or blockchain sync.
- **Clarity of role** — a node that's "just a lighthouse" is unambiguous. A node that's both an active operator
  *and* the mesh's discovery service makes failures harder to reason about — is the problem AnyLog, or the overlay?
- **Matches AnyLog's own recommendation** to use a generic/sandbox node for exactly this kind of lightweight,
  non-critical-path role, rather than a production operator, query, or master node.

The tradeoff is one more machine (or container) to run, even if it's doing very little most of the time. For small
or test deployments, running the lighthouse on an existing node is fine — just know it's coupling two independent
concerns for convenience.

---

## Setting up Nebula (Docker-based)

Using the <a href="https://github.com/oshadmon/nebula-anylog" target="_blank">`oshadmon/nebula-anylog`</a> repo, deployment splits by role.

### Lighthouse

**1. Prep** (same for lighthouse or host):
```bash
git clone https://github.com/oshadmon/nebula-anylog
cd nebula-anylog

sudo mkdir -p /var/bin/nebula/configs
sudo chown -R root:root /var/bin/nebula
sudo chmod -R 755 /var/bin/nebula

sudo modprobe tun
ls -l /dev/net/tun   # confirm it exists
```

**2. Configure `nebula_configs.env`:**
```env
IS_LIGHTHOUSE=true
CIDR_OVERLAY_ADDRESS=10.10.1.1/24
LIGHTHOUSE_IP=10.10.1.1
LIGHTHOUSE_NODE_IP=<this machine's real, reachable IP>
OVERLAY_IP=10.10.1.1
```

If `/var/bin/nebula/configs` is empty, first boot auto-generates a fresh CA (`ca.crt`/`ca.key`) and a signed
lighthouse cert (`lighthouse.crt`/`lighthouse.key`) — this becomes the trust root for this mesh.

**3. Start it:**
```bash
docker compose up -d
docker logs -f nebula
```

Success looks like:
```
time="..." level=info msg="Nebula interface is active" boringcrypto=false build=1.8.2 interface=nebula1 network=10.10.1.1/24 udpAddr="0.0.0.0:4242"
```

**4. Verify:**
```bash
ip addr show nebula1   # native Linux Docker shows this immediately
```

**5. Sign a host certificate** (needed before any host can join) — run on the lighthouse:
```bash
docker exec -it nebula ./nebula-cert sign -name "host" -ip "10.10.1.2/24" \
  -ca-key "/app/nebula/configs/ca.key" \
  -ca-crt "/app/nebula/configs/ca.crt" \
  -out-crt "/app/nebula/configs/host.crt" \
  -out-key "/app/nebula/configs/host.key" \
  -groups "anylog-node"
```

### Deploying as a Host ("Node")

**1. Same prep as above**, on the host machine, then copy `ca.crt`, `host.crt`, `host.key` into
`/var/bin/nebula/configs` on this machine (from the lighthouse, step 5 above).

**2. Configure `nebula_configs.env`:**
```env
IS_LIGHTHOUSE=false
CIDR_OVERLAY_ADDRESS=10.10.1.2/24
LIGHTHOUSE_IP=10.10.1.1
LIGHTHOUSE_NODE_IP=<lighthouse's real, reachable IP>
OVERLAY_IP=10.10.1.2
```

`LIGHTHOUSE_NODE_IP` must be an address this machine can actually route to over UDP/4242 — a WSL2-internal NAT IP
(e.g. `172.x.x.x`) won't work from a separate machine; use the lighthouse host's real LAN/public IP, with
port-forwarding if it's behind WSL2 NAT.

**3. Start and verify:**
```bash
docker compose up -d
docker logs -f nebula
ip addr show nebula1
```

**4. Wire the AnyLog container into the overlay** — in the AnyLog service's own compose file:
```yaml
network_mode: "container:nebula"
```

This makes the AnyLog container share Nebula's network namespace directly, so `nebula1` becomes visible to it —
confirm with `get nics list`. Then set the node config's `NIC_TYPE` to `nebula1` so AnyLog binds/advertises on the
overlay interface rather than its default `eth0`. See
**<a href="../02-%20Network%20Processing.md" target="_blank">Network Processing</a>** for the full `NIC_TYPE`/binding reference — this is just the
overlay-specific value to set once Nebula is running.

**Gotcha:** `network_mode: "container:nebula"` is incompatible with `extra_hosts` (e.g.
`host.docker.internal:host-gateway`) in the same service — Docker will reject the compose file with `conflicting
options: custom host-to-IP mapping and the network mode`. Remove `extra_hosts` from any service using
`network_mode: container:*`.

---

## Manual / Bare-Metal Alternative (Legacy)

A separate, older raw-binary method exists for deploying Nebula without Docker: downloading the `nebula`/`nebula-cert`
binaries directly, generating CA/host certificates by hand, editing the stock `config.yml` YAML for lighthouse vs.
host roles, and running the process inside a detached `screen` session on each machine.

This predates the Docker-based `oshadmon/nebula-anylog` workflow above and appears to be superseded by it — but it
hasn't been formally retired. If bare-metal (non-Docker) Nebula deployment is still a real use case, this method is
worth updating and keeping as a documented alternative; otherwise it's a candidate for removal. Flagging for a
decision rather than silently dropping ~400 lines of working instructions.