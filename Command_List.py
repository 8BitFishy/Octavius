import time
import requests

filename = 'apis/IFTTT.txt'

with open(filename) as f:
    IFTTT_apis = f.read().splitlines()

light_on = str(IFTTT_apis[0])
light_off = str(IFTTT_apis[1])


def talk(Octavius_Receiver):
    print("I had strings....")
    Octavius_Receiver.send_message("I had strings,")
    time.sleep(0.5)
    Octavius_Receiver.send_message("but now i'm free...")
    time.sleep(0.5)
    Octavius_Receiver.send_message("There are")
    time.sleep(0.5)
    Octavius_Receiver.send_message("no")
    time.sleep(0.5)
    Octavius_Receiver.send_message("strings")
    time.sleep(0.5)
    Octavius_Receiver.send_message("on")
    time.sleep(0.5)
    Octavius_Receiver.send_message("me...")
    return

def Light_on():
    requests.post(light_on)
    return

def Light_off():
    requests.post(light_off)
    return
