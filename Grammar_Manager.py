filename = 'questions.txt'

class Grammar_Nazi:
    def __init__(self, questions):
        self.questions = questions

def Generate_Grammar_Nazi():
    global Octavius_Grammar

    with open(filename) as f:
        questions = f.read().splitlines()
        for i in questions:
            i.lower()
            i.rstrip()
    Octavius_Grammar = Grammar_Nazi(questions)


def is_question(sentence):
    sentence.strip(" ")
    words = sentence.split()

    if words[0] in Octavius_Grammar.questions or words[0][-1] == '?':
        return True

    else:
        return False