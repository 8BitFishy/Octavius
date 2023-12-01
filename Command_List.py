import time
import requests
#import Arduino_Manager

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


def Ceiling_Light(action, Octavius_Receiver):
     #send command to IFTTT api to turn on ceiling light
    if 'on' in action:
        requests.post(light_on)
        Octavius_Receiver.send_message("Turning ceiling light on")
    #send command to IFTTT api to turn off ceiling light
    else:
        requests.post(light_off)
        Octavius_Receiver.send_message("Turning ceiling light off")

    return


def All_Lights(action, Octavius_Lists, Octavius_Receiver):
    #if 'on', send command to arduino to activate anything containing 'light' or 'lamp' in the name
    if 'on' in action:
        for device in Octavius_Lists.devicelist:
            if 'light' in device or 'lamp' in device:
                print("Needs fixing")
                #Arduino_Manager.generateserialcommand(Octavius_Lists.devicelist, device, action)
        #send command to IFTTT api to turn ceiling light on
        Ceiling_Light('on', Octavius_Receiver)
        Octavius_Receiver.send_message("Turning lights on")
    #otherwise do same for off
    else:
        for device in Octavius_Lists.devicelist:
            if 'light' in device or 'lamp' in device:
                print("needs fixing")
                #Arduino_Manager.generateserialcommand(Octavius_Lists.devicelist, device, action)
        Ceiling_Light('off', Octavius_Receiver)
        Octavius_Receiver.send_message("Turning lights off")
    return