---
title: Deployment Scripts
description: A general sense orientation to how AnyLog's deployment-scripts repository configures and launches a node.
layout: page
visibility: public
version: open source
tags:
- install
- getting-started
---
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**      | **Version** |
 |------------|----------------|------------------|----------|
 |            |                |                  |          |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 |            |

## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks
- 2026-04-25 | updated [page.html](../../_layouts/page.html) to support pop-up for env configs 
- 2026-07-12 | 
    - Restructured around 4 sections: the AnyLog/deployment-scripts split, repo structure (top-level only —
      see 09- Integrations for the file-by-file tree), what happens at startup + local_script.al, and the
      DEPLOYMENTS_REPO/DEPLOYMENTS_BRANCH env vars (including the default = `main`, built into the image).
    - Intentionally kept at "general sense" depth — internals, policy/script mechanics, process vs thread, and
      the full build/runtime env-var matrix live in 09- Integrations instead.
- 2026-07-12 (rev 2) |
    - Grammar/typo pass: "that work with" -> "that works with", `local_scripts.al` -> `local_script.al`,
      "writting" -> "writing", stray double comma, missing "that" in the env-var sentence.
    - Split the local_script.al instructions into two labeled paths (auto-run on restart vs. edit-and-apply
      on an already-running node) instead of one ambiguous 4-step sequence.
    - Flagged two open items below for a decision: whether `test-network-local-scripts/` belongs in the
      top-level tree, and whether the "define relative paths" step belongs in the Deployment Process list.
-->

# Deployment Scripts

AnyLog's deployment-scripts is a GitHub repo that works with the configuration file to define which services are enabled,
and how they are configured.

In many ways the deployment scripts convert the AnyLog instance into an active agent that is part of the larger edge
network infrastructure.


## The structure of deployment-scripts

At a high level, the repo is organized like this:

```
deployment-scripts/
├── node-deployment/             ← core startup logic — always runs, for every node
├── data-generator/              ← sample scripts for ingesting test data
├── sample-scripts/              ← ready-to-run connector examples (MQTT, Telegraf, aggregation...)
├── southbound-industrial/       ← optional: OPC-UA, Modbus, and other industrial protocol ingestion
├── southbound-monitoring/       ← optional: node, Docker, and syslog monitoring
├── southbound-video-streaming/  ← optional: video ingestion and AI inference
├── gRPC/                        ← sample gRPC connections and protocol definitions
└── aggregations/                ← optional: streaming data aggregation setup
```

<!-- Open item: test-network-local-scripts/ also exists at the top level of the real repo but isn't listed
     above — confirm whether that's an intentional omission for a "general sense" audience, or should be added back. -->

The pattern worth internalizing: **`node-deployment/` is the only folder every node touches.** Everything else is
optional and only runs if you've turned the corresponding feature on.


## The Deployment Process

The following describes the steps within AnyLog once the AnyLog instance gets deployed and calls 
`process deployment-scripts/node-deployment/main.al`

1. Enables `echo queue` — `echo queue` is a print logic that stores output to a side queue the user can access,
rather than printing it to the screen.
2. Disable authentication — this is so that when the node first starts up, and has yet to define public/private keys for 
itself, it's able to send & accept an initial copy of the blockchain.
3. Convert the user defined environment variables (e.g. `-e NODE_TYPE=master`) into AnyLog variables (`!node_type`).
This includes resolving relative directory paths for `!local_scripts` and `!test_scripts`. 
4. Define a configuration policy on the blockchain, if one for this type of node does not yet exist. 
A sample policy is shown below.
   * Note, a configuration policy contains the variables for network connectivity, while using script paths for more 
   complex configurations like connecting to database and defining node specific policies.   
5. Using the configuration policy, enable the correct services with the user defined variables.


```json
{'config' : {
    'name' : 'operator-configs',
    'company' : 'My Company',
    'node_type' : 'operator',
    'ip' : '!external_ip',
    'port' : '!anylog_server_port.int',
    'rest_port': '!anylog_rest_port.int',
    'broker_port': '!anylog_broker_port.int',
    'tcp_threads': '!tcp_threads.int',
    'rest_threads': '!rest_threads.int',
    'broker_threads': '!broker_threads.int',
    'script' : [
      'process !local_scripts/connect_blockchain.al',
      'process !local_scripts/policies/cluster_policy.al',
      'process !local_scripts/policies/node_policy.al',
      'process !local_scripts/database/deploy_database.al',
      'run scheduler 1',
      'run streamer',
      'if !enable_ha == true then run data distributor',
      'if !operator_id and !blockchain_source != master then run operator where ...',
      'process !anylog_path/deployment-scripts/southbound-monitoring/config_monitoring_policy.al',
      'process !anylog_path/deployment-scripts/southbound-industrial/industrial_policy.al',
      'if !deploy_local_script == true then process !local_scripts/node-deployment/local_script.al',
      'if !is_edgelake == false then process !local_scripts/policies/license_policy.al'
    ],
    'id' : '2e54c04ce4e1241d41e68cbbd31a2469',
    'ledger' : 'global'
}}
```

### local_script.al

Within the config policy, there's a line that conditionally runs `!local_scripts/node-deployment/local_script.al`
(gated by the `!deploy_local_script` flag). This script is an empty file provided as a way to run "simple"
additional processes and scripts that a specific node may need but that aren't part of the default set of options.

Examples include things like ingesting from a unique southbound data source, or running a "complex" command
that's needed regularly (or manually) and isn't worth retyping every time.

**To have it run automatically on every restart:**
1. In the node configuration file, set `DEPLOY_LOCAL_SCRIPT=true`. This guarantees `local_script.al` automatically
runs whenever the node (re)starts.
2. Start the node.

**To edit and apply it while a node is already running (no restart):**
1. Access the `local-scripts` volume directly, or `exec` into the running container, and edit
`deployment-scripts/node-deployment/local_script.al` with the commands you need.
2. Attach to the AnyLog agent (`docker attach`) and manually apply the change by running:
`process !local_scripts/node-deployment/local_script.al`

If `DEPLOY_LOCAL_SCRIPT` isn't set to `true`, the script never runs automatically — manual `process` calls like the one
above are the only way it executes.

## A note on which deployment-scripts you're actually running

In `node_configs.env`, there are two environment variables that control the version of `deployment-scripts` the container uses:

```dotenv
DEPLOYMENTS_REPO="https://github.com/AnyLog-co/deployment-scripts"
DEPLOYMENTS_BRANCH="main"
```

**If you don't set these at all, you get the default** — the `main` branch of AnyLog's own `deployment-scripts` repo,
already baked into the Docker image. You only need to touch these two variables once you want to point at a different
branch, a local checkout on your machine, or your own fork entirely.

> The full breakdown of *how* that pointer is resolved (there are four different modes depending on what you set
> `DEPLOYMENTS_REPO` to) lives in **09- Integrations** — this page is just flagging that the knob exists and what
> happens if you leave it alone.