import time

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
