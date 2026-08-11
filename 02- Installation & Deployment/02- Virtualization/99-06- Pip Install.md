---
title: "AnyLog as a _pip_ Package"
description: ""
layout: page
source_path: "training/advanced/99-06- Pip Install.md"
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Version**      | **Change** |
 |------------|----------------|------------------|----------|
 |            |                |                  |          |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 |            |
--->

# AnyLog as a _pip_ Package 

## Deployment Process 
1. Prerequisites
 
   **General**
   * <a href="https://pypi.org/project/Cython/" target="_blank">cython</a>
   * <a href="https://docs.python.org/3/library/ast.html" target="_blank">ast</a>
   * <a href="https://pypi.org/project/requests/" target="_blank">requests</a>
   * <a href="https://pypi.org/project/cryptography/" target="_blank">cryptography</a>
   * <a href="https://pypi.org/project/jwt/" target="_blank">jwt</a> (for alpine - install <a href="https://pyjwt.readthedocs.io/en/stable/" target="_blank">py3-jwt</a>)
   * <a href="https://pypi.org/project/pyOpenSSL/" target="_blank">pyOpenSSL</a>
   * <a href="https://pypi.org/project/psutil/" target="_blank">psutil</a>
   * <a href="https://pypi.org/project/python-dateutil/" target="_blank">python-dateutil</a>
   * <a href="https://pypi.org/project/pytz/" target="_blank">pytz</a>
   
   **Database Specific** (optional)
   * <a href="https://www.psycopg.org/docs/" target="_blank">psycopg2-binary</a> (for PostgresSQL, if you're using SQLite, there's no need to install this)
   * <a href="https://pymongo.readthedocs.io/en/stable/" target="_blank">pymongo</a> (for storing blobs in MongoDB, alternatively, users can store blobs in files)
   
   **North / Southbound** (optional)
   * <a href="https://pypi.org/project/paho-mqtt/" target="_blank">paho-mqtt</a>
   * <a href="https://pypi.org/project/kafka-python/" target="_blank">kafka-python</a> (for accepting and sending data via Kafka)
   
   **Utilizing Blockchain instead of Master Node** (optional)
   * <a href="https://pypi.org/project/web3/" target="_blank">web3</a>
   * <a href="https://pypi.org/project/py4j/" target="_blank">py4j</a>

    **Images & Video Processing** (optional)
    * <a href="https://pypi.org/project/numpy/" target="_blank">numpy</a> (for alpine - install <a href="https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-numpy" target="_blank">py3-numpy</a>)
    * <a href="https://pypi.org/project/opencv-python/" target="_blank">opencv-python</a> (for alpine - install <a href="https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-opencv" target="_blank">py3-opencv</a>)

The script below installs all prerequisites.
```shell
python3 -m pip install --upgrade -r https://raw.githubusercontent.com/AnyLog-co/documentation/master/deployments/Support/requirements.txt
```

2. Install AnyLog as a `pip` package  

    Note: Use the following Python version:
    * python3.10 for Ubuntu and Mac OS X
    * Python3.11 for Alpine

Versions of AnyLog can be found in the <a href="http://173.255.254.34:31900/" target="_blank">Downloads Page</a>

```shell
# Ubuntu
python3 -m pip install --upgrade http://173.255.254.34:31900/ubuntu/anylog_network-0.0.7-cp310-cp310-linux_x86_64.whl 

# Alpine
python3 -m pip install --upgrade http://173.255.254.34:31900/alpine/anylog_network-0.0.7-cp311-cp311-linux_x86_64.whl 

# Mac OSX  
python3 -m pip install --upgrade http://173.255.254.34:31900/macosx/anylog_network-0.0.7-cp310-cp310-macosx_12_0_x86_64.whl
```

3. Deploy <a href="https://raw.githubusercontent.com/AnyLog-co/deployment-scripts/main/scripts/anylog.py" target="_blank">AnyLog node</a> 
```python
import sys
import anylog_node.cmd.user_cmd as user_cmd  # import AnyLog Node 

argv = sys.argv
argc = len(argv)

user_input = user_cmd.UserInput()
user_input.process_input(arguments=argc, arguments_list=argv) # Start AnyLog with CLI
```

4. Enable AnyLog (key valid until November 1, 2023) - for a personalized license key, <a href="mailto:info@anylog.co" target="_blank">contact us</a> 
```anylog
set license where activation_key=01954e0dbfa1b5c1785aed6790a34097c5db148cb78405fd16ae2494045de3e844895851d03e0e599a799d6e6f03cbd2233a5f65a6dfb74832fb1034d5a56d8fa02563061a321da246e7660c4d00b9ea050b5d6fc4c61d7f9d53d58accec0434eb3b0fa98ae9237dfe09a6a75e0c6efcc4bc7860e9e358672b3d93943dbb416c2023-11-01bGuest
```
