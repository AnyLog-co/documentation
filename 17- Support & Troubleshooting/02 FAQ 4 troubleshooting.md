---
title: FAQ & Troubleshooting
description: Common questions, known issues, and troubleshooting guidance for AnyLog deployments.
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**                                                                                                             | **Version** |
 |------------|----------------|------------------------------------------------------------------------------------------------------------------------|----------|
 |            |                |                                                                                                                        |          |
 | 2026-07-20 | Eric Aquaronne | added change log                                                                                                       | 2.0.2606 |
 | 2026-04-23 |                | Added REST/CORS/AnyLog-Agent, POST vs GET, blockchain insert, mapping policy pitfalls, MCP, Docker networking sections |          |
 | 2026-04-17 |                | creation                                                                                                               |          |
--->

---

## General

**Q: What is the difference between an Operator and a Publisher?**
An Operator stores data locally in its own databases and responds to queries. A Publisher receives data files and routes them to Operator nodes — it does not store data itself. They cannot run on the same node.

**Q: What is the difference between a master node and a blockchain platform?**
A master node is a simple AnyLog node that stores the metadata ledger in a local database and serves it to peers. A blockchain platform (e.g. Optimism) stores the ledger on a distributed, trustless chain. Either can be used; a blockchain is not required.

**Q: Can I run multiple AnyLog nodes on the same machine?**
Yes. Each node needs its own set of ports (TCP, REST, broker) and its own root directory. Use different `ANYLOG_SERVER_PORT`, `ANYLOG_REST_PORT`, and `ANYLOG_BROKER_PORT` values per node.

**Q: How do I exit an AnyLog node?**
```anylog
exit node
```

**Q: How do I run AnyLog in the background?**
Use Docker with `-d` (detached mode), or configure AnyLog as a systemd service. When running in the background, the local CLI is disabled — use the Remote CLI or REST API instead.

---

## REST API

**Q: What is the difference between GET and POST for AnyLog commands?**
Both methods execute the same commands. The difference is where the parameters go:
- **GET** — command and options are passed as HTTP headers (`-H 'command: get status'`)
- **POST** — the same headers become keys in a JSON body (`{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}`)

POST is preferred for browser-based clients and any environment where setting custom HTTP headers is restricted.

**Q: Should I use `User-Agent` or `AnyLog-Agent`?**
Both are accepted and treated identically by the node. Use `AnyLog-Agent` when calling from a browser. Browsers treat `User-Agent` as a reserved header — `fetch()` cannot set it manually, and cross-origin requests using it can trigger a CORS preflight (`OPTIONS`) that AnyLog nodes are not configured to answer by default. `AnyLog-Agent` is a custom header that sidesteps this entirely.

**Q: My browser dashboard gets a CORS error when posting directly to an AnyLog node.**
There are two causes:

1. **Node not returning CORS headers** — the node is not responding with `Access-Control-Allow-Origin: *`. Use the nginx or Flask proxy instead, or launch Chrome with `--disable-web-security` for local dev only.

2. **CORS preflight blocked** — if you see `Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present`, a browser-reserved header triggered an `OPTIONS` preflight. Switch to `AnyLog-Agent` in your POST body and ensure the node whitelists it:
   ```
   Access-Control-Allow-Headers: AnyLog-Agent, Content-Type
   ```

For production, routing through the nginx or Flask proxy eliminates the CORS issue entirely — the browser never sees the cross-origin hop.

**Q: My SQL query via POST returns empty results but node status works.**
Missing `"destination": "network"` in the request body. Without it the query runs only on the query node, which holds no operator data:
```json
// ❌ Wrong — query node only
{"AnyLog-Agent": "AnyLog/1.23", "command": "sql mydb format=json:list and stat=false SELECT ..."}

// ✅ Correct — distributed to operator nodes
{"AnyLog-Agent": "AnyLog/1.23", "command": "sql mydb format=json:list and stat=false SELECT ...", "destination": "network"}
```

**Q: What is the correct format for PUT vs POST data publishing?**

