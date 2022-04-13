"""set data distribution where dbms = lsl_demo and table = ping_sensor and dest = 10.12.32.148:2048
set data distribution where dbms = lsl_demo and table = * and dest = 10.12.32.148:2048 and dest = 10.181.231.18:2048"""

import argparse
import requests


def __execute_query(conn:str, query:str)->str:
    """
    Execute GET request against the connection - used to extract cluster & operator info as needed
    :args:
        conn:str - REST connection information
        query:str - query to execute
    :params:
        output:str - content to return (either a list of cluster IDs or list of operator IP:Port
        headers:dict - REST header
        r:requests.Requests - results from REST request
    :return:
        content from REST request or None
    """
    output = None
    headers = {
        "command": query,
        "User-Agent": "AnyLog/1.23"
    }
    try:
        r = requests.get(url=f'http://{conn}', headers=headers)
    except Exception as e:
        print(f'Failed to execute {query} (Error: {e})')
    else:
        if int(r.status_code) == 200:
            try:
                output = r.json()
            except:
                output = r.text
        else:
            print(f'Failed to execute {query} (Network Error: {r.status_code})')

    return output


def set_distribution(conn:str, db_name:str, table:str, operators:str)->bool:
    """
    Set distribution based on user input
    :args:
        conn:str - publisher REST connection information
        db_name:str - logical database to set distribution for
        table:str - table to distribute data for
        operators:list -  comma separated list of operators (IP:Port) to distribute data
    :params:
        status:bool
        stmt:str - command to execute via REST
        headers:dict - REST header
        r:requests.Requests.post - results from POST request
    :return:
        status
    """
    status = True
    stmt = f"set data distribution where dbms={db_name} and table={table}"
    for operator in operators:
        stmt += f" and dest={operator}"
    headers = {
        "command": stmt,
        "User-Agent": "AnyLog/1.23"
    }

    try:
        r = requests.post(url=f'http://{conn}', headers=headers)
    except Exception as e:
        print(f"Failed to POST data distribution against {conn} (Error: {e})")
        bool = False
    else:
        if int(r.status_code) != 200:
            print(f"Failed to POST data distribution against {conn} (Network Error: {r.status_code})")
            bool = False

    return status


def main():
    """
    :positional arguments:
        conn                  publisher REST connection information
        db_name               logical database to set distribution for
    :optional arguments:
        -h, --help                      show this help message and exit
        --table         TABLE           table to distribute data for (default: *)
        --destination   DESTINATION     comma separated list of operators (IP:Port) to distribute data (default: None)
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('conn', type=str, default='127.0.0.1:2049', help='publisher REST connection information')
    parser.add_argument('db_name', type=str, default='test', help='logical database to set distribution for')
    parser.add_argument('--table', type=str, default='*', help='table to distribute data for')
    parser.add_argument('--destination', type=str, default=None, help='comma separated list of operators (IP:Port) to distribute data')
    args = parser.parse_args()

    if args.destination is not None:
        distribution_operators = args.distribution.split(',')
    else:
        distribution_operators = []
        cluster_ids = __execute_query(conn=args.conn, query=f'blockchain get cluster where dbms={args.db_name} bring [cluster][id] separator=,')
        for cluster in cluster_ids.split(','):
            operators = __execute_query(conn=args.conn, query=f'blockchain get operator where cluster={cluster} bring [operator][ip] : [operator][port] separator=,')
            if operators is not None:
                for operator in operators.split(','):
                    distribution_operators.append(operator)

    set_distribution(conn=args.conn, db_name=args.db_name, table=args.table, operators=distribution_operators)



if __name__ == '__main__':
    main()
