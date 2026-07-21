---
title: Test Suites
description: Commands to define, run, and compare test cases and test suites across AnyLog Network nodes.
layout: page
---
<!--
## Changelog
- 2026-05-25 | Reformatted to match troubleshooting style
-->

Nodes in the network can treat queries and their outputs as test cases and group them into test suites.
A single command can trigger one or more tests across one or more nodes; results from all participating nodes
can be stored in a database and queried from a single point, the same way time-series data is managed by the network.

| Step | Command | Confirms |
|---|---|---|
| 1 | `run client () sql … test=true file=…` | Query output written in test format |
| 2 | `analyze output` | Two test files are identical |
| 3 | `test case` | Single source file passes against live query |
| 4 | `test suite` | All source files in a directory pass |

---

## Test format

When a query is executed, query options can mark it as a test case and direct the output to a file in **test format**.

A test-format file has three sections:

| Section | Contents |
|---|---|
| **Header** | Title, date/time, query syntax, DBMS, output format |
| **Body** | The query result rows |
| **Footer** | Row count and execution time |

**Example output:**

```output
==========================================================================
Title:    List Unique Values
Date:     2022-01-21 10:20:28.681237
Command:  select distinct(value) as value from ping_sensor order by value
DBMS:     lsl_demo
Format:   json:output
==========================================================================
{"value": 2}
{"value": 21}
{"value": 121}
{"value": 201}
{"value": 221}
{"value": 231}
{"value": 241}
{"value": 261}
{"value": 1021}
{"value": 2021}
{"value": 2100}
{"value": 2221}
{"value": 3221}
{"value": 5621}
==========================================================================
Rows:     14
Run Time: 00:00:03
==========================================================================
```

---

## Comparison process

Any two files in test format can be compared:

- **Header differences** are ignored.
- **Body differences** trigger a failure with the reason and line number.
- **Footer differences** — slower execution time is flagged only when the `time` option is enabled.

---

## `analyze output`

**When:** You have two test-format files and want to verify they are identical.

**Why:** Confirms that a query result matches a previously captured trusted output, without re-running a full test case.

```anylog
analyze output where file = [file path and name] and source = [file path and name] and option = time
```

| Key | Value | Details | Default |
|---|---|---|---|
| `file` | path and file name | The output being tested | |
| `source` | path and file name | The trusted reference output | |
| `option` | `time` | Also fail if execution is slower than the source | (off) |

**Example:**

```anylog
analyze output where file = !test_dir/test_file3.out and source = !test_dir/test_file2.out and option = time
```

---

## Directing a query to a test-format file

Add the following key-value pairs to the query options section to write output in test format:

| Key | Value | Details | Default |
|---|---|---|---|
| `test` | `true` / `false` | Enable test format | `false` |
| `title` | any string | Added to the header | |
| `file` | path and file name | Destination file | |

> **Note:** If the file name is prefixed with `*`, the system appends a unique suffix to avoid overwriting existing files.

**Example:**

```anylog
run client () sql lsl_demo format=json and stat=true and test=true and file=!test_dir\query_*.out and title="Data set #35" "select distinct(value) as value from ping_sensor order by value"
```

---

## Executing a query and comparing to expected output

**When:** You want to run a query and immediately validate the result against a trusted reference file.

**Why:** Combines query execution and comparison into a single step, leaving a diff file only when the result diverges.

Add the standard test-format keys (above) plus:

| Key | Value | Details | Default |
|---|---|---|---|
| `source` | path and file name | File with expected results | |
| `option` | `time` | Also fail on slower execution | (off) |

**Example:**

```anylog
run client () sql lsl_demo format=json and stat=true and test=true and file=!test_dir\test_*.test and source=!test_dir\query_1.out and title="Data set #35" "select distinct(value) as value from ping_sensor order by value"
```

> **Notes:**
> - If the file name is `*`, a unique name is generated automatically.
> - If the result matches, the output file is deleted. If it differs, the file is kept for inspection.
> - Without `option=time`, execution time differences are ignored.

---

## `test case`

**When:** You have a single source file in test format and want to re-run its query and verify the result.

**Why:** Reads the query and metadata directly from the source file header — no need to re-specify the query manually. Results can be written to a database for monitoring and alerting.

```anylog
test case where source = [file path and name] and inform = [destination] and time = [true/false] and dest = [destination nodes]
```

