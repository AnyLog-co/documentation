# Example with User credentials

USERNAME=ori
PASSWORD=test 

if [[ `base64 --help  | grep "\--wrap"` ]] 
then
    AUTH=$(echo -ne "$USERNAME:$PASSWORD" | base64 --wrap 0)
else 
    AUTH=$(echo -ne "$USERNAME:$PASSWORD" | base64 --break 0)
fi 

curl -X GET 10.0.0.231:2049 -H "command: get status" -H "User-Agent: AnyLog/1.23" -H "Authorization: ${AUTH}" -w "\n" 
 
