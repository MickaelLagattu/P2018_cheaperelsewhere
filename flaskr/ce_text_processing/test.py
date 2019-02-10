
import unittest
try:
    from .ce_text_processing import BoV, Word2Vec, PreprocessSentence
    from .text_global_variables import w2vfile
except ModuleNotFoundError: # If we run the tests, the working directory is not the same
    from ce_text_processing import BoV, Word2Vec, PreprocessSentence
    from text_global_variables import w2vfile
import numpy as np

class TestBagOfWords(unittest.TestCase):

    w2v = Word2Vec(w2vfile)
    bov = BoV(w2v)
    prep = PreprocessSentence()

    def test_encode(self):
        sent = TestBagOfWords.prep.preprocess_sentence("")
        vect = TestBagOfWords.bov.encode([sent])
        self.assertEqual(vect[0].shape,(300,))
        self.assertTrue(np.array_equal(vect[0],np.zeros(300)))

        sent = TestBagOfWords.prep.preprocess_sentence("Polytechnique n'est pas une école d'ingénieurs")
        vect = TestBagOfWords.bov.encode([sent])
        self.assertEqual(vect[0].shape,(300,))
        self.assertFalse(np.array_equal(vect[0],np.zeros(300)))

    def test_score(self):
        sent = TestBagOfWords.prep.preprocess_sentence("Polytechnique n'est pas une école d'ingénieurs")

        # test that the same sentence have a score of 1
        score = TestBagOfWords.bov.score(sent,sent)
        epsilon = 0.001
        self.assertTrue(1-epsilon <= score <= 1+epsilon )

        # a sentence without words and a normal sentence
        empty_sent = TestBagOfWords.prep.preprocess_sentence("")
        score = TestBagOfWords.bov.score(sent,empty_sent)
        self.assertEqual(score,0)

    def test_build_idf(self):
        pass

class TestPreprocessSentence(unittest.TestCase):

    def test_preprocess(self):
        prep = PreprocessSentence()
        sent = "ab. c?/e 2k fd !!"
        sent_list =  ['ab', 'c', 'e', 'k', 'fd']
        self.assertEqual(prep.preprocess_sentence(sent),sent_list)

        sent = "!:,;:!;!,:;!:,;!,:;1231512:;,?;:,"
        sent_list = []
        self.assertEqual(prep.preprocess_sentence(sent),sent_list)

class TestWord2Vec(unittest.TestCase):

    def test_load_w2v(self):
        pass

    def test_word2v(self):
        # some different words
        pass

if __name__ == '__main__':
    unittest.main()
