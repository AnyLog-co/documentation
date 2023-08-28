# AnyLog as a _pip_ Package 

Deploying AnyLog can now be done via _pip install_ rather than just through [docker](../../deployments/Quick%20Deployment.md).

## Deployment Process 
1. Install requirements - except for _General_,  all other requirements are not required and can be installed per-need bases.
 
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
   
   **Database Specific** 
   * [psycopg2-binary](https://www.psycopg.org/docs/) (for PostgresSQL, if you're using SQLite, there's no need to install this)
   * [pymongo](https://pymongo.readthedocs.io/en/stable/) (for storing blobs in MongoDB, alternatively, users can store blobs in files)
   
   **North / Southbound**
   * [paho-mqtt](https://pypi.org/project/paho-mqtt/)
   * [kafka-python](https://pypi.org/project/kafka-python/) (for accepting and sending data via Kafka)
   
   **Utilizing Blockchain instead of Master Node**
   * [web3](https://pypi.org/project/web3/)
   * [py4j](https://pypi.org/project/py4j/)

    **Images & Video Processing**
    * [numpy](https://pypi.org/project/numpy/) (for alpine - install [py3-numpy](https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-numpy))
    * [opencv-python](https://pypi.org/project/opencv-python/) (for alpine - install [py3-opencv](https://pkgs.alpinelinux.org/package/edge/community/armv7/py3-opencv))

The requirements script installs all prerequisites.
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