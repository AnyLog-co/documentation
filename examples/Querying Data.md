# Adding Data and Queries 

## Queries 

### Executing Queries - General Consideration
   
|     | Consideration   | Explanation   |
| --- | ------------- | ------------- | 
|   1 | Specify time range  | In most cases, operators nodes partitioned data by time - specifying the date range limits processing to the relevant partitions.  |
|   2 | Specify include tables  | The same query will be executed concurrently in the different tables to provide the the best performance. Result set is grouped by the extend values (i.e. table name).|
|   3 | Specify the columns needed  | Less data would be transferred over the network (note also that each table includes management columns which are redundant in most queries processes).|
|   4 | Use the Increment function if possible  | The Increment query executes functions (min, max, avg, count and sum) on the operator nodes - it provides a higher degree of parallelism and much less data transferred over the network .|
|   5 | Configure the query on the AnyLog node | For efficient concurrent processing - see comment below. |  

Configuring the query pool size is as follows:
<pre>
set query pool [n]
</pre>
[n] is the number of threads in the pool and is determined as follows:  
For each query, all participating partitions can be processed concurrently, each with a dedicated thread - assuming the treads pool is able to provide the needed threads (otherwise processes would be serialized).  
For example, if data is partitioned by day and 2 days are considered, the process can leverage 2 threads per table.  
If the profile of the representative queries is to consider 4 tables and 2 days for each, a pool of 8 threads would be efficient.  
If the node satisfies multiple concurrent queries, then the pool size should increase accordingly.  
Note that the CPU availability on the specific hardware sets a cap on the availability of threads and only testing can determine the optimal pool size.

### Queries Examples

#### Example 1 - Get summary from multiple tables over the last 3 days

