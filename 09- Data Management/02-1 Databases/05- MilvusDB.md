---
title: "Milvus Vector Database"
description: "How Milvus fits into AnyLog — data/blockchain association, connecting and managing collections, inserting, and querying vector data."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon    | Restructured around how-it-works → connect/manage/disconnect → insert → query, and split the Docker install / full deployment walkthrough / troubleshooting out into a standalone "99- Milvus" doc (matching the MongoDB/MinIO split). Added a "How It Works" section covering data association (no built-in per-row link to SQL, unlike blob storage) and blockchain association (collections register on the blockchain after create/insert, confirmed from the existing Cluster section). Added constructed example query results, since none existed anywhere in the source material, flagged as illustrative rather than verified output. Noted that no `drop dbms` equivalent exists for Milvus connections — only `vector drop` at the collection level | |
 | 2026-07-28 | Ori Shadmon    | Added a paragraph to the intro explaining the transport: AnyLog talks to Milvus via pymilvus's `MilvusClient` over gRPC, distinct from the AnyLog-REST hop a user might use to issue the command, and distinct from MinIO/S3's HTTP-based `boto3` transport | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
--->

Milvus is an open-source, high-performance, and highly scalable vector database for semantic vector search, metadata
filtering, and document embedding. Within the AnyLog platform it's used as an Elasticsearch-like mechanism for
semantic/similarity search across any text-embeddable content — from documentation to sensor event descriptions —
for fast, reliable, and useful insight.

