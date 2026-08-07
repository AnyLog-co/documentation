---
title: Deployment Scripts — Integration Reference
description: Internals reference — why deployment-scripts exists, how policies and scripts communicate, and the execution model behind them.
layout: page
visibility: public
version: open source
tags:
- getting-started
- integration
---
<!--
## Changelog PUT LATEST CHANGES AT THE TOP PLEASE
-
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606
- 2026-07-09:** changed in this revision:
- Fixed heading level: "Last resort: forking the shipped scripts directly" was a sub-heading (`###`) under option 3;
  promoted to a top-level option (`##`) since it's a fourth choice, not a detail of option 3.
- Added an explicit cross-link to `04- deployment-process.md` next to the condensed table, so the two tables don't
  silently drift out of sync if the build logic changes.
- Expanded the "entry script isn't named `main.al`" section into two concrete, copy-pasteable overrides: one for
  docker-compose, one for `docker run` — including the tradeoff of bypassing `deploy_anylog.sh`'s other setup steps
  when you do this.
- `customizing-scripts.md` was retired (merged into `04- deployment-process.md`). The cross-link at the top now
  points to `04- deployment-process.md`'s "Pointing at Your Own Deployment-Scripts" / entry-point-override sections
  instead.
- No other content changes — this file remains the internals/mechanics reference (policy/script communication,
  process vs. thread). That content stays here rather than moving to `04- deployment-process.md`.
--->

# AnyLog / EdgeLake Deployment Scripts — How They Work

*A reference for understanding the `deployment-scripts` repository: why it exists, how policies and scripts communicate,
and the execution model behind them.*

This document covers:

