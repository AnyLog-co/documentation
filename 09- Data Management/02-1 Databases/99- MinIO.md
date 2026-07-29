---
title: "MinIO Object Storage"
description: "Connecting AnyLog to a MinIO endpoint for bucket file management — connection setup, Docker deployment, the bucket command family applied to MinIO, and troubleshooting."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Added missing frontmatter (this doc had none). Fixed both cross-reference links, which pointed at paths that don't match this repo (`04- Core Concepts/Bucket Data Management.md` and `06- Data Management/...` — the confirmed real folders are `99- Core Concepts` and `09- Data Management`); repointed the first to the actual Bucket Storage doc. Renamed the "remote host" connect example's group from `local_minio` (reused from the local example right above it) to `remote_minio`, since reusing the same name for a different endpoint was confusing. Flagged the MinIO bucket-naming-rules link, which points at a page about deploying a single-node MinIO server, not bucket naming. Standardized one stray `text` code fence to `anylog` to match every other example in this doc; fixed a trailing space inside a bold heading | |
--->

# MinIO object storage

AnyLog connects to a **MinIO** endpoint for bucket file management (upload, download, list, delete) via the `bucket` commands.

See also: [Bucket Commands](04-%20Bucket%20Storage.md) for the general, provider-agnostic command reference.

---

## Docker setup (MinIO standalone)

For a local MinIO server (API on **9000**, console on **9001**):

```yaml
# docker-compose.minio.yml
services:
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"

volumes:
  minio_data:
```

Start:

```bash
docker compose -f docker-compose.minio.yml up -d
```

| Endpoint      | URL                      |
| ------------- | ------------------------ |
| S3 API        | `http://MINIO_HOST:9000` |
| MinIO Console | `http://MINIO_HOST:9001` |

Replace `MINIO_HOST` with `localhost` on the same machine, or the host IP from a remote AnyLog node.

### Credentials

Default MinIO install values (change these in production):

| Field      | Value        | AnyLog keyword                     |
| ---------- | ------------ | ---------------------------------- |
| Access key | `minioadmin` | `id` or `access_key`               |
| Secret key | `minioadmin` | `password` or `secret_key`         |
| Region     | optional     | `region` (defaults to `us-east-1`) |

---

## Connect

`group` is a **logical** connection name. Two groups with the same endpoint and keys see the same object store.

### MinIO (local)

**connect**

```anylog
<bucket provider connect where
    group = local_minio and
    provider = minio and
    id = minioadmin and
    password = minioadmin and
    endpoint_url = http://localhost:9000
>
```

Equivalent using `access_key` / `secret_key`:

```anylog
<bucket provider connect where
    group = local_minio and
    provider = minio and
    access_key = minioadmin and
    secret_key = minioadmin and
    endpoint_url = http://localhost:9000
>
```

Optional region (MinIO does not use region for placement; boto3 still needs a signing region — AnyLog defaults to 
`us-east-1` when omitted):

```anylog
<bucket provider connect where
    group = local_minio and
    provider = minio and
    id = minioadmin and
    password = minioadmin and
    region = us-east-1 and
    endpoint_url = http://localhost:9000
>
```

### MinIO (remote host)

**connect**

```anylog
<bucket provider connect where
    group = remote_minio and
    provider = minio and
    id = minioadmin and
    password = minioadmin and
    endpoint_url = http://MINIO_HOST:9000
>
```

### Verify

**get**

```anylog
get bucket groups
```

```anylog
get bucket names where group = local_minio
```

### Disconnect

**disconnect**

```anylog
bucket provider disconnect where group = local_minio
```

---

## Quickstart

Full walkthrough against a local MinIO. Create a small local file before upload if needed:

```bash
echo "hello minio" > /tmp/my-test-file.txt
```

**connect**

```anylog
<bucket provider connect where
    group = local_minio and
    provider = minio and
    id = minioadmin and
    password = minioadmin and
    endpoint_url = http://localhost:9000
>
```

**get**

```anylog
get bucket groups
```

**create**

```anylog
bucket create where group = local_minio and name = python-test-bucket
```

**get**