AnyLog talks to Milvus through <a href="https://milvus.io/api-reference/pymilvus/v3.0.x/About.md" target="_blank">pymilvus</a>'s
`MilvusClient`, which communicates with the Milvus server over gRPC — not AnyLog's own REST API, and not a custom
internal protocol. Issuing a `vector` command yourself (via the CLI or AnyLog's REST API) is a separate hop from
this: however you reach AnyLog, the AnyLog-to-Milvus leg underneath is always gRPC. This is different from how
AnyLog talks to MinIO/S3-style object storage (via `boto3`, over plain HTTP) — two different backends behind the
same command surface, using two different transport protocols.

### Supported backends

* **Milvus Lite**: A file store mechanism for the Milvus database.
* **Milvus Server**: A physical deployment of the Milvus engine.

For installing Milvus (Docker) and a full connect-to-query deployment walkthrough, see
[Milvus support](../../13-%20Support%20&%20Troubleshooting/04-%20Third-Party%20Support/03-%20MilvusDB.md).

---

## How It Works

### Data association

Unlike blob storage — where the SQL row keeps a hash/filename reference back to the actual file — there's no
built-in link between a Milvus vector row and any SQL row. `vector insert` creates a standalone entity in its own
collection, with its own auto-generated `id`; there's no `bring [field]`/mapping-policy mechanism tying it to
anything else. If you want a vector row to relate to other data, that's on you to design — typically by adding a
scalar metadata field (e.g. `subject`, or an ID matching a SQL row) at insert time, and filtering/joining on it
yourself. Milvus data is best thought of as its own independent store that happens to sit alongside your SQL
databases under the same command surface, not as an extension of any particular SQL table.

### Blockchain association

Collections **are** registered on the blockchain — after `vector create`/`vector insert`, the collection becomes
discoverable the same way a SQL table is, which is what lets `run client()` fan a `vector search`/`query`/`delete`
out to whichever operators actually host that collection (see [Cluster / `run client()`](#cluster--run-client)
below).

> **To verify:** the source material confirms collections get registered on the blockchain, but doesn't name the
> actual policy type used (unlike SQL's `table` policy) — worth confirming before stating it more specifically.

---

## Connect, Manage Collections, and Disconnect

`group`... — actually, for Milvus this is expressed directly as a logical `dbms`, not a `group` (that concept
belongs to the `bucket` commands for MinIO/Akave/S3). Each `connect dbms` call ties a logical database name to a
physical Milvus Lite file or Milvus Server endpoint.

### Connect

**Milvus Lite (local file)** — creates or opens a local database file; parent directories are created automatically.

```anylog
connect dbms vectors where type = milvus and path = !data_dir/milvus_demo.db and dimension = 768
```

Absolute path example:

```anylog
connect dbms vectors where type = milvus and path = /data/milvus_demo.db and dimension = 768
```

**Milvus Server (URI):**

```anylog
connect dbms vectors where type = milvus and uri = http://MILVUS_HOST:19530 and token = root:Milvus and dimension = 768
```

**Milvus Server (host + port):**

```anylog
<connect dbms vectors where 
    type = milvus and 
    ip = MILVUS_HOST and 
    port = 19530 and 
    user = root and 
    password = Milvus and 
    dimension = 768>
```
(`user` + `password` are combined into the Milvus token.)

Verify:

```anylog
get databases
```

Collections appear under `Structure.Tables.vectors` (collections are exposed as tables), or list them directly —
see `vector list` below.

### Managing Collections

A collection is roughly Milvus's equivalent of a SQL table — created explicitly, listed, and dropped independently
of the database connection itself.

**`vector create`** — create a collection with auto-increment id (`auto_id`). Default metric: `COSINE` (`L2`,
`COSINE`, `IP` supported).

```anylog
vector create where dbms = vectors and collection = sensors

vector create where dbms = vectors and collection = sensors and metric_type = L2 and drop = true
```

**`vector list`** — list collections on a connected dbms in a table (`collection`, `dimension`, `metric_type`, `rows`):

```anylog
vector list where dbms = vectors

vector list format = json and stat = true where dbms = vectors
```

Same collections as `get databases` → `Structure.Tables.<dbms>`, with per-collection stats.

**`vector drop`** — remove an entire collection (schema + data):

```anylog
vector drop where dbms = vectors and collection = readings
```

### Disconnect

```anylog
disconnect dbms vectors
```

> **No `drop dbms` equivalent exists for Milvus** — dropping the logical database connection itself isn't
> documented anywhere in the source material; only `vector drop` (collection-level) and `disconnect dbms` (the
> connection) are. If a full database-level drop is needed, that's an open gap rather than an oversight in this
> rewrite.

---

## Text embedding (`text` / `query`)

`text` and `query` use pymilvus `DefaultEmbeddingFunction` — an ONNX model (~50 MB) from Hugging Face.
`pip install` provides the loader code only; the model weights are downloaded separately.

Vectors are **768-dimensional** — set `dimension = 768` on `connect dbms`.

| Repo                                  | Role               |
| ------------------------------------- | ------------------ |
| `GPTCache/paraphrase-albert-onnx`     | `model.onnx`       |
| `GPTCache/paraphrase-albert-small-v2` | tokenizer + config |

> **Developer mode** (not required with Docker build) — download once on a machine with internet, after `pip install -r requirements.txt`:
> ```bash
> # if huggingface.co is blocked: export HF_ENDPOINT=https://hf-mirror.com
> python3 -c "from pymilvus import model; fn = model.DefaultEmbeddingFunction(); fn.encode_documents(['warmup']); fn.encode_queries(['warmup']); print('OK dim=', fn.dim)"
> ```
>
> Cache location: `HF_HOME` (default `~/.cache/huggingface`). Docker images set `HF_HOME=/app/.anylog-model-cache` (baked in at build time). For downloading the model once and shipping it to an offline node, see [Milvus support](../../13-%20Support%20&%20Troubleshooting/04-%20Third-Party%20Support/03-%20MilvusDB.md).

---

## Insert Data

Insert **one** entity per command. Two ways to supply the vector:

**Auto-embed from text** — omit `vector`. AnyLog calls the embedding model (`DefaultEmbeddingFunction`) and stores
the resulting 768-float vector plus the original `text` string. Requires the Hugging Face ONNX model (see above).
Use this for natural-language content you want to search semantically later.

```anylog
vector insert where dbms = vectors and collection = sensors and text = "door open"
```

**Pre-computed vector** — pass `vector = […]` yourself (must match collection dimension, e.g. 768 floats). The
model is **not** called. Add `text` only as an optional human-readable label stored alongside the vector — useful
offline, for custom embedders, or vectors produced by an external pipeline.

```anylog
vector insert where dbms = vectors and collection = sensors and id = 1 and text = "door open" and vector = [0.1,0.2,0.3,...]
```

If both `vector` and `text` are present, the explicit `vector` wins; `text` is stored as metadata only.

Extra scalar fields (e.g. `subject`, `measure`) are stored as metadata on either form — this is the mechanism
described in [Data association](#data-association) above for relating a vector row to other context.

If the collection does not exist, it is created automatically on insert.

---

## Query Data

### `vector search` — semantic similarity search (ANN)

Use `query` for text embedding, or `vector` for a raw float list. Optional Milvus filter expression.

```anylog
vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

vector search where dbms = vectors and collection = sensors and query = "AI information" and filter = "subject == 'biology'" and limit = 2
```

JSON output:

```anylog
vector search format = json and stat = true where dbms = vectors and collection = sensors and query = "door open" and limit = 5
```

**What a result would look like** *(constructed illustration, following AnyLog's standard SQL JSON result shape
`{"Query": [...], "Statistics": [...]}` — not verified against real output; field name for the similarity score
may differ)*:

```json
{
  "Query": [
    {"id": 453889217700111234, "distance": 0.9998, "text": "door open", "subject": "security"},
    {"id": 453889217700111240, "distance": 0.3421, "text": "temperature high", "subject": "process"}
  ],
  "Statistics": [{"Count": 2, "Time": "00:00:00", "Nodes": 1}]
}
```
> Since this collection defaults to `metric_type = COSINE`, **higher** values mean a **closer** match — the
> opposite of `L2` distance, where lower means closer. The near-exact match ("door open" vs. the query "door
> open") scores close to 1.0; the unrelated row scores much lower.

### `vector query` — scalar metadata query (no vector similarity)

Returns all rows, or filter by expression / ids.

```anylog
vector query where dbms = vectors and collection = sensors

vector query where dbms = vectors and collection = sensors and filter = "subject == 'history'"

vector query where dbms = vectors and collection = sensors and ids = (1,2) and output_fields = (id,text,subject)
```

**What a result would look like** *(constructed illustration — no similarity score, since this isn't an ANN
search)*:

```json
{
  "Query": [
    {"id": 453889217700111234, "text": "door open", "subject": "security"}
  ],
  "Statistics": [{"Count": 1, "Time": "00:00:00", "Nodes": 1}]
}
```

### `vector delete` — delete by primary key id(s) or filter

Requires `ids` **or** `filter` (not both).

```anylog
vector delete where dbms = vectors and collection = readings and ids = 467493353131606734

vector delete where dbms = vectors and collection = readings and ids = (467493353131606728,467493353131606730)

vector delete where dbms = vectors and collection = readings and filter = "measure == 'float'"

vector delete where dbms = vectors and collection = readings and filter = "text == 'sensor3'"
```

---

## Cluster / `run client()`

Vector **query**, **search**, and **delete** can fan out to operators that host the collection (registered on the
blockchain after create/insert — see [Blockchain association](#blockchain-association) above).

```anylog
run client () vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

run client (subset=true,timeout=30) vector search format = json and stat = true where dbms = vectors and collection = sensors and query = "door open" and limit = 5

run client () vector query where dbms = vectors and collection = sensors

run client () vector query format = json and stat = true where dbms = vectors and collection = sensors

run client () vector delete where dbms = vectors and collection = readings and filter = "measure == 'txt'"
```

`vector create` and `vector insert` run **locally** on the connected operator only (`run client()` supports
**query**, **search**, and **delete** only).

---

## Implementation notes

| Topic                     | Detail                                                                                                               |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Concurrency**           | One shared `MilvusClient` per logical dbms; thread-safe gRPC                                                         |
| **Collections as tables** | Listed via `get databases` / `Structure.Tables.<dbms>`                                                               |
| **Index metric**          | `COSINE` default; set with `metric_type` on `vector create`                                                          |
| **HA / replication**      | Not supported — no Milvus replication or sync across operators. Use **one Milvus connection per HA setup**, or on operators in **different cluster names** |
| **gRPC noise**            | Milvus Lite may log `GOAWAY ... too_many_pings` on stderr; usually harmless. Keepalive is tuned in `milvus_dbms.py`. |