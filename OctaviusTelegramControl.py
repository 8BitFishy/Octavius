import time
import random
import Telegram_Manager
import Arduino_Manager
import Grammar_Manager
import Format_Manager
import Vocab_Manager



class List_Manager:
    def __init__(self, devicelist):
        self.devicelist = devicelist


def talk():
    print("I had strings....")
    Telegram_Manager.send_message("I had strings,")
    time.sleep(0.5)
    Telegram_Manager.send_message("but now i'm free...")
    time.sleep(0.5)
    Telegram_Manager.send_message("There are")
    time.sleep(0.5)
    Telegram_Manager.send_message("no")
    time.sleep(0.5)
    Telegram_Manager.send_message("strings")
    time.sleep(0.5)
    Telegram_Manager.send_message("on")
    time.sleep(0.5)
    Telegram_Manager.send_message("me...")


def updatedevicelist(Octavius_List_Manager, Octavius_Receiver):
    Telegram_Manager.send_message(f'Current devices:')
    for device in Octavius_List_Manager.devicelist:
        Telegram_Manager.send_message(device)

    Telegram_Manager.send_message('Which device would you like to replace?')

    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        Octavius_Receiver = Telegram_Manager.get_response(Octavius_Receiver)
        response1 = Octavius_Receiver.text
        Telegram_Manager.send_message(response1)
        if response1 in Octavius_List_Manager.devicelist:
            incomplete = False
        else:
            Telegram_Manager.send_message('Device not in list')

    Telegram_Manager.send_message('and the name for the new device is?')

    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        Octavius_Receiver = Telegram_Manager.get_response(Octavius_Receiver)
        response2 = Octavius_Receiver.text
        Telegram_Manager.send_message(response2)
        if response2 in Octavius_List_Manager.devicelist:
            Telegram_Manager.send_message('Device already listed, please choose another name')
            continue
        Telegram_Manager.send_message('Are you sure?')
        Octavius_Receiver = Telegram_Manager.get_response(Octavius_Receiver)
        response3 = Octavius_Receiver.text
        print(response3)
        if response3 in Octavius_Vocab.affirmativelist:
            incomplete = False
        else:
            Telegram_Manager.send_message('Please repeat device name')

    if loops == 0:
        Telegram_Manager.send_message("Timed out, exiting...")


    with open('devicelist.txt', 'w') as f:
        for i in range(len(Octavius_List_Manager.devicelist)):
            if Octavius_List_Manager.devicelist[i] != response1:
                f.write(str(Octavius_List_Manager.devicelist[i]))
                f.write("\n")
            else:
                f.write(str(response2))
                f.write("\n")
                Octavius_List_Manager.devicelist[i] = response2

    Telegram_Manager.send_message('New device list:')

    for device in Octavius_List_Manager.devicelist:
        Telegram_Manager.send_message(device)
    return Octavius_List_Manager


def commandhandler(text, Octavius_Vocab, Octavius_List_Manager):
    global updatingdevicelist
    inputcommand = Format_Manager.lowercase_word(text)
    if Grammar_Manager.is_question(inputcommand):
        Telegram_Manager.send_message("I don't know how to answer questions yet")
        print("Is question")
    command = Format_Manager.split_sentence(inputcommand)
    print(f'Received command: {inputcommand}')
    Telegram_Manager.send_message(f'Received command: {inputcommand}')

    if updatingdevicelist == 0:


        if len(command) == 1:
            action = inputcommand
            if action == 'talk':
                talk()


            elif action in Octavius_Vocab.greetings:
                word = random.randint(0, len(Octavius_Vocab.greetings)-1)
                Telegram_Manager.send_message(f'{Octavius_Vocab.greetings[word]}')

            else:
                Telegram_Manager.send_message("Command not recognised, please repeat")

        elif len(command) == 2:
            target = command[0]
            action = command[1]
            if target in Octavius_List_Manager.devicelist or target == 'all':
                Arduino_Manager.generateserialcommand(Octavius_List_Manager.devicelist, target, action)

            elif 'update' in inputcommand:

                if 'device' in inputcommand:
                    Telegram_Manager.send_message(f"Updating device list")
                    Octavius_List_Manager = updatedevicelist(Octavius_List_Manager, Octavius_Receiver)
                    updatingdevicelist = 0
                    return

                elif 'affirmative' in inputcommand:
                    Octavius_Vocab = Vocab_Manager.updateaffirmatives(Octavius_Vocab, Octavius_Receiver)

            else:
                if action == 'on' or action == 'off':
                    Telegram_Manager.send_message(f"Device not currently listed, would you like to update device list?")
                    updatingdevicelist = 1
                else:
                    Telegram_Manager.send_message(f"Command not recognised, please repeat")

        else:
            Telegram_Manager.send_message(f'Command not recognised, please repeat')

    else:
        print("Updating device list")
        if inputcommand in Octavius_Vocab.affirmativelist:
            updatingdevicelist = 0
            Octavius_List_Manager = updatedevicelist(Octavius_List_Manager, Octavius_Receiver)
        else:
            updatingdevicelist = 0
            Telegram_Manager.send_message(f'Acknowledged, please repeat original command')




def receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_List_Manager):
    while True:
        Octavius_Receiver = Telegram_Manager.get_response(Octavius_Receiver)
        if Octavius_Receiver.text != "":
            commandhandler(Octavius_Receiver.text, Octavius_Vocab, Octavius_List_Manager)
            if 'hi' in Octavius_Receiver.text:
                print("hi in text")
                Telegram_Manager.send_message("HELLO")
        time.sleep(0.5)

if __name__ == '__main__':

    updatingdevicelist = 0
    previousmessage = ''

    with open('devicelist.txt') as f:
        devicelist = f.read().splitlines()

    Octavius_Vocab = Vocab_Manager.Generate_Wordlists()

    Octavius_Receiver = Telegram_Manager.Message_Receiver("", None)
    Octavius_List_Manager = List_Manager(devicelist)
    print(f"initial ID - {Octavius_Receiver.last_update_id}")
    receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_List_Manager)
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    #ser.flush()

    print('I am sleepy...')
