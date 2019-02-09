from .ce_text_processing import BoV, Word2Vec, PreprocessSentence
from . import text_global_variables as tgv
from .read_txt import read_sentences_file

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
    text1 = "Dans une copropriété calme et sécurisée à deux pas des transports et commerces, nous vous proposons un trois pièces de 68m² il comporte une entrée, un grand séjour, deux chambres, une cuisine, et un WC indépendant, une cave et un parking couvert complètent également ce bien."
    text2 = "Appartement 3 pièces 68 m²plus parking cave , double vitrage équipé, (7e étage) vue dégagée sur espace vert avec ascenseur.Une cave et un parking.Situé à 2 min du métro (ligne 7) et du tramway (T3) station Porte de Choisy et à 5 min de la station Maison Blanche (future ligne 14).Bus, commerces et restaurants à proximité.Appartement comprenant une entrée avec placard aménagé, 2 chambres, un séjour de 22 m², une salle de bain, un wc séparé et une cuisine séparée.le chauffage collectif, et surveillance gardien 24h/24.Plus de photos sur demande.Si vous êtes intéressé, appeler ou laisser un message."
    text3 = "MURAT MOLITOR. Votre agence Century 21 Via conseil vous propose dans un bel immeuble pierre de taille 1930, avec gardien, au 5ème étage ascenseur, beau 3 pièces comprenant salon, salle à manger, chambre (2 possibles), cuisine, salle d'eau, wc séparé, rangement, cave. Traversant, bien distribué, bonne hauteur sous plafond, charme de l'ancien, lumineux. Proche des transports et commerces."
    print(TextScoring.get_score(text1,text2))
    print(TextScoring.get_score(text1,text3))
    print(TextScoring.get_score(text2,text3))
