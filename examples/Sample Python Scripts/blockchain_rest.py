import json
import requests


def post(conn:str, master_node:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
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