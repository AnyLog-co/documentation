# Bucket Commands

The ***bucket*** command provides a means to push (upload) and pull (download) files from a bucket object storage.
See [examples](#examples) below.

## 🌐 Supported Backends
- **Akave Cloud** (currently supported for file object management).  
- **AWS S3** (the API is AWS-compatible, but direct support is not yet fully tested. Official AWS support will be extended soon).  

---

## 🔧 Operations Supported
Operations supported:

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

<a id="bucket-provider-connect"></a>
### Bucket Provider Connect
Defines a logical connection to a named bucket object storage. For access to Akave, please contact the AnyLog team.

```bash
bucket provider connect where group = [group_name] and provider = [provider] and id = 123 and access_key = [access_key] and secret_key = [secret_key] and region = [region] and endpoint_url = [endpoint_url]
```
| Parameter                                                                  | -                                 | 
|----------------------------------------------------------------------------|-----------------------------------|
| group                                                                      | Logical connection name           |
| provider                                                                   | Provider name                     |
| access_key                                                                 | Private access key                | 
| secret_key                                                                 | Private secret key                | 
| region                                                                     | Region name                       |
| endpoint_url                                                               | URL connection to object storage  |

<a id="get-bucket-groups"></a>
### Get Bucket Groups
Displays a list of logically defined bucket group by name.
```bash
get bucket groups
```

<a id="get-bucket-names"></a>
### Get All Bucket Names
List all buckets defined or available to the group
```bash
get bucket names where group = [group_name]
```
| Parameter                                                                  | -                         | 
|----------------------------------------------------------------------------|---------------------------|
| group                                                                      | Logical connection name   |

<a id="bucket-create"></a>
### Bucket Create
Create a physical bucket for file/object storage. 
```bash
bucket create where group = [group_name] and name = [bucket_name]
```
| Parameter | -                                                                                                                                                      | 
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| group     | Logical connection name (str)                                                                                                                          |
| name      | The bucket name. Note that there are restrictions on bucket naming conventions. Please check the reference [bucket naming convention documentation](https://docs.akave.xyz/akave-o3/bucket-management/bucket-naming-rules/). |


<a id="get-bucket-files"></a>
### Get Bucket Files
List all files in bucket. If prefix is not specified, then all files in bucket are displayed, otherwise only files whose
keys start with the prefix string will be displayed. 
```bash
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
```bash
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
```bash
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
```bash
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
Delete bucket. Note that you cannot delete an empty bucket; however, we've added support to delete all files within the command.
```bash
bucket drop where group = [group_name] and name = [bucket_name] and deleteAllFiles = [true/false]  
bucket drop where group = [group_name] and name = [bucket_name] and deleteAllFiles = false  # will only delete an empty bucket
bucket drop where group = [group_name] and name = [bucket_name] and deleteAllFiles = true  # will delete a non-empty bucket
```
| Parameter      | -                                            | 
|----------------|----------------------------------------------|
| group          | Logical connection name                      |
| name           | Bucket name                                  |
| deleteAllFiles | Boolean parameter to delete non-empty bucket |

<a id="examples"></a>
# Examples
```bash
#Step 1 - declare provider 
bucket provider connect where group = my_group and provider = akave and id = 123 and access_key = [access_key] and secret_key = [secret_key] and region = akave-network and endpoint_url = [endpoint_url]

# Step 2 - view providers 
get bucket groups

# Step 3 - create bucket (See bucket naming restrictions Bucket Naming Rules )
bucket create where group = my_group and name = my-bucket

#Step 4 - view all buckets by group
get bucket names where group = my_group

#Step 5 - view all files in bucket or by prefix
get bucket files where group = my_group and name = my-bucket and prefix = dir1 and format = json
get bucket files where group = my_group and name = my-bucket and format = json

#Step 6 - upload file
bucket file upload where group = my_group and name = my-bucket and source_dir = /Users/roy and file_name = test.txt and key = dir1/test2.txt

#Step 7 - download file
bucket file download where group = my_group and name = my-bucket and key = test.txt and dest_dir = /Users/roy/test2 and file_name = test.txt

#Step 8 - delete file by key or set of files by prefix (note if prefix and key set, both will be deleted)
bucket file delete where group = my_group and name = my-bucket and key = test.txt
bucket file delete where group = my_group and name = my-bucket and prefix = dir1
bucket file delete where group = my_group and name = my-bucket and key = test2.txt and prefix = dir1

#Step 8 - get file metadata
get bucket file info where group = my_group and name = my-bucket and key = test2.txt

#Step 9 - drop/delete bucket (note that you cannot delete a non-empty bucket. to delete non-empty bucket, set deleteAllFiles = true)
bucket drop where group = my_group and name = my-bucket and deleteAllFiles = false
bucket drop where group = my_group and name = my-bucket and deleteAllFiles = true
```







