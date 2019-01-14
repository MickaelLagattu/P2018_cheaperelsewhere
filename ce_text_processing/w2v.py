import io
import numpy as np

class Word2Vec:
    def __init__(self, fname, nmax=5000):
        self.load_wordvec(fname, nmax)
        self.word2id = {i:list(self.word2vec.keys()).index(i) for i in self.word2vec.keys()}
        self.id2word = {v: k for k, v in self.word2id.items()}
        self.embeddings = np.array(self.word2vec.values())
        print(len(self.id2word.keys()))

    def load_wordvec(self, fname, nmax):
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
        sorted_scores = []
        for wi in self.word2vec.keys() :
          sorted_scores = sorted_scores  + [ self.score(w, wi) ]

        sorted_indices = np.argsort(sorted_scores)
        reversed_sorted_indices = sorted_indices [::-1]
        top_indices = reversed_sorted_indices[0:K+1]
        return [self.id2word[i] for i in top_indices]

    def score(self, w1, w2):
        if type(w1)== str :
            emb1 = self.word2vec[w1]
        else :
            emb1 = w1
        emb2 = self.word2vec[w2]
        similarity_score = np.dot(emb1,emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return similarity_score
