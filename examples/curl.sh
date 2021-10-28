# Example with User credentials

USERNAME=ori
PASSWORD=test 

AUTH=$(echo -ne "$USERNAME:$PASSWORD" | base64 --wrap 0)

curl -X GET 10.0.0.231:2049 -H "command: get status" -H "User-Agent: AnyLog/1.23" -H "Authorization: ${AUTH}" 

 
