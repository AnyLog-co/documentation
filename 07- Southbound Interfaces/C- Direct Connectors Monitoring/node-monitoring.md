---
title: Node Monitoring
description: Collect node health metrics and stream them for live viewing via Remote GUI or persistent storage across Operator nodes.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Each AnyLog node can collect its own health metrics and distribute them in one or both of two ways:

- **Live view** — push metrics to a Query Node and visualise them in the <a href="{{ '/docs/Tools-UI/remote-gui/' | relative_url }}">Remote GUI</a> without storing any data
- **Persistent storage** — stream metrics into an Operator's database for historical queries and dashboards

The monitoring schedule is deployed as a blockchain policy and activated automatically when `NODE_MONITORING=true` is set in the node configuration.

---

## Collecting node insight

Each participating node runs a set of scheduled tasks that build a JSON object called `node_insight`. This object is assembled from system metrics collected at two intervals:

| Metric | AnyLog command | Frequency |
|---|---|---|
| Operator ingestion stats | `get stats where service = operator and topic = summary` | `!monitoring_frequency` |
| Timestamp | `get datetime local now()` | `!monitoring_frequency` |
| Node type | `!node_type` | `!monitoring_frequency` |
| Disk free (%) | `get disk percentage .` | 30 seconds |
| CPU usage (%) | `get node info cpu_percent` | 30 seconds |
| Network packets received | `get node info net_io_counters packets_recv` | 30 seconds |
| Network packets sent | `get node info net_io_counters packets_sent` | 30 seconds |
| Network error count | `errin + errout` | 30 seconds |
| Status | `Active` | 30 seconds |

The resulting `node_insight` object:

```json
{
  "timestamp": "2026-03-07 18:41:11",
  "node type": "operator",
  "Free Space Percent": 72.4,
  "CPU Percent": 6.7,
  "Packets Recv": 1482930,
  "Packets Sent": 983421,
  "Network Error": 0,
  "status": "Active"
}
```

`!monitoring_frequency` is set in the node's `.env` file (default: 60 seconds). Hardware metrics always collect at 30 seconds regardless.

---

## Option 1 — Live view via Remote GUI

Each node pushes its `node_insight` to the Query Node, which aggregates status from all participating nodes into a single view. The <a href="{{ '/docs/Tools-UI/remote-gui/' | relative_url }}">Remote GUI</a> reads from the Query Node to display a live network-wide dashboard — no database required.

```
Node A  ──┐
Node B  ──┼──► Query Node  ──► Remote GUI
Node C  ──┘     (aggregator)
```

The Query Node destination is resolved automatically from the blockchain:

```anylog
view_monitoring_dest = blockchain get query bring.ip_port
```

Each node then pushes its metrics on a 30-second schedule:

```anylog
run client (!view_monitoring_dest) monitor operators where info = !node_insight
```

The Remote GUI Monitor Node section shows a live table of all nodes pushing metrics to the Query Node:

<a href="{{ '/assets/img/remote_gui_monitoring.png' | relative_url }}" target="_blank" rel="noopener">
  <img src="{{ '/assets/img/remote_gui_monitoring.png' | relative_url }}" alt="Monitor Node Section in Remote GUI">
</a>

Each row represents one node, showing its name, operational time, elapsed time since last update, new and total rows 
ingested, and the hardware metrics — free disk space, CPU usage, network packets, and error count.

The **Add Threshold Monitor** panel at the top lets you set alert thresholds on any column — for example, alert when 
CPU Percent exceeds 80 or Free Space Percent drops below 20.

**View from the CLI:**
```anylog
get monitored                          # list all monitored topics
get monitored operators                # current status from all nodes
reset monitored operators              # clear the aggregated list
```

This option requires no storage configuration — metrics are held in memory on the Query Node and reflect the current 
state only.

---

## Option 2 — Persistent storage across Operators

When `STORE_MONITORING=true`, each node streams its `node_insight` into a `monitoring.node_insight` table on an 
Operator node, enabling historical queries and Grafana dashboards.

```
Node A  ──┐
Node B  ──┼──► Operator (monitoring.node_insight)
Node C  ──┘
```

**On Operator nodes** — stored locally:
```anylog
stream !node_insight where dbms = monitoring and table = node_insight
```

**On non-Operator nodes** — routed to a remote Operator:
```anylog
run client (!monitoring_storage_dest) stream !node_insight where dbms = monitoring and table = node_insight
```

The target Operator is resolved automatically:
```anylog
monitoring_storage_dest = blockchain get operator bring.last [*][ip]:[*][port]
```

### Table setup

On the Operator hosting the monitoring data, the `node_insight` table is created automatically on startup:

```anylog
connect dbms monitoring where type = sqlite
process !anylog_path/deployment-scripts/southbound-monitoring/create_node_monitoring_table.al
```

### Querying stored metrics

```anylog
# Local query on the Operator
sql monitoring format = table "select * from node_insight order by timestamp desc limit 20"

# Network query from any node
run client () sql monitoring format = table "select timestamp, node_type, cpu_percent, free_space_percent from node_insight where timestamp >= NOW() - 1 hour"
```

---

## Using both options together

Options 1 and 2 are not mutually exclusive. Most deployments run both — live view for real-time dashboards and 
persistent storage for historical analysis and alerting.

---

## Configuration

| Variable | Description | Default |
|---|---|---|
| `NODE_MONITORING` | Enable the monitoring schedule | `true` |
| `STORE_MONITORING` | Enable persistent storage to Operator | `true` |
| `MONITORING_FREQUENCY` | Collection frequency for operator stats | `60 seconds` |

The monitoring schedule is stored as a blockchain policy and can be inspected at any time:

```anylog
blockchain get schedule where id = node-monitoring
```