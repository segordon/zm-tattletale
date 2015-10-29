#!/usr/bin/env python

__author__ = "Sam Gordon"
__email__ = "seg@well.com"

import json
import websocket
import ssl
import time
import sys
from tkinter import messagebox # dialog window option
import tkinter # dialog window option


### Put your credentials here!
user = "admin"
password = "admin"

### Put your server information here!
event_server = "wss://192.168.1.7:9000"
zoneminder_server = "https://192.168.1.7/zm" # no trailing slashes.

### Set some options!

alert_dialog_windows = False # Work In Progress.
alert_sounds = True
alert_sound_file = "alert.wav"
alert_taskbar_popups = True #TODO
alert_log_to_file = True
alert_sleep_time = 0 #TODO
retry_sleep_time = 3
retry_count = 3
debug_logging = False
zm_log_file_name = "zm_alert_log.txt"

### NO USER OPTIONS BELOW

# an attempt to handle optional dependencies and options better at load-time.
def optional_dependencies():
    if alert_sounds == True:
        global pyglet
        import pyglet
    if alert_dialog_windows == True:
        root = tkinter.Tk()
        root.withdraw()
    else:
        pass


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


def dialog_window(message, event_url_message):
    import webbrowser
    if debug_logging == True:
        print("Opening dialog window.")
    else:
        pass
    browser_result = messagebox.askquestion("Event",message + "\n" + "Open browser to event?")
    if browser_result == 'yes':
        webbrowser.open(event_url_message,2,True)
    else:
        pass


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


def play_alert_sound():
    if debug_logging == True:
        print("Playing alert_sound_file.")
    else:
        pass
    alert_sound = pyglet.media.load(alert_sound_file)
    alert_sound.play()
    time.sleep(.5)


def log_to_file(event_name, monitor_id, event_id, event_time):
    if debug_logging == True:
        print("Writing line to log.")
    else:
        pass
    with open(zm_log_file_name, "a") as event_log:
        event_log.write(event_time + " , " + "monitor_id: " + monitor_id +
            " , " + "event_id: " + event_id + " , " + "event_name: " +
            event_name + "\n")


# function to parse and print events in a human-readable manner.
def event_parser(received):
    events = received['events']
    for event in events:
        event_name = event['Name']
        monitor_id = event['MonitorId']
        event_id = event['EventId']
        event_time = time.strftime("%X %x")

        message = ("\n" + "Monitor name: " + event_name + "\n"
            + "Monitor ID: " + monitor_id + "\n" +
            "Event ID: " + event_id + "\n" + "Time processed: " +
            event_time + "\n" + "\n")

        event_unique_url = (zoneminder_server +
        "/index.php?view=event&eid=" + event_id +
        "&trms=1&attr1=MonitorId&op1=%3d&val1=5&page=1")
        event_url_message = (event_unique_url)

        print(message + event_url_message)

        # begin handling of optional alert types.
        try:
            if alert_sounds == True:
                play_alert_sound()
            if alert_log_to_file == True:
                log_to_file(event_name, monitor_id, event_id, event_time)
            if alert_dialog_windows == True:
                dialog_window(message, event_url_message)
            else:
                break

        except:
            e = sys.exc_info()[0]
            print("event_parser function error: %s" % e)
            return False


def main():
    optional_dependencies()
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



# TODO: Alert_Dialog_Windows ARE BLOCKING as of now. They will make for
# dishonest timestamps, because the dialog waits for user interaction on the
# main thread. This will be fixed one day, til then be aware of this
# limitation.

# TODO: get rid of websocket dependency and add taskbar alerts.

# TODO: event parser shouldn't be the event barker. Let's fix that
#       one day.

# TODO: add interface for telling zmeventserver which monitors to report on

# TODO: new zmeventserver seems to have broken this. will fix when time permits.
