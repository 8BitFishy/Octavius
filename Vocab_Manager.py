import Telegram_Manager

class WordList_Manager:
    def __init__(self, affirmativelist, greetings, negativelist):
        self.affirmativelist = affirmativelist
        self.greetings = greetings
        self.negativelist = negativelist



def Generate_Wordlists():
    Octavius_Vocab = WordList_Manager([],[],[])
    with open('affirmativelist.txt') as f:
        affirmativelist = f.read().splitlines()
        for i in affirmativelist:
            i.lower()
            i.rstrip()
    Octavius_Vocab.affirmativelist = affirmativelist


    with open('negativelist.txt') as f:
        negativelist = f.read().splitlines()
        for i in negativelist:
            i.lower()
            i.rstrip()
    Octavius_Vocab.negativelist = negativelist

    with open('greetings.txt') as f:
        greetings = f.read().splitlines()
        for i in greetings:
            i.lower()
            i.rstrip()
    Octavius_Vocab.greetings = greetings

    return Octavius_Vocab

def updateaffirmatives(Octavius_Vocab, Octavius_Receiver):
    Telegram_Manager.send_message('Please write affirmative to add to list')
    incomplete = True
    loops = 3
    while incomplete and loops > 0:
        loops -= 1
        # receive response
        Octavius_Receiver = Telegram_Manager.get_response(Octavius_Receiver)
        response = Octavius_Receiver.text
        if response not in Octavius_Vocab.affirmativelist:
            Octavius_Vocab.affirmativelist.append(response)
            print(Octavius_Vocab.affirmativelist)
            with open('affirmativelist.txt', 'w') as f:
                for i in Octavius_Vocab.affirmativelist:
                    f.write(i)
                    f.write("\n")
            Telegram_Manager.send_message(f"{response} added to affirmative list")
            incomplete = False

        else:
            Telegram_Manager.send_message('Already logged, repeat?')

    if loops == 0:
        Telegram_Manager.send_message("Timed out, exiting...")
    return Octavius_Vocab.affirmativelist

