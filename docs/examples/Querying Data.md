# Querying Data

This document provides examples of queries to retrieve data from the AnyLog Network.  
An explanation of the query syntax is detailed in the [Query nodes in the network](../queries.md) page. 

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
curl -X GET 20.97.12.66:2049 -H 'command: sql aiops include=(pdic1000_sv, pdic1000_mv, pdic1000_aimvsic1001_pv, sic1001_sv, sic1001_mv, sic1002_pv, sic1002_sv, sic1002_mv, sic1003_pv, sic1003_sv, sic1003_mv, tic1001a_pv, tic1001a_sv, tic1001a_mv, tic1001b_pv, tic1001b_sv, tic1001b_mv, tic1001c_pv, tic1001c_sv, tic1001c_mv, tic1001d_pv, tic1001d_sv, tic1001d_mv, tic1002a_pv, tic1002a_sv, tic1002a_mv, tic1002b_pv, tic1002b_sv, tic1002b_mv, tic1002c_pv, tic1002c_sv, tic1002c_mv, tic1002d_pv, tic1002d_sv, tic1002d_mv, tic1003a_pv, tic1003a_sv, tic1003a_mv, tic1003b_pv, tic1003b_sv, tic1003b_mv, tic1003c_pv, tic1003c_sv, tic1003c_mv, tic1003d_pv, tic1003d_sv, tic1003d_mv) and extend=(@table_name as table) and format=table "SELECT timestamp, value FROM pdic1000_pv WHERE timestamp > NOW() - 1 minute;"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"

</pre>
**Sample Output**: 
<pre>
table       timestamp                  value              
----------- -------------------------- ------------------ 
tic1001d_pv 2021-07-08 18:19:04.979354   88.2449085515011 
tic1002b_sv 2021-07-08 18:19:04.979354               65.0 
tic1001c_mv 2021-07-08 18:19:04.979354   37.6733999072454 
tic1003b_sv 2021-07-08 18:19:04.979354               77.0 
tic1001c_sv 2021-07-08 18:19:04.979354               88.0 
tic1003c_pv 2021-07-08 18:19:04.979354   77.2422568991932 
sic1001_mv  2021-07-08 18:19:04.979354   64.9716613827291 
pdic1000_sv 2021-07-08 18:19:04.979354 1.7000000000000002 
tic1002b_mv 2021-07-08 18:19:04.979354 14.850591794255505 
tic1001c_pv 2021-07-08 18:19:04.979354   88.2472641929698 
tic1003c_mv 2021-07-08 18:19:04.979354 26.886259691403556 
tic1001b_mv 2021-07-08 18:19:04.979354   38.3979534411363 
pdic1000_pv 2021-07-08 18:19:04.979354 1.6694853540171364 
tic1002d_mv 2021-07-08 18:19:04.979354  14.67298242489326 
tic1002b_pv 2021-07-08 18:19:04.979354   65.2412332296145 
tic1003d_mv 2021-07-08 18:19:04.979354 27.321843807872185 
tic1003c_sv 2021-07-08 18:19:04.979354               77.0 
sic1001_sv  2021-07-08 18:19:04.979354 1112.6295349885281 
tic1002a_mv 2021-07-08 18:19:04.979354 15.239008949995238 
tic1002c_sv 2021-07-08 18:19:04.979354               65.0 
tic1002a_sv 2021-07-08 18:19:04.979354               65.0 
tic1003a_pv 2021-07-08 18:19:04.979354   77.2438187767012 
tic1001b_sv 2021-07-08 18:19:04.979354               88.0 
tic1002a_pv 2021-07-08 18:19:04.979354   65.2423583125674 
tic1001b_pv 2021-07-08 18:19:04.979354   88.2485414195323 
...

{"Statistics":[{"Count": 1030,"Time": 00:00:11}]}
</pre>


#### Example #5 - last value generated for each included table

**Command**: 
<pre>
# AnyLog CLI format 
run client () sql aiops include=(lic1_pv,lic1_sv,lic1_mv,fic11_pv,fic12_pv) and extend=(@table_name as table) and format = table "SELECT table_name, timestamp, value FROM fic13_pv WHERE timestamp > timestamp(now, '- 1 day') order by timestamp desc limit 1 per table;"
</pre>
**Sample Output**: 
<pre>
table    timestamp                  value
-------- -------------------------- ----------------
lic1_pv  2021-09-22 19:50:22.247229 50.0120689683407
lic1_mv  2021-09-22 19:50:22.247229 65.3239553149617
fic13_pv 2021-09-22 19:50:22.247229 104.169663032697
fic11_pv 2021-09-22 19:50:22.247229 24.3174650020081
fic12_pv 2021-09-22 19:50:22.247229 74.2116546634527
lic1_sv  2021-09-22 19:50:22.247229             50.0


