import argparse
import json
import time

import import_packages
import_packages.import_dirs()

import anylog_api
import blockchain_cmd

def __format_print(blockchain:list):
    """
    Format output
    :args:
        blockchain:list - results from blockchain query
    """
    if isinstance(blockchain, list): 
        for policy in blockchain: 
            print(policy) 
    else: 
        print(blockchain) 
    print('\n') 

def main():
    """
    The following is an example of querying blockchain, using the blockchain policy types that are in the added example(s) 
    The example is used by a client who's interested in knowing where their solar panels are located.
    :positional arguments:
        rest_conn             REST connection information
        master_node           TCP master information
    :optional arguments:
        -h, --help            show this help message and exit
        -a AUTH, --auth         AUTH      REST authentication information (default: None)
        -t TIMEOUT, --timeout   TIMEOUT   REST timeout period (default: 30)
    :params:
        policy:dict - new policy to be added into blockchain
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=str,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('-a', '--auth',        type=str, default=None, help='REST authentication information')
    parser.add_argument('-t', '--timeout',     type=int, default=30,   help='REST timeout period')
    args = parser.parse_args()

    # connect to AnyLog
    auth = ()
    if args.auth is not None: 
        auth = tuple(args.auth.split(','))
    anylog_conn = anylog_api.AnyLogConnect(conn=args.rest_conn, auth=auth, timeout=args.timeout)

    # Example 1 - blockchain get * 
    output = blockchain_cmd.blockchain_get(conn=anylog_conn, policy_type='*', where_conditions=[], exception=True)
    __format_print(output) 

    # Example 2 - blockchain get panel 
    output = blockchain_cmd.blockchain_get(conn=anylog_conn, policy_type='panel', where_conditions=[], exception=True)
    __format_print(output) 


    # Example 3 - blockchain get sensor where sensor_type=fic11 
    output = blockchain_cmd.blockchain_get(conn=anylog_conn, policy_type='sensor_type', where_conditions=['name="fic11"'], exception=True)
    sensor_type_id = output[0]['sensor_type']['id'] 
    output = blockchain_cmd.blockchain_get(conn=anylog_conn, policy_type='sensor', where_conditions=['sensor_type=%s' % sensor_type_id], exception=True)
    __format_print(output) 


if __name__ == '__main__':
    main()
