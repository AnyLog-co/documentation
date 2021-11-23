import argparse
import json

import import_packages
import_packages.import_dirs()

import anylog_api
import policy_cmd

LOCATIONS = [
    'Los Angeles, CA',
    'San Francisco, CA',
    'Seattle, WA',
    'Philadelphia, PN',
    'Arlington, VA',
    'Washington DC',
    'New York City, NY',
    'Orlando, FL',
    'Houston, TX',
    'Las Vegas'
]


def main():
    """
    The following is an example of removing a policy from the AnyLog blockchain this process can only be used with
        master node.
    The example is based on he policies that are created in simple_deploy_generic_policy
    :positional arguments:
        rest_conn             REST connection information
        master_node           TCP master information
    :optional arguments:
        -h, --help            show this help message and exit
        -a AUTH, --auth         AUTH      REST authentication information (default: None)
        -t TIMEOUT, --timeout   TIMEOUT   REST timeout period (default: 30)
    :params:

    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=str,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('master_node',     type=str,   default='127.0.0.1:2048', help='TCP master information')
    parser.add_argument('-a', '--auth',    type=tuple, default=None, help='REST authentication information')
    parser.add_argument('-t', '--timeout', type=int,   default=30,   help='REST timeout period')
    args = parser.parse_args()

    # connect to AnyLog
    auth = ()
    if args.auth is not None: 
        auth = tuple(args.auth.split(','))
    anylog_conn = anylog_api.AnyLogConnect(conn=args.rest_conn, auth=auth, timeout=args.timeout)


    # drop policy
    for city in LOCATIONS:
        status = policy_cmd.drop_policy(conn=anylog_conn, master_node=args.master_node, policy_type='panel',
                                       query_params={'city': city}, exception=True)
        if status is True:
            print('Policy for %s was dropped' % city)
        else:
            print('Policy fro %s was not dropped' % city)


if __name__ == '__main__':
    main()
    
