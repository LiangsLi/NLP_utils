# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     easy_ltp
   Description :
   Author :       Liangs
   date：          2019/5/7
-------------------------------------------------
   Change Activity:
                   2019/5/7:
-------------------------------------------------
"""
import os
import pyltp
import re


class EasyLTP(object):
    def __init__(self, ltp_path, dependency=False):
        self.dependency = dependency
        cws_model_path = os.path.join(ltp_path, 'cws.model')
        pos_model_path = os.path.join(ltp_path, 'pos.model')
        ner_model_path = os.path.join(ltp_path, 'ner.model')
        dp_model_path = os.path.join(ltp_path, 'parser.model')
        # srl_model_path = os.path.join(ltp_path, 'pisrl.model')
        self.seg = pyltp.Segmentor()
        self.pos = pyltp.Postagger()
        self.ner = pyltp.NamedEntityRecognizer()
        # self.srl = pyltp.SementicRoleLabeller()
        self.seg.load(cws_model_path)
        self.pos.load(pos_model_path)
        self.ner.load(ner_model_path)
        # self.srl.load(srl_model_path)
        if dependency:
            self.dp = pyltp.Parser()
            self.dp.load(dp_model_path)

    def seg_sent(self, sent):
        words = self.seg.segment(sent)
        return [str(w) for w in words]

    # def fix_seg(self,sent,pattern):
    #     if '@' not in

    def pos_sent(self, sent):
        words = self.seg.segment(sent)
        poss = self.pos.postag(words)
        return [str(p) for p in poss]

    def pos_words(self, words):
        poss = self.pos.postag(words)
        return [str(p) for p in poss]

    def ner_sent(self, sent):
        # Nh:人名
        # Ni:机构名
        # Ns:地名
        words = self.seg.segment(sent)
        poss = self.pos.postag(words)
        ners = self.ner.recognize(words, poss)
        ner_ch = []
        for n in ners:
            if str(n).endswith('Nh'):
                ner_ch.append(str(n).replace('Nh', 'person'))
            elif str(n).endswith('Ni'):
                ner_ch.append(str(n).replace('Ni', 'organization'))
            elif str(n).endswith('Ns'):
                ner_ch.append(str(n).replace('Ns', 'location'))
            else:
                ner_ch.append(str(n))
        return ner_ch

    def ner_words(self, words):
        poss = self.pos.postag(words)
        ners = self.ner.recognize(words, poss)
        return list(ners)

    def seg_with_ner_sent(self, sentence):
        words = self.seg_sent(sentence)
        ners = self.ner_words(words)
        new_words = []
        cat_word = ''
        for word, ner in zip(words, ners):
            if ner[0] in ['O', 'S']:
                new_words.append(word)
            elif ner[0] in ['B', 'I']:
                cat_word += word
            elif ner[0] == 'E':
                cat_word += word
                new_words.append(cat_word)
                cat_word = ''
            else:
                raise ValueError(f'bad ner value:{ner}')
        return new_words

    # def fix_seg_sent(self):

    def dependency_sent(self, sent):
        words = list(self.seg.segment(sent))
        words_root = ['Root'] + words
        poss = self.pos.postag(words)
        arcs = self.dp.parse(words, poss)
        result = []
        for arc, (child_index, child_word) in zip(arcs, enumerate(words)):
            result.append(((arc.head, words_root[arc.head]), arc.relation, (child_index + 1, child_word)))
        return result

    def judge_sent(self, sentence):
        """
            判读root指向的词是否发出了SBV弧
        """
        dependency = self.dependency_sent(sentence)
        core_word_idx = -1
        for dep in dependency:
            if dep[0][0] == 0 and dep[1] == 'HED':
                core_word_idx = dep[2][0]
        # print(core_word_idx)
        if core_word_idx == -1:
            return False
        for dep in dependency:
            if dep[1] == 'SBV' and dep[0][0] == core_word_idx:
                return True
        return False

    def release(self):
        self.seg.release()
        self.pos.release()
        self.ner.release()


if __name__ == '__main__':
    # from utils.constant import LTP_path
    LTP_path = r'E:\data\ltp_data_v3.4.0'
    ltp = EasyLTP(LTP_path, dependency=True)
    while True:
        sent = input('sent:')
        # print(f'seg:{ltp.seg_sent(sent)}')
        for word, ner in zip(ltp.seg_sent(sent), ltp.ner_sent(sent)):
            print(f'{word}:{ner}', end=' | ')
        print('\n' + '-----' * 30)
        # print(f'ner:{ltp.ner_sent(sent)}')
    #     print(ltp.dependency_sent(sent))
    #     print(ltp.judge(sent))
    # with open(r'../medical/血液病学上.txt', encoding='utf-8')as f, \
    #         open(r'../medical/血液病学上_False.txt','w',encoding='utf-8')as f_out:
    #     for line in f:
    #         line = line.strip()
    #         if not ltp.judge(line):
    #             f_out.write(line+'\n')
