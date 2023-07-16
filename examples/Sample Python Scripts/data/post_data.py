import requests


def post_data(conn:str, auth:tuple, topic:str, payload:str)->bool:
    """
    Send data via REST using POST command
    :ur:
        https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-post-command
    :requirement:
        an MQTT client that uses a REST connection as a broker
    :args:
        conn:str - REST IP & port
        topic:str - topic correlated to the MQTT client using a REST
        auth:tuple - rest authentication
        payload:dict - data to post into AnyLog - should contain logical database name and table
    :params:
        headers:dict - REST header
    :return:
        False if fails, else True
    :sample-mqtt-client-call:
        run mqtt client where broker = rest and port=2049 and user-agent = anylog and topic = (name=yudash-rest and dbms = "bring [dbms]" and table = "bring [table]" and column.timestamp.timestamp = "bring [timestamp]" and column.value.float = "bring [value]")
    :sample-data:
        {
            'dbms': 'new_dbms',
            'table': 'new_table',
            'timestamp': '2021-10-20 15:35:49.32145',
            'value': 3.1459
        }
    """
    headers = {
        'command': 'data',
        'topic': topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.post('http://%s' % conn, auth=auth, timeout=30, headers=headers, data=payload)
    except Exception as e:
        print('Failed to send data via POST against %s (Error: %s)' % (conn, e))
    else:
        if int(r.status_code) != 200:
            print('Failed to send data via POST against %s due to network error: %s' % (conn, r.status_code))