- **PUT** — bypasses topic mapping. Database and table are specified directly in the HTTP headers. No `run msg client` required.
- **POST** — requires a `run msg client` with `broker=rest` active on the node, plus a topic mapping. The POST body is the raw data; `command: data` and `topic: [name]` are set as headers (or body keys).

See <a href="/docs/network-services/using-rest/">Using REST</a> for full examples and Python code.

---

## Networking

**Q: My node shows `Not connected` or peers can't reach it — what do I check?**

1. Confirm the TCP service is running: `get processes`
2. Confirm the correct IPs are published: `get connections`
3. Test local connectivity: `test node`
4. Test network connectivity: `test network`
5. Check firewall rules — the TCP and REST ports must be open inbound
6. If behind NAT, verify port forwarding is configured correctly
7. Check the blockchain sync is running and the local metadata file is populated: `get synchronizer`

**Q: What does `bind = true` vs `bind = false` mean?**
`bind = true` — the service only accepts connections on the single specified IP.
`bind = false` — the service accepts connections on all available IPs on that port. Use `false` when you want both local and external traffic accepted.

**Q: How do I check what ports AnyLog is listening on?**
```anylog
get connections
```

**Q: The `test network` command shows some nodes as unreachable — is that a problem?**
Not necessarily. Nodes may be offline, in a different network segment, or behind a firewall. Use `subset = true` in `run client` commands to tolerate partial responses:
```anylog
run client (blockchain get operator bring.ip_port, subset = true) get status
```

---

## Data ingestion

**Q: Data is arriving at the broker/MQTT but not appearing in the database — what do I check?**

1. Is the Streamer running? `get processes` — check `Streamer` row
2. Is the Operator running? Check `Operator` row in `get processes`
3. Is the watch directory being populated? `get !watch_dir`
4. Check the error directory for failed files: `get !err_dir`
5. Check the operator log: `get operator`
6. Confirm the database is connected: `get databases`
7. Confirm `create_table = true` is set in `run operator`, or create the table manually

**Q: What is the watch directory?**
The watch directory is where JSON data files are staged before the Operator processes them. Any file placed in this directory is automatically picked up and ingested.
```anylog
get !watch_dir
```

**Q: Why are rows not appearing immediately after data arrives?**
If the Streamer is running in buffered mode, data is held in memory until the time or volume threshold is reached. Default: 60 seconds or 10,000 bytes.
```anylog
get streaming                                              # check thresholds
set buffer threshold where write_immediate = true         # disable buffering
```

**Q: The Operator is running but showing errors — where do I look?**
```anylog
get operator
get error log
```
Check the error directory: `get !err_dir`. Files moved there failed to process — inspect them for format issues.

**Q: How do I verify data is being ingested?**
```anylog
get rows count where dbms = my_data
get operator inserts
get operator summary
```

**Q: My `run msg client` with `broker=rest` is configured but POST data isn't being ingested.**
Check these in order:

1. Confirm the msg client is running: `get msg clients`
2. Confirm the `topic` name in the POST request matches exactly the `name` in `run msg client`
3. Confirm `command: data` is set (as a header for server-side POST, or as a body key for browser POST)
4. Confirm the Streamer is running: `get processes`
5. Check for mapping errors: `get error log`

**Q: What is the difference between inline column mapping and a mapping policy?**
- **Inline mapping** — column definitions are written directly into the `run msg client` command. Simple, no blockchain dependency, but not reusable across nodes.
- **Mapping policy** — stored on the blockchain, referenced by ID. Required when using the Operator's `policy` parameter, or when the same mapping needs to be shared across nodes.

Publish a mapping policy with:
```anylog
blockchain insert where policy = !mapping_policy and local = true and master = !master_node
```

---

## Mapping policy pitfalls

**Q: My mapping policy JSON is rejected — what are the most common errors?**

Three issues come up repeatedly:

1. **`Null` instead of `null`** — JSON is case-sensitive. The only valid null literal is lowercase:
   ```json
   "default": null   ✅
   "default": Null   ❌
   ```

