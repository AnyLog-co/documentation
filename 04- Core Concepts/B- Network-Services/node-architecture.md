---
title: Node Architecture
description: How AnyLog nodes form a distributed fabric and what runs inside each node.
layout: page
---
<!--
## Changelog
- 2026-04-24 | Created document
- 2026-04-25 | hyperlink 
-->

AnyLog is a **peer-to-peer data fabric**. There is no central broker or cloud gateway — each node connects directly to 
the others, shares metadata over a distributed ledger, and routes data and queries across the network autonomously. 
Nodes can sit on the same machine, across a LAN, or distributed globally over the internet.


## The flow of Data 

The block diagram below maps the architecture described above onto the actual services running inside a node. 
* **Southbound** ingestion enters from the bottom
* moves up through the **storage and event engine**,  
* Insight, based on data, exits **Northbound** on the right 

The orchestration column on the left runs continuously in the background, keeping the node in sync with the rest of the 
network.

<div class="home-diagram" align="center">
  <a href="{{ '/assets/img/anylog_block_architecture.svg' | relative_url }}"
     target="_blank"
     rel="noopener"
     title="Click to view full size">
    <img src="{{ '/assets/img/anylog_block_architecture.svg' | relative_url }}"
         alt="AnyLog node architecture diagram"
         height="60%"
         width="60%"
         style="cursor: zoom-in;">
  </a>
</div>

### Data in
Data enters a node from the edge: sensors, PLCs, cameras, historians, or any system that can speak REST, MQTT, Kafka, 
gRPC, or OPC-UA. The node does not care what protocol the source uses — all ingestion paths converge on the same 
internal pipeline.


When data arrives, the node applies a mapping policy to translate the raw payload into a structured row. The mapping 
defines which JSON fields become which database columns, what types they carry, and which logical database and table 
the row belongs to. This happens at the edge, before anything is stored, so the data is clean and typed by the time it 
touches disk.


The ingestion pipeline then buffers incoming rows in a streaming buffer and flushes them to local storage in batches — 
tunable by time threshold, volume threshold, or immediately. This keeps write throughput high without sacrificing 
durability.


### Data at rest

Once written, data lives in the node's local storage layer. Structured time-series data goes into a SQL store (SQLite 
by default, PostgresSQL for larger deployments). Unstructured data — video frames, images, binary blobs — goes into a 
separate blob store, with a pointer record in the SQL layer linking the metadata to the file.

Above the storage layer, the event engine runs continuously. It handles three things in parallel: network monitoring 
(watching peer connectivity and alerting on anomalies), scheduled processes (recurring queries, aggregations, or cleanup 
tasks defined as policies), and event-driven cleanup (archiving or purging data that has aged past a retention 
threshold).

The orchestration layer on the left side of the node manages everything that keeps the node coherent with the rest of 
the network. This includes syncing the local copy of the blockchain (the distributed metadata ledger), enforcing 
configuration policies, managing high-availability replication to peer nodes in the same cluster, and maintaining the 
scheduler for long-running background tasks.


### Data out

Queries arrive at the node's REST API — either from a dashboard, a BI tool, a Python client, or another AnyLog node 
acting as a query coordinator. The node inspects the query, consults the blockchain metadata to determine which nodes 
in the network hold the relevant data, and fans the query out to those nodes in parallel.


Each operator node that receives a partial query executes it locally — computing aggregates like `SUM` and `COUNT` on 
its own slice of the data — and returns a partial result. The coordinating node merges the partial results and returns 
a single unified response to the caller. From the caller's perspective it is a single SQL query against a single 
endpoint; the distribution is invisible.

Data can leave the node over REST, Kafka, gRPC, or direct SQL — whichever interface the consuming system expects. A 
BI tool like Grafana connects to the REST endpoint and issues SQL. A downstream Kafka consumer subscribes to a topic 
the node publishes to. A custom application calls the gRPC interface. The node speaks all of them simultaneously.
