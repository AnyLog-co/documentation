# Onboarding

This document contains the example commands demonstrated in the Onboarding Presentation.
These are basic commands which are frequently used on the AnyLog CLI.

## Using Help

<pre>
help
help index
help index streaming
help run kafka consumer
</pre>

## Event Log and Error Log
<pre>
get event log
help get error log
get error log
</pre>


## The Local Dictionary
<pre>
get dictionary
abc = 123
!abc

!blockchain_file

get env var
$HOME
</pre>

## The Local Setup
<pre>
get dictionary        # Keys prefixed with _dir represent directories
get dictionary _dir   # New feature - only supported on the latest release
</pre>

## Connect to the network
<pre>
get connections
run tcp server where internal_ip = !ip and internal_port = 20048 and external_ip = !external_ip and external_port = 20048 and bind = false and threads = 6
run rest server where internal_ip = !ip and internal_port = 20049 and external_ip = !external_ip and external_port = 20049 and bind = false
get connections
</pre>

## Disable Authentication, Enable Message Queue
<pre>
set authentication off
set echo queue on

echo this is a test message
get echo queue
</pre>

## Connect to a DBMS
<pre>
connect dbms system_query where type = sqlite and memory = true # Used for local processing

get databases     # 2 system databases - system_query and almgm
</pre>

## Get and query the metadata (copy the metadata from a peer node)
<pre>
run client 23.239.12.151:32348 file get !!blockchain_file !blockchain_file
blockchain reload metadata

blockchain get *
blockchain get operator

blockchain get operator bring.table [operator][name] [operator][city] [operator][ip]  [operator][port] 
blockchain get operator where [city] = toronto  bring.table [operator][name] [operator][city] [operator][ip]  [operator][port] 

blockchain get operator where [city] = toronto  bring [operator][ip] : [operator][port] separator = ,

blockchain get operator where [city] = toronto  bring.ip_port
</pre>

## Monitoring
<pre>
run client (blockchain get operator where [city] = toronto  bring.ip_port) get status

run client (blockchain get operator where [city] = toronto  bring.ip_port) get disk usage .

destination = blockchain get operator where [city] = toronto  bring.ip_port

!destination
run client (!destination) get status
run client (!destination) get disk usage .
run client (!destination) get memory info

run client (!destination) get processes

run client (!destination) get databases
</pre>
 
## Data Setup Status
<pre>
get virtual tables
get tables where dbms = litsanleandro
get columns where table = ping_sensor and dbms = litsanleandro

get data nodes
</pre>


## Data Query
<pre>
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"

query status

run client () sql edgex format=table "select increments(minute, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value,  count(*) as row_count from rand_data where timestamp >= NOW() - 1 hour;"

run client () sql edgex format=table "select timestamp, value FROM rand_data WHERE period(minute, 5, NOW(), timestamp) ORDER BY times
</pre>