2. **Trailing comma on the last key in an object** — JSON does not allow this:
   ```json
   {"type": "bool", "root": true,}   ❌
   {"type": "bool", "root": true}    ✅
   ```

3. **Double-opening quote on a string** — easy to miss in copy-paste:
   ```json
   "bring": ["success", ""tagName", "value"]   ❌
   "bring": ["success", "tagName", "value"]    ✅
   ```

**Q: My mapping policy is published but the Operator isn't using it.**
Confirm the policy ID referenced in `run operator` or `run msg client` matches what was actually stored:
```anylog
blockchain get mapping where name = [name] bring [id]
```
Also confirm the blockchain sync has propagated the new policy to the Operator node:
```anylog
run blockchain sync
get metadata version
```

---

## Queries

**Q: My query returns no results even though data exists — what do I check?**

1. Confirm the Operator node is running and the data is there: `get rows count`
2. Confirm the blockchain sync is up to date: `get synchronizer`
3. Use `run client (blockchain get operator bring.ip_port) get status` to confirm Operators are reachable
4. Check that the `dbms` and `table` names in the query match exactly what is in the database
5. Verify the time filter — `NOW() - N hours` not PostgreSQL `INTERVAL` syntax
6. For POST-based queries, confirm `"destination": "network"` is in the request body

**Q: Can I query data from a specific node only?**
```anylog
run client (10.0.0.78:32048) sql my_data "select * from ping_sensor limit 10"
```

**Q: How do I profile slow queries?**
```anylog
set query log on
set query log profile 5 seconds     # log queries slower than 5 seconds
get query log
```

---

## Docker & deployment

**Q: How do I view AnyLog logs in Docker?**
```bash
docker logs [container-name]
docker attach --detach-keys=ctrl-d [container-name]   # attach to CLI
```

**Q: The container started but AnyLog isn't responding — what do I check?**

1. Check the container is running: `docker ps`
2. Attach to the CLI and check `get processes`
3. Verify the port mappings in your `docker run` or `docker-compose.yaml`
4. Check environment variables are set correctly (TCP port, REST port, etc.)

**Q: How do I update AnyLog?**
```bash
docker pull anylogco/anylog-network:latest
docker stop [container-name]
docker rm [container-name]
docker run ... anylogco/anylog-network:latest
```

**Q: nginx (or another Docker service) can't reach an AnyLog node running on the same Windows machine.**
Docker containers on Windows cannot reach the host via `localhost`. Use `host.docker.internal` instead, and add the host alias to your `docker-compose.yaml`:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
environment:
  - ANYLOG_NODE_URL=http://host.docker.internal:PORT/
```

---

## AWS / cloud networking

**Q: I deployed on AWS (or GCP/Azure) and nodes can't connect to each other.**

- Ensure the security group (or firewall rule) allows **inbound TCP** on the AnyLog TCP and REST ports from the relevant IP ranges
- On AWS, the instance's public IP is typically the `external_ip`; the private IP is the `internal_ip`
- Use `bind = false` so the node accepts connections on all interfaces
- If using VPC peering or a private subnet, ensure routing tables allow traffic between instances

**Q: What MTU size should I use?**
In some cloud and overlay network setups, the default MTU of 1500 bytes can cause packet fragmentation. If you see dropped connections or slow transfers, try reducing the MTU:
```bash
ip link set eth0 mtu 1400
```
Check your cloud provider's recommended MTU for your network type (e.g. AWS uses 9001 for jumbo frames in VPC, or 1500 for standard).

---

## Blockchain / metadata

**Q: `blockchain test` fails — what does that mean?**
The local blockchain file is missing, corrupt, or empty. Re-sync from a peer:
```anylog
blockchain pull to json [peer-ip:port]
```

**Q: I added a policy but it's not visible on other nodes.**
The blockchain sync interval controls when peers pick up new policies. Force an immediate sync:
```anylog
run blockchain sync
```
On peers:
```anylog
run blockchain sync
get metadata version     # confirm the version updated
```

**Q: How do I find the ID of a policy I just created?**
```anylog
blockchain get [policy-type] where name = [name] bring [id]
```

**Q: What is the correct command to publish a policy to the blockchain?**
Use `blockchain insert` — the older `blockchain push` command is deprecated:
```anylog
blockchain insert where policy = !new_policy and local = true and master = !ledger_conn
```
The `master` parameter is optional — include it to also publish to a master ledger node. `local = true` writes the policy to the local blockchain file immediately.

---

## MCP & AI integration

**Q: Claude Desktop shows the AnyLog MCP tools but all tool calls fail.**
The MCP endpoint URL is missing the `/mcp/sse` suffix. The bare node URL (`http://HOST:PORT`) appears to connect but all tool calls fail silently. The correct URL is:
```
http://HOST:PORT/mcp/sse
```

