---
layout: default
parent: Northbound
title: Using Postman
nav_order: 7
---
# Using Postman against EdgeLake Network
 
Postman is an API platform that can serve as a tool to issue EdgeLake Commands to nodes in the 
EdgeLake Network and as a tool to issue queries to data in the network.

Commands and queries through Postman can be issues with SSL enabled or disabled.  

Download Postman here: https://www.postman.com/downloads/.  

### Without SSL
To run EdgeLake queries using _Postman_ without SSL enabled, follow the following steps:
<ol start="1">
    <li>Open Postman</li>
    <li>Create a collection</li>
    <li>Add a request</li>
    <li>Enter the request URL and port number (the URL can also be an IP address)</li>
    <li>Add 2 header keys: "User-Agent" and "command" with values "AnyLog/1.23" and "[query command]", respectively:
        <div class="image-frame"><img src="https://user-images.githubusercontent.com/16313057/132929390-0f89b6c7-b88c-4665-a963-2da17645df20.png" /></div>
    </li>
    <li>Press send, and wait for a response</li>
</ol>


### With SSL

For SSL, the explanation on generating the needed files is available at the [Using SSL Certificates](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#using-ssl-certificates) section.

To run EdgeLake queries using Postman with SSL enabled, follow the following steps:
<ol start="1">
    <li>Open Postman</li>
    <li>Create a collection</li>
    <li>Add a request</li>
    <li>Enter the request URL and port number with "https://" prepended (the URL can also be an IP address)
        <div class="image-frame"><img src="https://user-images.githubusercontent.com/16313057/132929414-7b75bc13-4d51-4a48-b189-6a8a75e41c8f.png" /></div>
    </li>
    <li>Add 2 header keys:
        <pre class="code-frame"><code class="language-json">{
    "command": "[Query Command]",
    "User-Agent": "AnyLog/1.23"
}</code></pre></li>
    <li>In "Settings" turn off the toggle for "Enable SSL certificate verification"
        <div class="image-frame"><img src="https://user-images.githubusercontent.com/16313057/132929419-282c6933-9c08-40a9-ae16-ef77224ff2fe.png" /></div>    
    </li>
    <li>In "Default Settings" add the certificate (public key) of the certificate authority</li>
    <li>Add your certificate and private key pair given by the certificate authority
        <div class="image-frame"><img src="https://user-images.githubusercontent.com/16313057/132929434-baa81c83-2ba8-467d-8b2d-a0db12bf6544.png" /></div>
    </li>
</ol>
