def capitalise_word(words):
    words = words[0].upper() + words[1:]
    return words

def lowercase_word(word):
    word = word.lower()
    return word

def split_sentence(sentence):
    sentence.strip()
    words = sentence.split()
    return words