**Q: MCP tools are not visible in Claude Desktop after editing the config.**
Quit and fully reopen Claude Desktop — it does not hot-reload the config file. Also verify the config is valid JSON (no trailing commas) and the `mcp-proxy` path is correct:
```bash
which mcp-proxy       # macOS / Linux
mcp-proxy --version   # confirm it's installed
```

**Q: Do I need MCP running at all times to use a generated dashboard?**
No. Dashboards generated via Example 1 (the recommended approach) run entirely over plain REST at runtime — MCP is only used once at generation time to discover the schema and topology. Only the experimental MCP-backed live dashboard (Example 3) requires MCP at runtime, and that has real cost and latency implications.

**Q: My generated dashboard works from curl but fails in the browser with a CORS error.**
The dashboard is making direct browser-to-node POST calls and the node is not returning CORS headers. Options:
1. Run the nginx proxy (`proxy-nginx/`) and set Mode → nginx in the dashboard config bar
2. Run the Flask proxy (`proxy-generic/`) and set Mode → proxy
3. Use `AnyLog-Agent` as a body key and configure the node to return the required CORS headers

See <a href="/docs/docs/mcp-ai-integration/#browser-connection-modes">MCP & AI Integration</a> for setup details.


# FAQ

This repository serves as a reference for understanding node types in the AnyLog ecosystem, common operational issues, and 
differences between the enterprise-grade AnyLog and EdgeLake deployments.



## 📖 Overview

**AnyLog** is a decentralized data platform for managing and querying operational and IoT data.  
**EdgeLake** is the open-source version of AnyLog

| Feature                              | EdgeLake (Community Version)         | AnyLog Enterprise (Subscription)    |
|--------------------------------------|--------------------------------------|-------------------------------------|
| **License**                          | Open-source (Linux Foundation)       | Commercial (Contact for pricing)    |
| **Virtual Edge Layer**               | ✅                                    | ✅                                  |
| **Rule Engine**                      | ✅                                    | ✅                                  |
| **Policy-Based Data Management**     | ✅                                    | ✅                                  |
| **Node Management**                  | ✅                                    | ✅                                  |
| **Unified APIs, CLIs, Admin UI**     | ✅                                    | ✅                                  |
| **Supported IoT Connectors**         | ✅                                    | ✅                                  |
| **Blockchain Abstraction**           | Optional Add-on                      | ✅                                  |
| **Aggregations**                     | ❌                                    | ✅                                  |
| **Security Protocol**                | ❌                                    | ✅                                  |
| **High Availability (HA)**           | ❌                                    | ✅                                  |
| **Test Suites**                      | ❌                                    | ✅                                  |
| **Training**                         | ❌                                    | ✅                                  |
| **Technical Support**                | ❌                                    | ✅                                  |

For details: <a href="https://www.anylog.network/pricing" target="_blank">AnyLog Pricing</a>



## ❓ Frequently Asked Questions (FAQ)

### What are the different types of nodes in the AnyLog Network?

All AnyLog containers run the same source code / image, it is the configurations that force a distinction in behavior between the node types:

