import time
import Telegram_Manager
import Grammar_Manager
import Vocab_Manager
import Interpret_Commands
import List_Manager
import Camera_Manager
import RF_Manager


def receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_Lists, Octavius_Grammar, Octavius_Camera_Manager, Octavius_RF_Manager):
    while True:
        text = Octavius_Receiver.get_response()
        if text != "":
            Interpret_Commands.commandhandler(text, Octavius_Vocab, Octavius_Lists, Octavius_Grammar, Octavius_Receiver, Octavius_Camera_Manager, Octavius_RF_Manager)

        time.sleep(0.5)


if __name__ == '__main__':
    print("Starting")
    
    Octavius_Lists = List_Manager.Generate_Lists()
    Octavius_Vocab = Vocab_Manager.Generate_Wordlists()
    Octavius_Grammar = Grammar_Manager.Generate_Grammar_Nazi()
    Octavius_Receiver = Telegram_Manager.generate_receiver()
    Octavius_Receiver.send_message("Online...")
    Octavius_Camera_Manager = Camera_Manager.Generate_Camera_Manager()
    Octavius_RF_Manager = RF_Manager.Generate_RF_Manager()
    
    receiver_loop(Octavius_Receiver, Octavius_Vocab, Octavius_Lists, Octavius_Grammar, Octavius_Camera_Manager, Octavius_RF_Manager)

    print('I am sleepy...')
