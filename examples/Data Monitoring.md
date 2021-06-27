# Data Monitoring
## Initiate Data Monitoring
```
data monitor where dbms = aiops and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
```

## Query Data Monitoring
**Commnad**: Get Data monitored 
```
get data monitored 
```

**Sample Output**: 
```
DBMS  Table     H:M:S Events/sec Count Min   Max    Avg
-----|---------|-----|----------|-----|-----|------|------|
aiops|fic12    |0:9:0|      0.17|   10|47.36| 52.36| 49.99|
aiops|fic12    |0:8:0|      0.18|   11|48.39| 52.72| 50.83|
aiops|fic12    |0:7:0|      0.20|   12|47.09| 52.22| 49.41|
aiops|fic12    |0:6:0|      0.17|   10|47.57| 52.64| 50.53|
aiops|fic12    |0:5:0|      0.17|   10|47.15| 53.25| 50.12|
aiops|fic12    |0:4:0|      0.17|   10|46.89| 52.70| 49.83|
aiops|fic12    |0:3:0|      0.20|   12|47.61| 52.51| 49.47|
aiops|fic12    |0:2:0|      0.18|   11|47.62| 51.96| 49.65|
aiops|fic12    |0:1:0|      0.17|   10|47.47| 52.92| 50.12|
aiops|fic12    |0:0:0|      0.02|    1|49.14| 49.14| 49.14|
aiops|fic11    |0:9:0|      0.17|   10|62.31| 67.43| 64.97|
aiops|fic11    |0:8:0|      0.18|   11|63.45| 67.79| 65.85|
aiops|fic11    |0:7:0|      0.20|   12|61.97| 67.29| 64.38|
aiops|fic11    |0:6:0|      0.17|   10|62.45| 67.71| 65.56|
aiops|fic11    |0:5:0|      0.17|   10|61.96| 68.40| 65.09|
aiops|fic11    |0:4:0|      0.17|   10|61.71| 67.80| 64.84|
aiops|fic11    |0:3:0|      0.20|   12|62.46| 67.54| 64.44|
aiops|fic11    |0:2:0|      0.18|   11|62.61| 67.05| 64.67|
aiops|fic11    |0:1:0|      0.17|   10|62.35| 68.06| 65.14|
aiops|fic11    |0:0:0|      0.02|    1|64.13| 64.13| 64.13|
aiops|lic1     |0:9:0|      0.17|   10|51.23| 51.24| 51.23|
aiops|lic1     |0:8:0|      0.18|   11|51.22| 51.24| 51.23|
...
```

**Command**: Get streaming status 
```
get streaming
```

**Sample Output**: 
```

Flush Thresholds
Threshold         Value  Streamer
-----------------|------|--------|
Default Time     |    60|Running |
Default Volume   |10,000|        |
Default Immediate|True  |        |
Buffered Rows    |     1|        |
Flushed Rows     |     5|        |

Statistics
DBMS-Table      File Put File Rows Streaming Put Streaming Rows Immediate Last Process
---------------|--------|---------|-------------|--------------|---------|-------------------|
aiops.fic11    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:06|
aiops.fic12    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:06|
aiops.fic13    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.lic1     |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.lic1_sp  |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.ai_mv    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.valve_pos|       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.err      |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
```

**Command**: Get summary of rows count for a given operator node
```
get rows count
```

**Sample Output**: 
```
DBMS Name Table Name                                           Rows Count
---------|----------------------------------------------------|----------|
aiops    |ai_mv                                               |         0|
         |err                                                 |         0|
         |fic11                                               |         0|
         |fic11_fb_factualvalue                               |         0|
         |fic12                                               |         0|
         |fic12_fb_fic12_fout                                 |         0|
         |fic12_fb_fsetpointvalue                             |         0|
         |fic13                                               |         0|
         |fic13_fb_factualvalue                               |         0|
         |lic1                                                |         0|
         |lic1_fb__lic1_fout                                  |         0|
         |lic1_sp                                             |         0|
         |modbus_data                                         |         0|
         |par_ai_mv_2021_06_17_d01_timestamp                  |       150|
         |par_ai_mv_2021_06_18_d01_timestamp                  |     31388|
         |par_ai_mv_2021_06_19_d01_timestamp                  |      7825|
         |par_ai_mv_2021_06_21_d01_timestamp                  |      9380|
         |par_ai_mv_2021_06_22_d01_timestamp                  |     23832|
         |par_ai_mv_2021_06_23_d01_timestamp                  |     22016|
         |par_ai_mv_2021_06_24_d01_timestamp                  |     16425|
         |par_err_2021_06_17_d01_timestamp                    |       150|
         |par_err_2021_06_18_d01_timestamp                    |     31390|
         |par_err_2021_06_19_d01_timestamp                    |      7825|
         |par_err_2021_06_21_d01_timestamp                    |      9377|
         |par_err_2021_06_22_d01_timestamp                    |     23832|
         |par_err_2021_06_23_d01_timestamp                    |     22007|
         |par_err_2021_06_24_d01_timestamp                    |     16425|
         |par_fic11_2021_06_17_d01_timestamp                  |       150|
         |par_fic11_2021_06_18_d01_timestamp                  |     31392|
         |par_fic11_2021_06_19_d01_timestamp                  |      7825|
         |par_fic11_2021_06_21_d01_timestamp                  |      9381|
         |par_fic11_2021_06_22_d01_timestamp                  |     23834|
         |par_fic11_2021_06_23_d01_timestamp                  |     22017|
         |par_fic11_2021_06_24_d01_timestamp                  |     16428|
         |par_fic11_fb_factualvalue_2021_06_21_d01_timestamp  |         1|
         |par_fic12_2021_06_17_d01_timestamp                  |       150|
         |par_fic12_2021_06_18_d01_timestamp                  |     31382|
         |par_fic12_2021_06_19_d01_timestamp                  |      7825|
         |par_fic12_2021_06_21_d01_timestamp                  |      9383|
         |par_fic12_2021_06_22_d01_timestamp                  |     23834|
         |par_fic12_2021_06_23_d01_timestamp                  |     22005|
         |par_fic12_2021_06_24_d01_timestamp                  |     16428|
         |par_fic12_fb_fic12_fout_2021_06_21_d01_timestamp    |         1|
         |par_fic12_fb_fsetpointvalue_2021_06_03_d01_timestamp|       100|
         |par_fic13_2021_06_17_d01_timestamp                  |       150|
         |par_fic13_2021_06_18_d01_timestamp                  |     31373|
         |par_fic13_2021_06_19_d01_timestamp                  |      7825|
         |par_fic13_2021_06_21_d01_timestamp                  |      9377|
         |par_fic13_2021_06_22_d01_timestamp                  |     23833|
         |par_fic13_2021_06_23_d01_timestamp                  |     22005|
         |par_fic13_2021_06_24_d01_timestamp                  |     16426|
         |par_fic13_fb_factualvalue_2021_06_03_d01_timestamp  |       103|
         |par_lic1_2021_06_17_d01_timestamp                   |       150|
         |par_lic1_2021_06_18_d01_timestamp                   |     31375|
         |par_lic1_2021_06_19_d01_timestamp                   |      7825|
         |par_lic1_2021_06_21_d01_timestamp                   |      9377|
         |par_lic1_2021_06_22_d01_timestamp                   |     23833|
         |par_lic1_2021_06_23_d01_timestamp                   |     22016|
         |par_lic1_2021_06_24_d01_timestamp                   |     16426|
...
```
