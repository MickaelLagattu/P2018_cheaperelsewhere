french_pos_tagger = r'C:\Users\Hamza\Centrale3A\OSY_2018_2019\DEV_LOG\stanford-postagger-full-2018-10-16\stanford-postagger-full-2018-10-16\models\french.tagger'
st_pos_tagger = r'C:\Users\Hamza\Centrale3A\OSY_2018_2019\DEV_LOG\stanford-postagger-full-2018-10-16\stanford-postagger-full-2018-10-16\stanford-postagger.jar'
java_path = "C://Program Files (x86)//Java//jre1.8.0_191//bin//java.exe"
word_list_name = "words_list_all.csv"
w2vfile = "wiki.fr.vec"

### parameters for for word2vec
nmax = 50000 # maximum number of words useds for word2vec

### parameters for Bag of Vectors
idf = False # to use idf or not
sentences_file = "" # path to file that contains text from different announces

### parameters for text preprocessing
keep_num = False # False : delete numerical caracters, True : keep numerical caracters
keep_ponc = False # True : keep ponctuation , False : not
split_by = " " # caracter to split the sentence by
to_lower = True # True : transfrom all characters to lowercase, Fale : keep the characters as they are
##
