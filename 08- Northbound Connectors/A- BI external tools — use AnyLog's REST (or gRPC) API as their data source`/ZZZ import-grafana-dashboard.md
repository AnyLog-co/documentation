---
title: Grafana Dashboards 
description: Demonstration on how to connect to AnyLog and gather data for analysis on Google Drive applicaitons
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Instructions to create and manage your Grafana instance with AnyLog, can be found in <a href="{{ '/docs/Querying-Data-Northbound/using%20grafana/' | relative_url }}">Using Grafana</a> 


The following document provides 3 sample Grafana dashboards
* <a href="{{ '/docs/Querying-Data-Northbound/grafana.json/' | relative_url }}">Network Map</a> - The dashboard consists of a map showing all the nodes 
in the network, a list of operator nodes and a list of  tables supported in the network.

!<a href="{{ '/docs/Querying-Data-Northbound/..%2Fimgs%2Fgrafana_network_map.png/' | relative_url }}">grafana_network_map.png</a>

  
* <a href="{{ '/docs/Querying-Data-Northbound/examples/' | relative_url }}">EdgeX Diagram</a> - The dashboard consists of a line graph demonstrating min/avg/max, as well gages showing 
the overall number of rows as well as the number of rows per node. The content for these widgets is via our third-party
MQTT client sample connection.  

!<a href="{{ '/docs/Querying-Data-Northbound/..%2Fimgs%2Fgrafana_edgex_dashboard.png/' | relative_url }}">grafana_edgex_dashboard.png</a>

## Setting Up Grafana

* An [installation of Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) - We support _Grafana_ version 7.5 and higher, we recommend using _Grafana_ version 9.5.16 or higher. 
```shell
docker run --name=grafana \
  -e GRAFANA_ADMIN_USER=admin \
  -e GRAFANA_ADMIN_PASSWORD=admin \
  -e GF_AUTH_DISABLE_LOGIN_FORM=false \
  -e GF_AUTH_ANONYMOUS_ENABLED=true \
  -e GF_SECURITY_ALLOW_EMBEDDING=true \
  -e GF_INSTALL_PLUGINS=simpod-json-datasource,grafana-worldmap-panel \
  -e GF_SERVER_HTTP_PORT=3000 \
  -v grafana-data:/var/lib/grafana \
  -v grafana-log:/var/log/grafana \
  -v grafana-config:/etc/grafana \
  -it -d -p 3000:3000 --rm grafana/grafana:9.5.16
```

Log into Grafana and Declare a _(JSON) Data Source_

1. [Login to Grafana](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) - The default Grafana HTTP port is 3000  
   * URL: http://localhost:3000/ 
   * username: admin | password: admin

<img src="../../assets/img/grafana_login.png" alt="Grafana page" width="50%" height="50%" />

2. In _Data Sources_ section, create a new JSON data source
   * select a JSON data source.
   * On the name tab provide a unique name to the connection.
   * On the URL tab add the REST address offered by the AnyLog node (i.e. http://10.0.0.25:2049)
   * On the ***Custom HTTP Headers***, name the default database. If no header is set, then all AnyLog hosted databases will be available to a query process.


|<img src="../../assets/img/grafana_datasource_connector.png" alt="Data Source Option" /> | <img src="../../assets/img/grafana_datasource_configuration.png" alt="Data Source Config" /> | 
| :---: | :---: |


## Uploading Dashboard

1. In a new Dashboard goto the _Settings_  
<img src="../../assets/img/grafana_base_dashboard.png" alt="Empty Dashboard" />


2. Go _JSON Model_ and add desired model - A model is the JSON object being used to generate the grafana dashboard (for example: <a href="{{ '/docs/examples/grafana_json/edgex_dashboard.json/' | relative_url }}">EdgeX Dashboard</a>).

| <img src="../../assets/img/grafana_json_model_empty.png" alt="Empty JSON Model" width="75%" height="75%" /> | <img src="../../assets/img/grafana_json_model.png" alt="JSON Model" width="75%" height="75%"/> |
|:--------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------:|

3. Save Changes


4. Once the changes are saved, you should see a new Dashboard 

| Before |                                After                                |
| :---: |:-------------------------------------------------------------------:|
| <img src="../../assets/img/grafana_no_dashboard.png" alt="No Dashboards" /> | <img src="../../assets/img/grafana_new_dashboard.png" alt="New Dashboard" /> | 

5. For each of the widgets update the following information:
   * Data Source 
   * Metric value (AnyLog table name)

Once these changes are saved, the outcome should look something like this:

|          View when accessing Dashboard          |                             Update Data Source                              | Update Metric Value | Outcome | 
|:-----------------------------------------------:|:---------------------------------------------------------------------------:| :---: | :---:  |
| !<a href="{{ '/docs/assets/img/grafana_edit_button.png/' | relative_url }}">Edit Widget</a> | !<a href="{{ '/docs/Querying-Data-Northbound/..%2Fimgs%2Fgrafana_update_datasource.png/' | relative_url }}">grafana_update_datasource.png</a> | !<a href="{{ '/docs/Querying-Data-Northbound/..%2Fimgs%2Fgrafana_update_table.png/' | relative_url }}">grafana_update_table.png</a> | !<a href="{{ '/docs/Querying-Data-Northbound/..%2Fimgs%2Fgrafana_outcome.png/' | relative_url }}">grafana_outcome.png</a> |   
