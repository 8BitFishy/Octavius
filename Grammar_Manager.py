filename = 'vocab/questions.txt'

class Grammar_Nazi:
    def __init__(self, questions):
        self.questions = questions

    def is_question(self, sentence):
        sentence.strip(" ")
        words = sentence.split()

        if words[0] in self.questions or words[0][-1] == '?':
            return True

        else:
            return False



def Generate_Grammar_Nazi():

    with open(filename) as f:
        questions = f.read().splitlines()
        for i in questions:
            i.lower()
            i.rstrip()
    Octavius_Grammar = Grammar_Nazi(questions)
    return Octavius_Grammar

