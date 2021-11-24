import json
import requests


def blockchain_get_by_id(conn:str, policy_id:str, auth:tuple=(), timeout:int=30)->list:
    """
    GET blockchain policy by ID
    :args:
        conn:str - REST connection info
        policy_id:str - policy UUID to query by
        auth:tuple - authentication info [ex. (${USERNAME}, ${PASSWORD}) ]
        timeout:int - REST timeout length
    :params:
        policy:dict - extracted policy
        headers:dict - REST header information for GET
    :print:
        error if any
    :return:
        policy if fails {}
    """
    policy = {}
    headers = {
        'command': 'blockchain get * where id=%s' % policy_id,
        'User-Agent': 'AnyLog/1.23'
    }

    try:
        r = requests.get(url='http://%s' % conn, headers=headers, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to execute GET against %s (Error: %s)' % (conn, e))
        return policy
    else:
        if int(r.status_code) != 200:
            print('Failed to execute GET against %s (Network Error: %s)' % (conn, r.status_code))
            return policy

    try:
        policy = r.json()
    except Exception as e:
        print('Failed to extract results from GET request (Error: %s)' % e)
        return policy

    # Since no 2 policies can have the same ID there's no need to check if len(policy) > 1
    if len(policy) == 0:
        print('Unable to locate policy with ID: %s' % policy_id)
        policy = {}
    else:
        policy = policy[0]
    return policy


def prepare_policy(conn:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    POST `prepare policy` command against an AnyLog instance
    :args:
        conn:str - REST connection information for machine requesting to POST data
        policy:dict - policy to prepare for blockchain
        auth:tuple - authentication info [ex. (${USERNAME}, ${PASSWORD}) ]
        timeout:int - REST timeout length
    :params:
        status:bool - status
        policy_id:dict - new policy ID  generated in prepare process
        headers:dict - REST header information for POST request
        raw_policy:str - policy to prepare
    :print:
        error if any
    :return:
        status
    """
    status = True
    header = {
        'command': 'blockchain prepare policy !new_policy',
        'User-Agent': 'AnyLog/1.23'
    }

    if isinstance(policy, dict): # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy="<new_policy=%s>" % policy

    # execute prepare policy
    try:
        r = requests.post(url='http://%s' % conn, headers=header, data=raw_policy, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to POST policy against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
            status = False

    return status


def get_policy_id(conn:str, auth:tuple=(), timeout:int=30):
    """
    Extract policy ID from dictionary (based on prepare)
    :process:
        1. Execute `get dictionary`
        2. extract dictionary content
        3. extract policy ID
    :args:
        conn:str - REST connection information
        auth:tuple - authentication info [ex. (${USERNAME}, ${PASSWORD}) ]
        timeout:int - REST timeout length
    :params:
        content:str - content from GET request
        policy_id:str - extracted policy ID
        headers:dict - REST header information
    :print:
        error if any
    :return:
        if an error occurs || id isn't extracted returns None
        if all works (new) policy ID
    """
    policy_id = None
    content = None
    headers = {
        'command': 'get dictionary',
        'User-Agent': 'AnyLog/1.23'
    }

    try:
        r = requests.get(url='http://%s' % conn, headers=headers, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to execute GET against %s (Error: %s)' % (conn, e))
        return None
    else:
        if int(r.status_code) != 200:
            print('Failed to execute GET against %s (Network Error: %s)' % (conn, e))
            return None

    try:
        content = r.text
    except Exception as e:
        print('Failed to extract content from GET request (Error: %s)' % e)

    if 'new_policy' in content:
        try:
            policy = json.loads(content.split('new_policy')[-1].split('\n')[0].split(':', 1)[-1].rstrip().lstrip())
        except Exception as e:
            print('Failed to extract full prepare policy (Error: %s)' % e)
        else:
            policy_id = policy[list(policy.keys())[0]]['id']

    return policy_id


def post_policy(conn:str, master_node:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    :args:
        conn:str - REST connection information for machine requesting to POST data
        master_node:str - TCP connection information for master node to store the data in
        policy:dict - policy to add to blockchain
        auth:tuple - authentication info [ex. (${USERNAME}, ${PASSWORD}) ]
        timeout:int - REST timeout length
    :params:
        status:bool
        headers:dict - REST header information
        raw_policy:str - policy to post to blockchain as string
    :print:
        error if any
    :return:
        True for success, False if fails
    """
    status = True

    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': master_node
    }

    if isinstance(policy, dict):  # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy="<new_policy=%s>" % policy

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


def drop_policy(conn:str, master_node:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    Drop policy from blockchain (database)
    :args:
        conn:str - REST connection information for machine requesting to POST data
        master_node:str - TCP connection information for master node to store the data in
        policy:dict - policy to add to blockchain
        auth:tuple - authentication info [ex. (${USERNAME}, ${PASSWORD}) ]
        timeout:int - REST timeout length
    :params:
        status:bool
        headers:dict - REST header information
        raw_policy:str - policy to post to blockchain as string
    :print:
        error if any
    :return:
        True for success, False if fails
    """
    status = True
    headers = {
        'command': 'blockchain drop policy !rm_policy',
        'destination': master_node,
        'User-Agent': 'AnyLog/1.23'
    }

    if isinstance(policy, dict):  # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy="<rm_policy=%s>" % policy

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=raw_policy, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to execute POST against %s (Error: %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to execute POST against %s (Network Error: %s)' % (conn, r.status_code))
            status = False

    return status

