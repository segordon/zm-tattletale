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
zoneminder_api_server = "https://192.168.1.7/zm/api"

### Set some options!
alert_dialog_windows = "1"
alert_sounds = "1"
alert_taskbar_popups = "1"
alert_log_to_file = "1"
alert_sleep_time = "0"

### No user options below

# Form a JSON object with the authentication data to send later.
def make_credentials(user, password):
    credentials = json.dumps(
        {"event":"auth","data":{"user":user,"password":password}})
    return credentials

#ws = websocket.create_connection(
#    event_server,
#    sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})

ws = websocket.WebSocket(sslopt = {"cert_reqs": ssl.CERT_NONE,
    "check_hostname": False})
ws.connect(event_server)
print(ws.recv())