1. [Why This Repository Exists](#why-this-repository-exists)
2. [The Deployment Flow](#the-deployment-flow)
3. [How Policies and Scripts Actually Communicate](#how-policies-and-scripts-actually-communicate)
4. [`process` vs. `thread` — the Execution Model](#process-vs-thread--the-execution-model)

## Why This Repository Exists

`deployment-scripts` is the **default deployment toolkit for AnyLog and EdgeLake nodes**. It contains the scripts that
set up, configure, and manage a node so that a user doesn't have to hand-write deployment logic every time.

Two things make this repo work the way it does:

- **It's downloaded automatically** when a node runs via Docker, Podman, or Kubernetes — the container pulls this repo in and executes it as part of startup.
- **It's config-driven.** A user doesn't write deployment code. They set environment variables and/or a policy, and the scripts in this repo translate that into a running, networked, database-backed AnyLog/EdgeLake node.

The core idea: separate what an agent should be (declared once, as config) from how that gets built (scripts, written
once, reused everywhere).

For the full build-time/runtime mechanics of *how* this repo actually gets loaded into a container (default image, host
bind mount, reclone-at-startup, or a secondary container), how to point at your own repo, and how to override the entry
point, see [Deployment Integration](04- deployment-process.md).

**Repository Structure**
```
├───node-deployment             <- Core deployment orchestration (start here)
│   ├───main.al                        <- Entry orchestrator: env→params, call policy generator, end-of-script check
│   ├───set_params.al                  <- Converts $ENV_VARS into !anylog_variables, with defaults
│   ├───connect_blockchain.al          <- Connects to blockchain platform (master or optimism) and starts sync
│   ├───local_script.al                <- Empty placeholder hook for user custom logic (runs if DEPLOY_LOCAL_SCRIPT=true)
│   ├───blockchain.md                  <- Docs
│   ├───database                       <- Database setup and initialization
│   │   ├───deploy_database.al              <- Dispatcher: routes to the right DB setup scripts based on !node_type
│   │   ├───configure_dbms_blockchain.al    <- Creates the `blockchain` logical db + `ledger` table (master nodes)
│   │   ├───configure_dbms_almgm.al         <- Creates the `almgm` logical db + `tsd_info` table (publisher/operator)
│   │   ├───configure_dbms_operator.al      <- Connects the operator's default dbms; sets up partitioning if enabled
│   │   ├───configure_dbms_monitoring.al    <- Sets up `monitoring` db partitioning (12h partitions, 36h retention)
│   │   ├───configure_dbms_nosql.al         <- Connects a NoSQL (Mongo) db and enables the blobs archiver
│   │   ├───configure_blob_storage.al       <- Validates blob-storage config, connects storage, enables blobs archiver
│   │   ├───connect_dbms_sql.al             <- Generic SQL connection helper (PostgreSQL / SQLite)
│   │   ├───connect_dbms_nosql.al           <- Generic NoSQL connection helper (MongoDB)
│   │   ├───connect_dbms_objstore.al        <- Object storage connection helper (Akave / S3 / MinIO)
│   │   └───connect_dbms_system_query.al    <- Connects the `system_query` db (query / system-query-enabled nodes)
│   └───policies                       <- Policy declaration scripts (configuration, cluster, node, license, blockchain...)
│       ├───config_policy.al             <- THE dispatcher — builds, publishes, and applies the node's full config policy
│       ├───config_policy_networking.al  <- Fills in networking fields (ip/port/rest/broker) into the config policy
│       ├───cluster_policy.al            <- Declares/publishes the cluster policy (operator nodes)
│       ├───node_policy.al               <- Declares/publishes the node's own identity policy
│       ├───validate_node_policy.al      <- Checks whether a matching node policy already exists on the blockchain
│       ├───blockchain_policy.al         <- Declares a blockchain-info policy (live/optimism blockchain use)
│       ├───license_policy.al            <- Declares/activates the license policy (AnyLog only — skipped for EdgeLake)
│       ├───hzn_policy.al                <- Declares an Open Horizon (HZN) policy, if HZN_* env vars are set
│       └───publish_policy.al            <- Generic helper — signs, validates, publishes any policy to the blockchain
├───data-generator              <- Scripts for ingesting sample/test data
├───gRPC                        <- Sample gRPC connections, protocol defs, compilation utilities
├───sample-scripts              <- Scripts for receiving data from third-party applications
├───southbound-industrial       <- Sample Ingest from OPC-UA, Modbus, EtherIP, and other industrial protocols
├───southbound-monitoring       <- Sample Node/Docker/syslog monitoring collection scripts
├───southbound-video-streaming  <- Sample Video stream ingestion scripts
├───test-network-local-scripts  <- Scripts used by the local test network
└───aggregations                <- Sample Scripts to configure streaming data aggregation
```

`main.al` itself only does three things
* convert env vars to params
* call the policy generator
* do an end-of-script check.

It never directly touches any of the actual deployment-script processes that define databases and/or services for
a given node. Those actions get reached indirectly, because the policy generator (`policies/config_policy.al`) defines and
applies / executes a node-type-specific list of instructions.


## The Deployment Flow

Everything starts with one command:

```bash
# AnyLog
./anylog_node process deployment-scripts/node-deployment/main.al

# EdgeLake
./edgelake_node process deployment-scripts/node-deployment/main.al
```

When main initiates it does the following steps:
1. enables `echo queue` and disables authentication
    * `echo queue` is a print like logic that stores content to a `get event log` like structure rather than print to screen. The default deployment process uses it in order to record errors that might not have been caught by the error log
    * `authentication` is disabled at start up but maybe enabled at a later point through configuration policies. This is so the node can easily accept an initial copy of the blockchain and set any relationships it may need without needing to worry about public / private keys
2. define relative paths to be used through out (ex. `!local_scripts`)
3. convert environment variables (`-e` in docker) to AnyLog variables (found in dictionary)
4. define the config policy for the node if one does not exists.


## How Policies and Scripts Actually Communicate

This is the part that's easy to misread as "the policy contains the deployment code." It doesn't. Here's the real mechanism.

A **policy** is a piece of declarative JSON, published to the AnyLog blockchain/ledger, that describes what a node *is*.
Note the example below uses AnyLog's own single-quoted policy syntax rather than strict JSON (which requires double
quotes) — this is the format AnyLog commands actually accept, not a typo:

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

Notice that within the config policy we are defining the relative network configurations (`'!anylog_server_port.int'`)
as opposed to hardcoded (`32148`), followed by the actual databases and services need for the given instance type.

The reason the config policy uses relative network configuration is so that the same policy can be reused across multiple
instances of the same type.


The communication works like this:

1. **The policy's `script` field is a list of instructions, not implementation.** Each line is either a `process` call to
a `.al` file, or a direct AnyLog command (`run scheduler`, `run streamer`, `run operator where ...`). The choice between
a script and a raw command depends on whether there are dependencies to resolve first — for example, connecting to a
logical database where the user defines the db type — versus a standalone command that's simply required for this type
of AnyLog agent (e.g. `run operator`).

2. **Every `!variable` referenced in the policy** (`!anylog_server_port`, `!operator_id`, `!enable_ha`, `!deploy_local_script`, etc.)
was already set by `set_params.al` in the previous step, and could be unique per Agent / container. The policy doesn't
compute these values — it just consumes them.

3. **Conditionals live in the policy, logic lives in the scripts.** Lines like `'if !enable_ha == true then run data distributor'`
mean the policy decides *whether* a capability turns on, but the actual mechanics of what "run data distributor" does are
internal to AnyLog/EdgeLake or defined in the referenced `.al` file — never inlined into the policy itself.

4. **The policy is data first.** Because it's stored on the blockchain as part of our metadata, ie a ledger record, it needs
to stay small, inspectable, and diffable — a list of strings and key/value pairs, not an executable program. This is
*why* it calls out to scripts rather than embedding them: the ledger holds intent, the filesystem holds mechanism.

The "communication" between a policy and the scripts is really just **variable substitution + ordered dispatch**:
`set_params.al` populates the variable namespace, the policy reads that namespace to decide what to enable and in what
order, and each `process` line in the policy's `script` array hands control to a dedicated file that knows how to carry
out one piece of that intent (database setup, cluster/node policy declaration, monitoring, industrial ingestion,
licensing).

## `process` vs. `thread` — the Execution Model

The reason this repository cares about `process` vs. `thread` at all isn't academic — it matters the moment you go from
*using* the default deployment scripts to *writing or modifying your own* (see
[Deployment Integration](04- deployment-process.md)). Every script you add has to make the same choice every
built-in script makes: does this need to block until it's done, or can it run alongside everything else?

Both commands do the same basic thing — **run the commands in a script file** — but they differ in *how* that execution
relates to the caller:

```
help process
        Usage: process [path and file name]
        Explanation: Process the commands in the specified file

help thread
        Usage: thread [path and file name]
        Explanation: Initiate a new thread to process the commands in the specified file
```

| | `process` | `thread` |
|---|---|---|
| Execution | Runs in the **current** execution context | Spawns a **new thread** to run the file |
| Blocking? | Yes — the caller waits for it to finish (synchronous) before moving to the next line | No — the caller continues immediately; the file runs concurrently (asynchronous) |
| Use case | Ordered setup steps where each step depends on the previous one having finished | Independent, long-running, or parallel work that shouldn't block the main flow |

### Why the deployment scripts use `process` almost everywhere

Look back at `main.al` and every policy `script` array — they're built almost entirely out of `process` calls. That's
not incidental: **deployment is a strictly ordered dependency chain.**

- The AnyLog agent cannot define itself as an operator before it knows which cluster the instance would ultimately belong to.
- The AnyLog agent cannot run the database deployment logic before `set_params.al` has populated the variables it references.
- You can't enable monitoring or industrial ingestion meaningfully before the node's core identity (ports, database,
blockchain connection) exists.

If these were dispatched with `thread`, they'd all fire off concurrently with no guarantee of ordering — and the second
step might run before the first step's variables or policies exist, breaking the deployment. `process` guarantees
"step 2 only starts once step 1 is fully done," which is exactly the contract this repo depends on.

`thread` becomes the right tool when you *want* concurrency — e.g., running two independent, long-lived monitoring or
ingestion loops side-by-side without one blocking the other. That's a pattern you'd reach for in custom/local scripts
for things like parallel MQTT listeners, rather than in the core deployment sequence itself.

**Rule of thumb:** if step B needs something step A produced (a variable, a policy, a database), use `process`. If step A
and step B are independent and both need to run continuously/concurrently, `thread` is the right call.

There's an exception to the rule though — when running a process in a scheduled manner, as the deployment-scripts do
with monitoring, each command runs in its own thread otherwise the CLI would not be accessible to the user most of the time.