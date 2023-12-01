class WordList_Manager:
    def __init__(self, affirmativelist, greetings, negativelist, gratitude):
        self.affirmativelist = affirmativelist
        self.greetings = greetings
        self.negativelist = negativelist
        self.gratitude = gratitude

    def updateaffirmatives(self, Octavius_Receiver):
        Octavius_Receiver.send_message('Please write affirmative to add to list')
        incomplete = True
        loops = 3
        while incomplete and loops > 0:
            loops -= 1
            # receive response
            response = Octavius_Receiver.get_response()
            if response not in self.affirmativelist:
                self.affirmativelist.append(response)
                print(self.affirmativelist)
                with open('vocab/affirmativelist.txt', 'w') as f:
                    for i in self.affirmativelist:
                        f.write(i)
                        f.write("\n")
                Octavius_Receiver.send_message(f"{response} added to affirmative list")
                incomplete = False

            else:
                Octavius_Receiver.send_message('Already logged, repeat?')

        if loops == 0:
            Octavius_Receiver.send_message("Timed out, exiting...")
        return self.affirmativelist


def Generate_Wordlists():
    Octavius_Vocab = WordList_Manager([],[],[], [])
    with open('vocab/affirmativelist.txt') as f:
        affirmativelist = f.read().splitlines()
        for i in range(len(affirmativelist)):
            affirmativelist[i] = affirmativelist[i].lower()
            affirmativelist[i].rstrip()
    Octavius_Vocab.affirmativelist = affirmativelist


    with open('vocab/negativelist.txt') as f:
        negativelist = f.read().splitlines()
        for i in negativelist:
            i = i.lower()
            i.rstrip()
    Octavius_Vocab.negativelist = negativelist

    with open('vocab/greetings.txt') as f:
        greetings = f.read().splitlines()
        for i in range(len(greetings)):
            greetings[i] = greetings[i].lower()
            greetings[i].rstrip()
    Octavius_Vocab.greetings = greetings

    with open('vocab/gratitude.txt') as f:
        gratitude = f.read().splitlines()
        for i in range(len(gratitude)):
            gratitude[i] = gratitude[i].lower()
            gratitude[i].rstrip()
    Octavius_Vocab.gratitude = gratitude





    return Octavius_Vocab