```anylog
get bucket names where group = local_minio
```

**upload**

```anylog
<bucket file upload where
    group = local_minio and
    name = python-test-bucket and
    source_dir = /tmp and
    file_name = my-test-file.txt and
    key = my-test-file.txt
>
```

**get**

```anylog
get bucket files where group = local_minio and name = python-test-bucket and format = json
```

**download**

```anylog
<bucket file download where
    group = local_minio and
    name = python-test-bucket and
    key = my-test-file.txt and
    dest_dir = /tmp and
    file_name = minio-download.txt
>
```

**get bucket info**

```anylog
get bucket file info where group = local_minio and name = python-test-bucket and key = my-test-file.txt
```

**delete file by key**

```anylog
bucket file delete where group = local_minio and name = python-test-bucket and key = my-test-file.txt
```

**drop bucket (and all files)**

```anylog
bucket drop where group = local_minio and name = python-test-bucket and delete_all = true
```

**disconnect**

```anylog
bucket provider disconnect where group = local_minio
```

---

## Bucket commands (MinIO)

All commands use the form:

```anylog
bucket <method> where group = <name> [and name = <bucket>] [options]
```

Help: `help bucket` or `help bucket provider connect`.

### `bucket provider connect`

**connect** — create a logical connection to MinIO.

| Parameter      | Required | Meaning                                 |
| -------------- | -------- | --------------------------------------- |
| `group`        | yes      | Logical connection name                 |
| `provider`     | yes      | `minio`                                 |
| `id`           | yes*     | Access key (`access_key` also accepted) |
| `password`     | yes*     | Secret key (`secret_key` also accepted) |
| `endpoint_url` | yes      | MinIO S3 API URL (`http://host:9000`)   |
| `region`       | no       | Defaults to `us-east-1` for MinIO       |

 Use either `id`/`password` or `access_key`/`secret_key`.

### `get bucket groups`

**get** — list active bucket groups on this node.

```anylog
get bucket groups
```

### `get bucket names`

**get** — list buckets visible to a group.

```anylog
get bucket names where group = local_minio
```

### `bucket create`

**create** — create a physical bucket.

```anylog
bucket create where group = local_minio and name = python-test-bucket
```

Follow S3-compatible bucket naming rules (lowercase, no underscores in many setups).

### `get bucket files`

**get** — list objects in a bucket. Optional `prefix` filters keys.

```anylog
get bucket files where group = local_minio and name = python-test-bucket and format = json
```

```anylog
get bucket files where group = local_minio and name = python-test-bucket and prefix = dir1/ and format = json
```

### `bucket file upload`

**upload** — upload a local file. `source_dir` is the directory only (no file name); `key` is the object name in the bucket.

```anylog
<bucket file upload where
    group = local_minio and
    name = python-test-bucket and
    source_dir = /tmp and
    file_name = my-test-file.txt and
    key = my-test-file.txt
>
```

**download** — download by object `key`.

```anylog
<bucket file download where
    group = local_minio and
    name = python-test-bucket and
    key = my-test-file.txt and
    dest_dir = /tmp and
    file_name = minio-download.txt
>
```

**get** — object metadata for a key.

```anylog
get bucket file info where group = local_minio and name = python-test-bucket and key = my-test-file.txt
```

**delete** — delete by `key`, by `prefix`, or both.

```anylog
bucket file delete where group = local_minio and name = python-test-bucket and key = my-test-file.txt
```

```anylog
bucket file delete where group = local_minio and name = python-test-bucket and prefix = dir1/
```

**drop** — delete a bucket. For MinIO, `delete_all = true` removes objects then drops the bucket; `delete_all = false` only succeeds on an already-empty bucket.

```anylog
bucket drop where group = local_minio and name = python-test-bucket and delete_all = false
```

```anylog
bucket drop where group = local_minio and name = python-test-bucket and delete_all = true
```

**disconnect**

```anylog
bucket provider disconnect where group = local_minio
```

## Related

- [Bucket Commands](04-%20Bucket%20Storage.md) — general, provider-agnostic command reference
- [MinIO documentation](https://min.io/docs/minio/linux/index.html)