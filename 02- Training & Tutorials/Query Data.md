---
title: "Introduction to Querying Data"
description: A hands-on introduction to querying AnyLog — the same query via CLI and REST, plus the two functions that make time-series querying easy (period and increments).
layout: page
source_path: "Query Data.md"
---
<!--
## Changelog
- 2026-07-14 | Created document as a beginner-friendly on-ramp for 02- Training & Tutorials, distinct from the
              full reference in 08- Northbound Connectors/queries.md (query options, casts, formatting) — this
              page covers run client (), the REST/curl equivalent, and period/increments, then hands off to the
              full reference for everything else.
-->

# Introduction to Querying Data

AnyLog data lives on **Operator** nodes, scattered across the network. You never query an Operator directly —
instead, you send a query to any node acting as a **Query Node**, which uses the network's shared metadata to
figure out which Operators actually hold the data, fans the query out to them, and assembles one combined
result. This page is a hands-on walkthrough of that process: the same query issued from the CLI and from REST,
and the two functions — `period` and `increments` — that make time-series querying in AnyLog noticeably easier
than plain SQL.

For the complete reference — every query option, every cast, every output format — see
[Querying Data (Northbound)](../08-%20Northbound%20Connectors/queries.md). This page is deliberately narrower:
enough to get a first real query running and understand what you're looking at.

---

## Step 1: A query on a single node

The simplest possible query just runs against whichever node you're connected to right now, with no
distribution at all:

```anylog
sql my_data "select * from ping_sensor limit 10"
```

This is useful for a quick sanity check on data that just arrived, but it only sees what's stored locally on
this one node — which is rarely what you actually want in a network with more than one Operator.

## Step 2: A query across the network — `run client ()`

To query every relevant Operator and get back one combined result, wrap the query in `run client ()`:

```anylog
run client () sql my_data format=table "select * from ping_sensor limit 10"
```

The empty parentheses tell AnyLog to work out the target nodes itself, from the network's metadata — you don't
need to know or list any IP addresses. This is the form you'll use for almost everything; the single-node `sql`
command from Step 1 is really just a debugging shortcut.

You *can* target specific nodes explicitly if you ever need to:

```anylog
run client (24.23.250.144:7848, 16.87.143.85:7848) sql my_data format=table "select * from ping_sensor limit 10"
```

`format=table` here just makes the result readable on the CLI — see [Step 5](#step-5-reading-the-output) below
for the other format options.

## Step 3: The same query over REST

Everything above works exactly the same way from outside AnyLog entirely — over plain HTTP. This is what a
dashboard, script, or any external application actually does under the hood; the CLI form and the REST form are
two doors into the same thing.

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql my_data format=table select * from ping_sensor limit 10" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```

Two things to notice, since they trip people up the first time:

- **`destination: network`** is the REST equivalent of the empty `()` in `run client ()` — it's what tells
  AnyLog to fan the query out across the network rather than answering only from the node you happened to
  connect to. Leaving it out is the single most common reason a query "returns nothing" when the data clearly
  exists somewhere in the network.
- Keep the `command` value on one line, and always add `-w "\n"` — without it, some terminals will mash the
  response together with your next prompt in a way that looks like the query failed when it didn't.

## Step 4: Two functions worth learning early

Plain `WHERE` clauses work in AnyLog, but two purpose-built functions cover the two things you'll actually want
to do with time-series data constantly: find the most recent reading, and bucket a range of readings for a
chart.

### `period` — "what was the reading right before this moment?"

`period` finds the first occurrence of data at or before a given timestamp, within a bounded window — the
question you're usually actually asking when you write `ORDER BY timestamp DESC LIMIT 1`:

```anylog
run client () sql my_data "select max(timestamp), avg(value) from ping_sensor where period(minute, 1, now(), timestamp)"
```

Read the arguments as: "look back up to 1 minute from now, for the timestamp column." Swap `now()` for a
specific timestamp to ask the same question about any point in the past, not just the present moment.

### `increments` — bucketing a time range for a chart

`increments` divides a time range into fixed buckets and aggregates each bucket — this is the function behind
essentially every time-series chart built on AnyLog data:

```anylog
run client () sql my_data format=table "
  SELECT increments(minute, 5, timestamp), min(timestamp), max(timestamp), avg(value)
  FROM ping_sensor
  WHERE timestamp >= NOW() - 1 hour"
```

That's "5-minute buckets, over the last hour, with the average value per bucket" — one line, no manual
`GROUP BY` bucketing math.

Both functions have more options (filter criteria for `period`; auto-sized buckets for `increments`) — see
[Time-series optimised queries](../08-%20Northbound%20Connectors/queries.md#time-series-optimised-queries) in
the full reference once you're comfortable with the basic form above.

## Step 5: Reading the output

The `format` option controls how results come back — you've already seen `format=table` above, which is the
easiest to read on a terminal:

| Format | When to use it |
|---|---|
| `format=table` | Reading results yourself on the CLI |
| `format=json` (default) | Programmatic consumption — wraps rows in `{"Query": [...]}` |
| `format=json:list` | A flatter list format some BI tools (e.g. Power BI) expect |

## Putting it together

A single, realistic query, run both ways:

```anylog
run client () sql new_company format=table "
  SELECT increments(minute, 5, timestamp), min(timestamp), avg(value)
  FROM rand_data
  WHERE timestamp >= NOW() - 1 hour"
```

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql new_company format=table SELECT increments(minute, 5, timestamp), min(timestamp), avg(value) FROM rand_data WHERE timestamp >= NOW() - 1 hour" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```

Same query, same result, two different doors.

---

## Where to go next

This page covered enough to run and read real queries. For everything else — casting and formatting columns
(`::float(2)`, `::datetime(...)`), the full list of query options (`stat`, `max_time`, `timezone`, HA-related
`nodes`/`committed`), discovering what tables/columns exist before you query them, and the auto-sized
`increments` variant — see the full reference:
[Querying Data (Northbound)](../08-%20Northbound%20Connectors/queries.md).