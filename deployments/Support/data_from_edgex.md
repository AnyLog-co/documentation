# Publishing Data via EdgeXpert Manager

EdgeX (Foundry) is an Open-Source framework that serves as a foundation for building and deploying Internet of Things (IoT)
edge computing solutions. While EdgeXpert is an enterprise version of _EdgeX_, provided by IoTech System. 

Note: a detailed explanation on how data is added to the AnyLog Network nodes is available at the [adding data](../../adding%20data.md) section.

This document demonstrates how to publish data into AnyLog via EdgeXpert Management tool.   
Edgex related documentation is available with the links below:

* [EdgeX Foundry](https://www.edgexfoundry.org/)
* [IoTech System](https://www.iotechsys.com/)
* [User Guide](https://docs.iotechsys.com/)
* [Manual Deployment of EdgeX](EdgeX.md)


For demonstration, the examples used is **retail-1** data source, provided by IoTech System.  
```json
{
  "apiVersion":"v2",
  "id":"ff3013c3-2f96-48b6-ac06-5eeb4cde1ecf",
  "deviceName":"retail-device-1",
  "profileName":"RetailVirtualDevice",
  "sourceName":"FreezerTemp1",
  "origin":1694737678685722461,
  "readings":[{
    "id":"000a2227-0ff8-4534-8131-310a7efcdd47",
    "origin":1694737678685722461,
    "deviceName":"retail-device-1",
    "resourceName":"FreezerTemp1",
    "profileName":"RetailVirtualDevice",
    "valueType":"Float32",
    "units":"F",
    "value":"3.140839e+01"
  }]
}
{
  "apiVersion":"v2",
  "id":"e60989ad-ab59-456e-bb00-b90518ca83e1",
  "deviceName":"retail-device-1",
  "profileName":"RetailVirtualDevice",
  "sourceName":"PeopleCount",
  "origin":1694737678704913648,
  "readings":[{
    "id":"e789d093-0392-4a4e-9890-eee615f647f2",
    "origin":1694737678704913648,
    "deviceName":"retail-device-1",
    "resourceName":"PeopleCount",
    "profileName":"RetailVirtualDevice",
    "valueType":"Int32",
    "value":"48"
  }]
}	
```

## AnyLog Prerequisites

* To send data to AnyLog via REST, configure the REST service. See details in the [REST Server](../../background%20processes.md#rest-requests) section. 
* To Treat AnyLog as a message broker, configure the Message Broker service. See details in the [Message Broker](../../background%20processes.md#message-broker) section. 

These services enable the node to receive the data via REST or published data.

## Creating an Application Service in Edgex
1. Install EdgeX and EdgeXpert Management tools

2. In browser goto EdgeXpert login page
   * **URL**: `https://${YOUR_IP}:9090` 
   * **Username**: `admin` | **Password**: `admin`

![Login Screen](../../imgs/edgex_login.png)

3. On the left-side of the screen, press _App Services_

![Xpert Management Homepage](../../imgs/edgex_homepage.png)

4. On the right-side of the screen add a _Basic Service_

![Basic Service location](../../imgs/edgex_basic_service.png)

From this point, configure the application service(s) based on the way by which to process the data on AnyLog.

## Transferring data from Edgex to AnyLog
Edgex can transfer data into AnyLog using the following calls:
* Using REST PUT - this option receives data from Edgex and stores the data in AnyLog without data transformation.
* Using REST POST - this option receives data from Edgex and stores the data in AnyLog with data transformation.
* Treating AnyLog as a Message Broker - data transformation is supported.

Note that users can configure an AnyLog node to receive data from third-party brokers such as CloudMQTT and Eclipse 
Mosquitto. This option is detailed [here](../../message%20broker.md#subscribing-to-a-third-party-broker).

### Transferring data into AnyLog via PUT

Using PUT, configuration is done only on the EdgeXpert platform:
* The user determines the data transferred to AnyLog on the Edgex platform.
* The database and table assigned to the data are specified in the REST message header. 

#### The following step is done locally, on your machine

Create a JavaScript script that selects the data generated in EdgeXpert to be sent into AnyLog. The provided 
[sample script](https://raw.githubusercontent.com/AnyLog-co/documentation/master/deployments/Support/edgex_transformation.js) 
extracts reading values from EdgeXpert and transfers the readings to an AnyLog node.
```javascript
// file name: edgex_transformation.js
var outputObject = { value: inputObject.readings[0] };
return outputObject;
```

#### The following steps are done on the EdgeXpert GUI interface.

1. [Create Basic Application Service](#creating-an-application-service)

![Basic Service location](../../imgs/edgex_basic_service.png)

2. Update Basic App Service
* **Basic Info** 
  * Name
  * Destination: HTTP

![Basic Information](../../imgs/edgex_put_basic_info.png)

* **Address Info**
  * Method: PUT 
  * URL (operator REST service IP and Port)
  * HTTP Request Headers
    * type: _json_
    * dbms (database to store data in)
    * table (table name)
    * mode: _streaming_
    * Content-Type: _text/plain_

![Address Information](../../imgs/edgex_put_address_info.png)

* **Data Format**
  * JavaScript Transform: edgex_transformation.js 

![Data Format](../../imgs/edgex_put_data_format.png) 

* **Filter**
  * Device Filter

![Filter Value(s)](../../imgs/edgex_put_filter.png)

3. Once the changes are saved (at the bottom of the screen), data should automatically be sent into AnyLog via PUT.

![Save Button](../../imgs/edgex_save.png)


### Publishing Data into AnyLog via POST

Publishing data into AnyLog via REST _POST_ allows the data to be transformed locally within AnyLog. After the data is 
transformed, it is stored on the AnyLog node.   

In the case of POST, the database and table can be determined from the headers or retrieved from the data received.

The transformation is triggered by associating mapping rules to a topic. The POST headers include a topic and 
when the data is recieved in the AnyLog node, the mapping rules assigned to the topic are applied on the data.

This process is identical to the procesess used when data is published on an AnyLog node as a message broker.  
The mapping rules are declared using a client service, and a description is available at the
[run mqtt client](../../message%20broker.md) section. 

#### The following steps are done on the AnyLog (operator) node that's receiving the data

1. Declare the mapping rules associated to a topic. If the database and table assigned to the data are not included in
   the headers, the maaping rules need to include the database and table to use.

2. Enable the mapping rules using the client service (described in run [mqtt client](../../message%20broker.md)).   
   Note: This service is enabled using the command: `run mqtt client` 

The example below declares the mapping rules on the data detailed above.
```anylog 
<run mqtt client where broker=rest and user-agent=anylog and log=false and topic=(
  name=anylogedgex-post and 
  dbms=!company_name.name and 
  table="bring [readings][0][resourceName]" and 
  column.timestamp.timestamp=now and 
  column.value=(type=float and value="bring [readings][0][value]"))>
```

#### The following steps are done on the EdgeXpert GUI interface.

1. [Create Basic Application Service](#creating-an-application-service)

![Basic Service location](../../imgs/edgex_basic_service.png)

2. Update Basic App Service
* **Basic Info** 
  * Name
  * Destination: HTTP
  
![Basic Information](../../imgs/edgex_post_basic_info.png)

* **Address Info**
  * Method: POST 
  * URL (operator REST service IP and Port)
  * HTTP Request Headers
    * command: data 
    * topic: anylogedgex-post
    * User-Agent: AnyLog/1.23
    * Content-Type: text/plain

![Address Information](../../imgs/edgex_post_address_info.png)
  
* **Filter**
  * Device Filter

![Filter Value(s)](../../imgs/edgex_put_filter.png)

3. Once the changes are saved (at the bottom of the screen), data should automatically be sent into AnyLog via POST.

![Save Button](../../imgs/edgex_save.png)

### Publishing Data into AnyLog using the AnyLog Message Broker service

1. Declare the mapping rules associated to a topic. The rules need to include the database name and table name that are 
assigned to the data.

2. Similar to _POST_, when using the _message broker_ service, enable the mapping rules using the client service 
(described in run [mqtt client](../../message%20broker.md)). This service is enabled using the command: 
`run mqtt client` 

The example below declares the mapping rules on the data detailed above.

```anylog
<run mqtt client where broker=local and log=false and topic=(
  name=anylogedgex-mqtt and 
  dbms=!default_dbms and 
  table="bring [readings][0][resourceName]" and 
  column.timestamp.timestamp=now and 
  column.value=(type=float and value="bring [readings][0][value]"))>
```

#### The following steps are done on the EdgeXpert GUI interface.

1. [Create Basic Application Service](#creating-an-application-service)

![Basic Service location](../../imgs/edgex_basic_service.png)

2. Update Basic App Service
* **Basic Info** 
  * Name
  * Destination: MQTT
  
![Basic Information](../../imgs/edgex_mqtt_basic_info.png)

* **Address Info** 
  * URL (operator Message Broker service IP and Port)
  * Topic

![Address Information](../../imgs/edgex_mqtt_address_info.png)
  
* **Filter**
  * Device Filter

![Filter Value(s)](../../imgs/edgex_put_filter.png)

3. Once the changes are saved (at the bottom of the screen), data should automatically be sent into AnyLog via POST.

![Save Button](../../imgs/edgex_save.png)



