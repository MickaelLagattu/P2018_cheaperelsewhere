__version__ = 1.0
__author__      = "Cheaper Elsewhere team"
__copyright__   = "Copyright 2019, CS-CE"


import io
import numpy as np
import re

class Word2Vec:
    """
    Class to get words' representation
    """
    def __init__(self, fname, nmax=5000):
        self.load_wordvec(fname, nmax)
        self.word2id = {i:list(self.word2vec.keys()).index(i) for i in self.word2vec.keys()}
        self.id2word = {v: k for k, v in self.word2id.items()}
        self.embeddings = np.array(self.word2vec.values())
        print(len(self.id2word.keys()))


    def load_wordvec(self, fname, nmax):
        """
        load a word2vec module from .vec file
        Parameters
        -----------
        fname : str
            Path for the file .vec (contains words' embeddings)
        nmax : int
            number of maximal desired words
        """
        self.word2vec = {}
        with io.open(fname, encoding='utf-8') as f:
            next(f)
            for i, line in enumerate(f):
                word, vec = line.split(' ', 1)
                self.word2vec[word] = np.fromstring(vec, sep=' ')
                if i == (nmax - 1):
                    break
        print('Loaded %s pretrained word vectors' % (len(self.word2vec)))

    def most_similar(self, w, K=5):
        """
        Parameters
        -----------
        w : str or array
            the desired word if it's a string or its vectorial representation
        K (optional) : int
            the number of desired similar words

        Returns
        -----------
        list of k similar words for the given word w

        """
        sorted_scores = []
        for wi in self.word2vec.keys() :
          sorted_scores = sorted_scores  + [ self.score(w, wi) ]

        sorted_indices = np.argsort(sorted_scores)
        reversed_sorted_indices = sorted_indices [::-1]
        top_indices = reversed_sorted_indices[0:K+1]
        return [self.id2word[i] for i in top_indices]

    def score(self, w1, w2):
        """
        give a score between 0 and 1 for a 2 given words (1 : very similar, 0: not similar)
        Parameters
        -----------
        w1 : str or array
        w2 : str or array

        Returns
        -----------
        cosine similarity between the 2 given words
        """
        if type(w1)== str :
            emb1 = self.word2vec[w1]
        else :
            emb1 = w1
        emb2 = self.word2vec[w2]
        similarity_score = 0.5 + 0.5*(np.dot(emb1,emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
        return similarity_score

class PreprocessSentence():
    """
    Class for sentence preprocessing
    attributes
    ---------------
    to_lower (optional) : bool, default : True
        True : transform all words to lower case, False: keep their original form

    keep_num (optional) : bool, default : False
        True : keep the numerical characters in the sentence, False: delete all numerical characters from the sentence

    keep_ponc (optional) : bool, default : False
        True : keep all the ponctuation in the sentence, False : delete all the ponctuation characters from the sentence

    split_by (optional) : str, default : " "
        used character to split the sentence into list of words
    """
    def __init__(self,to_lower = True, keep_num = False,keep_ponc = False, split_by = " "): # add some params
        self._to_lower = to_lower
        self._keep_num = keep_num
        self._split_by = split_by
        self._keep_ponc = keep_ponc

    def is_keep_num(self)->bool:
        return self._keep_num

    def get_split_by(self)->str:
        return self._split_by

    def is_to_lower(self)->bool:
        return self._to_lower

    def is_keep_ponc(self)->bool:
        return self._keep_ponc

    def set_keep_num(self,value: bool):
        self._keep_num = value

    def set_split_by(self,value: str):
        self._split_by = value

    def set_to_lower(self,value: bool):
        self._to_lower = value

    def set_keep_ponc(self,value: bool):
        self._keep_ponc = value

    keep_num = property(is_keep_num, set_keep_num )
    split_by = property(get_split_by, set_split_by )
    to_lower = property(is_to_lower, set_to_lower )
    keep_ponc = property(is_keep_ponc, set_keep_ponc )


    def preprocess_sentence(self,sentence:str)-> list:
        """
        parameters
        -----------
        sentence : str
            the sentence to be preprocessed

        Returns
        -------
            list of words after preprocessing
        """
        preprocess_sentence = sentence.strip()
        if self.to_lower :
            preprocess_sentence = preprocess_sentence.lower()
        if not self.keep_num :
            preprocess_sentence = re.sub("\d+", self.split_by, preprocess_sentence)
        if not self.keep_ponc :
            preprocess_sentence = re.sub(r'[^\w\s]',self.split_by,preprocess_sentence)
        preprocess_sentence = re.sub(' +', ' ', preprocess_sentence)
        return [x for x in preprocess_sentence.split(self.split_by) if x != ""]

class BoV():
    """
    Class for sentence representation
    attributes
    ---------------
    w2v : Word2Vec
        a word2vec instance (see Word2Vec class)
    """
    def __init__(self, w2v):
        self._w2v = w2v
        self._idf = {}

    def get_w2v(self)->Word2Vec:
        return self._w2v

    def set_w2v(self,value: Word2Vec):
        self._w2v = value

    def get_w2v(self)->dict:
        return self._idf
    w2v = property(get_w2v, set_w2v )
    idf = property(get_w2v)

    def encode(self, sentences: list, idf=False):
        """
        Encode (transform to vector) a list of a given sentences
        parameters
        ---------------
        sentences : list[list[str]]
            a list of sentences, each sentence is a list of words (str)

        Returns
        -------
        np.array with shape (n, d) (n = number of sentences, d = dimension of the word encoding)
        """

        if not isinstance(idf,bool):
            raise ValueError("idf must be a boolean")
        if not isinstance(sentences,list):
            raise ValueError(" sentences must be a list")
        for sent in sentences :
            if not isinstance(sent,list):
                raise ValueError("sentence must be a list")
            for word in sent :
                if not isinstance(word,str):
                    raise ValueError("word must be a string")
        sentemb = []
        for sent in sentences:
            if not idf:

                embeddings = [self._w2v.word2vec[word] for word in sent if word in self._w2v.word2vec]
                if not embeddings :
                    embeddings = [np.zeros(300)]
                mean = np.mean(embeddings, axis = 0)

            else:
                embeddings = [self._idf[word] * self._w2v.word2vec[word] for word in sent if word in self._w2v.word2vec]
                if not embeddings :
                    embeddings = [np.zeros(300)]
                mean = np.mean(embeddings, axis = 0)
            sentemb.append(mean)

        return np.vstack(sentemb)

    def most_similar(self, s, sentences, idf=False, K=5):

        scores = [self.score(s, sent, idf = idf) for sent in sentences if sent!=s]
        sorted_indices = np.argsort(np.array(scores))
        top_indices = sorted_indices[-K-1:-1]
        return [sentences[i] for i in top_indices]

    def score(self, s1, s2, idf=False):
        emb1 = self.encode([s1,s2], idf = idf)
        if np.array_equal(emb1[0],np.zeros(len(emb1[0]))) :
            return 0
        if np.array_equal(emb1[1],np.zeros(len(emb1[1]))) :
            return 0
        similarity_score = float(np.dot(emb1[0], emb1[1])) / (np.linalg.norm(emb1[0]) * np.linalg.norm(emb1[1]))
        return similarity_score

    def build_idf(self, sentences):
        idf = {}
        for sent in sentences :
            for w in sent:
                idf[w] = idf.get(w, 0) + 1
        for w in idf :
                idf[w] = max(1, np.log10(len(sentences) / idf[w]))
        self._idf = idf
        return idf
