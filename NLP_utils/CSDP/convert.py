# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     convert
   Description :
   Author :       Liangs
   date：          2019/8/7
-------------------------------------------------
   Change Activity:
                   2019/8/7:
-------------------------------------------------
"""


def sentence2empty_conllu(sentence_seg: list,
                          sentence_pos: list):
    assert len(sentence_pos) == len(sentence_seg)
    conllu = []
    for index, (word, pos) in enumerate(zip(sentence_seg, sentence_pos), start=1):
        conllu.append(f"{index}\t{word}\t{word}\t{pos}\t{pos}\t_\t_\t_\t_\t_\n")
    return conllu
