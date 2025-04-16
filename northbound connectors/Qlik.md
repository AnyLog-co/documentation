# Qlik

Qlik is a data integration, analytics, and artificial intelligence platform. Using their <a href="https://help.qlik.com/en-US/connectors/Subsystems/REST_connector_help/Content/Connectors_REST/REST-connector.htm" target="_blank">REST connector plugin</a>, 
users are able to pull data from AnyLog/EdgeLake and use it to generate insight on their data. 

## Requirements 
1. An active AnyLog network 
2. A subscription with QLik 

## Preparing the Environment   
1. From _Home_ goto _Create_
2. In _Create_ we want to use the _Analytics App_
3. Data is coming from _Files & Other Data  Sources_
<img src="imgs/qlik1.png" height=50% width=50% alt="source options" />
4. We use a standard _REST_ 
<img src="imgs/qlik2.png" height=50% width=50% alt="source options" />

For this demo we'll be creating REST connections for\ _blockchain get_, _increments_ and _period_ function respectively.
The main components of the REST interface delt with are the URL bar and cURL request headers. 

| <img src="imgs/qlik3.png" height=50% width=50% /> | <img src="imgs/qlik4.png" height=50% width=50% /> |
|:-------------------------------------------------:|:-------------------------------------------------:|


