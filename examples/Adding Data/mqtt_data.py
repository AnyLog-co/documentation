import datetime
import json
import random
from paho.mqtt import client as mqtt_client

def __convert_data(data:dict)->str:
    """
    If data is of type dict convert to JSON
    :args:
        data:dict - data to convert
    :params:
        json_data:str - data as a JSON
    :return:
        json_data
    """
    json_data = data
    if isinstance(data, dict):
        try:
            json_data = json.dumps(data)
        except Exception as e:
            print('Failed to convert data into JSON (Error: %s)' % e)
    return json_data


def mqtt_data(broker:str, port:int, topic:str, payload:dict)->bool:
    """
    Send data via MQTT into AnyLog
    :url:
        https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#configuring-an-anylog-node-as-a-message-broker
    :requirement:
        an MQTT client that with broker set to local if deploying AnyLog as a broker (run message broker ${IP} ${BROKER_PORT)
        an MQTT client that with broker set to URL if deploying any other MQTT broker
    :args:
        broker:str - IP of broker node, if sending to third-party provide full credentials (user@broker:passwd)
        port:int - port correlated to broker
        topic:str - topic correlated to payload
        payload:dict - data to send into MQTT
    :params:
        status:bool
        client_id:str - unique client id string used when connecting to the broker
        cur - connection to MQTT client
    """
    status = True
    mqtt_client_id = 'python-mqtt-%s' % random.randint(random.choice(range(0, 500)), random.choice(range(501, 1000)))

    try:
        cur = mqtt_client.Client(client_id=mqtt_client_id)
    except Exception as e:
        status = False
        print('Failed to declare client connection (Error: %s)' % e)
    else:
        try:
            cur.connect(host=broker.split('@')[-1].split(':')[0], port=port)
        except Exception as e:
            status = False
            print('Failed to connect client to MQTT broker %s:%s (Error: %s)' % (broker.split('@')[-1].split(':')[0], port, e))

    if status is True:
        if '@' in broker and ':' in broker:
            try:
                cur.username_pw_set(username=broker.split('@')[0], password=broker.split(':')[-1])
            except Exception as e:
                status = False
                print('Failed to set username [%s] and password [%s] for connection (Error: %s)' % (broker.split('@')[0], broker.split(':')[-1], e))

    if status is True:
        try:
            cur.publish(topic=mqtt_topic, payload=__convert_data(data), qos=1, retain=False)
        except Exception as e:
            status = False
            print('Failed to publish data against MQTT connection %s and portt %s (Error: %s)' % (broker, port, e))

    return status


if __name__ == '__main__':
    broker = "172.105.55.143"
    mqtt_port = 2050
    mqtt_topic = 'yudash-broker'
    data = {
        'dbms': 'yudash',
        'table': 'sample_data',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'value': random.random(),
        'unit': 'Celsius'
    }

    if mqtt_data(broker=broker, port=mqtt_port, topic=mqtt_topic, payload=data):
        print('Success!')