| Key | Value | Details |
|---|---|---|
| `source` | path and file name | The trusted reference file |
| `inform` | see table below | Where test results are sent |
| `time` | `true` / `false` | Whether to fail on slower execution |
| `dest` | `IP:Port, …` | Optional: restrict to specific Operator nodes |

**`inform` destinations:**

| Value | Description |
|---|---|
| `stdout` | The stdout of the node running the query |
| `stdout@ip:port` | The stdout of a remote node (TCP port) |
| `dbms.dbms_name.table_name@ip:port` | A table on a remote node (REST port) |

Multiple `inform` values are allowed.

**Example:**

```anylog
test case where source = !test_dir/output_test.out and inform = stdout and inform = dbms.qa.testing@!qa_node
```

**Example failure output:**

```anylog
{"result"   : "Failed",
 "Title"    : "List Unique Values",
 "Reason"   : "The value for the key 'timestamp' in line 11 is different: '2019-10-11 10:15:53.150009' vs. '2019-10-11 10:15:53.15000",
 "File"     : "D:\Node\AnyLog-Network\data\test\run_of_test_1642789228.out",
 "Trusted"  : "D:\Node\AnyLog-Network\data\test\test_1642789228.out"}
```

---

## `test suite`

**When:** You have multiple test cases organized in a directory (or directory tree) and want to run them all in one call.

**Why:** Scales `test case` across an entire folder of source files — useful for regression testing a deployment or validating a data set after a network change.

```anylog
test suite where source = [file path and name] and inform = [destination] and subdir = [true/false] and time = [true/false] and dest = [destination nodes]
```

| Key | Value | Details |
|---|---|---|
| `source` | path and file pattern | Source files to test; supports `*` prefix on name or type |
| `inform` | see `test case` | Where results are sent |
| `subdir` | `true` / `false` | If `true`, recurse into subdirectories |
| `time` | `true` / `false` | Whether to fail on slower execution |
| `dest` | `IP:Port, …` | Optional: restrict to specific Operator nodes |

**Examples:**

```anylog
test suite where source = !test_dir/test_*.out and inform = dbms.qa.testing@!dest_node
test suite where source = !test_dir/test_*.out and inform = stdout and subdir = true and dest = 127.32.52.103:20048
```

---

## Scheduling tests

Test cases and test suites can be added to the scheduler so they run periodically:

```anylog
schedule time = 1 hour and name = "Hourly regression" task test suite where source = !test_dir/test_*.out and inform = dbms.qa.testing@!dest_node
```

Results written to a database table via `inform` can then be monitored and used to trigger alerts.

---

## End-to-end example

The following walkthrough uses a real power-monitoring data set (`cos` DBMS, `pp_pm` table) to illustrate the full
test suite workflow: load data → generate trusted output files → re-run and validate.

### Step 1 — Load the test data set

Save the 50 rows below to a file named `cos.pp_pm.json` and load it into the `cos` database before running any queries.

