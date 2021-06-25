# Adding Data and Queries 

## Adding Data 
```
curl --location --request POST '192.168.50.159:2051' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'Content-Type: text/plain' \
--data-raw ' [{"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
 {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
 {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}]'
```

## Queries 
**Command**: Tags Summary 
```
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include=(fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
```
**Sample Outout**: 
```

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
```

**Command**: Using _PERIOD_ find the last occurence & calculate to the nearest value
```
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include=(fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend=(@table_name as table) and format=table "select max(timestamp) as max_timestamp, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11 where period(day, 1, now(), timestamp);"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
```
**Sample Output**: 
```
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
```

**Command**: Using _INCREMENTS_ consider a partitioned segment of time
```
curl -X GET 13.67.180.124:2149 -H 'command: sql aiops include = (fic12,fic11,valve_pos,lic1_sp,fic13,err,lic1,ai_mv) and extend = (@table_name as table) and format=table "select increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value, count(*) as row_count from fic11 limit 10"' -H "destination: network" -H "User-Agent: AnyLog/1.23" -w "\n"
```
**Sample Output**: 
```
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
```
