1. Orchestration install -- @Mark
* [03- Barbara.md](02-%20Installation%20%26%20Deployment/03-%20Orchestrators/03-%20Barbara.md)
* [04- DELL Distributed Private Cloud.md](02-%20Installation%20%26%20Deployment/03-%20Orchestrators/04-%20DELL%20Distributed%20Private%20Cloud.md)
* [05- Zededa.md](02-%20Installation%20%26%20Deployment/03-%20Orchestrators/05-%20Zededa.md)* 

2. [02- TMP Configuration.md](06-%20Networking%20%26%20Security/07-%20Security/02-%20Trusted%20Platform%20Module%20%28TPM%29/02-%20TMP%20Configuration.md) -- @Roy / @Massimiliano 

3. Edge Dta Manager -- @Roy 
there should be the following files: 

10- EDM (Edge Data Manager)/ 👤 100% Roy
  |- edm.md <-- Main EDM overview.
  |   📍 11- EDM tool (Edge Data Manager)/02 EDM.md
  |   ⚠️ Not accounted for anywhere in this plan: 11- EDM tool (Edge Data Manager)/01 remote-gui.md, also
  |      present in the source folder.
  |- install.md 🆕
  |   Purpose: EDM installation process.
  |- UNS.md 🆕
  |   Purpose: Explain EDM integration with UNS.
  |- MCP.md 🆕
  |   Purpose: Explain EDM MCP integration.
  |- add-remove-plugins.md 🆕
  |   Purpose: Plugin lifecycle management.
  |   Topics:
  |      - Add plugins
  |      - Remove plugins
  |      - Configure plugins
document explaining how to query blobs through an application using `file to` and `file from` logic 


4. We need Examples & Use Cases -- @Mark 


# Examples & Use Cases

The following provides an array of examples on deploying AnyLog and EdgeLake from start to finish.

## Example 1 — Standalone Deployment with MQTT

A standalone deployment with random timestamp/value data coming in via MQTT.

This example demonstrates:
1. How to install a standalone AnyLog agent with the default configs, with random data flowing in via MQTT.
2. Attaching to and detaching from the node.
3. Simple queries via the CLI and REST.

## Example 2 — Node Monitoring & Network Testing

A small network — master, operator, and query as independent agents on the same machine — with monitoring data
flowing in.

This example demonstrates:
1. How to install multiple nodes, and understanding `LEDGER_CONN`.
2. Inserting data via a scheduled process — node/Docker monitoring and syslog monitoring.
3. Querying the data.

## Example 3 — Smart City Demo

Replicates our Smart City demo.

This example demonstrates:
1. Installing a small network with 3 operators, including directions on using Postgres.
2. Querying across nodes.
3. Using MCP and an LLM to generate dashboards.

## Example 4 — Live Video Streaming

TBD
