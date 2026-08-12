---
title: FAQ
description: Frequently asked questions about AnyLog architecture, deployment, networking, data management, querying, and blockchain — organized by topic, with links to full documentation where it already exists.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-23 | Added REST/CORS/AnyLog-Agent, POST vs GET, blockchain insert, mapping policy pitfalls, MCP, Docker networking sections
- 2026-07-14 | Merged in the separate architecture/editions FAQ
- 2026-07-29 | Reorganized around General / Network / Data Management / Query / Blockchain / REST, per the plan to
              make this simpler: short answers + forward links to the dedicated doc wherever one already exists,
              rather than restating full explanations that now live elsewhere. Troubleshooting-only content
              (diagnostic procedure, known error signatures) moved to the standalone Troubleshooting doc, since
              that's a different kind of content (a procedure to run, not a question to answer) — this FAQ now
              links to it rather than duplicating it. Kept full answers only where no single dedicated doc
              exists yet (comparison tables, "why does X happen" explanations specific to this FAQ).
-->

## General

**Q: What's the difference between AnyLog and EdgeLake?**

**EdgeLake** is the open-source version. **AnyLog Enterprise** is the commercial edition, adding: full blockchain
abstraction, aggregations, the security protocol, HA, test suites, training, and technical support.

| Feature | EdgeLake (Community) | AnyLog Enterprise (Subscription) |
|---|:---:|:---:|
| License | Open-source (Linux Foundation) | Commercial (contact for pricing) |
| Virtual Edge Layer | ✅ | ✅ |
| Rule Engine | ✅ | ✅ |
| Policy-Based Data Management | ✅ | ✅ |
| Node Management | ✅ | ✅ |
| Unified APIs, CLIs, Admin UI | ✅ | ✅ |
| Supported IoT Connectors | ✅ | ✅ |
| Blockchain Abstraction | Optional add-on | ✅ |
| Aggregations | ❌ | ✅ |
| Security Protocol | ❌ | ✅ |
| High Availability (HA) | ❌ | ✅ |
| Test Suites | ❌ | ✅ |
| Training | ❌ | ✅ |
| Technical Support | ❌ | ✅ |
| Publisher node | ❌ Not supported | ✅ |

For pricing: <a href="https://www.anylog.network/pricing" target="_blank">AnyLog Pricing</a>. Upgrading is as simple as changing the
`docker-compose` image from `anylogco/edgelake` to `anylogco/anylog-network`. *(Detailed upgrade steps: not yet
documented.)*

**Q: What are the hardware/resource requirements?**

| Category | Requirement |
|---|---|
| Operating System | Linux (Ubuntu, RedHat, Alpine, SUSE), Windows, Mac |
| Memory footprint | 100 MB available without Docker; 300 MB available with Docker |
| Databases | PostgreSQL (optional); SQLite (default, no install needed); MongoDB (only if blob storage is needed) |
| CPU | Intel, ARM, and AMD supported; single-CPU machines up to large multi-core servers (gateways, Raspberry Pi, etc.) |
| Network | TCP-based network required; overlay networks recommended (Nebula is default); static IP and 3 open ports per node |
| Deployment options | Executable (background process), Docker, or Kubernetes |

See [Prerequisites](../01-%20Getting%20Started/02-%20Prerequisite.md) for the full compatibility matrix.

**Q: What are the node types, and what's a Cluster?**

All AnyLog containers run the same image — configuration determines behavior:

- **Metadata Manager (Master)** — emulates a blockchain, coordinating metadata for the network.

- **Operator** — stores data collected from devices. Belongs to exactly one **Cluster** — a policy grouping
  Operators together for HA and telling the network where data lives.

- **Query** — processes/executes queries; any node with the `system_query` logical database can serve this role.

- **Publisher** — routes data to Operators; doesn't store data itself. Not supported in EdgeLake, and cannot run
  on the same node as Operator.

