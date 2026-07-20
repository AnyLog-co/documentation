---
title: "Milvus Vector Database"
description: ""
layout: page
source_path: ""
---

### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 |            |                |                  |          |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |






# Milvus vector database

AnyLog integrates **Milvus** as a **Vector Database** for semantic vector search, metadata filtering, and document embeddings.

Supported backends:


| Mode              | How                                     |
| ----------------- | --------------------------------------- |
| **Milvus Lite**   | Local file path (`path = ...`)          |
| **Milvus server** | TCP/gRPC (`uri = ...` or `ip` + `port`) |


---

## Requirements

**Nuitka / split builds:** install the Milvus plugin (not compiled into `anylog_agent`):

```bash
./build/build_plugin_milvusdb.sh
# or: ./build_anylog.sh   # installs opcua, web3, modbus, milvusdb
export ANYLOG_PLUGIN_DIR="$(pwd)/plugins"
```

Plugin pack: `plugins/milvusdb/` (import name `pymilvus`).

**Developer / PyInstaller:** `pip install -r requirements.txt` or:

```
pymilvus[milvus_lite,model]>=3.0.0
transformers>=4.36,<5
onnxruntime
```

### Text embedding (`text` / `query`)

`text` and `query` use pymilvus `DefaultEmbeddingFunction` — an ONNX model (~50 MB) from Hugging Face.  
`pip install` provides the loader code only; the model weights are downloaded separately.


| Repo                                  | Role               |
| ------------------------------------- | ------------------ |
| `GPTCache/paraphrase-albert-onnx`     | `model.onnx`       |
| `GPTCache/paraphrase-albert-small-v2` | tokenizer + config |


Vectors are **768-dimensional** — set `dimension = 768` on `connect dbms`.

**Developer mode** (not required with Docker build) — download once on a machine with internet, after `pip install -r requirements.txt`:

```bash
# if huggingface.co is blocked: export HF_ENDPOINT=https://hf-mirror.com
python3 -c "from pymilvus import model; fn = model.DefaultEmbeddingFunction(); fn.encode_documents(['warmup']); fn.encode_queries(['warmup']); print('OK dim=', fn.dim)"
```

Cache location: `HF_HOME` (default `~/.cache/huggingface`). Docker images set `HF_HOME=/app/.anylog-model-cache` (baked in at build time).

**Offline node** — run the command above on a build machine, ship the cache, then on the target host:

```bash
# build machine
export HF_HOME=/tmp/anylog-model-cache && mkdir -p "$HF_HOME"
python3 -c "from pymilvus import model; fn = model.DefaultEmbeddingFunction(); fn.encode_documents(['warmup']); fn.encode_queries(['warmup'])"
tar -C "$HF_HOME" -czf milvus-embedding-model.tgz hub

# target host (Docker default path)
mkdir -p /app/.anylog-model-cache
tar -xzf milvus-embedding-model.tgz -C /app/.anylog-model-cache
export HF_HOME=/app/.anylog-model-cache
export HF_HUB_OFFLINE=1    # optional
```

---

## Connect

### Milvus Lite (local file)

Creates or opens a local database file. Parent directories are created automatically.

```text
connect dbms vectors where type = milvus and path = !data_dir/milvus_demo.db and dimension = 768
```

Absolute path example:

```text
connect dbms vectors where type = milvus and path = /data/milvus_demo.db and dimension = 768
```

Verify:

```text
get databases
```

Collections appear under `Structure.Tables.vectors` (collections are exposed as tables), or list them directly:

```text
vector list where dbms = vectors
```

### Milvus server (URI)

```text
connect dbms vectors where type = milvus and uri = http://MILVUS_HOST:19530 and token = root:Milvus and dimension = 768
```

### Milvus server (host + port)

```text
connect dbms vectors where type = milvus and ip = MILVUS_HOST and port = 19530 and user = root and password = Milvus and dimension = 768
```

(`user` + `password` are combined into the Milvus token.)

### Disconnect

```text
disconnect dbms vectors
```

---

## Docker setup (Milvus standalone)

For a local Milvus **server** (not Lite), use a compose stack with etcd, MinIO, and Milvus standalone.

Example layout (tested on Apple Silicon; adjust `platform` for amd64 if needed):

```yaml
# docker-compose.milvus.yml
services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - etcd_data:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd

  minio:
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - minio_data:/minio_data
    command: minio server /minio_data --console-address ":9001"

  milvus:
    image: milvusdb/milvus:v2.4.15
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - milvus_data:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - etcd
      - minio

  attu:
    image: zilliz/attu:v2.4.12
    ports:
      # GUI — open http://MILVUS_HOST:3001 in a browser
      - "3001:3000"
    environment:
      # Attu runs inside Compose — use the Milvus *service name*, not MILVUS_HOST
      MILVUS_URL: milvus:19530
      MILVUS_USERNAME: root
      MILVUS_PASSWORD: YOUR_PASSWORD
    depends_on:
      - milvus

volumes:
  etcd_data:
  minio_data:
  milvus_data:
```

