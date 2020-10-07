#!/usr/bin/env python3
''' example program which sets up async keyboard input and sends
    the key strokes to mqtt '''

import os
import select
import signal
import socket
import sys
import termios
import time
import tty

from threading import Event, Thread

import paho.mqtt.client as mqtt

BROKER = 'cc-vm19.home.mansfield.co.uk'
CLIENT_PREFIX = 'paulm'
TOPIC = 'paulm'
USER = 'paulm'
PASS = 'secret123'


##########################################################################################
def sigint_handler(_signal_number, _frame):
    ''' called when signal 2 or CTRL-C hits process, this triggers an orderly shutdown '''

    global QUIT_FLAG
    global EVENT
    print('\nCTRL-C QUIT')
    QUIT_FLAG = True
    EVENT.set()


##########################################################################################
def keyboard_listen_thread(event):
    '''keyboard listening thread, sets raw input and uses sockets to
       get single key strokes without waiting, triggering an event '''

    global QUIT_FLAG
    global KEY_STROKE

    # set term to raw, so doesn't wait for return
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    # loop waiting on keyboard or quit
    while not QUIT_FLAG:
        # we need a timeout just so's we occasionally check QUIT_FLAG
        readable_sockets, _o, _e = select.select([sys.stdin], [], [], 0.2)
        if readable_sockets:
            KEY_STROKE = sys.stdin.read(1)
            event.set()

    # set term back to cooked before shutting down
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


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

    global QUIT_FLAG
    global DBG_LEVEL
    global KEY_STROKE

    print('main entry point')

    # if hostname is unique, client name will be too
    unique_client_name = '%s_%s_%d' % (CLIENT_PREFIX, socket.gethostname(), os.getpid())

    mqttc = mqtt.Client(unique_client_name)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish

    mqttc.username_pw_set(USER, PASS)
    mqttc.connect(BROKER)

    signal.signal(signal.SIGINT, sigint_handler)

    threads = []
    threads.append(Thread(target=keyboard_listen_thread, args=(EVENT, )))
    threads[-1].start()

    print('press keys, or ctrl-c to quit')
    while not QUIT_FLAG:
        EVENT.wait() # Blocks until the flag becomes true.
        if KEY_STROKE != '':
            print('key_stroke %s' % (KEY_STROKE, ))
            mqttc.publish(TOPIC, 'key press %s' % (KEY_STROKE,))

        # reset states/flags
        KEY_STROKE = ''
        EVENT.clear()

    #shut down nicely
    for thread in threads:
        thread.join()

    time.sleep(2)
    mqttc.disconnect()


#############################################################################

if __name__ == "__main__":
    # nasty hacky globals, pretend you don't see these
    DBG_LEVEL = 0
    KEY_STROKE = ''
    QUIT_FLAG = False
    EVENT = Event()

    main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
