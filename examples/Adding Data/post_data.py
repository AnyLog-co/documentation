import datetime
import json
import random
import requests

def __convert_data(data:dict)->str:
    """
    If data is of type dict convert to JSON
    :args:
        data:dict - data to convert
    :params:
        json_data:str - data as a JSON
    :return:
        json_data
    """
    json_data = data
    if isinstance(data, dict):
        try:
            json_data = json.dumps(data)
        except Exception as e:
            print('Failed to convert data into JSON (Error: %s)' % e)
    return json_data


def post_data(conn:str, rest_topic:str, payload:dict)->bool:
    """
    Send data via REST using POST command
    :ur:
        https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-post-command
    :requirement:
        an MQTT client that uses a REST connection as a broker
    :args:
        conn:str - REST IP & port
        rest_topic:str - topic correlated to the MQTT client using a REST
        payload:dict - data to post into AnyLog - should contain logical database name and table
    :params:
        status:bool -
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
    status = True
    headers = {
        'command': 'data',
        'topic': rest_topic,
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.post('http://%s' % conn, headers=headers, data=__convert_data(data=payload))
    except Exception as e:
        print('Failed to send data via POST against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            status = False
            print('Failed to send data via POST against %s due to network error: %s' % (conn, r.status_code))

    return status


if __name__ == '__main__':
    conn = "172.105.55.143:2049"
    rest_topic = 'yudash-rest'
    data = {
        'dbms': 'yudash',
        'table': 'sample_data',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'value': random.random(),
        'unit': 'Celsius'
    }

    if post_data(conn=conn, rest_topic=rest_topic, payload=data):
        print('Success!')