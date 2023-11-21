import argparse
from classes import *
from functions import *

'''
  --freq N ARQUIVO
    Exibe o número de ocorrência das N palavras que mais aparecem em ARQUIVO, em
    ordem decrescente de ocorrência. *ta funcionando como n-1, se coloca 5 aparece 4
  --freq-word PALAVRA ARQUIVO
    Exibe o número de ocorrências de PALAVRA em ARQUIVO. *OK
  --search TERMO ARQUIVO [ARQUIVO ...]
    Exibe uma listagem dos ARQUIVOS mais relevantes encontrados pela busca por 
    TERMO. A listagem é apresentada em ordem descrescente de relevância. 
    TERMO pode conter mais de uma palavra. Neste caso, deve ser indicado entre 
    àspas.

  - `py indexer.py --freq <frequencia> arquivo`

	- `py indexer.py --freq-word <palavra> arquivo`

	- `py indexer.py --search <termo> arquivo`
'''

# Argumentos do Python
parser = argparse.ArgumentParser()
parser.add_argument("--freq", metavar = "freq")
parser.add_argument("--freq-word", metavar = "freqword")
parser.add_argument("--search", metavar = "search")
parser.add_argument("files", nargs="*")
args = parser.parse_args()

frequency = args.freq
word_frequency = args.freq_word
search_word = args.search
files = args.files

def indexer(frequency, word_frequency, search_word, files):
    '''
      Metódo "main" que verifica os argumentos e chama a função selecionada
    '''
    trie = Trie(files)
    if frequency is not None:
        freq(trie=trie, frequency=int(frequency) + 1) # Tive que adicionar + 1 pois estava estranho, se digitava 3 vinha 2 palavras
    elif word_frequency is not None:
        freq_word(trie=trie, word_frequency=word_frequency)
    elif search_word is not None:
        search(trie=trie, search_word=search_word)

indexer(frequency, word_frequency, search_word, files)
