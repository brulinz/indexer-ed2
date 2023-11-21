from utils import sanitize_word
# define algumas classes relacionadas a uma estrutura de dados de árvore Trie,
# bem como uma tabela de frequência para armazenar a contagem de palavras em diferentes arquivos


class File:
    '''
        Representa um arquivo
    '''
    def __init__(self, filename: str, hashed_name: int):
        self.name = filename # nome do arquivo
        self.word_count = 0 # contagem de palavras
        self.hashed_name = str(hashed_name) #nome do arquivo hash
        self.next_file = None #prox arquivo na lista
        
class Word:
    '''
        representa uma palavra na estrutura Trie, mantendo informações sobre a
        contagem de arquivos em que a palavra aparece, a contagem total de
        ocorrências e a frequência global da palavra
    '''
    def __init__(self, trie_file_count: int):
        self.word = ""
        self.files = {} # dicionário de arquivos (onde a palavra aparece)
        self.file_count = 0 # quantas vezes aparece
        self.overall_frequency = 0 # frequencia global
        self.idf = 0 #inverso da frequencia

    def __repr__(self):
        return "<{}:{}>".format(self.word, self.overall_frequency)

    def __str__(self) -> str:
        return "<Word: {}>".format(self.word) # mostra a palavra em si

    def insert_file_name(self, file: File):
      '''
        Atualiza os atributos relacionados à contagem de arquivos e frequência global da palavra

        1 - verifica se o nome hash do arquivo já está no dicionário self.files.
        2 - Se estiver, incrementa o contador; caso contrário, adiciona uma entrada ao dicionário.
        3 - Atualiza self.file_count e self.overall_frequency
      '''
      if file.hashed_name in self.files.keys():
          self.files[file.hashed_name] += 1
      else:
          self.file_count += 1
          self.files[file.hashed_name] = 1

      self.overall_frequency+=1

    def add_instance(self, file: File):
        '''
            Chama insert_file_name para adicionar uma instância de arquivo à palavra
        '''
        self.insert_file_name(file)

class Trie:
    '''
        Representa uma Trie, uma estrutura de dados de árvore usada para armazenar um conjunto dinâmico
        ou uma coleção associativa onde as chaves são sequências, geralmente strings.
        Complexidade O(W*L) - Onde W é o número de palavras, e L é o tamanho médio das palavras
    '''
    def __init__(self, files_names):
        self.root = {}  # inicializando raiz
        self.files = self.wrap_files(files_names) # lista de arquivos
        self.file_count = len(files_names) # armazena o total de arquivos

    def insert_word(self, word, file: File):
        '''
          Insere uma palavra na Trie junto com uma referência ao arquivo em que a palavra foi encontrada
        '''
  
        current_node = self.root # inicializado como nó da raiz da Trie
        word = sanitize_word(word) # normaliza a palavra

        # Para cada letra na palavra, um novo nó é criado no caminho se a letra ainda não estiver presente
        # Se a palavra já existe na Trie, o objeto da palavra existente é recuperado;
        # Caso contrário, um novo objeto da palavra é criado e associado ao nó atual
        for letter in word:
            if letter not in current_node:
                current_node[letter] = {}
            current_node = current_node[letter]

        word_obj = current_node.get("word", None)
        if not word_obj:
            current_node["word"] = Word(self.file_count)
            current_node["word"].word = word
            word_obj = current_node.get("word", None)

        # É chamado para atualizar a contagem de arquivos e frequência global da palavra,
        # É a contagem de palavras no arquivo também é incrementada
        word_obj.add_instance(file)
        file.word_count += 1
        return word_obj

    def word_exists(self, word) -> Word:
        '''
          Método verifica se uma palavra existe na Trie.
          A lógica é semelhante à inserção, percorrendo a Trie letra por letra e retornando o objeto
          da palavra se a palavra estiver presente, ou None (null) se não estiver.        
        '''

        current_node = self.root

        word = sanitize_word(word)

        for letter in word:
            if letter not in current_node:
                return None
            current_node = current_node[letter]
            word_obj = current_node.get("word", None)

        return word_obj
    
    def wrap_files(self, files_names):
        '''
            Recebe uma lista de nomes de arquivos e retorna uma lista de objetos de arquivo (File)
        '''

        # cada objeto da classe File é associado a um nome de arquivo específico
        # e mantém a informação do índice desse arquivo na lista original
        table_size = len(files_names)
        wrapped = [None] * table_size

        for i in range(len(files_names)):
            wrapped[i] = File(files_names[i], i)

        return wrapped
     
class FrequencyTable:
    '''
        Tabela de frequência para armazenar e classificar/ordenar palavras com base em suas frequências
        mantém a tabela atualizada sempre que inserida uma palavra
    '''
    def __init__(self, table_size):
        self.table_size = table_size
        self.table = [None] * self.table_size # armazena as palavras
        self.word_count = 0 # número de palavras na tabela

    def print(self):
        '''
          Imprime a tabela, contendo a palavra e a frequência de vezes que foi encontrada
        '''
        for i in range(self.table_size - 1, 0, -1):
            if self.table[i] is not None:
                print("{} - Frequencia: {}".format(self.table[i].word, self.table[i].overall_frequency))

    def search_word(self, word):
        '''
          Busca uma palavra na tabela
        '''
        for i in range(self.table_size):
            if self.table[i] == word:
                return i
        return None

    def insert_ordered(self, word, starting_index = 0):
        '''
          Insere uma palavra ordenadamente\n
          Itera sobre a tabela para ajustar a ordem das palavras com base em suas frequências globais (de forma decrescente)      
        '''
        self.table[starting_index] = word
        for i in range(starting_index, self.table_size - 1):
            if self.table[i + 1] is None:
                self.table[i + 1] = word
                self.table[i] = None
            elif self.table[i + 1].overall_frequency < self.table[i].overall_frequency:
                aux = self.table[i + 1]
                self.table[i + 1] = word
                self.table[i] = aux

    def insert_word(self, word):
        '''
            Insere uma palavra na tabela. se ela já existe, então a palavra é inserida ordenadamente na posição onde ela já está na tabela\n
            Se é nova, insere ordenada
        '''
        potential_duplicate = self.search_word(word)
        if potential_duplicate is not None:
            self.insert_ordered(word, potential_duplicate)
        else:
            self.insert_ordered(word)