* **Master**: An AnyLog instance that simulates the role of a blockchain, serving as a decentralized "oracle" for managing metadata, smart contracts, and overall network coordination.
* **Operator**: An AnyLog instance responsible for storing data collected from devices.
  * **Cluster**: A logical policy that defines the relationship between Operator nodes, enabling high availability (HA) and informing members of the network about the location and distribution of data. Each Operator node belongs to a Cluster, and a Cluster can consist of multiple Operator nodes.
* **Query**: An AnyLog instance dedicated to processing and executing data queries. Any node can serve as a Query Node if it includes the `system_query` logical database.
* **Publisher**: An AnyLog instance responsible for distributing or publishing data to Operator nodes. Publishers typically act as gateways for ingesting real-time data into the network.
> ⚠️ **Note**: Publisher is not supported in **EdgeLake**.

### How do I configure an AnyLog node to act as a specific node type?

Configuration is done through either a dotenv file for Docker / Podman or YAML file for Kubernetes.
The configurations can be done in 2 parts
* **basic** which consists of the standard configurations, such as networking and database configurations
* **advance** which consists of more advanced configurations such as number of threads to use and enabling advanced services.   

Configurations can be found in our <a href="https://github.com/AnyLog-co/docker-compose/" target="_blank">docker-compose</a> 

### How does the deployment process work? 

A node is deployed using the following logic

1. Using the dotenv / YAML configuration file(s), a user defines an AnyLog node (type) with their prefered configurations
2. The user then deploys the docker or Kubernetes container with the given configurations
3. The docker image will download a copy of our <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">deployment-scripts</a> 
4. It will then convert the user-defined environment variables to AnyLog variables
5. The code will then declare a configurations policy (if not exists) that specifies how to configure a node.    
```json
{"config" : {
    "name" : "operator-iotech-configs", 
    "company" : "IoTech System", 
    "node_type" : "operator",
    "ip" : "!external_ip",
    "local_ip" : "!overlay_ip",
    "port" : "!anylog_server_port.int",
    "rest_port" : "!anylog_rest_port.int",
    "broker_port" : "!anylog_broker_port.int",
    "threads" : "!tcp_threads.int",
    "tcp_bind" : "!tcp_bind",
    "rest_threads" : "!rest_threads.int",
    "rest_timeout" : "!rest_timeout.int",
    "rest_bind" : "!rest_bind",
    "broker_threads" : "!broker_threads.int",
    "broker_bind" : "!broker_bind",
    "script" : [
      "process !local_scripts/connect_blockchain.al", 
      "process !local_scripts/policies/cluster_policy.al",
      "process !local_scripts/policies/node_policy.al",
      "process !local_scripts/database/deploy_database.al",
      "run scheduler 1",
      "set buffer threshold where time=!threshold_time and volume=!threshold_volume and write_immediate=!write_immediate",
      "run streamer", 
      "if !enable_ha == true then run data distributor",
      "if !enable_ha == true then run data consumer where start_date=!start_data",
      "if !operator_id and !blockchain_source != master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!00- archive and archive_sql=!archive_sql and blockchain=!blockchain_source and policy=!operator_id and threads=!operator_threads",
      "if !operator_id and !blockchain_source == master then run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and compress_json=!compress_file and compress_sql=!compress_sql and archive_json=!00- archive and archive_sql=!archive_sql and master_node=!ledger_conn and policy=!operator_id and threads=!operator_threads",
      "if !enable_mqtt == true then process !anylog_path/deployment-scripts/demo-scripts/basic_msg_client.al",
      "if !enable_opcua == true then process !anylog_path/deployment-scripts/demo-scripts/opcua_client.al", 
      "if !enable_aggregations == true then set aggregations where dbms=!default_dbms and intervals=!aggregations_intervals and time=!aggregations_time and time_column=!aggregation_time_column and value_column=!aggregation_value_column", 
      "if !monitor_nodes == true then process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al",
      "if !syslog_monitoring == true then process !anylog_path/deployment-scripts/demo-scripts/syslog.al",
      "if !deploy_local_script == true then process !local_scripts/local_script.al",
      "if !is_edgelake == false then process !local_scripts/policies/license_policy.al"
    ],
    "id" : "87ac01c5b6e4a95fb7f96898a5bf8cc0",
    "date" : "2025-05-15T22:20:38.799160Z",
    "ledger" : "global"
}}
```
6. AnyLog will then deploy / configure the different services based on the configuration policy.  
> `!` is the equivalent of `$` for AnyLog/EdgeLake. 

