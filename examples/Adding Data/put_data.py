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


def put_data(conn:str, dbms:str, table:str, payload:dict, mode:str='streaming')->bool:
    """
    Send data via REST using PUT command
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#using-a-put-command
    :args:
        conn:str - IP & Port of rest connection
        dbms:str - logical database name
        table:str - table name to store data in
        payload:dict - data to post into AnyLog
        mode:str - whether to PUT data continuously (streaming) or one at a time (file)
    :params:
        status:bool -
        headers:dict - REST header
    :return:
        False if fails, else True
    """
    status = True
    headers = {
        'type': 'json',
        'dbms': dbms,
        'table': table,
        'mode': mode,
        'Content-Type': 'text/plain'
    }

    try:
        r = requests.put('http://%s' % conn, headers=headers, data=__convert_data(data=payload))
    except Exception as e:
        print('Failed to send data via PUT against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            status = False
            print('Failed to send data via PUT against %s due to network error: %s' % (conn, r.status_code))

    return status


if __name__ == '__main__':
    conn = "172.105.55.143:2049"
    dbms = "yudash"
    table = "sample_data"
    mode = "streaming"
    data = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f +08:00'),
        'value': random.random(),
        'unit': 'Celsius'
    }

    if put_data(conn=conn, dbms=dbms, table=table, payload=data, mode=mode):
        print('Success!')

