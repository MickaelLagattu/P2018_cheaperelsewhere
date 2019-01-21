from ce_text_processing import BoV, Word2Vec, PreprocessSentence
import text_global_variables as tgv
from read_txt import read_sentences_file

class TextScoring():
    print("-- creating word2vec")
    w2v = Word2Vec(tgv.w2vfile,tgv.nmax)
    print("-- word2vec created")
    print("-- creating Bag of vectors")
    bov = BoV(w2v=w2v)
    print("-- Bag of vectors created")
    print("-- creating preprocessing")
    preprocess = PreprocessSentence(to_lower = tgv.to_lower,
                keep_num = tgv.keep_num,
                keep_ponc = tgv.keep_ponc,
                split_by = tgv.split_by)

    print("-- preprocessing created")
    if tgv.idf :
        print("-- uploading sentences")
        list_of_sentences = read_sentences_file(tgv.sentences_file)
        print("-- sentences uploaded")
        print("-- preprocessing sentences")
        sentences = [preprocess.preprocess_sentence(sent) for sent in list_of_sentences]
        print("-- building idf")
        bov.build_idf(sentences)
        print("-- idf built")

    @staticmethod
    def get_score(text1: str, text2: str)-> float:
        sent1 = TextScoring.preprocess.preprocess_sentence(text1)
        sent2 = TextScoring.preprocess.preprocess_sentence(text2)
        return TextScoring.bov.score(sent1, sent2)

if __name__=="__main__":
    text1 = "Je n'arrive pas me connecter au serveur de données"
    text2 = "Il arrive as ne pas se connecter au choses aléatoires des données"
    print(TextScoring.get_score(text1,text2))