**Command**: Tags Summary 
<pre>
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include=(fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11 where timestamp > NOW() - 3 days AND timestamp < NOW()"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
</pre>

**Sample Outout**: 
<pre>

table     min_ts                     max_ts                     min_value          avg_value          max_value        row_count 
--------- -------------------------- -------------------------- ------------------ ------------------ ---------------- --------- 
err       2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653                0.0                0.0              0.0    107822 
fic13     2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653   80.6143484115391  96.53215326296014 105.279845629465    107805 
fic12     2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653   46.5446253812245 60.394872749909005 99.5267719113708    107823 
lic1      2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653 0.0580851549752362  50.91715512561892 64.2873305621064    107818 
fic11     2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653   61.3789165600246  74.23786651358891 109.453146002271    215686 
ai_mv     2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653                0.0 38.001171585858664 98.1128334999084    107832 
valve_pos 2021-06-17 21:36:29.710816 2021-06-24 18:29:47.755653                0.0  30.53904173433069            100.0    107801 
lic1_sp   2021-06-17 21:35:28.345601 2021-06-24 18:29:47.755653               50.0  50.94744400110993 51.2325785564247    107812 
{"Statistics":[{"Count": 8,"Time": 00:00:02}]}
</pre>


#### Example 2 - The Period query

The ***period*** query gets a starting date and time. From that time it would find the nearest occurrence of data earlier
to the provided time and process the requested functions on a time interval that ends at the nearest occurrence.

**Command**: 
<pre>
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include=(fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select max(timestamp) as max_timestamp, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11 where period(day, 1, now(), timestamp);"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
</pre>
**Sample Output**: 
<pre>

table     max_timestamp              min_value          avg_value          max_value        row_count 
--------- -------------------------- ------------------ ------------------ ---------------- --------- 
err       2021-06-24 20:41:18.063693                0.0                0.0              0.0     17408 
fic13     2021-06-24 20:41:18.063693   94.9898387262977 100.02135415632446 105.181488739002     17407 
fic12     2021-06-24 20:41:18.063693    46.676844469727  50.01477294499575 53.6952177610664     17409 
lic1      2021-06-24 20:41:18.063693 0.0580851549752362 51.100734423295094 64.2873305621064     17418 
fic11     2021-06-24 20:41:18.063693   61.5013386574535  65.01510800743591 68.8252900598139     34842 
ai_mv     2021-06-24 20:41:18.063693                0.0  40.04704018814899 95.6107079982758     17417 
valve_pos 2021-06-24 20:41:18.063693                0.0 33.239299279330346            100.0     17408 
lic1_sp   2021-06-24 20:41:18.063693   51.2325785564247 51.232578556424706 51.2325785564247     17408 
{"Statistics":[{"Count": 8,"Time": 00:00:01}]}
</pre>


#### Example 3 - The Increment query
The increment query considers a time interval. The time interval is partitioned to segments. The functions requested are 
processed on each segment and the data transferred over the network only includes the values calculated for each function per each segment.

For example, one day of data includes a value every second. Transferring a day of the source data includes 60 X 60 X 24 =  86,400 data instances.  
If the query partitions the data to minutes and calculates the needed functions on each minute (i.e. min(val), max(val)), only 1/60 data instances are transferred.  
* With this type of query - rather than returning the source data, the time interval considered is sliced into segments and the query returns a smaller set of values representing functions calculated for each segment.
* This type of query can provide significant performance advantage with large data sets and in particular with queries that consider large data sets hosted in multiple operator nodes. 

**Command**:
<pre>
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include = (fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend = (@table_name as table) and format=table "select increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11 limit 10"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
</pre>
**Sample Output**: 
<pre>

table     min_ts                     max_ts                     min_value        avg_value          max_value        row_count 
--------- -------------------------- -------------------------- ---------------- ------------------ ---------------- --------- 
fic11     2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479  101.21904438785    104.98534195167 109.274003264401       300 
valve_pos 2021-06-17 21:36:29.710816 2021-06-17 21:43:02.706479  22.320718161593  22.33864373954124 22.3581088089281       129 
ai_mv     2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479 29.9923539161682 30.369866788387267 30.7534277439117       150 
fic13     2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479 81.0654558159646  84.98458076582867 89.3334206350424       150 
fic12     2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479 91.1074474574371  94.98462551607133 99.3263548031351       150 
err       2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479              0.0                0.0              0.0       150 
lic1_sp   2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479             50.0               50.0             50.0       150 
lic1      2021-06-17 21:35:28.345601 2021-06-17 21:43:02.706479 49.9895726612152 50.000172898089936 50.0111872873829       150 
ai_mv     2021-06-18 02:46:10.643434 2021-06-18 23:59:57.882238 29.9952775239944  32.47524779401523 56.1007857322693     31388 
fic13     2021-06-18 02:46:10.643434 2021-06-18 23:59:57.882238 80.6143484115391  88.15540538945622 105.059081405841     31373 
{"Statistics":[{"Count": 10,"Time": 00:00:04}]}
</pre>


#### Example 4 - Source Data


**Command**: 
<pre>
# Bash cURL format 
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include=(fic12,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select timestamp, value from fic11 where timestamp > NOW() - 1 day order by timestamp asc;"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"

# Python3 format 
import requests 
conn = '13.67.180.124:2149'
r = requests.get('http://%s' % conn, headers={
    'command': 'sql aiops include=(valve_pos, fic11, fic12, ai_mv, err, lic1, fic13, sic1003_mv, sic1002_pv, pdic1000_pv, sic1003_sv, tic1001a_mv, sic1001_pv, pdic1000_sv, sic1001_mv, pdic1000_mv, sic1002_mv, sic1003_pv, sic1002_sv, tic1001a_pv, tic10
01a_sv, sic1001_sv, pdic1000_aimv, tic1001b_mv, tic1001d_mv, tic1001c_mv, tic1002b_mv, tic1002a_mv, tic1003a_mv, tic1003b_mv, tic1003d_mv, tic1002c_mv, tic1002d_mv, tic1003c_mv) and extend=(@table_name as table) and format=table "SELECT timestamp, val
ue FROM lic1_sp WHERE timestamp > NOW() - 1 day order by timestampi asc"', 
    'destination': 'network', 
    'User-Agent': 'AnyLog/1.23'
}) 
try: 
    output = r.json()
except Exception as e:
    output = r.text
print(output)  

</pre>
**Sample Output**: 
<pre>

table     timestamp                  value             
--------- -------------------------- ----------------- 
lic1      2021-07-07 00:27:15.898272  43.4801443571863 
ai_mv     2021-07-07 00:27:15.898272               0.0 
fic13     2021-07-07 00:27:15.898272  30.0381783080729 
err       2021-07-07 00:27:15.898272               0.0 
valve_pos 2021-07-07 00:27:15.898272  56.4906663401367 
lic1_sp   2021-07-07 00:27:15.898272 43.48649047431325 
fic12     2021-07-07 00:27:15.898272  51.0311249999719 
fic11     2021-07-07 00:27:15.898272  36.0335187495409 
fic12     2021-07-07 00:27:17.713731  48.8032271058607 
lic1      2021-07-07 00:27:17.713731  43.4827153219738 
fic13     2021-07-07 00:27:17.713731  27.8497703750513 
lic1_sp   2021-07-07 00:27:17.713731 43.48649047431325 
ai_mv     2021-07-07 00:27:17.713731               0.0 
fic11     2021-07-07 00:27:17.713731  33.8344706401114 
valve_pos 2021-07-07 00:27:17.713731  56.4909473172322 
err       2021-07-07 00:27:17.713731               0.0 
err       2021-07-07 00:27:19.520875               0.0 
fic13     2021-07-07 00:27:19.520875  30.0022483511345 
ai_mv     2021-07-07 00:27:19.520875               0.0 
valve_pos 2021-07-07 00:27:19.520875  56.4936246116901 
lic1      2021-07-07 00:27:19.520875  43.4794950306474 
fic12     2021-07-07 00:27:19.520875  51.0064269297124 
fic11     2021-07-07 00:27:19.520875  35.9976516493904 
lic1_sp   2021-07-07 00:27:19.520875 43.48649047431325 
ai_mv     2021-07-07 00:27:21.378099               0.0 
...
{"Statistics":[{"Count": 1415,"Time": 00:00:00}]}
</pre>


#### Example 5 - Python3 script to execute query
<pre>
import requests

# REST connection information (IP + Port) 
conn = '192.168.50.159:2051' 

# Header for POST data 
query = 'sql aiops include=(fic12,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and stat=false "select timestamp, value from fic11 where date(timestamp) = \'2021-06-30\';"'
headers = {
    'command': query,
    'destination': 'network', 
    'User-Agent': 'AnyLog/1.23',
    'Content-Type': 'text/plain'
}

# Query data 
try:
    r = requests.get('http://%s' % conn, headers=headers)
except Exception as e: 
    print('Failed to GET data to %s (Error: %s)' % (conn, e))
else: 
    if r.status_code != 200: 
        print('Failed to POST data to %s due to network error: %s' % (conn, r.status_code))
    else:
        print(r.json()) 
</pre> 
