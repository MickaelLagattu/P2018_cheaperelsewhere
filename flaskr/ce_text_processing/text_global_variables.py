import os
word_list_name = "words_list_all.csv"
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
w2vfile = os.path.join(path, "wiki.fr.vec")

### parameters for for word2vec
nmax = 50000 # maximum number of words useds for word2vec

### parameters for Bag of Vectors
idf = False # to use idf or not
sentences_file = "" # path to file that contains text from different announces

### parameters for text preprocessing
keep_num = False # False : delete numerical caracters, True : keep numerical caracters
keep_ponc = False # True : keep ponctuation , False : not
split_by = " " # caracter to split the sentence by
to_lower = True # True : transfrom all characters to lowercase, False : keep the characters as they are
##
