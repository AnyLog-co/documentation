# Overlay Networking

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

## Nebula Overlay Network

Nebula was originally built for Slack and is now managed by Defined. It's relatively straightforward to deploy, and 
its architecture lines up well with how AnyLog agents are typically deployed and communicate.

### Why Nebula as the Example Overlay

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

### Nebula Nodes

* **Lighthouse**: a Nebula node responsible for node discovery within the overlay network. It acts as a static 
reference point that other nodes register with and query — when Node A wants to reach Node B, it asks the lighthouse 
"where is 10.10.1.5 right now?" and the lighthouse returns B's real, routable location. Once discovered, traffic 
between A and B flows directly between them; the lighthouse is a directory service, not a relay sitting in the data 
path.

> Relying on a single lighthouse creates a single point of failure for discovery (existing tunnels keep working, but 
> new nodes can't join and existing nodes can't find new peers if the lighthouse goes down). Nebula supports multiple 
> lighthouses to eliminate this centralization — each lighthouse independently tracks the mesh, and nodes can report 
> to and query from more than one.
>
> **Note:** this is a Nebula capability in theory, not something we've applied in an AnyLog deployment. Treat it as 
> a known option to investigate if single-lighthouse availability becomes a real concern, not as a documented, 
> ready-to-use path today.

* **Host**: A host (sometimes called a regular "node" to distinguish it from the lighthouse) is any other machine 
participating in the mesh — a server, laptop, container, etc. Every host has its own signed certificate and private 
key (see [Certificate Authority](overlay-certificate-authority.md) for how these are issued and trusted), used to 
prove its identity when establishing tunnels with peers. A host doesn't perform discovery for anyone else; it just 
registers itself with the lighthouse(s) and queries them to find other hosts.

### Where Should the Lighthouse Live?

A related design question: should the lighthouse be one of the actual EDF nodes (e.g. an operator or query node doing 
double duty), or a separate, dedicated instance that exists purely to run Nebula?

**Running the lighthouse as a separate, dedicated instance is the better default**, for a few reasons:

- **Decoupled lifecycle.** If the lighthouse is also a working EDF node, restarting, redeploying, or troubleshooting 
  that node's AnyLog software risks taking discovery down for the entire mesh at the same time — even though the two 
  concerns (running AnyLog vs. running Nebula) have nothing to do with each other.
- **Blast radius.** A dedicated lighthouse instance can be minimal and purpose-built, with a smaller attack surface 
  than a full AnyLog node that's also handling operational data, queries, or blockchain sync.
- **Clarity of role.** A node that's "just a lighthouse" is unambiguous in its function. A node that's both an active 
  operator *and* the mesh's discovery service is doing two jobs, and failures become harder to reason about — is the 
  problem the AnyLog service, or the overlay?
- **This is consistent with AnyLog's own recommendation** to use a generic/sandbox node as the lighthouse rather than 
  a production operator, query, or master node — the generic node exists specifically to serve as this kind of 
  lightweight, non-critical-path instance.

The tradeoff is one more machine (or container) to stand up and keep running, even if it's doing very little most of 
the time. For small or test deployments, running the lighthouse on an existing node is fine — just worth knowing 
it's coupling two independent concerns for convenience, the same way `nebula-anylog`'s CA-on-lighthouse default does 
(see [Certificate Authority](overlay-certificate-authority.md)).

---

## Setting up Nebula

Setting up Nebula is almost as simple as deploying docker containers — the process is simply to define configurations 
and deploy if using a lighthouse. The _host_ instances require an additional step of having a certificate key 
provided by the Certificate Authority (see [Certificate Authority](overlay-certificate-authority.md)).

Using the `oshadmon/nebula-anylog` repo, deployment splits into two paths depending on the node's role: lighthouse or 
host.

