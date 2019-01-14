import os
from global_variables import java_path, french_pos_tagger, st_pos_tagger,word_list_name
# from nltk.tag.stanford import StanfordPOSTagger
from nltk import sent_tokenize, word_tokenize, RegexpParser
from nltk.metrics.distance import jaccard_distance

from scipy.spatial.distance import cosine
import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd



import re
# os.environ['JAVAHOME'] = java_path
# stanford_pos_tagger = StanfordPOSTagger(french_pos_tagger,st_pos_tagger)
# stop_words = ["le","la","de","à","a","des"]
# tf_idf = TfidfVectorizer(stop_words=stop_words)

words_df = pd.read_csv(word_list_name)
words_list = words_df.word.values.tolist()


def _get_sentences(text: str) -> list:
    """ takes a text and returns a list of the sentences"""
    if not isinstance(text, str):
        raise ValueError(" text must be a string")
    sentences = sent_tokenize(text)
    return sentences

def _tokenize_sentence(sentence:str) -> list:
    """ takes a sentence and return a list of words"""
    if not isinstance(sentence,str):
        raise ValueError(" sentence must be a string ")
    sentence = re.sub('\[[^]]*\]–', '', sentence)
    sentence_list = word_tokenize(sentence)
    sentence_list = [word.lower() for word in sentence_list]
    return sentence_list

def _pos_tag(sentence_list: list) -> list:
    """ takes  a list of words and returns a list of couples : the first element of the i-th couple
     contains the i-th word of the input, the second element is its corresonding POS tag"""
    sent = stanford_pos_tagger.tag(sentence_list)
    return sent

def get_taggers(text:str):
    taggers = []
    sentences = _get_sentences(text)
    for sent in sentences :
        sent_list = _tokenize_sentence(sent)
        sent_tag = _pos_tag(sent_list)
        taggers.append(sent_tag)
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        cp = RegexpParser(pattern)
        try:
            cs = cp.parse(sent_tag)
            print(cs)
        except:
            continue
    return taggers

def print_pos_tagger(pos_tag_list):
    for el in pos_tag_list :
        for ps in el:
            try :
                print(ps)
            except:
                continue

def get_tf_idf_representation(text: str):
    tf_idf.fit_transform(text)
    # TO DO

def get_bag_of_words(text_list:list , french_words_list : list)-> list :
    n = len(french_words_list)
    bag_of_words = [0 for _ in range(n)]
    for word in text_list :
        try :
            bag_of_words[french_words_list.index(word)] += 1
        except :
            continue
    return bag_of_words

def cosine_similarity(bag_of_words_1 : np.array, bag_of_words_2 :np.array ) -> float :
    return np.dot(bag_of_words_1,bag_of_words_2)/(np.linalg.norm(bag_of_words_1)*np.linalg.norm(bag_of_words_2))


if __name__ == '__main__' :

    text1 = "Appartement 3 pièces 69 m²plus parking cave , double vitrage équipé, (7e étage) vue dégagée sur espace vert avec ascenseur.Une cave et un parking. Situé à 2 min du métro (ligne 7) et du tramway (T3) station Porte de Choisy et à 5 min de la station Maison Blanche (future ligne 14). Bus, commerces et restaurants à proximité. Appartement comprenant une entrée avec placard aménagé, 2 chambres, un séjour de 22 m², une salle de bain, un wc séparé et une cuisine séparée.le chauffage collectif, et surveillance gardien 24h/24. Plus de hotos sur demande. Si vous êtes intéressé, appeler ou laisser un message."

    text2 = "Dans une copropriété calme et sécurisée à deux pas des transports et commerces, nous vous proposons un trois pièces de 68m² il comporte une entrée, un grand séjour, deux chambres, une cuisine, et un WC indépendant, une cave et un parking couvert complètent également ce bien."

    text3 = "Appartement 2 pièces de 61 m² dans immeuble Béryl situé 40 avenue d'Italie 75013 Description de l'immeuble: Résidence de bon standing de 243 lots Gestionnaire : NEXITY Gardiennage 24h/24 - 7jours/7 Accès sécurisé à l'immeuble, soit par l'avenue d'Italie, soit par le centre commercial Italie 2 Description du bien : 1) Appartement : Niveau : 23 ème étage orienté à l'ouest (belle vue panoramique) accessible par 2 ascenseurs Porte blindée Superficie diagnostic Carrez : 61m2 Diagnostics techniques disponibles, dont : - GES : D - DPE : D Charges de 4650€ annuels (comprenant : le chauffage CPCU, l'eau chaude/froide par compteurs individuels, le gardiennage, les ascenseurs, le local à vélo) Taxe foncière 2017 : 917 € 2) Cave (3 m² avec porte blindée) en sous-sol 3) Parking en sous-sol (accès via le centre commercial Italie 2) Environnement : Accès au parc privé avec jardin d'enfants de l'Ilot Vandrezanne Accès direct au Centre Commercial Italie2 (130 magasins dont Carrefour, Printemps, Fnac, Boulanger, Bricorama, etc… ; Pharmacie, Restaurants, etc…) Station Place d'Italie (3 lignes de métro : 5, 6 et 7 et 6 lignes de bus : 27, 47, 57, 64, 67 et 83) Prix net vendeur. Agences s'abstenir Merci d'appeler entre 19 et 22h Tolbiac Place d'Italie Corvisart"

    text_list1 = _tokenize_sentence(text1)
    bow1 = get_bag_of_words(text_list1, words_list)
    bow1 = np.array(bow1)

    text_list2 = _tokenize_sentence(text2)
    bow2 = get_bag_of_words(text_list2, words_list)
    bow2 = np.array(bow2)
    print("cosine : 2 vs 1")
    print(cosine_similarity(bow2,bow1))

    text_list3 = _tokenize_sentence(text3)
    bow3 = get_bag_of_words(text_list3, words_list)
    bow3 = np.array(bow3)
    print("cosine : 2 vs 3")
    print(cosine_similarity(bow2,bow3))

    print("cosine : 1 vs 3")
    print(cosine_similarity(bow1,bow3))

    print(" jaccard : 1 vs 2")
    print(jaccard_distance(set(text_list1),set(text_list2)))

    print(" jaccard : 1 vs 3")
    print(jaccard_distance(set(text_list1),set(text_list3)))

    # text_list = text1.split(" ")
    # tf_idf = TfidfVectorizer()
    # tf_idf.fit(text_list)
    # print(tf_idf.transform([text1]).toarray())
