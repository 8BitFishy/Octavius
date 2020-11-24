import time
import Telegram_Manager
import Grammar_Manager
import Vocab_Manager
import Interpret_Commands

class List_Manager:
    def __init__(self, devicelist, protectedwords):
        self.devicelist = devicelist
        self.protectedwords = protectedwords



def receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_List_Manager, Octavius_Grammar):
    while True:
        text = Octavius_Receiver.get_response()
        if text != "":
            Interpret_Commands.commandhandler(text, Octavius_Vocab, Octavius_List_Manager, Octavius_Grammar, Octavius_Receiver)

        time.sleep(0.5)


if __name__ == '__main__':
    print("Starting")
    updatingdevicelist = 0
    previousmessage = ''

    with open('lists/devicelist.txt') as f:
        devicelist = f.read().splitlines()
        for i in range(len(devicelist)):
            devicelist[i] = devicelist[i].lower()
            devicelist[i].rstrip()

    with open('lists/protectedwords.txt') as f:
        protectedwords = f.read().splitlines()
        for i in range(len(protectedwords)):
            protectedwords[i] = protectedwords[i].lower()
            protectedwords[i].rstrip()


    Octavius_Vocab = Vocab_Manager.Generate_Wordlists()
    Octavius_Grammar = Grammar_Manager.Generate_Grammar_Nazi()
    Octavius_Receiver = Telegram_Manager.generate_receiver()
    Octavius_List_Manager = List_Manager(devicelist, protectedwords)
    Octavius_Receiver.send_message("I am awake...")
    receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_List_Manager, Octavius_Grammar)
    # ser = serial.Serial('/dev/ttyACM0', 9600)
    # ser.flush()

    print('I am sleepy...')
