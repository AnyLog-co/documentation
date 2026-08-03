---
title: Using REST
description: Execute AnyLog commands and publish data over HTTP using GET, PUT, and POST.
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**                                                                                     | **Version** |
 |------------|----------------|------------------------------------------------------------------------------------------------|----------|
 | 2026-04-17 |                | creation                                                                                       |  |
 | 2026-04-23 |                | added POST as GET alternative, AnyLog-Agent header, blockchain insert command, Python examples |  |
 | 2026-04-24 |                | there was an issue with the REST POST of commands example                                      |  |
 | 2026-04-25 |                | REST GET via browser support                                                                                               |  |
 | 2026-04-25 |                | hyperlink support                                                                                               |  |
 | 2026-07-20 | Eric Aquaronne | added change log                                                                               | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Fixed several real bugs: the query-string GET example used repeated `?` instead of `&` between
   parameters; the table row for `test` was missing its closing pipe, breaking the table; one example's curl
   command was typo'd as `curp`; a comment label said "GET" over what is actually a POST request; "acame"
   → "Acme" (and standardized casing on "Acme" throughout — examples mixed "Acme"/"acme"); removed the invalid
   trailing `....` inside a JSON literal. Fixed typos ("network network," "currebly," "over comes," "the the").
   Reworded two hard-to-parse sentences (the SQL-only empty-parentheses caveat, and the User-Agent explanation)
   without changing their meaning. Flagged, not resolved: the blockchain-insert example mixes a header-based
   command with a form-style `-d` body for the policy variable — a third request pattern not covered by the
   HTTP method mapping table above; worth a clarifying sentence once someone can confirm the intended mechanics.
--->

Any AnyLog node with the REST service enabled, can receive commands and data over HTTP. This lets external applications, 
dashboards, and scripts interact with the network without running AnyLog themselves.

---

## HTTP method mapping

| Method | Used for |
|---|---|
| `GET` | Retrieve information — `sql`, `get`, `blockchain get`, `help` |
| `GET` (query string) | Browser-native GET — command and options passed as `?key=value&key=value` parameters |
| `POST` | All commands (alternative to GET) and data publishing via topic mapping |
| `PUT` | Publish time-series data directly to a node |


### The AnyLog commands supported by REST

| AnyLog command | HTTP Method       | Comments |
|----------------|-------------------|--------------------------------------------------------------------------------|
| GET            | sql               | Issue queries to data hosted by nodes of the network                          |
| GET            | help              | Help on the AnyLog commands                                                    |
| GET            | get               | Retrieve information from nodes members of the network                         |
| GET            | blockchain get    | Query the metadata that is considered by the node                              |
| GET            | blockchain read   | Query the disk image of the metadata                                           |
| POST           | blockchain drop   | Drop a policy                                                                  |
| GET            | query status      | Retrieve the status of the currently or previous executed queries              |
| GET            | query explain     | Explain how the currently or previous queries are processed                    |
| GET            | query destination | Detail the participating nodes in each query                                   |
| GET            | job status        | Retrieve status info on jobs assigned to the rule engine                       |
| GET            | job active        | Retrieve status info on the currently executed jobs assigned to the rule engine |
| POST           | job run           | Execute a specific job assigned to the rule engine                             |
| POST           | job stop          | Stop the execution of a specific job assigned to the rule engine               |
| GET            | file get          | Copy a file from a remote node to the local node                               |
| GET            | file retrieve     | Retrieve a file or files from the designated database                          |
| POST           | file store        | Insert a file into the blobs dbms                                              |
| POST           | file to           | Copy a file to a folder                                                        |
| GET            | test              | Issue a test command                                                          |
| POST           | reset             | Issue a reset command                                                          |
| POST           | process           | Process an AnyLog script file                                                  |


## `run client ()` vs `destination` header 

When running AnyLog via the CLI, the `run client ()` command tells the node to send the request across the network.
When the parentheses are empty — as in `run client ()` — and only for SQL commands, the network automatically scans
the blockchain ledger to determine where the relevant data resides.

The command can also take manually defined connection information, sending the request directly to a given node
instead of needing to scan the blockchain:

```anylog
# specific IP:port
run client (10.1.10.15:32148) [anylog command]

# send to all operators 
run client (blockchain get operator where company=Acme bring.ip_port) [anylog command]
```

**Note:** the `[IP]:[port]` used here is the **TCP** port, not the REST port.

When running over REST, the header `destination` replaces `run client (...)`:
* AnyLog command: `run client ()` → REST header: `-H "destination: network"` 
* AnyLog command: `run client (blockchain get operator where company=Acme bring.ip_port)` → `-H "destination: blockchain get operator where company=Acme bring.ip_port"`

## `AnyLog-Agent` vs `User-Agent` 

`User-Agent` is a standard HTTP header meant to identify the client making the request. Under certain conditions,
though, browsers and browser-based clients can run into a **CORS** (Cross-Origin Resource Sharing) failure: the
server and browser have to agree on allowed origins, methods, and headers, and `User-Agent` is one of the headers
browser JavaScript is not allowed to set or override — it's on the browser's "forbidden header" list, so scripts
running in a browser can't reliably control its value.

To avoid depending on a header the client may not fully control, AnyLog also accepts `AnyLog-Agent` as an
equivalent, and it's the one we recommend using.

## Examples

* check node status 
```shell
# basic GET request for status
curl -X GET http://[Node IP]:[Node REST Port] \
  -H "command: get status" \
  -H "AnyLog-Agent: AnyLog/1.23"

# basic POST request for status 
curl -X POST http://[Node IP]:[Node REST Port] \
  -H "Content-Type: application/json" \
  -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}'
  
# POST request for status, scoped to operators where `company=Acme`
curl -X POST http://[Node IP]:[Node REST Port] \
  -H "Content-Type: application/json" \
  -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23", "destination": "blockchain get operator where company=Acme bring.ip_port"}'
```

* publish blockchain policy - this is only a _POST_ command.
The `blockchain insert` command is interesting as the destination is part of the command as opposed to being part of the header. 
The document [blockchain.md](../08-%20Blockchain%20&%20Metadata/01-%20Blockchain.md) provides more information. 

```shell
curl -X POST  http://[Node IP]:[Node REST Port] \
  -H "command: blockchain insert where policy=!new_policy and local=true and master_node=!ledger_conn" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -d 'new_policy={"my-policy": {"name": "my policy 3", "company": "Acme"}}'
```

* execute query 

```shell
# example using GET where destination is "unknown" 
curl -X GET http://[Node IP]:[Node REST Port] \
  -H "command: sql mydb format=json:list and stat=false SELECT * FROM my_data" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "destination: network"

# example using POST against a specific operator 
curl -X POST http://[Node IP]:[Node REST Port] \
  -H "Content-Type: application/json" \
  -d '{"command": "sql mydb format=json:list and stat=false SELECT * FROM my_data", "AnyLog-Agent": "AnyLog/1.23", "destination": "10.0.0.73:32148"}'
```