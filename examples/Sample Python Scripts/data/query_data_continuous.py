import json
import datetime
import os
import requests
import time

LOCAL_DR = os.path.expanduser(os.path.expanduser(__file__)).strip('query_data_continuous.py')


def __create_query(db_name:str, table_name:str, last_timestamp:str=None):
    """
    Create query
    :args:
        db_name:str - logical database name
        table_name:str - table to query data
        last_timestamp:str - last timestamp
    :param:
        query:str - query being created
    :return:
        query
    """
    query = f'sql {db_name} format=json and stat=false "select timestamp, value from {table_name}'
    if last_timestamp is not None:
        query += f" WHERE timestamp >= '{last_timestamp}'"
    else:
        query += f" WHERE timestamp >= NOW() - 1 minute"

    query += f' ORDER BY timestamp desc;"'

    return query


def __execute_query(anylog_conn:str, query:str, auth:tuple=None, timeout:int=30)->list:
    """
    Execute query
    :args:
        anylog_conn:str - REST IP:PORT
        query:str - query to execute
        auth:tuple - (user, password) authentication
        timeout:int - REST timeout
    :params:
        output:lst - results from query
        headers:dict - REST header info
        r:requests.get - result from REST
    :return:
        output
    """
    output = None
    headers = {
        'command': query,
        'User-Agent': 'AnyLog/1.23',
        'destination': 'network'
    }

    try:
        r = requests.get(url=f'http://{anylog_conn}', headers=headers, auth=(), timeout=timeout)
    except Exception as error:
        print(f'Failed to execute query (Error; {error})')
    else:
        if int(r.status_code) == 200:
            try:
                output = r.json()
            except:
                try:
                    output = r.text
                except Exception as error:
                    print(f'Failed to extract results from query (Error: {error})')
            else:
                if 'Query' in output:
                    output = output['Query']
        else:
            print(f'Failed to extract results from query (Network Error: {r.status_code})')

    return output


def __store_results(db_name:str, table_name:str, results:list, timestamp:str):
    """
    Store results in file
    :args:
        db_name:str - logical database name
        table_name:str - table to query data
        results:list - Results values to store
        timestamp:str - timestamp used for string
    :params:
        ts:str - timestamp  formatted for file name
        file_name:str - file to store resultts in
        json_row:str - result dict converted to JSON-string
    """
    ts = datetime.datetime.strftime(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'), '%Y%m%d%H%M%S%f')
    file_name = os.path.join(LOCAL_DR, f'{db_name}.{table_name}.{ts}.0.json')
    try:
        with open(file_name, 'w') as f:
            for row in results:
                try:
                    json_row = json.dumps(row)
                except Exception as error:
                    print(f'Failed to convert from dict to JSON (Error: {error})')
                else:
                    if row != results[-1]:
                        input_row = f'{json_row},\n'
                    else:
                        input_row = json_row
                    try:
                        f.write(input_row)
                    except Exception as error:
                        print(f'Failed to write row in file (Error: {error}')
    except Exception as error:
        print(f'Failed to open file {file_name} to write content (Error: {error})')


def main(anylog_conn:str, db_name:str, table_name:str, repeat:int=10, sleep:int=5, auth:tuple=None, timeout:int=30):
    """
    """
    last_timestamp = None
    for i in range(repeat):
        query = __create_query(db_name=db_name, table_name=table_name, last_timestamp=last_timestamp)
        results = __execute_query(anylog_conn=anylog_conn, query=query, auth=auth, timeout=timeout)
        if results is not None:
            oldest = results[-1]['timestamp']
            last_timestamp = results[0]['timestamp']
            __store_results(db_name=db_name, table_name=table_name, results=results, timestamp=oldest)
        time.sleep(sleep)


if __name__ == '__main__':
    main(anylog_conn='23.239.12.151:32349', db_name='edgex', table_name='rand_data', repeat=30, sleep=10, auth=None, timeout=30)