Start:

```bash
docker compose -f docker-compose.milvus.yml up -d
```


| Endpoint   | URL                                                |
| ---------- | -------------------------------------------------- |
| gRPC API   | `http://MILVUS_HOST:19530` |
| Attu (GUI) | `http://MILVUS_HOST:3001`  |


### Authentication

The Milvus standalone image enables authentication by default. Credentials (replace `YOUR_PASSWORD` — default install uses `Milvus`):


| Field    | Value                                                                     |
| -------- | ------------------------------------------------------------------------- |
| Username | `root`                                                                    |
| Password | `YOUR_PASSWORD`                                                           |
| Token    | `root:YOUR_PASSWORD` (`username:password` — pymilvus `MilvusClient` format) |


Set `MILVUS_HOST` to the machine running the compose stack (e.g. `localhost` on the same machine, or the host IP from a remote client):

```text
connect dbms vectors where type = milvus and uri = http://MILVUS_HOST:19530 and token = root:YOUR_PASSWORD and dimension = 768
```

Equivalent using host + port (`user` + `password` are combined into the token):

```text
connect dbms vectors where type = milvus and ip = MILVUS_HOST and port = 19530 and user = root and password = YOUR_PASSWORD and dimension = 768
```

Attu uses the same credentials (`MILVUS_USERNAME` / `MILVUS_PASSWORD` in the compose file above). If you change the Milvus password, update Attu and AnyLog to match.

---

## Quickstart (Milvus Lite)

Full walkthrough on a standalone operator:

```text
connect dbms vectors where type = milvus and path = !data_dir/milvus_demo.db and dimension = 768

vector create where dbms = vectors and collection = sensors and metric_type = COSINE

vector insert where dbms = vectors and collection = sensors and text = "door open" and subject = "security"
vector insert where dbms = vectors and collection = sensors and text = "temperature high" and subject = "process"

vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

vector query where dbms = vectors and collection = sensors and filter = "subject == 'security'"

get databases
```

### Text embedding example (`HISTORY_DOCS`)

Three separate sentences (as in the Milvus quickstart) need **three** `vector insert` commands — one row per `text` value:

```text
vector insert where dbms = vectors and collection = history and text = "Artificial intelligence was founded as an academic discipline in 1956." and subject = "history"

vector insert where dbms = vectors and collection = history and text = "Alan Turing was the first person to conduct substantial research in AI." and subject = "history"

vector insert where dbms = vectors and collection = history and text = "Born in Maida Vale, London, Turing was raised in southern England." and subject = "history"

vector search where dbms = vectors and collection = history and query = "Who worked on early artificial intelligence?" and limit = 3
```

If all sentences are in **one** `text` string (commas do **not** split documents):

```text
vector insert where dbms = vectors and collection = history and text = "Artificial intelligence was founded as an academic discipline in 1956., Alan Turing was the first person to conduct substantial research in AI., Born in Maida Vale, London, Turing was raised in southern England." and subject = "history"
```

| Step | What happens |
|------|----------------|
| **Processed by** | pymilvus `DefaultEmbeddingFunction` (`encode_documents`) — ONNX model `GPTCache/paraphrase-albert-onnx` (~768 dimensions) |
| **Inserted by** | `vector insert` → `milvus_dbms.py` → Milvus `insert` — **one entity**, one vector for the full string |

Search embeds the query the same way (`encode_queries`) via `vector search ... query = "..."`.

For bulk load from a file (many rows), use the standalone scripts in `/Users/massimiliano/Documents/milvusdb` (`milvus_prepare_data.py` → `milvus_insert_data.py`).

---

## Vector commands

All commands use the form:

```text
vector <method> where dbms = <name> [and collection = <name>] [options]
```

Help: `help vector` or `help vector search`.

### `vector create`

Create a collection with **auto-increment id** (`auto_id`). Default metric: **COSINE** (`L2`, `COSINE`, `IP` supported).

```text
vector create where dbms = vectors and collection = sensors

vector create where dbms = vectors and collection = sensors and metric_type = L2 and drop = true
```

### `vector list`

List collections on a connected dbms in a table (`collection`, `dimension`, `metric_type`, `rows`):

```text
vector list where dbms = vectors

vector list format = json and stat = true where dbms = vectors
```

Same collections as `get databases` → `Structure.Tables.<dbms>`, with per-collection stats.

### `vector insert`

