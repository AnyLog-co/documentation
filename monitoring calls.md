# Monitoring calls from external applications

## Get REST Calls

The ***get rest calls*** command returns statistics on the REST calls issued and their execution results.

Usage: 
<pre>
get rest calls
</pre>

Example reply:
<pre>
Statistics
Caller Call Processed Errors Last Error              First Call          Last Call           Last Caller
------|----|---------|------|-----------------------|-------------------|-------------------|---------------|
anylog|GET |        3|     1|Error Command Structure|2021-11-24 13:29:01|2021-11-24 13:29:19|10.0.0.78:50183|
      |POST|        4|     0|                       |2021-11-24 13:29:08|2021-11-24 13:29:24|10.0.0.78:50185|
</pre>


