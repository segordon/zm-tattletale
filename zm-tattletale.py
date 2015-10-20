

import websocket
import ssl
import json
import ctypes
import webbrowser
#import _thread
#import time

# change these things
user = "admin"
password = "admin"
server = "wss://192.168.1.7:9000" # the zmeventserver uses wss:// !
server_zm = "https://192.168.1.7/zm" # no trailing slashes, this script isn't too bright.
enable_irritating_dialog_windows = "1" # windows only for now. windows in windows, get it?
enable_irritating_sounds = "1" # not yet implemented
enable_irritating_taskbar_pops = "1" # not yet implemented

# you should probably leave the following stuff alone.
credentials = json.dumps({"event":"auth","data":{"user":user,"password":password}})

# let's make a web socket
ws = websocket.create_connection(
    server,
    sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False})

# let's make those irritating dialog windows.
# FIXME: windows only.
messageBox = ctypes.windll.user32.MessageBoxW

def main():
    # I am me.
    print("\n" + "Sending auth...")
    ws.send(credentials)
    print("Receiving auth reply...")
    result = json.loads(ws.recv())

    # You are you.
    if result['status'] == 'Success':
        print(result['status'] + "\n" + "\n" + "Starting to listen for events..")
        event_listener()
        
    # Except when you aren't.
    else:
        print("They say you ain't who you said you are, kid. " + result['reason'])
        ws.close()
        if enable_irritating_dialog_windows == "1":
            messageBox(0, "They say you ain't who you said you are, kid. ", result['reason'], 0x40 | 0x0)
        else:
            pass

# "The opposite of talking isn't listening. The opposite of talking is waiting." 
def event_listener():
    try:
        while True:
            received = json.loads(ws.recv())
            events = received['events']
            eventName = events[0]['Name']
            monitorId = events[0]['MonitorId']
            eventId = events[0]['EventId']

            # god, what a mess.
            message = "Monitor name: " + eventName + "\n" + "Monitor ID: " + monitorId + "\n" + "Event ID: " + eventId + "\n"
            eventUniqueUrl = server_zm + "/index.php?view=event&eid=" + eventId + "&trms=1&attr1=MonitorId&op1=%3d&val1=5&page=1"
            eventUrlMessage = "Event URL: " + eventUniqueUrl + "\n" + "\n" + "Open event in browser?" + "\n"

            # print that mess
            print(message + eventUrlMessage)

            # if enabled, make an obnoxious dialog window
            if enable_irritating_dialog_windows == "1":
                messageBody = message + "\n" + eventUrlMessage
                dialogReturn = messageBox(0, messageBody, eventName, 0x40 | 0x4 )
                if dialogReturn == 6:
                    webbrowser.open_new_tab(eventUniqueUrl)
                elif dialogReturn == 7:
                    print("User cancelled event preview" + "\n")
            else:
                pass
    except KeyboardInterrupt:
        pass

main()