Insert **one** entity per command. Two ways to supply the vector:

**Auto-embed from text** — omit `vector`. AnyLog calls the embedding model (`DefaultEmbeddingFunction`) and stores the resulting 768-float vector plus the original `text` string. Requires the Hugging Face ONNX model (see [Text embedding](#text-embedding-text--query)). Use this for natural-language content you want to search semantically later.

```text
vector insert where dbms = vectors and collection = sensors and text = "door open"
```

**Pre-computed vector** — pass `vector = […]` yourself (must match collection dimension, e.g. 768 floats). The model is **not** called. Add `text` only as an optional human-readable label stored alongside the vector — useful offline, custom embedders, or vectors produced by `milvus_prepare_data.py`.

```text
vector insert where dbms = vectors and collection = sensors and id = 1 and text = "door open" and vector = [0.1,0.2,0.3,...]
```

If both `vector` and `text` are present, the explicit `vector` wins; `text` is stored as metadata only.

Extra scalar fields (e.g. `subject`, `measure`) are stored as metadata on either form.

If the collection does not exist, it is created automatically on insert.

### `vector search`

Semantic similarity search (ANN). Use `query` for text embedding, or `vector` for a raw float list. Optional Milvus filter expression.

```text
vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

vector search where dbms = vectors and collection = sensors and query = "AI information" and filter = "subject == 'biology'" and limit = 2
```

JSON output:

```text
vector search format = json and stat = true where dbms = vectors and collection = sensors and query = "door open" and limit = 5
```

### `vector query`

Scalar metadata query (no vector similarity). Returns all rows, or filter by expression / ids.

```text
vector query where dbms = vectors and collection = sensors

vector query where dbms = vectors and collection = sensors and filter = "subject == 'history'"

vector query where dbms = vectors and collection = sensors and ids = (1,2) and output_fields = (id,text,subject)
```

### `vector delete`

Delete by primary key id(s) or filter. Requires `ids` **or** `filter` (not both).

```text
vector delete where dbms = vectors and collection = readings and ids = 467493353131606734

vector delete where dbms = vectors and collection = readings and ids = (467493353131606728,467493353131606730)

vector delete where dbms = vectors and collection = readings and filter = "measure == 'float'"

vector delete where dbms = vectors and collection = readings and filter = "text == 'sensor3'"
```

### `vector drop`

Remove an entire collection (schema + data).

```text
vector drop where dbms = vectors and collection = readings
```

---

## Cluster / `run client ()`

Vector **query**, **search**, and **delete** can fan out to operators that host the collection (registered on the blockchain after create/insert).

```text
run client () vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

run client (subset=true,timeout=30) vector search format = json and stat = true where dbms = vectors and collection = sensors and query = "door open" and limit = 5

run client () vector query where dbms = vectors and collection = sensors

run client () vector query format = json and stat = true where dbms = vectors and collection = sensors

run client () vector delete where dbms = vectors and collection = readings and filter = "measure == 'txt'"
```

`vector create` and `vector insert` run **locally** on the connected operator only (`run client ()` supports **query**, **search**, and **delete** only).

---

## Implementation notes


| Topic                     | Detail                                                                                                               |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Concurrency**           | One shared `MilvusClient` per logical dbms; thread-safe gRPC                                                         |
| **Collections as tables** | Listed via `get databases` / `Structure.Tables.<dbms>`                                                               |
| **Index metric**          | `COSINE` default; set with `metric_type` on `vector create`                                                          |
| **HA / replication**      | Not supported — no Milvus replication or sync across operators. Use **one Milvus connection per HA setup**, or on operators in **different cluster names** |
| **gRPC noise**            | Milvus Lite may log `GOAWAY ... too_many_pings` on stderr; usually harmless. Keepalive is tuned in `milvus_dbms.py`. |


---

## Troubleshooting

`**Milvus library not installed**`

```bash
pip install "pymilvus[milvus_lite,model]>=3.0.0" "transformers>=4.36,<5" onnxruntime
```

For Nuitka: reinstall deps, then rebuild `./build/nuitka_core.sh`.

**Collection exists without auto_id**

Recreate:

```text
vector create where dbms = vectors and collection = sensors and drop = true
```

**Embedding model unavailable (offline)**

Provide explicit vectors instead of `text` / `query`:

```text
vector insert where dbms = vectors and collection = sensors and vector = [0.1,0.2,...] and text = "label only"
```

**onnxruntime `Unknown CPU vendor` warning**

Harmless on some CPUs / Docker (especially Apple Silicon). Embedding still works if the command completes.

**Suppress gRPC stderr (optional)**

```bash
export GRPC_VERBOSITY=NONE
export GLOG_minloglevel=3
```

