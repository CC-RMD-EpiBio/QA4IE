###############################################################################
#
#                           COPYRIGHT NOTICE
#                  Mark O. Hatfield Clinical Research Center
#                       National Institutes of Health
#            United States Department of Health and Human Services
#
# This software was developed and is owned by the National Institutes of
# Health Clinical Center (NIHCC), an agency of the United States Department
# of Health and Human Services, which is making the software available to the
# public for any commercial or non-commercial purpose under the following
# open-source BSD license.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# (1) Redistributions of source code must retain this copyright
# notice, this list of conditions and the following disclaimer.
# 
# (2) Redistributions in binary form must reproduce this copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# (3) Neither the names of the National Institutes of Health Clinical
# Center, the National Institutes of Health, the U.S. Department of
# Health and Human Services, nor the names of any of the software
# developers may be used to endorse or promote products derived from
# this software without specific prior written permission.
# 
# (4) Please acknowledge NIHCC as the source of this software by including
# the phrase "Courtesy of the U.S. National Institutes of Health Clinical
# Center"or "Source: U.S. National Institutes of Health Clinical Center."
# 
# THIS SOFTWARE IS PROVIDED BY THE U.S. GOVERNMENT AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
# 
# You are under no obligation whatsoever to provide any bug fixes,
# patches, or upgrades to the features, functionality or performance of
# the source code ("Enhancements") to anyone; however, if you choose to
# make your Enhancements available either publicly, or directly to
# the National Institutes of Health Clinical Center, without imposing a
# separate written license agreement for such Enhancements, then you hereby
# grant the following license: a non-exclusive, royalty-free perpetual license
# to install, use, modify, prepare derivative works, incorporate into
# other computer software, distribute, and sublicense such Enhancements or
# derivative works thereof, in binary and source code form.
#
###############################################################################

'''
    Funtions that represent a series of steps for finding errors in documents that were annotated using GATE.
'''


import difflib as dl
from tokenizer.tokenizer import tokenizer


def compare_texts(text_a = None, text_b = None):
    '''
        compares the text section of an annotated gate xml between two annotators
        :param text_a: annotators a text
        :type str
        :param text_b: annotators b text
        :type str

        :return conflicts: the conflicts found for this check

    '''
    assert text_a or text_b, 'please provide a texts to compare'

    conflicts = []

    if not text_a == text_b:
        a_tokens = [t[2] for t in tokenizer(text_a)]
        b_tokens = [t[2] for t in tokenizer(text_b)]
        diff_texts = dl.context_diff(a_tokens, b_tokens)
        
        conflicts = [str(d) for d in diff_texts]

    return conflicts


def compare_set_names(sets_a, sets_b):
    '''
        compares the set namesof an annotated gate xml between two annotators
        :param sets_a: annotators a list of set names
        :type list
        :param sets_b: annotators b list of set names
        :type list

        :return conflicts: the conflicts found for this check

    '''
    assert sets_a or sets_b, 'please provide set names to compare'
    conflicts = set(sets_a) - set(sets_b)
    conflicts = conflicts.union(set(sets_b) - set(sets_a))

    return conflicts
