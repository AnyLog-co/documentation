# Data Monitoring
## Initiate Data Monitoring
```
data monitor where dbms = aiops and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
```

## Query Data Monitoring
**Commnad**: 
```
get monitored data
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
