# Operator Process Simplified 

AnyLog's _Operator_ node(s) is responsible for storing the actual data that's ultimately queried. As such, it is 
responsible for providing the following information to the blockchain: 

* cluster it's a member of (if it doesn't exist)
* information about itself, policy of type `operator`
* policy of type `table` with the `CREATE TABLE` statement associated with the table
* policy of type `cluster` which is associated to a "parent" `cluster`, and contains information regarding the table - 
database and table name respectively. 

**Note**: This process is done automatically by AnyLog! We're providing the steps as a way to better understand how AnyLog,
and in particular an _Operator_ node, works. 

### Requirements 
In order to execute the step-by-step process, the directions assume that the code is run against an AnyLog _operator_
instance, that has `test`as its logical database. Additionally, for simplicity reasons, the script will not wortk properly if 
_partitions_ are declared against `test.trig_readings`. 
 
 
## Storing Data
The following demonstration downloading a JSON file. with 1 million rows. This data is then used to generate the `CREATE TABLE`
statement, as well as both the `table` and (new) `cluster` policies. Once those two are declared, and the table gets created, 
we'll generate the SQL file and store the data locally.   

The following steps can be executed as a single script: 
```anylog 
process !local_scripts/sample_code/data_to_db_process.al
```

1. Download [JSON Data](http://172.105.236.94/test.trig_data.1673093527.json) 
**Sample JSON**: 
```json
{
   "value": 1,
   "sin": 0.8414709848078965, 
   "cos": 0.5403023058681398, 
   "tan": 1.5574077246549023,
   "timestamp": "2023-01-14T05:10:07.143048Z"
 }
```
```anylog
[file=!prep_dir/test.trig_readings.0.0.json, key=results, show= true] = rest get where url = http://172.105.236.94/test.trig_data.1673093527.json
```

2. View data (this step is not done in the automated process)
```anylog
AL anylog-node > system cat !prep_dir/test.trig_readings.0.0.json | head -1
{"value": -3.141592653589793, "sin": -1.2246467991473532e-16, "cos": -1.0, "tan": 1.2246467991473532e-16, "timestamp": "2023-01-07T12:12:07.142635Z"}
{"value": -1.5707963267948966, "sin": -1.0, "cos": 6.123233995736766e-17, "tan": -1.633123935319537e+16, "timestamp": "2023-01-15T18:12:07.142703Z"}
{"value": -1.0471975511965976, "sin": -0.8660254037844386, "cos": 0.5000000000000001, "tan": -1.7320508075688767, "timestamp": "2022-12-26T16:15:07.142739Z"}
{"value": -1, "sin": -0.8414709848078965, "cos": 0.5403023058681398, "tan": -1.5574077246549023, "timestamp": "2023-01-03T03:07:07.142764Z"}
{"value": -0.7853981633974483, "sin": -0.7071067811865475, "cos": 0.7071067811865476, "tan": -0.9999999999999999, "timestamp": "2022-12-06T20:44:07.142790Z"}
{"value": -0.5235987755982988, "sin": -0.49999999999999994, "cos": 0.8660254037844387, "tan": -0.5773502691896257, "timestamp": "2023-01-02T13:49:07.142809Z"}
{"value": -0.39269908169872414, "sin": -0.3826834323650898, "cos": 0.9238795325112867, "tan": -0.41421356237309503, "timestamp": "2023-01-24T10:00:07.142829Z"}
{"value": 0, "sin": 0.0, "cos": 1.0, "tan": 0.0, "timestamp": "2022-12-01T09:55:07.142847Z"}
{"value": 0.39269908169872414, "sin": 0.3826834323650898, "cos": 0.9238795325112867, "tan": 0.41421356237309503, "timestamp": "2023-01-12T02:08:07.142865Z"}
{"value": 0.5235987755982988, "sin": 0.49999999999999994, "cos": 0.8660254037844387, "tan": 0.5773502691896257, "timestamp": "2022-12-15T11:38:07.142888Z"}
```

3. Create table statement 
```anylog
create_stmt = suggest create !prep_dir/test.trig_readings.0.0.json
```

4. Declare Table policy 

