import pandas
import matplotlib.pyplot as plt
import requests

def __get_data(conn:str='23.239.12.151:32349', db_name:str="litsanleandro",
               sql_cmd="select increments(minute, 1, timestamp),  min(timestamp) as ts, count(*) as row_count from ping_sensor where timestamp >= NOW() - 10 minutes")->list:
    """
    Simple GET request for getting data - notice results are in JSON format without stats
    :args:
        conn:str - REST connection information
        db_name:str - logical database to query against
        sql_cmd:str - SQL command
    :params:
        results:list - results from query
        headers:dict - REST header information
        r:requests.GET - GET request
    """
    results = []
    headers = {
        "command": f"sql {db_name} format=json and stat=false {sql_cmd}",
        "User-Agent": "AnyLog/1.23",
        "destination": "network"
    }

    try:
        r = requests.get(url=f"http://{conn}", headers=headers)
    except Exception as error:
        print(f"Failed to execute GET against {conn}  for query - {sql_cmd} (Error: {error})")
    else:
        if int(r.status_code) != 200:
            print(f"Failed to execute GET against {conn} for query - {sql_cmd} (Network Error: {r.status_code})")
        else:
            try:
                results = r.json()['Query']
            except:
                results = r.text

    return results

def main():
    results = __get_data()
    df = pandas.DataFrame(results)
    df['ts'] = pandas.to_datetime(df['Time [dd.mm.yyyy hh:mm:ss.ms]'], format="%d.%m.%Y %H:%M:%S.%f")
    print(df)


if __name__ == '__main__':
    main()
