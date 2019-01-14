import io
import numpy as np
import re

class PreprocessSentence():
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

        preprocess_sentence = sentence.strip()
        if self.to_lower :
            preprocess_sentence = preprocess_sentence.lower()
        if not self.keep_num :
            preprocess_sentence = re.sub("\d+", " ", preprocess_sentence)
        if not self.keep_ponc :
            preprocess_sentence = re.sub(r'[^\w\s]',' ',preprocess_sentence)
        preprocess_sentence = re.sub(' +', ' ', preprocess_sentence)
        return [x for x in preprocess_sentence.split(self.split_by) if x != ""]
