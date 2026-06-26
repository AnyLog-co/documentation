---
title: Live Data Generator
description: Connect to AnyLog's shared data generator and ingest synthetic industrial data in minutes.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

AnyLog provides two tools that work together for testing and demos:

- **Python data generator** (`data_generator_main.py`) — publishes synthetic industrial data via REST, MQTT, or OPC-UA
- **AnyLog `.al` scripts** (`data-generator/`) — declare mapping policies and `run msg client` on the operator node to receive that data

---

## Live MQTT broker

AnyLog runs a shared MQTT broker that continuously publishes data for all supported datasets. Connect your operator directly to skip running the Python generator locally.

| Parameter | Value |
|---|---|
| Broker | `172.104.228.251` |
| Port | `1883` |
| Username | `anyloguser` |
| Password | `mqtt4AnyLog!` |

---

## How it works — end to end flow

```
[ Python generator ]          [ AnyLog Operator Node ]
  data_generator_main.py
         │
         │  MQTT / REST POST / PUT
         ▼
  ┌─────────────┐       1. process mapping/*.al   → declare mapping policy on blockchain
  │  MQTT broker │  →   2. process [dataset].al   → declare run msg client + subscribe
  │  (or REST)   │      3. get msg client          → verify streaming is active
  └─────────────┘       4. query data              → run client () sql ...
```

**Step 1 — Mapping policy** defines the schema: which fields map to which columns and types. Stored on the blockchain so any node in the network can use it.

**Step 2 — `run msg client`** connects to the broker, subscribes to the topic(s), and maps incoming JSON to the target database and table using the policy.

**Step 3 — `get msg client`** verifies the subscription is active and shows message counts.

**Step 4 — Query** data is immediately queryable once ingested.

---

## deployment-scripts/data-generator — file reference

```
data-generator/
├── drone_telemetry.al          ← drone swarm telemetry (REST POST)
├── oil_rig_data.al             ← drilling metrics, 6 rigs, multiple topics
├── rand_data.al                ← simple timestamp/value (MQTT)
├── vessel_data.al              ← electric boat battery + charger data
├── wind_turbine_data.al        ← wind farm metrics across 10 turbines
├── mqtt_enterprise_c_sub.al    ← Enterprise C ProveIT data (MQTT)
├── opcua_enterprise_a.al       ← Enterprise A ProveIT data (OPC-UA)
└── mapping/
    ├── drone_mapping.al
    ├── rig_rig-data.al
    ├── vessel_BATTERY-PACK-DEVICE-LOGS.al
    ├── vessel_BATTERY-PACK-LOGS.al
    ├── vessel_CHARGER-DEVICE-LOGS.al
    ├── vessel_CHARGER-LOGS.al
    ├── vessel_VESSEL-POWER-LOGS.al
    ├── vessel_VESSEL-STATE-LOGS.al
    ├── wind_turbine_available-power.al
    ├── wind_turbine_blade-pitch.al
    ├── wind_turbine_energy.al
    └── wind_turbine_reactive-power.al
```

### Non-mapping scripts — process commands

| File | Process command | Data source |
|---|---|---|
| `rand_data.al` | `process !local_scripts/data-generator/rand_data.al` | `anylog-demo` topic — timestamp + value |
| `oil_rig_data.al` | `process !local_scripts/data-generator/oil_rig_data.al` | `rig-data/*` topics — drilling metrics |
| `vessel_data.al` | `process !local_scripts/data-generator/vessel_data.al` | `vessel-data/DLT` + `vessel-data/DLB` — battery + charger |
| `wind_turbine_data.al` | `process !local_scripts/data-generator/wind_turbine_data.al` | `wind-turbine/*` topics — 10 turbines |
| `drone_telemetry.al` | `process !local_scripts/data-generator/drone_telemetry.al` | `drone-telemetry` topic — REST POST |
| `mqtt_enterprise_c_sub.al` | `process !local_scripts/data-generator/mqtt_enterprise_c_sub.al` | ProveIT Enterprise C |
| `opcua_enterprise_a.al` | `process !local_scripts/data-generator/opcua_enterprise_a.al` | ProveIT Enterprise A (OPC-UA) |

