import datetime
import json
import random
from paho.mqtt import client as mqtt_client


def mqtt_data(conn:str, auth:tuple, topic:str, payload:str):
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
            cur.connect(host=conn.split(":")[0], port=int(conn.split(':')[-1]))
        except Exception as e:
            status = False
            print('Failed to connect client to MQTT broker %s (Error: %s)' % (conn, e))

    if status is True and auth != ():
        try:
            cur.username_pw_set(username=auth[0], password=auth[1])
        except Exception as e:
            status = False
            print('Failed to set username [%s] and password [%s] for connection (Error: %s)' % (auth[0], auth[1], e))

    if status is True:
        try:
            cur.publish(topic=topic, payload=payload, qos=1, retain=False)
        except Exception as e:
            status = False
            print('Failed to publish data against MQTT connection %s (Error: %s)' % (conn, e))

