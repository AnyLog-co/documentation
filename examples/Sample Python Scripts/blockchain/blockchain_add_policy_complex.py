import argparse
import blockchain_rest as blockchain

POLICIES = {
    'manufacturer': { # Manufacturer of device
        'name': 'Bosch',
        'Address': 'Robert-Bosch-Platz 1 70839 Gerlingen',
        'url': 'https://www.bosch-sensortec.com/',
        'contact': 'https://www.bosch-sensortec.com/about-us/contact/',
        'phone': '+4971140040990'

    },
    'owner': {  # Owner of device (usually the customer or company generating the data)
        'name': 'New Engineering',
        'Address': '400 St Louis St, Mobile, Nevada 36602, US',
        'url': 'http://www.new-engineering.com/',
        'contact': '+12515336844'
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
    Note - If the code is unable to generate a policy ID, the program stops
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
    :steps:
        1. create a dictionary of the desired policy
        2. POST policy to local node to extract ID
        3. GET policy ID from local node
        4. POST policy to blockchain
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

        if blockchain.prepare_policy(conn=args.rest_conn, policy=policy, auth=args.auth, timeout=args.timeout):
            policy_id[key] = blockchain.get_policy_id(conn=args.rest_conn, auth=args.auth, timeout=args.timeout)
            if policy_id[key] is None:
                print('Failed to add policy of type: %s' % key)
                exit(1)
            elif not blockchain.post(conn=args.rest_conn, master_node=args.master_node, policy=policy, auth=auth,
                                     timeout=args.timeout):
                print('Failed to add policy of type %s' % key)
            else:
                print('Successfully posted policy of type %s' % key)





if __name__ == '__main__':
    main()
