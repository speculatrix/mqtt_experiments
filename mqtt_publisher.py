#!/usr/bin/env python3
''' program to publish to mqtt '''

import os
import socket
import time
import paho.mqtt.client as mqtt

BROKER = 'cc-vm19.home.mansfield.co.uk'
CLIENT_PREFIX = 'paulm'
TOPIC = 'paulm'
USER = 'paulm'
PASS = 'secret123'


#############################################################################
def on_connect(_mqttc, _userdata, _flags, result_code):
    ''' callback function when connection established '''

    print('Connected with result code %s' % (str(result_code),))


#############################################################################
def on_message(_mqttc, _obj, msg):
    ''' callback function for message received '''

    print('topic %s, qos %d, payload %s' % (msg.topic, msg.qos, msg.payload))


#############################################################################
def on_publish(_mqttc, _obj, mid):
    ''' callback function when publishing'''

    print('Published with result code %s' % (str(mid),))


#############################################################################
def main():
    ''' main entry point '''
    print('main entry point')

    # client name must be unique, this is a hack towards that end
    unique_client_name = '%s_%s_%d' % (CLIENT_PREFIX, socket.gethostname(), os.getpid())

    mqttc = mqtt.Client(unique_client_name)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish

    mqttc.username_pw_set(USER, PASS)
    mqttc.connect(BROKER)
    mqttc.publish(TOPIC, 'hello from %s' % (unique_client_name,))

    time.sleep(2)
    mqttc.disconnect()


#############################################################################

if __name__ == "__main__":
    main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