### What is the purpose of the Cluster policy and how does it work?

The _cluster_ policy is a logical policy that defines the relationship between Operator nodes, enabling high availability 
HA) and informing members of the network about the location and distribution of data. Each Operator node belongs to a 
Cluster, and a Cluster can consist of multiple Operator nodes. 

When an operator receives new data one of the things it does is check whether the table (and cluster) definition exist both 
locally and on the blockchain (as metadata). this information is then used by all other members of the network to query 
and share the data. 

### How does AnyLog ensure data consistency across Operator nodes?

Each operator node has a management database that keeps track of the files coming in, where they came from and where 
they went (for HA). This guarantees consistency, validation and remove of repeating data (files).      

### Can a single AnyLog node perform multiple roles at once?

A node can perform different roles based on the enabled services and databases it is connected to. The only limitation is 
enabling the operator and publisher services on the same instance.

### How is data partitioned in AnyLog and why do some tables have the par_ prefix?

AnyLog / EdgeLake partition the data automatically for the user. This can be disabled 
or personalized in the configuration file. When executing a query, AnyLog/EdgeLake basically scans only the relevant 
partitioned rather than the entire data, making it that much more efficient. 

Details can be found in <a href="../metadata%20requests.md#creating-data-tables" target="_blank">Metadata Requests</a>.

### What are the hardware or resource requirements for running different node types?
| Feature            | Requirement                                                                                                                                                                                        |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Operating System**| Linux (Ubuntu, RedHat, Alpine, Suse) <br> Windows  <br> Mac                                              
                                                                                          |
| **Memory footprint**| 100 MB available for AnyLog deployed without Docker <br> 300 MB available for AnyLog with Docker                                                                                                   |
| **Databases**       | PostgreSQL installed (optional) <br> SQLite (default, no installation needed) <br> MongoDB (only if blob storage is needed)                                                                        |
| **CPU**             | Intel, ARM, and AMD architectures supported <br> Runs on single CPU machines up to large multi-core servers (including gateways, Raspberry Pi, etc.)                                               |
| **Storage**         | Supports horizontal scaling by adding nodes dynamically <br> Storage requirements depend on data volume and retention per node <br> Automated archival and data transfer to larger nodes supported |
| **Network**         | TCP-based network required (local, internet, or hybrid) <br> Overlay networks recommended (Nebula is default) <br> Static IP and 3 open ports accessible per node (via overlay or direct network)  |
| **Cloud Integration**| Built-in support for REST, Pub-Sub, and Kafka                                                                                                                                                      |
| **Deployment Options**| Executable (background process), Docker, or Kubernetes                                                                                                                                             |

Please visit <a href="../training/prerequisite.md" target="_blank">prerequisite.md</a> for farther details. 

### How do I monitor the health and status of nodes in the AnyLog network?

AnyLog (and EdgeLake) have alert and monitoring capabilities that both on the machine level (ex. CPU, RAM, Network I/O and disk usage)
as well as on the data level. 

Details can be found in <a href="../alerts%20and%20monitoring.md" target="_blank">alerts and monitoring.md</a>.

### What is the difference between blockchain abstraction in EdgeLake and AnyLog Enterprise?


### How do I handle node failures or network partitions?


### Is it possible to upgrade EdgeLake to AnyLog Enterprise?

Since AnyLog builds on top of EdgeLake and a node its services based on user-defined configurations, update is as simple
as updating the image name in the docker-compose file from `anylogco/edgelake` to `anylogco/anylog-network`.

Directions for upgrading can be found <a href="" target="_blank">here</a>.