Each script internally calls the relevant `mapping/*.al` files first, then declares `run msg client`.

---

## Python data generator

> **Repo:** [AnyLog-co/Sample-Data-Generator](https://github.com/AnyLog-co/Sample-Data-Generator) (branch: `data-generator2`)

### Architecture

```
Southbound (generates data)        Northbound (publishes)
──────────────────────────         ──────────────────────
random_data.py          ─────────► REST PUT
rig_data.py             ─────────► REST POST
vessel_data.py          ─────────► MQTT
wind_turbine.py         ─────────► OPC-UA (Proveit only)
proveit_data.py
```

### Supported datasets and publish formats

| Dataset | `data` argument | Publish formats | Tables |
|---|---|---|---|
| Random timestamp/value | `random` | print, put, post, mqtt | `rand_data` |
| Oil rig drilling | `rig` | print, put, post, mqtt | `rig_data` |
| Electric vessel | `vessel` | print, post, mqtt | 6 tables (battery, charger, power, state) |
| Wind turbine | `wind-turbine` | print, post, mqtt | 4 tables per turbine |
| Wind turbine v2 | `wind-turbine2` | print, post, mqtt, opcua | farm/turbine hierarchy |
| ProveIT 2026 | `proveit` | print, post, mqtt, opcua | Enterprise A / B / C |

### Usage

```bash
python data_generator_main.py [dataset] [publish_format] [options]
```

**Global options:**

| Option | Default | Description |
|---|---|---|
| `--control-conn IP:PORT` | — | AnyLog node used to declare mapping policies and `run msg client` |
| `--data-conn IP:PORT` | = `control-conn` | Data destination (REST/MQTT). Defaults to `control-conn` if omitted |
| `--db-name NAME` | `test` | Logical database name |
| `--repeat N` | `10` | Iterations. `0` = run continuously |
| `--sleep SECONDS` | `15` | Delay between iterations |
| `--offset-sleep SECONDS` | `0.5` | Delay between multiple IDs per iteration |
| `--skip-msg-client` | false | Skip declaring `run msg client` (useful if already running) |
| `--skip-inserts` | false | Only declare the `run msg client`, skip data publishing |

**Dataset-specific options:**

| Option | Dataset | Description |
|---|---|---|
| `--ids 1 3 7` | `rig` | Rig IDs to publish (default: all 6) |
| `--ids DLB DLT` | `vessel` | Engine sides (default: both) |
| `--ids 1 3 7` | `wind-turbine` | Turbine IDs 1–11, excluding 4 (default: all) |
| `--topics "Enterprise A"` | `proveit` | ProveIT topic groups (default: all) |

### Examples

```bash
# Print random data to console — no connection needed
python data_generator_main.py random print

# Publish all rigs via MQTT to local AnyLog broker
python data_generator_main.py rig mqtt --control-conn 127.0.0.1:32149 --data-conn 127.0.0.1:32150

# Publish specific rigs only
python data_generator_main.py rig mqtt --control-conn 127.0.0.1:32149 --data-conn 127.0.0.1:32150 --ids 1 3

# Publish all wind turbines except 4 via REST POST
python data_generator_main.py wind-turbine post --control-conn 127.0.0.1:32149

# Publish specific turbines
python data_generator_main.py wind-turbine post --control-conn 127.0.0.1:32149 --ids 2 7

# Vessel DLB side only
python data_generator_main.py vessel mqtt --control-conn 127.0.0.1:32149 --data-conn 127.0.0.1:32150 --ids DLB

# Run continuously (repeat=0)
python data_generator_main.py random mqtt --control-conn 127.0.0.1:32149 --data-conn 127.0.0.1:32150 --repeat 0 --sleep 5
```

---

## Validating ingestion on the operator

After running either the Python generator or a `process` command, verify on the operator node:

```anylog
# Check the msg client is subscribed and receiving
get msg client

# Check streaming buffer status
get streaming

# Query the data
run client () sql mydb format=table "SELECT * FROM rand_data ORDER BY timestamp DESC LIMIT 10"
```