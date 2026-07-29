---
title: "Milvus: Install & Full Deployment"
description: "Standing up Milvus via Docker, then a full connect-to-query walkthrough — matching the deployment style of the MongoDB and MinIO docs."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon    | Created — split out of "05- Milvus" to hold the Docker install, authentication, and full deployment walkthrough separately from the concept/command reference, matching the MongoDB/MinIO doc split | |
--->

This page covers standing up a Milvus **server** via Docker (for Milvus **Lite**, no server setup is needed — see
[05- Milvus](05-%20Milvus.md#connect)), then a full walkthrough from first connection through querying data back
out.

---

## Docker setup (Milvus standalone)

For a local Milvus **server** (not Lite), use a compose stack with etcd, MinIO, and Milvus standalone.

Example layout (tested on Apple Silicon; adjust `platform` for amd64 if needed):

> Image tags below are current as of this doc's writing — worth checking for newer releases before deploying.

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

Attu uses the same credentials (`MILVUS_USERNAME` / `MILVUS_PASSWORD` in the compose file above). If you change the
Milvus password, update Attu and AnyLog to match.

---

## Offline model setup

The text-embedding model (see [05- Milvus](05-%20Milvus.md#text-embedding-text--query)) needs internet access once
to download. For an offline node, download it on a build machine and ship the cache over:

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

## Full Deployment Walkthrough

Set `MILVUS_HOST` to the machine running the compose stack (`localhost` on the same machine, or the host IP from a
remote client) before starting.

1. Bring up the Milvus stack (see [Docker setup](#docker-setup-milvus-standalone) above)
```bash
docker compose -f docker-compose.milvus.yml up -d
```

2. Connect AnyLog to Milvus
```anylog
connect dbms vectors where type = milvus and uri = http://MILVUS_HOST:19530 and token = root:YOUR_PASSWORD and dimension = 768
```
Verify:
```anylog
get databases
```

3. Create a collection
```anylog
vector create where dbms = vectors and collection = sensors and metric_type = COSINE
```
Verify:
```anylog
vector list where dbms = vectors
```

4. Insert data
```anylog
vector insert where dbms = vectors and collection = sensors and text = "door open" and subject = "security"
vector insert where dbms = vectors and collection = sensors and text = "temperature high" and subject = "process"
```

5. Query data — semantic search
```anylog
vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5
```
See [Query Data](05-%20Milvus.md#query-data) for what the result looks like and how to interpret the similarity score.

6. Query across the network (if the collection is hosted on multiple operators)
```anylog
run client () vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5
```

7. Tear down
```anylog
disconnect dbms vectors
```
```bash
docker compose -f docker-compose.milvus.yml down
```

### Quickstart (Milvus Lite, no Docker/server needed)

If you don't need a full server deployment, the same flow works entirely locally against a Milvus Lite file:

```anylog
connect dbms vectors where type = milvus and path = !data_dir/milvus_demo.db and dimension = 768

vector create where dbms = vectors and collection = sensors and metric_type = COSINE

vector insert where dbms = vectors and collection = sensors and text = "door open" and subject = "security"
vector insert where dbms = vectors and collection = sensors and text = "temperature high" and subject = "process"

vector search where dbms = vectors and collection = sensors and query = "door open" and limit = 5

vector query where dbms = vectors and collection = sensors and filter = "subject == 'security'"

get databases
```

#### Text embedding example (`HISTORY_DOCS`)

Three separate sentences (as in the Milvus quickstart) need **three** `vector insert` commands — one row per `text` value:

```anylog
vector insert where dbms = vectors and collection = history and text = "Artificial intelligence was founded as an academic discipline in 1956." and subject = "history"

vector insert where dbms = vectors and collection = history and text = "Alan Turing was the first person to conduct substantial research in AI." and subject = "history"

vector insert where dbms = vectors and collection = history and text = "Born in Maida Vale, London, Turing was raised in southern England." and subject = "history"

vector search where dbms = vectors and collection = history and query = "Who worked on early artificial intelligence?" and limit = 3
```

If all sentences are in **one** `text` string (commas do **not** split documents):

```anylog
vector insert where dbms = vectors and collection = history and text = "Artificial intelligence was founded as an academic discipline in 1956., Alan Turing was the first person to conduct substantial research in AI., Born in Maida Vale, London, Turing was raised in southern England." and subject = "history"
```

| Step | What happens |
|------|----------------|
| **Processed by** | pymilvus `DefaultEmbeddingFunction` (`encode_documents`) — ONNX model `GPTCache/paraphrase-albert-onnx` (~768 dimensions) |
| **Inserted by** | `vector insert` → `milvus_dbms.py` → Milvus `insert` — **one entity**, one vector for the full string |

Search embeds the query the same way (`encode_queries`) via `vector search ... query = "..."`.

For bulk load from a file (many rows), use the standalone scripts under `[path to milvus scripts]/milvusdb`
(`milvus_prepare_data.py` → `milvus_insert_data.py`).

---

## Troubleshooting

**Milvus library not installed**

```bash
pip install "pymilvus[milvus_lite,model]>=3.0.0" "transformers>=4.36,<5" onnxruntime
```

For Nuitka: reinstall deps, then rebuild `./build/nuitka_core.sh`.

**Collection exists without auto_id**

Recreate:

```anylog
vector create where dbms = vectors and collection = sensors and drop = true
```

**Embedding model unavailable (offline)**

Provide explicit vectors instead of `text` / `query`:

```anylog
vector insert where dbms = vectors and collection = sensors and vector = [0.1,0.2,...] and text = "label only"
```

**onnxruntime `Unknown CPU vendor` warning**

Harmless on some CPUs / Docker (especially Apple Silicon). Embedding still works if the command completes.

**Suppress gRPC stderr (optional)**

```bash
export GRPC_VERBOSITY=NONE
export GLOG_minloglevel=3
```

---

## Related

- [05- Milvus](05-%20Milvus.md) — concepts, connection reference, and the full `vector` command set