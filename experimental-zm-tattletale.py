#!/usr/bin/env python

__author__ = "Sam Gordon"
__email__ = "seg@well.com"

import json
import websocket
import ssl
import time
import sys

### Put your credentials here!
user = "admin"
password = "admin"

### Put your server information here!
event_server = "wss://192.168.1.7:9000"
zoneminder_server = "https://192.168.1.7/zm/"

### Set some options!
alert_dialog_windows = True #TODO
alert_sounds = True #TODO
alert_taskbar_popups = True #TODO
alert_log_to_file = True #TODO
alert_sleep_time = 0 #TODO
retry_sleep_time = 3
retry_count = 3
debug_logging = False

### No user options below


# Function to form a JSON object with the authentication data needed.
def make_credentials(user, password):
    credentials = json.dumps(
        {"event":"auth","data":{"user":user,"password":password}})
    return credentials

# Function to form a web socket object to use as needed.
def make_websocket():
    # FIXME: global variables are hacky, but I like them :3
    global ws
    if debug_logging == True:
        print("Creating websocket.")
    else:
        pass
    ws = websocket.WebSocket(sslopt = {"cert_reqs": ssl.CERT_NONE})
    ws.connect(event_server)
    ws.send(make_credentials(user, password))
    credential_response = json.loads(ws.recv())
    if credential_response['status'] == 'Success':
        if debug_logging == True:
            print("Authentication successful.")
        return True
    else:
        print("credential_response: " + credential_response['status'])
        ws.close()
        return False


# A function to listen for output from our websocket.
def event_listener():
            try:
                if debug_logging == True:
                    print("...Listening...")
                else:
                    pass
                received = json.loads(ws.recv())
                return received
            # FIXME : general exception catches are hacky, too.
            except:
                e = sys.exc_info()[0]
                print("event_listener function error: %s" % e)
                return False


# function to parse and print events in a human-readable manner.
def event_parser(received):
    events = received['events']
    for event in events:
        event_name = event['Name']
        monitor_id = event['MonitorId']
        event_id = event['EventId']

        message = ("\n" + "Monitor name: " + event_name + "\n"
            + "Monitor ID: " + monitor_id + "\n" +
            "Event ID: " + event_id + "\n" + "Event time: " +
            time.strftime("%X %x") + "\n")

        event_unique_url = (zoneminder_server +
        "/index.php?view=event&eid=" + event_id +
        "&trms=1&attr1=MonitorId&op1=%3d&val1=5&page=1")
        event_url_message = ("\n" + "Event URL: " + event_unique_url)

        print(message + event_url_message)

def main():
    for i in range(0, retry_count):
        while True:
            try:
                time.sleep(retry_sleep_time)
                websocket = make_websocket()
                if websocket == True:
                    while True:
                        listener = event_listener()
                        if listener != False:
                            event_parser(listener)
                        if listener == False:
                            time.sleep(retry_sleep_time)
                            main()
                    else:
                        break
            except:
                e = sys.exc_info()[0]
                print("main function error: %s" % e)
                break

main()
