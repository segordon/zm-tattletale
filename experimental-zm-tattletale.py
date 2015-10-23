#!/usr/bin/env python

__author__ = "Sam Gordon"
__email__ = "seg@well.com"

import json
import websocket
import ssl

### Put your credentials here!
user = "admin"
password = "admin"

### Put your server information here!
event_server = "wss://192.168.1.7:9000"
zoneminder_api_server = "https://192.168.1.7/zm/api" #TODO

### Set some options!
alert_dialog_windows = "1" #TODO
alert_sounds = "1" #TODO
alert_taskbar_popups = "1" #TODO
alert_log_to_file = "1" #TODO
alert_sleep_time = "0" #TODO

### No user options below

# Function to form a JSON object with the authentication data needed.
def make_credentials(user, password):
    credentials = json.dumps(
        {"event":"auth","data":{"user":user,"password":password}})
    return credentials

# Function to form a web socket object to use as needed.
def make_websocket():
    global ws
    ws = websocket.WebSocket(sslopt = {"cert_reqs": ssl.CERT_NONE,
        "check_hostname": False})
    ws.connect(event_server)
    ws.send(make_credentials(user, password))

# A function to listen for output from our websocket.
def event_listener():
        while True:
            received = json.loads(ws.recv())
            print(received)

make_websocket()
event_listener()
