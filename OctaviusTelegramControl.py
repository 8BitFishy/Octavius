#import serial
import time
import json
import requests
import time
import urllib
import random

filename = 'telegramID.txt'

with open(filename) as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



class Message_Receiver:
    def __init__(self, text, last_update_id):
        self.text = text
        self.last_update_id = last_update_id


class List_Manager:
    def __init__(self, devicelist, affirmativelist, greetings, negativelist):
        self.devicelist = devicelist
        self.affirmativelist = affirmativelist
        self.greetings = greetings
        self.negativelist = negativelist

def talk():
    print("I had strings....")
    send_message("I had strings,")
    time.sleep(0.5)
    send_message("but now i'm free...")
    time.sleep(0.5)
    send_message("There are")
    time.sleep(0.5)
    send_message("no")
    time.sleep(0.5)
    send_message("strings")
    time.sleep(0.5)
    send_message("on")
    time.sleep(0.5)
    send_message("me...")

def updateaffirmatives(Octavius_List_Manager):
    send_message('Please write affirmative to add to list')
    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        # receive response
        response = 'yes'
        send_message(response)
        if response not in Octavius_List_Manager.affirmativelist:
            Octavius_List_Manager.affirmativelist.append(response)
            with open('affirmativelist.txt', 'w') as f:
                for i in Octavius_List_Manager.affirmativelist:
                    f.write(response)
                    f.write("\n")
            send_message(f"{response} added to affirmative list")
            incomplete = False

        else:
            send_message('Already logged, repeat?')

    if loops == 0:
        send_message("Timed out, exiting...")
    return Octavius_List_Manager.affirmativelist

def updatedevicelist(Octavius_List_Manager, Octavius_Receiver):
    send_message(f'Current devices:')
    for device in Octavius_List_Manager.devicelist:
        send_message(device)

    send_message('Which device would you like to replace?')

    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        Octavius_Receiver = get_response(Octavius_Receiver)
        response1 = Octavius_Receiver.text
        send_message(response1)
        if response1 in Octavius_List_Manager.devicelist:
            incomplete = False
        else:
            send_message('Device not in list')

    send_message('and the name for the new device is?')

    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        Octavius_Receiver = get_response(Octavius_Receiver)
        response2 = Octavius_Receiver.text
        send_message(response2)
        if response2 in Octavius_List_Manager.devicelist:
            send_message('Device already listed, please choose another name')
            continue
        send_message('Are you sure?')
        Octavius_Receiver = get_response(Octavius_Receiver)
        response3 = Octavius_Receiver.text
        for yes in Octavius_List_Manager.affirmativelist:
            print(yes)
        print(response3)
        if response3 in Octavius_List_Manager.affirmativelist:
            incomplete = False
        else:
            send_message('Please repeat device name')

    if loops == 0:
        send_message("Timed out, exiting...")


    with open('devicelist.txt', 'w') as f:
        for i in range(len(Octavius_List_Manager.devicelist)):
            if Octavius_List_Manager.devicelist[i] != response1:
                f.write(str(Octavius_List_Manager.devicelist[i]))
                f.write("\n")
            else:
                f.write(str(response2))
                f.write("\n")
                Octavius_List_Manager.devicelist[i] = response2

    send_message('New device list:')

    for device in Octavius_List_Manager.devicelist:
        send_message(device)

    return Octavius_List_Manager

def commandhandler(text, Octavius_List_Manager):
    global updatingdevicelist
    inputcommand = text.lower()
    command = inputcommand.split(' ')
    print(f'Received command: {inputcommand}')
    send_message(f'Received command: {inputcommand}')
    if updatingdevicelist == 0:
        if len(command) == 1:
            action = inputcommand
            if action == 'talk':
                talk()


            elif action in greetings:
                word = random.randint(0, len(greetings)-1)
                send_message(f'{greetings[word]}')


            else:
                send_message("Command not recognised, please repeat")


        elif len(command) == 2:
            target = command[0]
            action = command[1]
            if target in Octavius_List_Manager.devicelist or target == 'all':
                generateserialcommand(Octavius_List_Manager.devicelist, target, action)

            elif 'update' in inputcommand:

                if 'device' in inputcommand:
                    send_message(f"Updating device list")
                    Octavius_List_Manager = updatedevicelist(Octavius_List_Manager, Octavius_Receiver)
                    return

                elif 'affirmative' in inputcommand:
                    Octavius_List_Manager = updateaffirmatives(Octavius_List_Manager)



            else:
                if action == 'on' or action == 'off':
                    send_message(f"Device not currently listed, would you like to update device list?")
                    updatingdevicelist = 1
                else:
                    send_message(f"Command not recognised, please repeat")


        else:
            send_message(f'Command not recognised, please repeat')


    else:
        print("Updating device list")
        if inputcommand in Octavius_List_Manager.affirmativelist:
            updatingdevicelist = 0
            Octavius_List_Manager = updatedevicelist(Octavius_List_Manager, Octavius_Receiver)
        else:
            updatingdevicelist = 0
            send_message(f'Acknowledged, please repeat original command')


#HANDLING SERIAL COMMANDS
def generateserialcommand(devicelist, target, action):

    if target == 'all':
        for device in devicelist:
            command = f"{device} {action}\n"
            command = command.encode('UTF-8')
            sendcommand(command)
    else:
        command = f"{target} {action}\n"
        command = command.encode('UTF-8')
        sendcommand(command)
        print(f"Turning {target} {action}")

    return

def sendcommand(command):
    print("writing serial command")
    #ser.write(command)
    print(command)
    time.sleep(1)
    print("returning from send command")
    return

#HANDLING TELEGRAM MESSAGING

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_response(Octavius_Receiver):
    print("Entering get response")
    updates = get_updates(Octavius_Receiver.last_update_id)
    print(f"Update ID = {Octavius_Receiver.last_update_id}")
    if len(updates["result"]) > 0:
        print("Update found")
        Octavius_Receiver.last_update_id = get_last_update_id(updates) + 1
        print(f"Update ID = {Octavius_Receiver.last_update_id}")
        Octavius_Receiver.text = updates["result"][0]["message"]["text"]
        print(f'Received update - {updates["result"][0]["message"]["text"]}')
    else:
        Octavius_Receiver.text = ''
    print(f"Leaving get response with text: {Octavius_Receiver.text}")
    return Octavius_Receiver

def receiver_loop(Octavius_Receiver, Octavius_List_Manager):
    while True:
        Octavius_Receiver = get_response(Octavius_Receiver)
        if Octavius_Receiver.text != "":
            commandhandler(Octavius_Receiver.text, Octavius_List_Manager)
            if 'hi' in Octavius_Receiver.text:
                print("hi in text")
                send_message("HELLO")
        time.sleep(0.5)

if __name__ == '__main__':

    updatingdevicelist = 0
    previousmessage = ''

    with open('devicelist.txt') as f:
        devicelist = f.read().splitlines()

    with open('affirmativelist.txt') as f:
        affirmativelist = f.read().splitlines()

    with open('negativelist.txt') as f:
        negativelist = f.read().splitlines()

    with open('greetings.txt') as f:
        greetings = f.read().splitlines()

    Octavius_Receiver = Message_Receiver("", None)
    Octavius_List_Manager = List_Manager(devicelist, affirmativelist, greetings, negativelist)
    print(f"initial ID - {Octavius_Receiver.last_update_id}")
    receiver_loop(Octavius_Receiver, Octavius_List_Manager)
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    #ser.flush()

    print('I am sleepy...')
