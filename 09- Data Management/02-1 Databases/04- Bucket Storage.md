---
title: "Bucket Storage"
description: "General reference for AnyLog's bucket command family (upload/download/list/delete files against S3-compatible object storage), covering MinIO, Akave, and AWS S3."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Fixed the connect parameter table, which only listed `access_key`/`secret_key` while the example right below it used `id`/`password` — now documents both as aliases, matching MinIO.md. Added a note explaining why `provider` only lists `minio`/`akave` despite AWS S3 being mentioned in the intro (not yet fully tested). Removed a redundant/contradictory `id = 123` sitting alongside `access_key = [access_key]` in the same example command. Fixed duplicate "Step 8" numbering in the Examples walkthrough. Removed a real person's home directory (`/Users/roy`) from the upload/download examples. Standardized the `key` value used across the entire walkthrough — it previously changed at almost every step (`dir1/test2.txt`, `test.txt`, `test2.txt`), meaning the download/delete/metadata steps were referencing files that were never actually uploaded | |
--->

There are 2 ways by which to store blob data - [NoSQL](./03-%20NoSQL%20%28MongoDB%29.md) and bucket storage, whether it's
MinIO, Akave (Filecoin's S3 alternative), or AWS's S3 and the likes.

* MinIO (S3-compatible) — see [MinIO](../../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/02-%20MinIO.md) for connection setup, Docker deployment, and troubleshooting.
* Akave Cloud (currently supported for file object management).
* AWS S3 (the API is AWS-compatible, but direct support is not yet fully tested. Official AWS support will be extended soon).

## `bucket` command

The `bucket` command provides a means to push (upload) and pull (download) files from a bucket object storage.

| Operation                                           | Use case                                               |
|-----------------------------------------------------|--------------------------------------------------------|
| [bucket provider connect](#bucket-provider-connect) | Connect to bucket object store.                        |
| [get bucket groups](#get-bucket-groups)             | View all bucket groups.                                |
| [get bucket names](#get-bucket-names)    | View all buckets by group.                             |
| [bucket create](#bucket-create)                     | Create bucket.                                         |
| [get bucket files](#get-bucket-files)               | List all files from bucket.                            |
| [bucket file upload](#bucket-file-upload)           | Upload file to bucket.                                 |
| [bucket file download](#bucket-file-download)       | Download file from bucket.                             |
| [bucket file delete](#bucket-file-delete)           | Delete file from bucket.                               |
| [bucket drop](#bucket-drop)                         | Delete bucket.                                         |

### Bucket Provider Connect

Defines a logical connection to a named bucket object storage.

| Parameter      | -                                                 |
|----------------|----------------------------------------------------|
| group          | Logical connection name                             |
| provider       | Provider name (`minio` or `akave` — see note below) |
| id / access_key | Private access key (either name works)             |
| password / secret_key | Private secret key (either name works)       |
| region         | Region name (behavior/defaults vary by provider — see the provider-specific doc, e.g. [MinIO](../../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/02-%20MinIO.md#credentials)) |
| endpoint_url   | URL connection to object storage                    |

> `provider` currently lists `minio`/`akave` — AWS S3 is API-compatible and mentioned above as a future target, but
> isn't included here yet since direct AWS support isn't fully tested.

```anylog
<bucket provider connect where 
  group = [group_name] and 
  provider = [minio|akave] and 
  id = [access_key] and 
  password = [secret_key] and 
  endpoint_url = [endpoint_url] and 
  region = [region]>
```
> *Note* that `group` is a logical definition of a connection to an object storage location. If you define two
> different groups that connect to the same `endpoint_url`, `access_key`, and `secret_key`, then queries to either
> group will return the same object storage view.

### Get Bucket Groups

Displays a list of logically defined bucket group by name.

```anylog
get bucket groups
```

### Get All Bucket Names

List all buckets defined or available to the group

| Parameter                                                                  | -                         |
|----------------------------------------------------------------------------|---------------------------|
| group                                                                      | Logical connection name   |

```anylog
get bucket names where group = [group_name]
```

### Bucket Create

Create a physical bucket for file/object storage.

| Parameter | -                                                                                                                                                      |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| group     | Logical connection name (str)                                                                                                                          |
| name      | The bucket name. Note that there are restrictions on bucket naming conventions. Please check the reference [bucket naming convention documentation](https://docs.akave.xyz/akave-o3/bucket-management/bucket-naming-rules/). |

```anylog
bucket create where group = [group_name] and name = [bucket_name]
```

<a id="get-bucket-files"></a>
### Get Bucket Files
List all files in bucket. If prefix is not specified, then all files in bucket are displayed, otherwise only files whose
keys start with the prefix string will be displayed.
```anylog
get bucket files where group = [group_name] and name = [bucket_name] and prefix = [string-prefix] and format = json
get bucket files where group = [group_name] and name = [bucket_name] and format = json
```
| Parameter | -                                                                        |
|-----------|--------------------------------------------------------------------------|
| group     | Logical connection name                                                  |
| name      | Bucket name                                                              |
| prefix    | String prefix for search. Note that the prefix is an optional parameter  |

<a id="bucket-file-upload"></a>
### Bucket File Upload
Upload file to specified bucket.
```anylog
bucket file upload where group = [group_name] and name = [bucket_name] and source_dir = [local_source_directory] and file_name = [file_name] and key = [file_key]
```
| Parameter  | -                                                                                       |
|------------|-----------------------------------------------------------------------------------------|
| group      | Logical connection name                                                                 |
| name       | Bucket name                                                                             |
| source_dir | Source directory of file location (Note, do not include the filename)                   |
| file_name  | Filename to upload                                                                      |
| key        | Unique filename in bucket (Note that you use this key to download file from the bucket) |

<a id="bucket-file-download"></a>
### Bucket File Download
Download file from bucket
```anylog
bucket file download where group = [group_name] and name = [bucket_name] and key = [file_key] and dest_dir = [destination_dir] and file_name = [filename]
```
| Parameter | -                                                                                          |
|-----------|--------------------------------------------------------------------------------------------|
| group     | Logical connection name                                                                    |
| name      | Bucket name                                                                                |
| key       | Unique filename in bucket                                                                  |
| dest_dir  | Destination directory where to download file to (Note only put destination, not file name) |
| file_name | Filename to name downloaded file                                                           |

<a id="bucket-file-delete"></a>
### Bucket File Delete
Delete file from bucket by key or a set of files by specified prefix.
```anylog
bucket file delete where group = [group_name] and name = [bucket_name] and key = [file_key]    # deletes one file
bucket file delete where group = [group_name] and name = [bucket_name] and prefix = [str-prefix]  # deletes all files with keys that start with the prefix
bucket file delete where group = [group_name] and name = [bucket_name] and key = [file_key] and prefix = [str-prefix]  # deletes one file and all files with keys that start with the prefix
```
| Parameter | -                          |
|-----------|----------------------------|
| group     | Logical connection name    |
| name      | Bucket name                |
| key       | Unique filename in bucket  |
| prefix    | String prefix for search   |

<a id="bucket-drop"></a>
### Bucket Drop
Delete bucket. Note that you cannot delete a non-empty bucket by default; however, we've added support to delete all
files within the command.
```anylog
bucket drop where group = [group_name] and name = [bucket_name] and delete_all = [true/false]  
bucket drop where group = [group_name] and name = [bucket_name] and delete_all = false  # will only delete an empty bucket
bucket drop where group = [group_name] and name = [bucket_name] and delete_all = true  # will delete a non-empty bucket
```
| Parameter    | -                                             |
|--------------|-----------------------------------------------|
| group        | Logical connection name                       |
| name         | Bucket name                                   |
| delete_all   | Boolean parameter to delete a non-empty bucket |

<a id="examples"></a>
# Examples
```anylog
# Step 1 - declare provider
bucket provider connect where group = my_group and provider = akave and access_key = [access_key] and secret_key = [secret_key] and region = akave-network and endpoint_url = [endpoint_url]

# Step 2 - view providers
get bucket groups

# Step 3 - create bucket (see Bucket Naming Rules linked above)
bucket create where group = my_group and name = my-bucket

# Step 4 - view all buckets by group
get bucket names where group = my_group

# Step 5 - view all files in bucket or by prefix
get bucket files where group = my_group and name = my-bucket and prefix = dir1 and format = json
get bucket files where group = my_group and name = my-bucket and format = json

# Step 6 - upload file
bucket file upload where group = my_group and name = my-bucket and source_dir = /tmp and file_name = test.txt and key = dir1/test.txt

# Step 7 - download file
bucket file download where group = my_group and name = my-bucket and key = dir1/test.txt and dest_dir = /tmp/downloaded and file_name = test.txt

# Step 8 - delete file by key or set of files by prefix (note if prefix and key are both set, both are deleted)
bucket file delete where group = my_group and name = my-bucket and key = dir1/test.txt
bucket file delete where group = my_group and name = my-bucket and prefix = dir1

# Step 9 - get file metadata
get bucket file info where group = my_group and name = my-bucket and key = dir1/test.txt

# Step 10 - drop/delete bucket (note that you cannot delete a non-empty bucket unless delete_all = true)
bucket drop where group = my_group and name = my-bucket and delete_all = false
bucket drop where group = my_group and name = my-bucket and delete_all = true
```