# AnyLog as a _pip_ Package 

## Deployment Process 
1. Prerequisites
 
   **General**
   * [cython](https://pypi.org/project/Cython/)
   * [ast](https://docs.python.org/3/library/ast.html)
   * [requests](https://pypi.org/project/requests/)
   * [cryptography](https://pypi.org/project/cryptography/)
   * [jwt](https://pypi.org/project/jwt/) (for alpine - install [py3-jwt](https://pyjwt.readthedocs.io/en/stable/))
   * [pyOpenSSL](https://pypi.org/project/pyOpenSSL/)
   * [psutil](https://pypi.org/project/psutil/)
   * [python-dateutil](https://pypi.org/project/python-dateutil/)
   * [pytz](https://pypi.org/project/pytz/)
   
   **Database Specific** (optional)
   * [psycopg2-binary](https://www.psycopg.org/docs/) (for PostgresSQL, if you're using SQLite, there's no need to install this)
   * [pymongo](https://pymongo.readthedocs.io/en/stable/) (for storing blobs in MongoDB, alternatively, users can store blobs in files)
   
   **North / Southbound** (optional)
   * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
   * [kafka-python](https://pypi.org/project/kafka-python/) (for accepting and sending data via Kafka)
   
   **Utilizing Blockchain instead of Master Node** (optional)
   * [web3](https://pypi.org/project/web3/)
   * [py4j](https://pypi.org/project/py4j/)

    **Images & Video Processing** (optional)
    * [numpy](https://pypi.org/project/numpy/) (for alpine - install [py3-numpy](https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-numpy))
    * [opencv-python](https://pypi.org/project/opencv-python/) (for alpine - install [py3-opencv](https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-opencv))

The script bekow installs all prerequisites.
```shell
python3 -m pip install --upgrade -r https://raw.githubusercontent.com/AnyLog-co/documentation/master/deployments/Support/requirements.txt
```

2. Install AnyLog as a `pip` package - AnyLog pip package works with python3.10 for Ubuntu and MacOSX, as well as Python3.11 for Alpine.

Versions of AnyLog can be found in our [Downloads Page](http://173.255.254.34:31900/)

```shell
# Ubuntu
python3 -m pip install --upgrade http://173.255.254.34:31900/ubuntu/anylog_network-0.0.7-cp310-cp310-linux_x86_64.whl 

# Alpine
python3 -m pip install --upgrade http://173.255.254.34:31900/alpine/anylog_network-0.0.7-cp311-cp311-linux_x86_64.whl 

# Mac OSX  
python3 -m pip install --upgrade http://173.255.254.34:31900/macosx/anylog_network-0.0.7-cp310-cp310-macosx_12_0_x86_64.whl
```

3. Deploy [AnyLog node](https://raw.githubusercontent.com/AnyLog-co/deployment-scripts/main/scripts/anylog.py) 
```python
import sys
import anylog_node.cmd.user_cmd as user_cmd  # import AnyLog Node 

argv = sys.argv
argc = len(argv)

user_input = user_cmd.UserInput()
user_input.process_input(arguments=argc, arguments_list=argv) # Start AnyLog with CLI
```

4. Enable AnyLog (key valid until November 1, 2023) - for a personalized license key, [contact us](mailto:info@anylog.co) 
```anylog
set license where activation_key=01954e0dbfa1b5c1785aed6790a34097c5db148cb78405fd16ae2494045de3e844895851d03e0e599a799d6e6f03cbd2233a5f65a6dfb74832fb1034d5a56d8fa02563061a321da246e7660c4d00b9ea050b5d6fc4c61d7f9d53d58accec0434eb3b0fa98ae9237dfe09a6a75e0c6efcc4bc7860e9e358672b3d93943dbb416c2023-11-01bGuest
```
