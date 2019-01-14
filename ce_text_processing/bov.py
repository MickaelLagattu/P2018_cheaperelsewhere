from w2v import Word2Vec
import numpy as np

class BoV():
    def __init__(self, w2v):
        self._w2v = w2v

    def get_w2v(self)->Word2Vec:
        return self._w2v

    def set_w2v(self,value: Word2Vec):
        self._w2v = value

    w2v = property(get_w2v, set_w2v )

    def encode(self, sentences: list, idf=False):
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
            if idf is False:

                embeddings = [self.w2v.word2vec[word] for word in sent if word in self.w2v.word2vec]
                if not embeddings :
                    embeddings = [np.zeros(300)]
                mean = np.mean(embeddings, axis = 0)

            else:
                embeddings = [idf[word] * self.w2v.word2vec[word] for word in sent if word in self.w2v.word2vec]
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
        return idf
