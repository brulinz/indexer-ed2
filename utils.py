import re

def sanitize_line(line):
    '''
      Remove caracteres especiais e palavras com menos de 3 caracteres de uma linha.    
    '''
    splitted = line.replace("-", " ")
    return [word for word in splitted.split(" ") if len(word) > 2]

def sanitize_word(word):
    '''
      Remove caracteres especiais de uma palavra e a converte para minúsculas.
    '''
    reg = re.compile("[^a-zA-Z ]")
    return reg.sub("", word).lower()
