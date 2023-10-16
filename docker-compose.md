# Docker

This document aims to provide an overview of the fundamental services offered by AnyLog using a minimal image. 
AnyLog is designed to minimize its footprint on your machine through Dockerization. The Dockerization process consists 
of two parts:

* **Part I: Minimal Installation** - An image containing the essential components required to run AnyLog.

* **Part II: Extending Functionality** - Users have the flexibility to extend the minimalist image by utilizing it as 
their base image and adding functionality as needed. This can be things like _MQTT_, _PostgresSQL_, _MongoDB_ and blockchain support 
(ex. _Etherium_, _Hyperledger_ or even _eos_) 
 
| Operating System |   Image Tag   | Image Size | 
| :---: |:-------------:|:----------:|
| Alpine | latest-alpine |   380MB    |
| Ubuntu |    latest     |   380MB    | 


## Anylog Image Explained
By default, a minimal AnyLog installation provides the following capabilities using a predefined set of packages: 

**Capabilities**:
* SQLite is supported 
* Blobs (in base64 format) will be stored to file rather than (NoSQL / MongoDB) database
* Requires the use of a _Master_ node rather than an actual blockchain; such as - _Etherium_, _Hyperledger_ and _EOS_. 
* Mapping of data (ie `run mqtt client`) can be done using REST _POST_. However, not through other services (_Kafka_ and _MQTT_)
simply because the relevant plugins are **not** installed.
* Monitoring of the physical machine, as well as the AnyLog node     

**Python3 Packages**: 
* psutil 
* requests 
* pytz 
* dateutil 
* cryptography


## Extending the Image
As mentioned above, the default image, allows to deploy AnyLog with its core capabilities. However, many times a  node 
may need other services in order to truly complete its task. This section will cover the different options as well as how
to extend AnyLog images. 

**Python3 Packages**: 
* jwt (~1MB) - Used for encoding and decoding JSON Web Tokens, which are used for secure authentication and data exchange between parties
* pyOpenSSL (~5MB) - Wrapper for the OpenSSL library. It provides support for SSL/TLS encryption and decryption, making it useful for securing network communication. 
* psycopg2-binary (~5MB) - PostgresSQL adapter for Python
* pymongo (~5MB) - MongoDB adapter for Python
* numpy (~5MB) - Provides support for arrays when image and video processing is done through _bytesIO_ 
* opencv-python (~100MB) -  Computer vision library used by developers to work with image and video data, perform image 
processing, and build computer vision applications. It is used when images and videos coming in are of type _opencv_. 
* paho-mqtt (~1MB) - Client library for MQTT protocol. AnyLog uses it for both receiving and processing information via MQTT. 
* kafka-python (~1MB) - Client library for Kafka streaming platform. 
* web3 (~1MB) & py4j (~1MB) - _py4j_ is used to interact with Java packages, while _web3_ is intended for Etherium based blockchains. 
Both packages are required when connecting to an actual blockchain - such as _Etherium_, _Hyperledger_ and _EOS_.

**Sample Docker**: 
The following provides an example of a dockerfile with everything installed, Other examples can be found in out [deployments](https://github.com/AnyLog-co/deployments).
```dockerfile
#--------------------------------------------------------------------------------------------#
# The following provides a sample Dockerfile extending AnyLog to include all possible packages.
#
# Base Operating Syste: alpine:latest 
# Base image:  anylogco/anylog-netwokr:latest-alpine
#  
#--------------------------------------------------------------------------------------------#
FROM anylogco/anylog-netwokr:latest-alpine AS extended_base 

RUN apk update && \
    apk add openssl-dev build-base postgresql-libs libffi-dev libressl-dev py3-numpy && \
    pip3 install --upgrade pip && \
    pip3 install jwt pyOpenSSL psycopg2-binary pymongo paho-mqtt kafka-python web3 py4j opencv-python 
```

**Steps**: 
1. Create a personalized dockerfile - example shown above & in deployments. 
2. Build Dockerfile 
```shell
docker build . -t anylogco/anylog-network:personalized
```
3. Update `.env` and configurations as desired 
4. Deploy AnyLog using the `docker-compose up -d` command