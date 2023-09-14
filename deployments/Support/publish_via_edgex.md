# Publishing Data via Edge Xpert Manager

EdgeX (Foundry) is an Open-Source framework that serves as a foundation for building and deploying Internet of Things (IoT)
edge computing solutions. While Edge Xpert is an enterprise version of _EdgeX_, provided by IoTech System. 

This document will show how to publish data into Anylog via Edge Xpert Management tool.   

* [EdgeX Foundry](https://www.edgexfoundry.org/)
* [IoTech System](https://www.iotechsys.com/)
* [User Guide](https://docs.iotechsys.com/)


### Creating an Application Service
1. Make sure to install EdgeX and Edge Xpert Management tools

2. In browser goto EdgeXpert login page
   * **URL**: `https://${YOUR_IP}:9090` 
   * **Username**: `admin` | **Password**: `admin`

![Edge Xpert Login](../../imgs/edgex_login.png)

3. On the left-side of the screen, press _App Services_

![Edge Xpert Homepage](../../imgs/edgex_homepage.png)

4. On the right-side of the screen add a _Basic Service_ 

![EdgeX Add Service](../../imgs/edgex_appservice.png)

From this point, configure the service based on the way by which to process the data on AnyLog. 

## Publishing via PUT 

Sending data into AnyLog via _PUT_ is probably the easiest as there are no requirements on the AnyLog side. However,
unlike _POST_ and _MQTT_, the data wil not be analyzed but rather processed and stored as is. Additionally, the 

1. As shown above, [Create Basic Application Service](#creating-an-application-service)

![Default Application Service screen](../../imgs/edgex_appservice_default.png)

2. Update Basic App Service
   * **Basic Info** 
     * Name
     * Destination: HTTP
   * **Address Info**
     * Method: PUT 
     * URL
     * HTTP Request Headers
       * type: _json_
       * dbms
       * table
       * mode: _streaming_
       * Content-Type: _text/plain_ 
     * **Filter**
       * Device Filter

| Basic Info | Address Info |        Filter         |
| :---: | :---: |:---------------------:| 
| ![]() | ![]() | ![Filter](../../img/edgex_appservice_filter.png) | 

