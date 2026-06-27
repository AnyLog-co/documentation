"""
The following provides an example of adding policies to the (AnyLog) blockchain via REST.
The new policies are associated with data coming in via one of the sample data generator options; where we're showing
both the data coming in, and where that data is coming from.
"""

import argparse
import json
import re
import requests

LOCATIONS = {
    'Los Angeles, CA': '33.8121, -117.91899',
    'San Francisco, CA': '37.786163522, -122.404498382',
    'Seattle, WA': '47.620182, -122.34933',
    'Philadelphia, PN': '39.949566, -75.15026',
    'Arlington, VA': '38.870983,  -77.05598',
    'Washington DC': '38.89773, -77.03653',
    'New York City, NY': '40.758595, -73.98447',
    'Orlando, FL': '28.37128, -81.51216',
    'Houston, TX': '29.97980499267578, -95.56627655029297',
    'Las Vegas': '36.1147, -115.1728'
}

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
    # pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    for conn in conns.split(","):
        if not pattern1.match(conn) and not pattern2.match(conn):
            raise argparse.ArgumentTypeError(f'Invalid connection format: {conn}. Supported formats: 127.0.0.1:32049 or user:passwd@127.0.0.1:32049')

    return conns


def __publish_policy(conn:str, ledger_conn:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    Publish policy into a network via REST POST
    :args:
        conn:str - REST connection information
        ledger_conn:str - master node or blockchain ledger connection infromation
        policy_id:dict - policy to publish
        auth:tuple - rest authentication
        timeout:str - REST timeout
    """
    status = True

    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    if isinstance(policy, dict):  # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy = "<new_policy=%s>" % policy

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=raw_policy, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to POST policy against %s (Error; %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
            status = False

    return status

def main():
    """
    The following is an example of adding a single policy to the AnyLog blockchain.
    :positional arguments:
        rest_conn             REST connection information
        ledger_conn           TCP master information
    :optional arguments:
        -h, --help            show this help message and exit
        -a AUTH, --auth         AUTH      REST authentication information (default: None)
        -t TIMEOUT, --timeout   TIMEOUT   REST timeout period (default: 30)
    :params:
        policy:dict - new policy to be added into blockchain
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=__validate_conn_pattern,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('ledger_conn',     type=__validate_conn_pattern,   default='127.0.0.1:2048', help='TCP master information')
    parser.add_argument('-a', '--auth',    type=str, default=None, help='REST authentication information')
    parser.add_argument('-t', '--timeout', type=int,   default=30,   help='REST timeout period')
    args = parser.parse_args()

    # connect to AnyLog
    auth = ()
    if args.auth is not None: 
        auth = tuple(args.auth.split(','))

    # personalized hierarchy
    policy = {'panel': {
        'name': None,
        'city': None,
        'loc': None,
        'owner': 'AFG'
    }}

    for location in LOCATIONS:
        policy['panel']['name'] = f'Panel {str(int(list(LOCATIONS).index(location)) + 1)}'
        policy['panel']['city'] = location
        policy['panel']['loc'] = LOCATIONS[location]
        status = __publish_policy(conn=args.rest_conn, ledger_conn=args.ledger_conn, policy=policy, auth=auth,
                                  timeout=args.timeout)

        if status is True:
            print('Policy for %s added to blockchain' % policy['panel']['city'])
        else:
            print('Failed to add policy to blockchain')


if __name__ == '__main__':
    main()
