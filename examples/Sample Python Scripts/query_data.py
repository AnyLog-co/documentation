import requests


def json_execute_query():
    """
    Example of querying data against AnyLog & return results in JSON format
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/queries.md
    :params:
        status:bool - used to verify query gets executed
        conn:str - REST IP & Port
        cmd:str - query to execute
        headers:dict - REST header information
    :print:
        results from query
    """
    status = True
    conn = '172.105.55.143:2049'
    cmd = 'sql yudash format=json and stat=false "select timestamp, value from sample_table where period(day, 1, now(), timestamp) limit 10"'
    headers = {
        'command': cmd,
        'User-Agent': 'AnyLog/1.23',
        'destination': 'network'
    }

    try:
        r = requests.get('http://%s' % conn, headers=headers)
    except Exception as e:
        print('Failed to query data against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to query data against %s due to network error: %s' % (conn, r.status_code))
            status = False

    if status is True:
        try:
            print(r.json()['Query'])
        except Exception as e:
            print('Failed to extract data, printing raw content (Error: %s)...' % e)
            print(r.text)


def table_execute_query():
    """
    Example of querying data against AnyLog & return results in table format
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/queries.md
    :params:
        status:bool - used to verify query gets executed
        conn:str - REST IP & Port
        cmd:str - query to execute
        headers:dict - REST header information
    :print:
        results from query
    """
    status = True
    conn = '172.105.55.143:2049'
    cmd = 'sql yudash format=table "select timestamp, value from sample_table where period(day, 1, now(), timestamp) limit 10"'
    headers = {
        'command': cmd,
        'User-Agent': 'AnyLog/1.23',
        'destination': 'network'
    }

    try:
        r = requests.get('http://%s' % conn, headers=headers)
    except Exception as e:
        print('Failed to query data against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to query data against %s due to network error: %s' % (conn, r.status_code))
            status = False

    if status is True:
        try:
            print(r.text)
        except Exception as e:
            print('Failed to extract data raw content (Error: %s)' % e)


if __name__ == '__main__':
    json_execute_query()
    table_execute_query()