import argparse
import re
import request

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


def execute_query(conn:str, dbms:str, auth:tuple=(), timeout:float=30):
    # build query
    output_format="table"
    stat=True
    query = f"sql {dbms} format={output_format}"
    if stat is False:
        query += " and stat=false"
    query += ' "select * from sample_data;"'

    headers = {
        "command": query,
        "User-Agent": "AnyLog/1.23",
        "destination": "network"
    }

    try:
        r = request.get(url=f"http://{conn}", headers=headers)
    except Exception as error:
        print(f"Failed to execute query `{headers['command']}` (Error: {error})")
        return
    else:
        if int(r.status_code) < 200 or int(r.status_code) > 299:
            print(f"Failed to execute query `{headers['command']}` (Network Error: {r.status_code})")
            return
        try:
            print(r.json())
        except Exception as error:
            print(r.text)


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
    parse.add_argument("--rest-timeout", type=float, default=30, help="REST timeout")
    args = parse.parse_args()

    conn = args.conn
    auth = ()
    if '@' in args.conn:
        auth, conn = args.conn.split("@")
        auth = tuple(auth.split(":"))


