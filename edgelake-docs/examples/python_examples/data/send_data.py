import argparse
import datetime
import json
import random
import re
import time

import post_data
import put_data


def __validate_conn_pattern(conns:str)->str:
    """
    Validate connection information format is connect
    :valid formats:
        127.0.0.1:32049
        user:passwd@127.0.0.1:32049
    :args:
        conn:str - REST connection information
    :params:
        pattern1:str - compiled pattern 1 (127.0.0.1:32049)
        pattern2:str - compiled pattern 2 (user:passwd@127.0.0.1:32049)
    :return:
        if fails raises Error
        if success returns conn
    """
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
    pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    for conn in conns.split(","):
        if not pattern1.match(conn) and not pattern2.match(conn):
            raise argparse.ArgumentTypeError(f'Invalid connection format: {conn}. Supported formats: 127.0.0.1:32049 or user:passwd@127.0.0.1:32049')

    return conns

def __convert_data(data:list)->str:
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
    try:
        json_data = json.dumps(data, indent=None)
    except Exception as e:
        print('Failed to convert data into JSON (Error: %s)' % e)
    return json_data

def generate_data(total_rows=10)->list:
    """
    Generate an array wit X rows of timestamp/value to be inserted into database
    :sample-row:
        {
            "timestamp": "2023-01-04T10:15:32.245185Z",
            "value": "31.415923458"
        }
    :args:
        total_rows:str - number of rows to insert
    :params:
        data:list - list of generated rows
    :return:
        data
    """
    data = []
    for i in range(total_rows):
        data.append({
            "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "value": random.random() * 100
        })
        time.sleep(0.5)

    return data


def main():
    """
    :positional arguments:
        conn                  Either REST or MQTT connection information

    :optional arguments:
        -h, --help                  show this help message and exit
        --db-name       DB_NAME     logical database name
        --total-rows    TOTAL_ROWS  number of rows to generate
        --insert-process            which insert process type to utilize
            * put
            * post
            * mqtt
        --topic         TOPIC       POST or MQTT topic
    :Sample Data:
    {
        "timestamp": "2023-07-16T22:15:16.275270Z",
        "value": 26.760648537459296
    }
    """
    parse = argparse.ArgumentParser()
    parse.add_argument("conn", type=__validate_conn_pattern, default="127.0.0.1:32149", help="Either REST or MQTT connection information")
    parse.add_argument("--db-name", type=str, default="test", help="logical database name")
    parse.add_argument("--total-rows", type=int, default=10, help="number of rows to generate")
    parse.add_argument("--insert-process", type=str, default="put", choices=["put", "post"], help="which insert process type to utilize")
    parse.add_argument("--topic", type=str, default="sample-data", help="POST or MQTT topic")
    args = parse.parse_args()


    conn = args.conn
    auth = ()
    if '@' in args.conn:
        auth, conn = args.conn.split("@")
        auth = tuple(auth.split(":"))

    data = generate_data(total_rows=args.total_rows)
    if args.insert_process != "put":
        for row in data:
            row["db_name"] = args.db_name
            row["table"] = "sample_data"

    payload = __convert_data(data=data)
    if not isinstance(payload, str):
        exit(1)

    if args.insert_process == 'put':
        put_data.put_data(conn=conn, auth=auth, dbms=args.db_name, table='sample_data', payload=payload, mode='streaming')
    elif args.insert_process == 'post':
        post_data.post_data(conn=conn, auth=auth, topic=args.topic, payload=payload)


if __name__ == '__main__':
    main()