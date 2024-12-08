# HTTP Commands

AnyLog HTTP commands are used to interact with the AnyLog platform via HTTP requests, enabling users to query data, 
execute SQL commands, and customize the format of the response. 
These commands can specify the output format (such as HTML, PDF, or JSON), include additional styling or headers, 
and define the type of query or task to be performed. Through these HTTP commands, 
users can efficiently retrieve and manipulate data from the AnyLog system, 
making it flexible for various applications in data management and analytics.

## Prerequisites
Enabled REST service. The HTTP Commands are issued via the REST interface, which is required to be enabled. 
Details on the AnyLog REST service are available [here](anylog%20commands.md#rest-command).

## Usage

```anylog
http://[ip]:[port]/?User-Agent=[version]?into=[output format]?pdf=[true/false]?html=[html instructions]?destination=[network]?command=[AnyLog Command]"
```

## Explanation
The question mark separates between the different values delivered to the node. The options are detailed below:

* http://[ip]:[port]
  * [ip]: The IP address of the AnyLog instance (e.g., 10.0.0.78).
  * [port]: The port on which the REST service is running (e.g., 7849).
* User-Agent=[version]
  * Identifies the client or version of AnyLog issuing the request (e.g., AnyLog/1.23).
* into=[output format]
  * Specifies the desired output format, such as html, json, or text.
* pdf=[true/false]
  * Determines whether the output should be converted into a PDF document.
  * true: Converts the output to a PDF.
  * false (or omitted): No PDF generation.
* html=[html instructions]
  * Defines HTML formatting instructions for the response.
  * Allows customization of headers, styles, or body content.
* destination=[network]
  * Specifies the network or recipient of the command's response.
  * If not provided, the port addressed by the http request is the destination node.
* command=[AnyLog Command]
  * The AnyLog command to execute.
  * For example, a SQL query like: ```command=sql lsl_demo format=table "select timestamp, value from ping_sensor"```

## Example
```anglog
http://10.0.0.78:7849/?User-Agent=AnyLog/1.23?into=html?pdf=true?html={ ^head^ : { ^include^ : [^<title>AnyLog</title>^] } }?destination=network?command=sql lsl_demo format=table "select timestamp, value from ping_sensor"
```

## Using the Remote CLI to construct http requests

Using the "Code" option on the Remote CLI, CLI commands are transformed to HTTP requests.

### Example:
1. Place a command on the Remote CLI. Example: ```sql lsl_demo format = table "select timestamp, value from ping_sensor "```
2. Flag the Network box.
3. Select the "Code" option
4. Copy the following JSON to the "Input Data/JSON" box:
  ```
{ "head" : {
            "include" : ["<title>AnyLog</title>"],
            "style" : {
                    ".center-title" : {
                        "display" : "flex;",
                        "flex-direction" : "column;",
                        "align-items" : "center;",
                        "justify-content" : "center;",
                        "height" : "100vh;",
                        "margin" : "0;",
                        "color" : "blue;",
                        "font-size" : "2em;",
                        "text-align" : "center;"
                        }
                    }
            },
  "body" : {
		"include" : ["<div class='center-title'", "<h1>AnyLog</h1>", "</div>"]

	}
}
```
5. From the dropdown menu select "Text"

The HTTP command reflects the query and the output format. This command can be placed on a browser to issue the query and output the result in HTML.