```json
{"monitor_id": "KPL ", "a_current": 249, "a_n_voltage": 737, "b_current": 250, "b_n_voltage": 740, "c_current": 246, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 99, "reactivepower": 644, "realpower": 5454, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DSP ", "a_current": 8, "a_n_voltage": 245, "b_current": 15, "b_n_voltage": 247, "c_current": 11, "c_n_voltage": 245, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 99, "reactivepower": 5, "realpower": 46, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DG2 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DG3 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DG4 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DG5 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DG6 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DF1 ", "a_current": 50, "a_n_voltage": 245, "b_current": 23, "b_n_voltage": 247, "c_current": 49, "c_n_voltage": 245, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 97, "reactivepower": 39, "realpower": 161, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DF2 ", "a_current": 21, "a_n_voltage": 245, "b_current": 18, "b_n_voltage": 246, "c_current": 21, "c_n_voltage": 244, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 94, "reactivepower": 28, "realpower": 80, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DF3 ", "a_current": 0, "a_n_voltage": 245, "b_current": 0, "b_n_voltage": 247, "c_current": 0, "c_n_voltage": 245, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DF4 ", "a_current": 75, "a_n_voltage": 245, "b_current": 46, "b_n_voltage": 247, "c_current": 79, "c_n_voltage": 245, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 98, "reactivepower": 52, "realpower": 272, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "DCT ", "a_current": 154, "a_n_voltage": 245, "b_current": 102, "b_n_voltage": 247, "c_current": 158, "c_n_voltage": 245, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 98, "reactivepower": 122, "realpower": 564, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CSP ", "a_current": 2, "a_n_voltage": 739, "b_current": 2, "b_n_voltage": 741, "c_current": 2, "c_n_voltage": 738, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 100, "reactivepower": 5, "realpower": 52, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CG7 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CG12", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CF1 ", "a_current": 16, "a_n_voltage": 739, "b_current": 18, "b_n_voltage": 741, "c_current": 13, "c_n_voltage": 737, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 100, "reactivepower": -34, "realpower": 348, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CF2 ", "a_current": 48, "a_n_voltage": 739, "b_current": 42, "b_n_voltage": 741, "c_current": 30, "c_n_voltage": 738, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 98, "reactivepower": 192, "realpower": 863, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CF3 ", "a_current": 8, "a_n_voltage": 739, "b_current": 11, "b_n_voltage": 741, "c_current": 18, "c_n_voltage": 738, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 99, "reactivepower": 46, "realpower": 265, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CDT ", "a_current": 22, "a_n_voltage": 739, "b_current": 25, "b_n_voltage": 741, "c_current": 33, "c_n_voltage": 737, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 98, "reactivepower": 126, "realpower": 566, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "CBT ", "a_current": 96, "a_n_voltage": 739, "b_current": 98, "b_n_voltage": 741, "c_current": 97, "c_n_voltage": 738, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 98, "reactivepower": 400, "realpower": 2114, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BG8 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BG9 ", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BG10", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BG11", "a_current": 0, "a_n_voltage": 0, "b_current": 0, "b_n_voltage": 0, "c_current": 0, "c_n_voltage": 0, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 0, "realpower": 0, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BF1 ", "a_current": 30, "a_n_voltage": 737, "b_current": 35, "b_n_voltage": 740, "c_current": 30, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 99, "reactivepower": 83, "realpower": 696, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BF2 ", "a_current": 36, "a_n_voltage": 738, "b_current": 34, "b_n_voltage": 739, "c_current": 35, "c_n_voltage": 737, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 100, "reactivepower": 11, "realpower": 772, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BF3 ", "a_current": 34, "a_n_voltage": 737, "b_current": 24, "b_n_voltage": 740, "c_current": 32, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 100, "reactivepower": -20, "realpower": 665, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BF4 ", "a_current": 21, "a_n_voltage": 738, "b_current": 22, "b_n_voltage": 740, "c_current": 22, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 100, "reactivepower": 20, "realpower": 476, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BCT ", "a_current": 96, "a_n_voltage": 738, "b_current": 99, "b_n_voltage": 740, "c_current": 97, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6000, "powerfactor": 98, "reactivepower": 401, "realpower": 2118, "timestamp": "2025-12-22 00:00:26.023786"}
{"monitor_id": "BSP ", "a_current": 1, "a_n_voltage": 738, "b_current": 1, "b_n_voltage": 740, "c_current": 1, "c_n_voltage": 736, "commsstatus": true, "energymultiplier": 1, "frequency": 6001, "powerfactor": 100, "reactivepower": -1, "realpower": 17, "timestamp": "2025-12-22 00:00:26.023786"}
```

---

### Step 2 — Generate trusted output files

Run all eight queries once against the loaded data set. Each query writes its result to a numbered `.out` file in `!test_dir`.
These files become the trusted reference for all future validation runs.

| File | Query | What it tests |
|---|---|---|
| `query_1.out` | Q1 | `AVG`/`MIN`/`MAX` powerfactor per monitor, ordered by `max_powerfactor DESC` |
| `query_2.out` | Q2 | Same aggregation, ordered by `avg_powerfactor ASC` |
| `query_3.out` | Q3 | Per-minute increments of `MAX(b_n_voltage)` per monitor, ordered by `max_b_n_voltage` |
| `query_4.out` | Q4 | Per-minute increments of `AVG(b_n_voltage)` per monitor, ordered by `avg_b_n_voltage` |
| `query_5.out` | Q5 | Voltage stats with compound `AND` filter — expected row count: 9 |
| `query_6.out` | Q6 | Voltage stats with compound `OR` filter — expected row count: 41 |
| `query_7.out` | Q7 | Per-monitor voltage averages and extremes filtered by `a_n_voltage > 500 OR < 200`, ordered by `max_voltage DESC` |
| `query_8.out` | Q8 | Same filter as Q7, ordered by `avg_a_voltage DESC` |

