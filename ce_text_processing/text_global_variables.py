word_list_name = "words_list_all.csv"
w2vfile = "ce_text_processing/wiki.fr.vec"

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
