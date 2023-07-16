curl -X POST 127.0.0.1:32149 \
  -H "command: data" \
  -H "topic: sample-data" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:01:35.531498Z", "value": 0.34818421211998407, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.036593Z", "value": 43.03195182458719, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:36.540271Z", "value": 2.7131214097633305, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.044805Z", "value": 60.165240674173546, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:37.549647Z", "value": 73.94402366511534, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.053755Z", "value": 51.633021025712786, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:38.558580Z", "value": 41.02022743564046, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.062021Z", "value": 52.22346461071091, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:39.567019Z", "value": 63.078391396022596, "db_name": "test", "table": "sample_data"}, {"timestamp": "2023-07-16T22:01:40.071045Z", "value": 52.09570154599, "db_name": "test", "table": "sample_data"}]'

curl -X PUT 127.0.0.1:32149 \
  -H "type: json" \
  -H "dbms: test" \
  -H "table: sample_data" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  -d '[{"timestamp": "2023-07-16T22:15:16.275270Z", "value": 26.760648537459296}, {"timestamp": "2023-07-16T22:15:16.779954Z", "value": 99.07731050408944}, {"timestamp": "2023-07-16T22:15:17.282287Z", "value": 99.28450509848346}, {"timestamp": "2023-07-16T22:15:17.786096Z", "value": 80.41027907076285}, {"timestamp": "2023-07-16T22:15:18.290123Z", "value": 32.27699391736516}, {"timestamp": "2023-07-16T22:15:18.794041Z", "value": 44.586993538065876}, {"timestamp": "2023-07-16T22:15:19.296349Z", "value": 97.49718100436169}, {"timestamp": "2023-07-16T22:15:19.796996Z", "value": 14.902283983713582}, {"timestamp": "2023-07-16T22:15:20.299712Z", "value": 85.88924631087048}, {"timestamp": "2023-07-16T22:15:20.803080Z", "value": 15.671337182852396}]'
