# Sample Data Generator
Sample data generators used to insert demo data into AnyLog. 

When using _MQTT_ or REST _POST_ to insert data, users need to configure a [MQTT client](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#example) 
* [Ping or PercentageCPU](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/data_generator_generic_ping_percentage_demo.al)
* [Power](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/data_generator_generic_power.al)
* [Performance](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/data_generator_generic_performance.al)
* [Trig](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/data_generator_generic_trig.al)
* [OPCUA](https://github.com/AnyLog-co/deployment-scripts/blob/main/scripts/demo_scripts/data_generator_generic_opcua.al)

**Other Services**:
* [Blobs Data Generator](https://github.com/AnyLog-co/Sample-Data-Generator/blob/master/Blobs.md)
* [Store locations for Power Generator in blockchain](https://github.com/AnyLog-co/Sample-Data-Generator/blob/master/data_generator_generic_power_blockchain_coordinates.py)
```shell
python3 Sample-Data-Generator/data_generator_generic_power_blockchain_coordinates.py
```


## Docker Deployment 
* Help 
```shell
# generic
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
  -e HELP=true \
  --rm anylogco/sample-data-generator:latest
     
# generic help with detailed information such as sample call and aviloble data. 
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
  -e EXTENDED_HELP=true \
  --rm anylogco/sample-data-generator:latest
```

* Sample calls to send data into AnyLog 
```shell
# send ping data via REST PUT to multiple operator nodes
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
   -e DATA_TYPE=ping \
   -e INSERT_PROCESS=put \ 
   -e DB_NAME=test \
   -e TOTAL_ROWS=100 \ 
   -e BATCH_SIZE=10 \
   -e SLEEP=0.5 \
   -e CONN=198.74.50.131:32149,178.79.143.174:32149 \ 
   -e TIMEZONE=utc \
--rm anylogco/sample-data-generator:latest

# send ping and percentagecpu data via REST POST to an operator nodes
docker run -it --detach-keys=ctrl-d --name data-generator --network host \
   -e DATA_TYPE=ping,percentagecpu \
   -e INSERT_PROCESS=post \
   -e DB_NAME=test \
   -e TOTAL_ROWS=100 \
   -e BATCH_SIZE=10 \
   -e SLEEP=0.5 \
   -e CONN=198.74.50.131:32149 \
   -e TIMEZONE=utc \
--rm anylogco/sample-data-generator:latest
```

* Using print or file _INSERT_PROCESS_. Directions to access files stored in docker volume can be found [here](https://github.com/AnyLog-co/documentation/blob/master/deployments/Support/cheatsheet.md).   
```shell
# print OPCUA to screen 
docker run -it --detach-keys=ctrl-d --name data-generator --network host \ 
   -e DATA_TYPE=opcua \ 
   -e INSERT_PROCESS=print \ 
   -e DB_NAME=test \ 
   -e TOTAL_ROWS=100 \ 
   -e BATCH_SIZE=10 \ 
   -e SLEEP=0.5 \ 
   -e TIMEZONE=local \ 
--rm anylogco/sample-data-generator:latest

# store POWER data into file(s) with performance enabled - notice that unlike other examples, the file insert process 
# has a volume named data-generator
docker run -it --detach-keys=ctrl-d --name data-generator --network host \ 
   -e DATA_TYPE=power \ 
   -e INSERT_PROCESS=file \ 
   -e DB_NAME=test \ 
   -e TOTAL_ROWS=1000 \ 
   -e BATCH_SIZE=10 \ 
   -e SLEEP=0.5 \ 
   -e TIMEZONE=local \ 
   -v data-generator:/app/Sample-Data-Generator/data/new-data \ 
--rm anylogco/sample-data-generator:latest
```

## Local Install
1. Clone Sample Data Generator
```shell
git clone https://github.com/AnyLog-co/Sample-Data-Generator
```

2. Install requirements - make sure python3 and python3-pip are installed   
```shell
python3 -m pip install -r $HOME/Sample-Data-Generator/requirements.txt
```

3. Run Data Generator 
* Help 
```shell
# generic
python3 Sample-Data-Generator/data_generator_generic.py
<< COMMENT
:positional arguments:
  data_type             type of data to insert into AnyLog. Choices: trig, performance, ping, percentagecpu, opcua, power
  insert_process        format to store generated data. Choices: print, file, put, post, mqtt
  db_name               logical database name
:options:
  -h, --help            show this help message and exit
  --extended-help [EXTENDED_HELP]
                        Generates help, but extends to include a sample row per data type
  --table-name TABLE_NAME
                        Change default table name (valid for data_types except power)
  --total-rows TOTAL_ROWS
                        number of rows to insert. If set to 0, will run continuously
  --batch-size BATCH_SIZE
                        number of rows to insert per iteration
  --sleep SLEEP         wait time between each row
  --timezone {local,utc,et,br,jp,ws,au,it}
                        timezone for generated timestamp(s)
  --enable-timezone-range [ENABLE_TIMEZONE_RANGE]
                        set timestamp within a range of +/- 1 month. For performance testing, it is 
                        used to randomize the order timestamps are inserted.
  --performance-testing [PERFORMANCE_TESTING]
                        insert all rows within a 24 hour period
  --conn CONN           {user}:{password}@{ip}:{port} for sending data either via REST or MQTT
  --topic TOPIC         topic for publishing data via REST POST or MQTT
  --rest-timeout REST_TIMEOUT
                        how long to wait before stopping REST
  --qos {0,1,2}         MQTT Quality of Service
  --dir-name DIR_NAME   directory when storing to file
  --compress [COMPRESS]
                        whether to zip data dir
  --exception [EXCEPTION]
                        whether to print exceptions
<<
# generic help with detailed information such as sample call and aviloble data.
python3 Sample-Data-Generator/data_generator_generic.py --extended-help
```

* Sample calls to send data into AnyLog 
```shell
# send ping data via REST PUT to multiple operator nodes
python3 Sample-Data-Generator/data_generator_generic.py ping put test \
  --total-rows 100 \
  --batch-size 10 \
  --sleep 0.5 \
  --conn 198.74.50.131:32149,178.79.143.174:32149 \
  --timezone utc

# send ping and percentagecpu data via REST POST to an operator nodes
python3 Sample-Data-Generator/data_generator_generic.py ping,percentagecpu put test \
  --total-rows 100 \
  --batch-size 10 \
  --sleep 0.5 \
  --conn 198.74.50.131:32149 \
  --timezone utc
```

* Using print or file _INSERT_PROCESS_
```shell
# print OPCUA to screen 
python3 Sample-Data-Generator/data_generator_generic.py opcua print test \
  --total-rows 100
  --batch-size 10
  --sleep 0.5
  --timezone local

python3 Sample-Data-Generator/data_generator_generic.py power print test
  --total-rows 1000 \
  ---batch-size 10 \
  --sleep 0.5 \
  --timezone local \
  --data-dir Sample-Data-Generator/data/new-data # <-- this is the default directory 
```

## Sample JSON
```json
# Data Type: trig
  {"dbms": "test", "table": "trig_data", "value": -3.141592653589793, "sin": -1.2246467991473532e-16, "cos": -1.0, "tan": 1.2246467991473532e-16, "timestamp": "2022-08-27T15:50:12.001399Z"}
        
# Data Type: performance
  {"dbms": "test", "table": "rand_data", "value": -1.2246467991473532e-16, "timestamp": "2022-08-27T15:50:12.163818Z"}
        
# Data Type: ping
  {"dbms": "test", "table": "ping_sensor", "device_name": "Ubiquiti OLT", "parentelement": "d515dccb-58be-11ea-b46d-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw", "value": 44.74, "timestamp": "2022-08-27T15:50:12.059726Z"}
        
# Data Type: percentagecpu
  {"dbms": "test", "table": "percentagecpu_sensor", "device_name": "VM Lit SL NMS", "parentelement": "1ab3b14e-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H", "value": 9.59, "timestamp": "2022-08-27T15:50:12.116925Z"}
        
# Data Type: opcua
  {"dbms": "test2", "table": "opcua_readings", "fic1_pv": -103.29249139515318, "fic1_mv": -227.862187363, "fic1_sv": -48.493873977761645, "lic1_pv": 165.18648883311027, "lic1_mv": -84.59834643031611, "lic1_sv": 174.86936425992465, "fic2_pv": -37.52888216655371, "fic2_mv": 38.63696693385969, "fic2_sv": -182.07962937349504, "lic2_pv": 142.90402691921074, "lic2_mv": -35.64751556177472, "lic2_sv": -62.69296482664739, "fic3_pv": -147.060548270305, "fic3_mv": -57.93928389193016, "fic3_sv": 418.2631932904929, "lic3_pv": 176.7756420678825, "lic3_mv": -61.49695028678772, "lic3_sv": 220.60063882032966, "fic4_pv": -44.66240442407483, "fic4_mv": 11.529102739194443, "fic4_sv": 124.97175098185224, "lic4_pv": 9.507763915723592, "lic4_mv": 30.483647656168543, "lic4_sv": -213.4404433100362, "fic5_pv": -460.10226426203155, "fic5_mv": -72.96099747863087, "fic5_sv": -53.62672940378895, "lic5_pv": -89.93465024402398, "lic5_mv": -20.523831049180885, "lic5_sv": -125.29010564894106, "timestamp": "2022-09-24T14:30:10.575429Z"}
        
# Data Type: power
  {"dbms": "test", "table": "solar", "location": "38.89773, -77.03653", "value": 8.43453536493608, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "battery", "location": "38.89773, -77.03653", "value": 9.532695799656166, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "inverter", "location": "38.89773, -77.03653", "value": 20.03601934228979, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "eswitch", "location": "38.89773, -77.03653", "value": 9.530111494215165, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "pmu", "location": "38.89773, -77.03653", "value": 30.51712172789563, "timestamp": "2022-08-27T15:50:12.205323Z"}
  {"dbms": "test", "table": "synchrophasor", "location": "38.89773, -77.03653", "phasor": "bXlvzdYc", "frequency": 1216.6996978149687, "dfreq": 2326.468559576384, "analog": 4.591088473171304, "timestamp": "2022-08-27T15:50:12.205323Z"}
```