### Lighthouse
1. Prep (same for lighthouse or host)
```bash
git clone https://github.com/oshadmon/nebula-anylog
cd nebula-anylog

sudo mkdir -p /var/bin/nebula/configs
sudo chown -R root:root /var/bin/nebula
sudo chmod -R 755 /var/bin/nebula

sudo modprobe tun
ls -l /dev/net/tun   # confirm it exists
```

2. Configure `nebula_configs.env`

```env
IS_LIGHTHOUSE=true
CIDR_OVERLAY_ADDRESS=10.10.1.1/24
LIGHTHOUSE_IP=10.10.1.1
LIGHTHOUSE_NODE_IP=<this machine's real, reachable IP>
OVERLAY_IP=10.10.1.1
```

If `/var/bin/nebula/configs` is empty, first boot auto-generates a fresh CA (`ca.crt`/`ca.key`) and a signed 
lighthouse cert (`lighthouse.crt`/`lighthouse.key`) — this becomes the trust root for this mesh (see 
[Certificate Authority](overlay-certificate-authority.md) for the caveats on this default).

3. Start it

```bash
docker compose up -d
docker logs -f nebula
```

**Success looks like**:

```
time="..." level=info msg="Nebula interface is active" boringcrypto=false build=1.8.2 interface=nebula1 network=10.10.1.1/24 udpAddr="0.0.0.0:4242"
```

4. Verify

```bash
ip addr show nebula1   # native Linux Docker shows this immediately
```

5. Sign a host certificate (needed before any host can join)

Run this on the lighthouse:

```bash
docker exec -it nebula ./nebula-cert sign -name "host" -ip "10.10.1.2/24" \
  -ca-key "/app/nebula/configs/ca.key" \
  -ca-crt "/app/nebula/configs/ca.crt" \
  -out-crt "/app/nebula/configs/host.crt" \
  -out-key "/app/nebula/configs/host.key" \
  -groups "anylog-node"
```

### Deploying as a Host ("Node")

1. Same prep as above, on the host machine

```bash
git clone https://github.com/oshadmon/nebula-anylog
cd nebula-anylog

sudo mkdir -p /var/bin/nebula/configs
sudo chown -R root:root /var/bin/nebula
sudo chmod -R 755 /var/bin/nebula
sudo modprobe tun
```

Copy `ca.crt`, `host.crt`, `host.key` into `/var/bin/nebula/configs` on this machine (from the lighthouse, step 5 
above).

2. Configure `nebula_configs.env`

```env
IS_LIGHTHOUSE=false
CIDR_OVERLAY_ADDRESS=10.10.1.2/24
LIGHTHOUSE_IP=10.10.1.1
LIGHTHOUSE_NODE_IP=<lighthouse's real, reachable IP>
OVERLAY_IP=10.10.1.2
```

`LIGHTHOUSE_NODE_IP` must be an address this machine can actually route to over UDP/4242 — a WSL2-internal NAT IP 
(e.g. `172.x.x.x`) won't work from a separate machine; use the real LAN/public IP of the lighthouse's host, with 
port-forwarding if the lighthouse is behind WSL2 NAT.

3. Start and verify

```bash
docker compose up -d
docker logs -f nebula
ip addr show nebula1
```

4. Wire the AnyLog container into the overlay

In the AnyLog service's own compose file:

```yaml
network_mode: "container:nebula"
```

This makes the AnyLog container share Nebula's network namespace directly, so `nebula1` becomes visible to it — 
confirm with `get nics list`. Then set the node config's `NIC_TYPE` to `nebula1` so AnyLog binds/advertises on the 
overlay interface rather than its default `eth0`. `NIC_TYPE`, `OVERLAY_IP`, and binding are covered in full in 
[AnyLog Networking](networking.md) — this is simply the overlay-specific value to set once Nebula is running.

**Gotcha:** `network_mode: "container:nebula"` is incompatible with `extra_hosts` (e.g. 
`host.docker.internal:host-gateway`) in the same service — Docker will reject the compose file with `conflicting 
options: custom host-to-IP mapping and the network mode`. Remove `extra_hosts` from any service using 
`network_mode: container:*`.