{"Statistics":[{"Count": 6,
                 "Time": 00:00:00}]}
</pre>


#### Python3 Example for Query #4 
<pre> 
import requests 
conn = '20.97.12.66:2049'
headers = {
    'command': 'sql aiops include=(pdic1000_sv, pdic1000_mv, pdic1000_aimvsic1001_pv, sic1001_sv, sic1001_mv, sic1002_pv, sic1002_sv, sic1002_mv, sic1003_pv, sic1003_sv, sic1003_mv, tic1001a_pv, tic1001a_sv, tic1001a_mv, tic1001b_pv, tic1001b_sv, tic1001b_mv, tic1001c_pv, tic1001c_sv, tic1001c_mv, tic1001d_pv, tic1001d_sv, tic1001d_mv, tic1002a_pv, tic1002a_sv, tic1002a_mv, tic1002b_pv, tic1002b_sv, tic1002b_mv, tic1002c_pv, tic1002c_sv, tic1002c_mv, tic1002d_pv, tic1002d_sv, tic1002d_mv, tic1003a_pv, tic1003a_sv, tic1003a_mv, tic1003b_pv, tic1003b_sv, tic1003b_mv, tic1003c_pv, tic1003c_sv, tic1003c_mv, tic1003d_pv, tic1003d_sv, tic1003d_mv) and extend=(@table_name as table) and format=table "SELECT timestamp, value FROM pdic1000_pv WHERE timestamp > NOW() - 1 minute;"',
    'destination': 'network',
    'User-Agent': 'AnyLog/1.23'
} 

try: 
    r = requests.get('http://%s' % conn, headers=headers)
except Exception as e: 
    print('Failted to execute GET against %s (Error: %s)' % (conn, e))
    output = None 
else: 
    if r.status_code != 200: 
        print('Failed to execute GET against %s due to network error: %s' % (conn, r.status_code))
        output = None 
    else: 
        try: 
            output = r.json() 
        except: 
            output = r.text 
print(output) 
</pre>  

#### Example 5 - Python3 example for extracting data for a specific date
<pre>
import requests
conn = '20.97.12.66:2049'
timestamp = "'2021-06-30'"
headers = {
    'command':  'sql aiops include=(fic12,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select timestamp, value from fic11 where date(timestamp) = %s;"' % timestamp,
    'destination': 'network',
    'User-Agent': 'AnyLog/1.23'
}

try:
    r = requests.get('http://%s' % conn, headers=headers)
except Exception as e:
    print('Failted to execute GET against %s (Error: %s)' % (conn, e))
    output = None
else:
    if r.status_code != 200:
        print('Failed to execute GET against %s due to network error: %s' % (conn, r.status_code))
        output = None
    else:
        try:
            output = r.json()
        except:
            output = r.text
print(output)
</pre> 

**Sample Output**: 
<pre>
table     timestamp                  value            
--------- -------------------------- ---------------- 
lic1      2021-06-30 00:00:01.187161 51.2417970185479 
fic13     2021-06-30 00:00:01.187161 97.5027218603217 
valve_pos 2021-06-30 00:00:01.187161 32.8683365000774 
lic1_sp   2021-06-30 00:00:01.187161 51.2325785564247 
err       2021-06-30 00:00:01.187161              0.0 
fic12     2021-06-30 00:00:01.187161 48.4847256919909 
fic11     2021-06-30 00:00:01.187161 63.4247859436764 
ai_mv     2021-06-30 00:00:01.187161  40.369501709938 
fic11     2021-06-30 00:00:04.102653 62.3517240299968 
lic1      2021-06-30 00:00:04.102653 51.2396323321372 
fic13     2021-06-30 00:00:04.102653 95.8887756808981 
valve_pos 2021-06-30 00:00:04.102653 32.8672429316431 
ai_mv     2021-06-30 00:00:04.102653 40.3275907039642 
fic12     2021-06-30 00:00:04.102653 47.4013203318753 
err       2021-06-30 00:00:04.102653              0.0 
lic1_sp   2021-06-30 00:00:04.102653 51.2325785564247 
valve_pos 2021-06-30 00:00:05.576321 32.8682091413195 
err       2021-06-30 00:00:05.576321              0.0 
lic1      2021-06-30 00:00:05.576321 51.2342293232265 
fic11     2021-06-30 00:00:05.576321 65.9449471311061 
fic12     2021-06-30 00:00:05.576321 50.8891526566533 
fic13     2021-06-30 00:00:05.576321 102.405896621961 
lic1_sp   2021-06-30 00:00:05.576321 51.2325785564247 
ai_mv     2021-06-30 00:00:05.576321 40.1976078748703 
err       2021-06-30 00:00:07.530079              0.0 
{"Statistics":[{"Count": 1056,"Time": 00:00:02}]}
</pre> 
