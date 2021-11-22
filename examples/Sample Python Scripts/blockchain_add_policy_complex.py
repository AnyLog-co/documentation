import argparse
import json
import time

import import_packages

POLICIES = {
    'manufacturer': { # Manufacturer of device
        'name': 'Bosch',
        'Address': 'Robert-Bosch-Platz 1 70839 Gerlingen',
        'url': 'https://www.bosch-sensortec.com/',
        'contact': 'https://www.bosch-sensortec.com/about-us/contact/',
        'phone': '+4971140040990'

    },
    'owner': {  # Owner of device (usually the customer or company generating the data)
        'name': 'Precision Engineering Inc',
        'Address': '400 St Louis St, Mobile, Alabama 36602, US',
        'url': 'http://www.precision-eng.com/',
        'contact': '+12514438844'
    },
    'device': {  # device information
        'name': 'fic',
        'location': 'HQ Office',
        'owner': '',
        'manufacturer': '',
        'serial_number': 'SFb6HfZz'
    },
    # for AnyLog GUI a user can (optionally) add a layer for each type of sensor or go directly to sensor(s) policies
    # in this case we're showing having a middle layer between the device(s) and sensor(s)
    'sensor_type': {
        'name': 'fic11',
        'device': '',
        'serial_number': 'SFb6HfZz-fSAoEAvt'
    },
    # Sensor Information
    'sensor 1': {
        'sensor': {  # layer 3
            'name': 'fic11',
            'sensor_type': '',
            'serial_number': 'SFb6HfZz-fSAoEAvt-fic11'
        }
    },
    'sensor 2':{
        'sensor': {  # layer 3
            'name': 'fic11_pv',
            'sensor_type': '',
            'serial_number': 'SFb6HfZz-fSAoEAvt-fic11-pv'

        }
    },
    'sensor 3': {
        'sensor': {  # layer 3
            'name': 'fic11_mv',
            'sensor_type': '',
            'serial_number': 'SFb6HfZz-fSAoEAvt-fic11-mv'
        }
    }
}


def main():
    """
    The following is an example of adding a set of policies where each policy requires the ID of the previous policy.
    The example is used by a client who's interested in a hierarchical view of their sensors both in terms of
        manufacturer and customer.
    Note - in this case each sensor would corresponds to a different table in the database.
    :positional arguments:
        rest_conn             REST connection information
        master_node           TCP master information
    :optional arguments:
        -h, --help            show this help message and exit
        -a AUTH, --auth         AUTH      REST authentication information (default: None)
        -t TIMEOUT, --timeout   TIMEOUT   REST timeout period (default: 30)
    :params:
        anylog_conn:anylog_api.AnyLogConnect - connection to AnyLog
        policy_id:dict - new policy to be added into blockchain
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=str,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('master_node',     type=str,   default='127.0.0.1:2048', help='TCP master information')
    parser.add_argument('-a', '--auth',    type=str , default=None, help='REST authentication information')
    parser.add_argument('-t', '--timeout', type=int,   default=30,   help='REST timeout period')
    args = parser.parse_args()

    policy_id = {}

    # connect to AnyLog
    auth = ()
    if args.auth is not None: 
        auth = tuple(args.auth.split(','))
    anylog_conn = anylog_api.AnyLogConnect(conn=args.rest_conn, auth=auth, timeout=args.timeout)

    for key in POLICIES:
        # Generate policy based on POLICY
        policy = {key: POLICIES[key]}
        if key in ['sensor 1', 'sensor 2', 'sensor 3']:
            policy = POLICIES[key]
        if key == 'device':
            policy[key]['owner'] = policy_id['owner']
            policy[key]['manufacturer'] = policy_id['manufacturer']
        elif key == 'sensor_type':
            policy[key]['device'] = policy_id['device']
        elif 'sensor' in key:
            policy['sensor']['sensor_type'] = policy_id['sensor_type']

        # declare policy
        policy_id[key] = policy_cmd.declare_policy(conn=anylog_conn, master_node=args.master_node,
                                                   new_policy=policy, exception=True)

        # validate policy was added
        if policy_id[key] is None:
            print('Failed to add policy of type: %s' % key)
            exit(1)


if __name__ == '__main__':
    main()
