---
title: "Examples & Use Cases"
description: End-to-end deployment examples for AnyLog and EdgeLake, from a single standalone agent to a full multi-node demo network.
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name** | **Change** | **Version** |
 |------------|--|------------|----------|
 | 2026-07-25 | Ori Shadmon | Created document |
--->

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