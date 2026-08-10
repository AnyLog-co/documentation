General Item : always put a line in the change log when editing a file, keep latest change at the top of the changelog

FILES NEEDING UPDATES/CONTENT

SECTION 03 (orchestration)  : 
all .MD files below need to be written by Mark who did the work
  02 IEAM 
  03 Barbara 
  04 DELL distrib cloud 
  05 Zededa 

SECTION 06 (netw & Secu)
  07 security
      02 TPM
          01 TMP config  : Roy and Massimiliano should write/expand this

SECTION 10 (EDM)
  01 EDM : this needs contents, from Roy 

  suggestion on subfiles
  |- edm.md : Main EDM overview.
  |- install.md : EDM installation process.
  |- UNS.md : Explain EDM integration with UNS.
  |- MCP.md : Explain EDM MCP integration.
  |- add-remove-plugins.md : Plugin lifecycle management (Add plugins, Remove plugins, Configure plugins)
  |- + document explaining how to query blobs through an application using `file to` and `file from` logic 

SECTION 11 (Estended Svces)
  03 Federated Learning : Roy should complete this

SECTION 12 Examples & Use Cases 
  we need more inside this section, Mark ? and Volunteers !

    Suggestions :
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

