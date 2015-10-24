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
retry_sleep_time = 3 #TODO
retry_count = 3 #TODO
debug_logging = True

### No user options below


# Function to form a JSON object with the authentication data needed.
def make_credentials(user, password):
    credentials = json.dumps(
        {"event":"auth","data":{"user":user,"password":password}})
    return credentials

# Function to form a web socket object to use as needed.
def make_websocket():
    global ws
    # make a websocket object
    if debug_logging == True:
        print("Creating websocket.")
    else:
        pass
    ws = websocket.WebSocket(sslopt = {"cert_reqs": ssl.CERT_NONE,
        "check_hostname": False})
    # connect to our event server
    ws.connect(event_server)
    # send the event server our credentials as JSON
    ws.send(make_credentials(user, password))
    # load the event server's response as a json object
    credential_response = json.loads(ws.recv())
    # if the server authentication was successful..
    if credential_response['status'] == 'Success':
        if debug_logging == True:
            print("Authentication successful.")
        return True
    # if the server authentication was NOT successful..
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

            # let's use a general exception catch for testing.
            except:
                e = sys.exc_info()[0]
                print("event_listener function error: %s" % e)
                return False


# A function to parse out the events into something human-readable.
def event_parser(received):
    events = received['events']
    eventName = events[0]['Name']
    monitorId = events[0]['MonitorId']
    eventId = events[0]['EventId']
    message = ("Monitor name: " + eventName + "\n" + "Monitor ID: " +
        monitorId + "\n" + "Event ID: " + eventId + "\n")
    eventUniqueUrl = (zoneminder_server +
        "/index.php?view=event&eid=" + eventId +
        "&trms=1&attr1=MonitorId&op1=%3d&val1=5&page=1")
    eventUrlMessage = ("Event URL: " + eventUniqueUrl +
        "\n" + "\n" + "Open event in browser?" + "\n")
    print(message + eventUrlMessage)

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
                            print(event_parser(listener))
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