- **Generic** - this is not documented, but when specifying `NODE_TYPE=generic` the system will automatically deploy an
empty "stand box" with network (TCP, REST and Message broker) configured. 

See [Nodes](../01-%20Getting%20Started/01-%20Introduction.md#node-types) for the full breakdown, including cluster policy 
structure and main/backup roles.

**Q: How do I deploy, and do you support zero-touch?**

Deployment is entirely configuration based with default values pre-set in the <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">deployment-scripts</a>. 

From a Docker or Kubernetes point of view (as an example) the process is: 
1. User defines configurations in a dotenv file 
2. Anylog agent is deployed as a container, with environment variables from the dotenv file 
   1. image is pulled from docker 
   2. deployment-scripts is cloned (if not set to `main`)
   3. AnyLog agent is brought up 
      1. Environment variables become  AnyLog variables (`$NODE_TYPE` → `!node_type`) 
      2. databases get connected, services start and policies are defined on the blockchain based on the configurations 

Zero-touch, with a caveat: AnyLog can't guess *which* node type it should be, or which blockchain to connect
to — but everything else has default values. In practice this means only 3 parameters are required:

```commandline
docker run -it -d --detach-keys=ctrl-d --network host \
    -e NODE_TYPE=operator \
    -e LEDGER_CONN=192.167.78.32:32048 \
    -e LICENSE_KEY=XXX
```

See [Getting Started](../01-%20Getting%20Started/03-%20install.md) and
[Installation & Deployment](../02-%20Installation%20&%20Deployment/01-%20Install.md) for the full walkthrough.

**Q: What is the difference between an Operator and a Publisher?**

An Operator stores data locally and responds to queries. A Publisher receives data files and routes them to
Operators — it doesn't store data itself. They cannot run on the same docker / Kubernetes container due to the shared 
watch directory. 

**Q: Can I run multiple AnyLog nodes on the same machine?**

Yes. Each node needs its own set of ports (TCP, REST, broker) and its own root directory — use different
`ANYLOG_SERVER_PORT`, `ANYLOG_REST_PORT`, and `ANYLOG_BROKER_PORT` values per node.

**Q: How do I exit a node, or run it in the background?**

```anylog
exit node
```
For background: Docker with `-d` (detached), or a systemd service. The local CLI is disabled in background mode —
use the Remote CLI or REST API instead.

---

## Network

**Q: How do I connect to TCP / REST / the message broker, and what's the difference?**

TCP is peer-to-peer (node-to-node); REST is for external apps/scripts; the broker is MQTT-style pub/sub. See
[Background Processes → Network services](../07-%20CLI/02-%20Background%20Processes.md#network-services) for
setup commands and config options for all three.

**Q: How do I join a network — is that blockchain sync, or defining a policy?**

Different things, often both needed. 
1. **Sync** pulls in metadata that's already on the network (you're catching up to what exists). 
2. **Defining a policy** publishes new metadata about *you* (a node/operator/cluster policy) that other nodes then sync 
in. 

See [Blockchain Connectivity](../08-%20Blockchain%20&%20Metadata/03-%20Blockchain%20Commands.md#blockchain-sync) for sync, and
[Blockchain Policy](../08-%20Blockchain%20&%20Metadata/02-%20Policy%20&%20Metadata.md) for defining one.

**Q: My node can't connect to the network at all — where do I start?**

There are 2 questions here: 
    1. are you connected to _TCP_ service? If no, please review [network connectivity](../06-%20Networking%20%26%20Security/02-%20Network%20Processing.md)
    2. do you have `blockchain sync` configured? If no, please review  [blockchain connect & sync section](../08-%20Blockchain%20%26%20Metadata/03-%20Blockchain%20Commands.md#connect--sync)

See [Troubleshooting → `test node`](02-%20Troubleshooting.md#test-node) — run that first; if it fails, the
problem is local to the node, not a network path issue.

**Q: My node can't communicate with other nodes.**

1. When doing `get connections` do you see network configured 
2. When running `test node` does the node reply to itself 
3. are firewalls open? 

See [Troubleshooting → `test network`](02-%20Troubleshooting.md#test-network), including the common-causes list
for DNS/firewall/port-forwarding issues.

**Q: What does `bind = true` vs `bind = false` mean?**

`true` — the service only accepts connections on the single specified IP. 

`false` — accepts connections on all available IPs on that port. Use `false` when you want both local and external 
traffic accepted.

**Q: The `test network` command shows some nodes as unreachable — is that a problem?**

Not necessarily — they may be offline, on a different segment, or behind a firewall. Use `subset = true` in
`run client` to tolerate partial responses:

```anylog
run client (blockchain get operator bring.ip_port, subset = true) get status
```

**Q: I deployed on AWS (or GCP/Azure) and nodes can't connect to each other.**

Ensure the security group allows **inbound TCP** on the AnyLog TCP/REST ports from the relevant ranges; on AWS
the instance's public IP is `external_ip`, private IP is `internal_ip`; use `bind = false`; check VPC/subnet
routing if using private networking.

**Q: What MTU size should I use?**

Default 1500 bytes can cause fragmentation in some cloud/overlay setups. If you see dropped connections, try
`ip link set eth0 mtu 1400` — check your cloud provider's recommended MTU for your network type.

**Q: Nginx (or another Docker service) can't reach an AnyLog node on the same Windows machine.**

Docker on Windows can't reach the host via `localhost` — use `host.docker.internal` and add the alias to your
`docker-compose.yaml`:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

---

## Data Management

**Q: Which databases do you support, and when do I use each?**

AnyLog stores sensor /device data in a SQL database and files in a blob or NoSQL type of database. 
Supported Databases:
* PostresSQL 
* SQLite 
* MongoDB 
* S3 / S3-like buckets (Minio and Akave)

In addition, AnyLog can coonect to Milvus for vector/similarity search.

See [Databases](../09-%20Data%20Management/02-%20Databases.md) for the full breakdown and how SQL
and blob storage relate to each other.

**Q: How do I connect to them?**

CConnectivity logic / command differs by the database type

* [SQL Storage - PostgresSQL / SQLite](../09-%20Data%20Management/02-1%20Databases/01-%20SQL%20Storage.md)
* [MongoDB](../09-%20Data%20Management/02-1%20Databases/03-%20NoSQL%20%28MongoDB%29.md)
* [MinIO](04-%20Third-Party%20Support/02-%20MinIO.md)
* [Milvus](../09-%20Data%20Management/02-1%20Databases/05-%20MilvusDB.md) for connection syntax specific to each.

**Q: How is data partitioned, and why do some tables have a `par_` prefix?**

Partitioning is a configurable parameter that maybe used to split data into smaller logical tables (by timestamp data 
type) for better data management and query performance. 

See [SQL Storage → Table Partitioning](../09-%20Data%20Management/02-1%20Databases/01-%20SQL%20Storage.md#table-partitioning)
for interval syntax, viewing partitions, and dropping them.

**Q: Why did `drop partition` remove more data than I expected?**

If you don't specify how many partitions to keep (`keep=N`), the system keeps only the newest one — everything
else is dropped. If you don't specify a table name (or use `table=*`), the drop applies across **every** table
in the database. Always double-check `table=` and `keep=` before running this.

**Q: Do you support HA / DR?**

Yes — at least 2 operators residing in the same cluster gets you both data resilience (replication) and high
availability (query failover). See [High Availability & Data Resilience](../09-%20Data%20Management/03-%20High%20Availability.md) 
for the full mechanism.

**Q: Why isn't my data replicating across the cluster even though distributor/consumer are enabled?**

Two likely causes:
1. A configuration mismatch: 
   1. the logical database not being open on the secondary operator
   2. the two operators do not reside against the same relative cluster 
2. Networking / firewall connectivity issues on one of the two nodes 

**Q: Two of my operators ended up with the same Member ID.**

Most likely a hardcoded config value overwrote it, or the operator carried over an old policy from a previous
blockchain/platform. 

**Fix**: bring the operator down, remove its persisted local blockchain copy, and bring it back
up — confirming no duplicate IP+Port already exists on the network ledger first.

**Q: I reset/redeployed an operator on the same IP — do I need a new Member ID?**

No. Blockchain identity is meant to be persistent — a reset node should pick up its original Member ID again,
not get issued a new one.

### Data ingestion

**Q: Data isn't appearing in the database — what do I check?**

1. Streamer and Operator both running? `get processes`
2. Watch directory populated? `get !watch_dir` — check the error directory too: `get !err_dir`
3. Database connected? `get databases`
4. `create_table = true` set in `run operator`, or table created manually?

**Q: Why are rows not appearing immediately?**

The Streamer buffers by default (60s / 10,000 bytes). Check thresholds with `get streaming`, or disable
buffering: `set buffer threshold where write_immediate = true`.

**Q: What's the difference between inline column mapping and a mapping policy?**

Inline — written directly into `run msg client`, simple, not reusable. Mapping policy — stored on the
blockchain, referenced by ID, reusable across nodes and required for the Operator's `policy` parameter.

**Q: Can I use `dynamic=true` together with explicit column mapping?**

Yes — `dynamic` is an alternative to a fixed `table_name`, not to mapping. Combine `dynamic=true` with
`column.*` mapping whenever your payload has multiple fields to type/extract.

**Q: My dynamic ingestion is putting different sensor readings into one table instead of separate ones.**

`dynamic=true` with no mapping creates one table per sensor automatically. Once mapping is introduced, you need
to also split on a per-row `table` field, or distinct readings under the same topic merge into one table.

**Q: My mapping policy JSON is rejected.**

The three most common causes: `Null` instead of lowercase `null`; a trailing comma on the last key in an object;
a doubled opening quote on a string (easy to miss when copy-pasting). See
[Mapping Policy](../04-%20Southbound%20Interfaces/02-%20Mapping%20Policy.md) for the full schema
reference.

**Q: My mapping policy is published but the Operator isn't using it.**

1. `run msg client` is pointing to the wrong _mapping_ policy 
2. There's a mismatch between the _mapping_ logic and actual data coming in on the given port 
3.  `run operator` isn't running so content is coming in but not stored.

**Q: Why isn't my blob file (image/video) showing up when I query the SQL table?**

there are a few options here:
1. If there's a reference point then the issue has to do with `file to` / `file from` that transfers the blob from storage node (ie operator)
to the query and/or application. 
2. There's an issue with volume / data reliance directory for blobs on the query node side. 

Please review [blob extraction]() in the Edge Data Manager section. 

---

## Query

**Q: Can `period` and `increments` be used in the same query?**

Not at this time — `increments` needs a continuous range to bucket; `period` is looking for the last occurrence
before a timestamp. See [SQL Commands → Time-series optimized queries](../07-%20CLI/04-%20SQL.md#Time-series-optimized-queries).

**Q: Does AnyLog support SQL-style JOINs across tables?**

Yes, via `include` (not a `JOIN` keyword) — it pulls in data from additional tables beyond `FROM`. Pair it with
`extend=(+table_name)` to see which table each result row actually came from:
```anylog
sql my_data include=(other_table) and extend=(+table_name) "select * from my_table where reading_time >= now() -1d"
```
See [SQL Commands](../07-%20CLI/04-%20SQL.md#the-sql-command) for the full option reference.

**Q: My query returns no results even though data exists.**

Confirm the Operator has the data (`get rows count`), blockchain sync is current (`get synchronizer`), operators
are reachable, `dbms`/`table` names match exactly, the time filter uses `NOW() - N hours` (not PostgresSQL
`INTERVAL` syntax), and — for POST — that `"destination": "network"` is set.

**Q: Why did `SELECT *` (or `SELECT COUNT(*)`) fail even though I can see the data locally?**

The Query node needs a `table` policy on the blockchain to expand `*` into real columns before distributing the
request. Without it, the query fails not because it can't find the data, but because it can't determine how the
data is organized.

**Q: Can I query a specific node only, or profile slow queries?**

```anylog
run client (10.0.0.78:32048) sql my_data "select * from ping_sensor limit 10"

set query log on
set query log profile 5 seconds     # log queries slower than 5 seconds
get query log
```

**Q: What's the difference between Milvus's `distance` for COSINE vs. L2 metrics?**

*(Pending — needs an owner to confirm before this is documented.)*

**Q: What do `selection` and `description` do in a blob-aware query?**

*(Pending — needs an owner to confirm before this is documented.)*

---

## Blockchain

**Q: What's the difference between a Metadata Manager (master node) and a real blockchain?**

A metadata manager (or master) node is a simple AnyLog agent emulating a blockchain locally. A real blockchain 
(e.g. Optimism) is an actual distributed, trustless ledger. Either works; a real blockchain isn't required. See
[Blockchain Connectivity](../08-%20Blockchain%20&%20Metadata/03-1%20Blockchain%20Full%20Circle.md#which-ledger)
for the full tradeoff table.

**Q: How do I connect to a metadata manager node vs. a real blockchain?**

Connecting to a Metadata manager node by simply enabling the `blockchain sync` logic with a specific TCP IP and port 
of the metadata manager. While an actual blockchain is a bit more comprehensive as it requires wallets, keys and 
other components needed to conect to an actual blockcahin. 

See [Blockchain Connectivity](../08-%20Blockchain%20&%20Metadata/03-1%20Blockchain%20Full%20Circle.md) for both
paths.

**Q: Which blockchains does AnyLog actually support?**

Documented examples use Ethereum-compatible chains (Optimism shown specifically). *(Confirm whether support
extends beyond Ethereum-compatible chains — not established anywhere in this doc set.)*

**Q: What is a policy, and how do I define one?**

A blockchain policy is an object defining node information, data information and / or other information that's critical 
for the network and is immutable. AnyLog does not store the actual device / sensor data on the blockchain - just the 
metadata. 

See [Policies & Metadata](../08-%20Blockchain%20&%20Metadata/02-%20Policy%20&%20Metadata.md) for details.

**Q: How do I query the blockchain?**

The command `blockchain get [* | node type]` is the basic command struct used to query the blockchain. In addition, 
the command allows for `where` and `bring` conditions.    

See [Blockchain Commands → Query the Blockchain](../08-%20Blockchain%20&%20Metadata/03-%20Blockchain%20Commands.md#query-the-blockchain).

**Q: What does the blockchain actually do for AnyLog?**

The blockchain layer is the component that informs an AnyLog agent these are the nodes and data in your network.

See [Blockchain](../08-%20Blockchain%20&%20Metadata/01-%20Blockchain.md) for farther details.

**Q: `blockchain test` fails.**

The local blockchain file is missing, corrupt, or empty. 
* If you have a blockchain service running 
```anylog 
run blockchain sync 
blockchain reload metadata 
```

* If you'd like to copy the blockchain file once 
```anylog 
blockchain seed from [remote tcp ip]:[remote tcp port]
```
> `blockchain seed` works against any node with a blockchain (file) on it. The only word of caution is that if there's 
> an active blockchain service, the file will ultimately be re-synced with the configured ledger conn. 

**Q: I added a policy, but it's not visible on other nodes.**

Force an immediate sync: `run blockchain sync`, then confirm on peers with `get metadata version`.

**Q: What's the difference between `blockchain get` and `blockchain read`?**

`get` returns policies after runtime dynamic updates — the normal case. `read` returns them exactly as received
from the ledger, no post-processing. Using the wrong one can make results look inconsistent when nothing's
actually wrong.

**Q: What is the correct command to publish a policy?**

`blockchain insert` — the older `blockchain push` is deprecated:

```anylog
blockchain insert where policy = !new_policy and local = true and master = !ledger_conn
```

---

## REST

**Q: GET vs. POST vs. PUT — what's the difference?**

| | Where parameters go | Requires `run msg client`? | Typical use |
|---|---|---|---|
| **GET** | HTTP headers (`-H 'command: ...'`) | No | CLI-equivalent commands, scripts, curl |
| **POST** | JSON body (headers become body keys) | Yes, if publishing data (`broker=rest` + topic mapping) | Browsers, restricted-header environments, publishing data with mapping |
| **PUT** | HTTP headers, raw body | No — bypasses topic mapping entirely | Publishing data directly to a known dbms/table, no mapping needed |

Examples:
```bash
# GET
curl -X GET 127.0.0.1:32349 -H "command: get status" -H "AnyLog-Agent: AnyLog/1.23"

# POST
curl -X POST 127.0.0.1:32349 -H "Content-Type: application/json" \
  -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}'
```
See [Using REST](../06-%20Networking%20%26%20Security/04-%20Using%20REST.md) for full
publish examples (PUT and POST) and Python code.

**Q: Should I use `User-Agent` or `AnyLog-Agent`?**

Both work identically. Use `AnyLog-Agent` from a browser — `User-Agent` is a reserved header `fetch()` can't set
manually, and using it cross-origin can trigger a CORS preflight AnyLog nodes don't answer by default.

**Q: My browser dashboard gets a CORS error.**

Either the node isn't returning `Access-Control-Allow-Origin`, or a reserved header triggered a preflight. Use
the nginx/Flask proxy for production, or switch to `AnyLog-Agent` and whitelist it:
```
Access-Control-Allow-Headers: AnyLog-Agent, Content-Type
```

**Q: My SQL query via POST returns empty results but node status works.**

Missing `"destination": "network"` in the body — without it the query only runs on the query node, which holds
no operator data.

---

## Notifications

**Q: My Telegram/Pushover notification isn't sending, and there's no error.**

First check the AnyLog-side cause: `telegram_body`/`pushover_body` needs the `json` prefix
(`telegram_body = json {...}`), or the variable stores literal unresolved text instead of real values — the log
shows nothing wrong, but the destination silently rejects the malformed body. If that's not it: verify
config (username/auth key), confirm outbound firewall access, confirm the third-party service isn't down.

**Q: My SMS notification via carrier gateway stopped working.**

AnyLog's SMTP-based SMS logic still works — but most carriers have dropped free mail-to-SMS gateway support on
their end. This is a carrier policy change, not an AnyLog issue. Use a dedicated SMS API for anything you
depend on.

---

## MCP & AI integration

**Q: Claude Desktop shows AnyLog MCP tools but all calls fail.**

The endpoint is missing the `/mcp/sse` suffix — correct URL is `http://HOST:PORT/mcp/sse`.

**Q: MCP tools aren't visible after editing the config.**

Fully quit and reopen Claude Desktop — it doesn't hot-reload. Verify valid JSON (no trailing commas) and confirm
`mcp-proxy` is installed (`which mcp-proxy`).

**Q: Do I need MCP running at all times for a generated dashboard?**

No — the recommended approach runs entirely over REST at runtime; MCP is only used once, at generation time, to
discover schema/topology. Only the experimental live-MCP dashboard needs MCP at runtime.

**Q: My generated dashboard works from curl but fails in the browser with CORS.**

Same fix as the general CORS question above — run the nginx/Flask proxy, or use `AnyLog-Agent` with the node
configured to return the required CORS headers.