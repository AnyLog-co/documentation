---
title: Using REST
description: Execute AnyLog commands and publish data over HTTP using GET, PUT, and POST.
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**                                                                                     | **Version** |
 |------------|----------------|------------------------------------------------------------------------------------------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log                                                                               | 2.0.2606 |
 | 2026-04-25 |                | hyperlink support                                                                                               |  |
 | 2026-04-25 |                | REST GET via browser support                                                                                               |  |
 | 2026-04-24 |                | there was an issue with the REST POST of commands example                                      |  |
 | 2026-04-23 |                | added POST as GET alternative, AnyLog-Agent header, blockchain insert command, Python examples |  |
 | 2026-04-17 |                | creation                                                                                       |  |
--->

Any AnyLog node with the REST service enabled, can receive commands and data over HTTP. This lets external applications, 
dashboards, and scripts interact with the network without running AnyLog themselves.

---

## HTTP method mapping

| Method | Used for |
|---|---|
| `GET` | Retrieve information — `sql`, `get`, `blockchain get`, `help` |
| `GET` (query string) | Browser-native GET — command and options passed as `?key=value?key=value` parameters |
| `POST` | All commands (alternative to GET) and data publishing via topic mapping |
| `PUT` | Publish time-series data directly to a node |


### The AnyLog commands supported by REST

| AnyLog command | HTTP Method       | Comments |
|----------------|-------------------|--------------------------------------------------------------------------------|
| GET            | sql               | Issue queries to data hosted by nodes of the network network                   |
| GET            | help              | Help on the AnyLog commands                                                    |
| GET            | get               | Retrieve information from nodes members of the network                         |
| GET            | blockchain get    | Query the metadata that is considered by the node                              |
| GET            | blockchain read   | Query the disk image of the metadata                                           |
| POST           | blockchain drop   | Drop a policy                                                                  |
| GET            | query status      | Retrieve the status of the currently or previous executed queries              |
| GET            | query explain     | Explain how the currently or previous queries are processed                    |
| GET            | query destination | Detail the participating nodes in each query                                   |
| GET            | job status        | Retrieve status info on jobs assigned to the rule engine                       |
| GET            | job active        | Retrieve status info on the currebly executed jobs assigned to the rule engine |
| POST           | job run           | Execute a specific job assigned to the rule engine                             |
| POST           | job stop          | Stop the execution of a specific job assigned to the rule engine               |
| GET            | file get          | Copy a file from a remote node to the local node                               |
| GET            | file retrieve     | Retrieve a file or files from the designated database                          |
| POST           | file store        | Insert a file into the blobs dbms                                              |
| POST           | file to           | copy a file to a folder                                                        |
| GET            | test              | Issue a test command
| POST           | reset             | Issue a reset command                                                          |
| POST           | process           | process an AnyLog script file                                                  |