```anylog
# Q1 — order by Max powerfactor
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_1.out and title="Data set #1 - Sabetha Q1" SELECT monitor_id, AVG(powerfactor) as avg_powerfactor, MIN(powerfactor) as min_powerfactor, MAX(powerfactor) as max_powerfactor FROM pp_pm WHERE timestamp > '2025-01-01 00:00:00' GROUP BY monitor_id ORDER BY max_powerfactor desc

# Q2 — order by Avg powerfactor
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_2.out and title="Data set #1 - Sabetha Q2" SELECT monitor_id, AVG(powerfactor) as avg_powerfactor, MIN(powerfactor) as min_powerfactor, MAX(powerfactor) as max_powerfactor FROM pp_pm WHERE timestamp > '2025-01-01 00:00:00' GROUP BY monitor_id ORDER BY avg_powerfactor

# Q3 — increments, order by Max voltage
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_3.out and title="Data set #1 - Sabetha Q3" "SELECT increments(minute, 1, timestamp), monitor_id, min(timestamp), max(timestamp), MAX(b_n_voltage) as max_b_n_voltage FROM pp_pm WHERE insert_timestamp > '20250101' GROUP BY monitor_id ORDER BY max_b_n_voltage"

# Q4 — increments, order by Avg voltage
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_4.out and title="Data set #1 - Sabetha Q4" "SELECT increments(minute, 1, timestamp), monitor_id, min(timestamp), max(timestamp), AVG(b_n_voltage) as max_b_n_voltage FROM pp_pm WHERE insert_timestamp > '20250101' GROUP BY monitor_id ORDER BY max_b_n_voltage"

# Q5 — AND filter (expected count: 9)
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_5.out and title="Data set #1 - Sabetha Q5" "SELECT MAX(a_n_voltage) as max_voltage, MIN(a_n_voltage) as min_voltage, AVG(a_n_voltage) as avg_voltage, COUNT(a_n_voltage) as count_voltage from pp_pm where a_n_voltage < 739 and a_n_voltage > 700"

# Q6 — OR filter (expected count: 41)
run client () sql cos format=json and stat=true and test=true and file=!test_dir\query_6.out and title="Data set #1 - Sabetha Q6" "SELECT MAX(a_n_voltage) as max_voltage, MIN(a_n_voltage) as min_voltage, AVG(a_n_voltage) as avg_voltage, COUNT(a_n_voltage) as count_voltage from pp_pm where a_n_voltage >= 739 or a_n_voltage <= 700"

# Q7 — per-monitor voltage stats, order by max_voltage DESC
<run client () sql cos
    format=json and stat=true and test=true
    and file=!test_dir\query_7.out
    and title="Data set #1 - Sabetha Q7"
    SELECT monitor_id,
    AVG(a_n_voltage) as avg_a_voltage,
    AVG(b_n_voltage) as avg_b_voltage,
    AVG(c_n_voltage) as avg_c_voltage,
    MAX(a_n_voltage) as max_voltage,
    MIN(a_n_voltage) as min_voltage
FROM pp_pm
where a_n_voltage > 500 OR a_n_voltage < 200
GROUP BY monitor_id
ORDER BY max_voltage DESC;>

# Q8 — same filter as Q7, order by avg_a_voltage DESC
<run client () sql cos
    format=json and stat=true and test=true
    and file=!test_dir\query_8.out
    and title="Data set #1 - Sabetha Q8"
    SELECT monitor_id,
    AVG(a_n_voltage) as avg_a_voltage,
    AVG(b_n_voltage) as avg_b_voltage,
    AVG(c_n_voltage) as avg_c_voltage,
    MAX(a_n_voltage) as max_voltage,
    MIN(a_n_voltage) as min_voltage
FROM pp_pm
where a_n_voltage > 500 OR a_n_voltage < 200
GROUP BY monitor_id
ORDER BY avg_a_voltage DESC;>
```

---

### Step 3 — Validate a single query

Re-run one query and compare it against its trusted output file:

```anylog
test case where source = !test_dir/query_1.out and inform = stdout
```

---

### Step 4 — Validate all queries in one call

Re-run all eight queries and compare each against its trusted output file:

```anylog
test suite where source = !test_dir/query_*.out and inform = stdout
```

To also store results in a QA database on a remote node:

```anylog
test suite where source = !test_dir/query_*.out and inform = stdout and inform = dbms.qa.testing@!dest_node
```