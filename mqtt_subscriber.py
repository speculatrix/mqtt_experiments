#!/usr/bin/env python3
''' program to subscribe to mqtt and report messages
    Released under GPL v2 or later by Paul Mansfield
    (c) 2020 paul/at/mansfield.co.uk
'''

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
def on_connect(mqttc, _userdata, _flags, result_code):
    ''' callback function when connection established '''

    print('Connected with result code %s' % (str(result_code),))
    mqttc.subscribe(TOPIC, 0)


#############################################################################
def on_message(_mqttc, _obj, msg):
    ''' callback function for message received '''

    print('topic %s, qos %d, payload %s' % (msg.topic, msg.qos, msg.payload))


#############################################################################
def main():
    ''' main entry point '''

    print('main entry point')

    # if hostname is unique, client name will be too
    unique_client_name = '%s_%s_%d' % (CLIENT_PREFIX, socket.gethostname(), os.getpid())
    mqttc = mqtt.Client(unique_client_name)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.username_pw_set(USER, PASS)
    mqttc.connect(BROKER)

    mqttc.loop_forever()
    #mqttc.loop_start()

    time.sleep(1)
    #mqttc.loop_stop()
    mqttc.disconnect()


#############################################################################

if __name__ == "__main__":
    main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
