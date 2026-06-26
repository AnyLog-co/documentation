---
title: FAQ & Troubleshooting
description: Common questions, known issues, and troubleshooting guidance for AnyLog deployments.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-23 | Added REST/CORS/AnyLog-Agent, POST vs GET, blockchain insert, mapping policy pitfalls, MCP, Docker networking sections
-->

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

See <a href="{{ '/docs/network-services/using-rest/' | relative_url }}">Using REST</a> for full examples and Python code.

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

See <a href="{{ '/docs/docs/mcp-ai-integration/#browser-connection-modes' | relative_url }}">MCP & AI Integration</a> for setup details.