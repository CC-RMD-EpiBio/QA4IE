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

import os, sys
from tokenizer import tokenizer
import numpy as np

def acc_precision_recall_f1(cm):

    tp = cm[0][0]
    fp = cm[0][1]
    fn = cm[1][0]
    tn = cm[1][1]

    try:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        f_1_score = (2 * precision * recall) / (precision + recall)
    except ZeroDivisionError as e:
        precision = 0
        recall = 0
        accuracy = 0
        f_1_score = 0

    return precision, recall, accuracy, f_1_score


def compute_confusion_matrix(actual, predicted, normalize = False):

    unique = sorted(set(actual+predicted))
    #matrix = [[[0 for _ in unique] for _ in unique]]
    matrix = [[0,0],[0,0]]
    imap   = {key: i for i, key in enumerate(unique)}
    # Generate Confusion Matrix
    for p, a in zip(predicted, actual):
        try:
            matrix[imap[p]][imap[a]] += 1
        except KeyError as e:
            matrix[imap[p]][imap[a]] = 1
    # Matrix Normalization
    if normalize:
        sigma = sum([sum(matrix[imap[i]]) for i in unique])
        matrix = [row for row in map(lambda i: list(map(lambda j: j / sigma, i)), matrix)]

    matrix = [x[::-1] for x in matrix][::-1]

    try:
        matrix[0][1]
        matrix[1][1]
    except IndexError as e:
        temp_matrix = [[0,0], [0,0]]
        if 0 in unique:
            temp_matrix[1][1] = matrix[0][0]
        else:
            temp_matrix[0][0] = matrix[0][0]

        matrix = temp_matrix
    return matrix

def token_eval(y_pred, y_true):


    assert len(y_true) == len(y_pred), 'lists differ in length'
    results = {}
    
    confusion_matrix = compute_confusion_matrix(y_true, y_pred)


    results['confusion_matrix'] = confusion_matrix
    results['pre'], results['rec'], results['acc'], results['f_score'] = acc_precision_recall_f1(confusion_matrix)

    
    return results

def camelcase(s):
        """Camelcase tag names to remove spaces.
        This would also change lowercased or uppercased tags without spaces in them.
        """
        return ''.join(part.capitalize() for part in s.split())

def transform_to_bio(tokens, annotations, ann_types, tag_column='train', delimiter='\t'):

    def create_bio_tag(token, anns, concatenation_char='-'):
        if not anns:
            return 'O'
        #tag_parts = [] 
        tag_parts = ['B-{}'.format(camelcase(ann['mention'])) 
                            if ann['start'] in range(token[0], token[1]) 
                            else 'I-{}'.format(camelcase(ann['mention'])) 
                            for ann in anns]
        # for ann in anns:
        #     if ann['start'] in range(token[0], token[1]):
        #         ### Annotation starts inside a token. This approach would fail to produce
        #         ### a B-tag if the annotation starts in between token annotations
        #         tag_parts.append('B-{}'.format(camelcase(ann['mention'])))
        #     else:
        #         tag_parts.append('I-{}'.format(camelcase(ann['mention'])))
        return concatenation_char.join(tag_parts)

    list_out = []
    bio_list = []
    
    #if tag_column == 'train':
    #tags = []
    #for token in tokens:
        #intersecting = []
    tags = [create_bio_tag(token, [a for ann_type in ann_types   
                          for a in [a for a in annotations if a['mention'] == ann_type] 
                          if token[0] in range(a['start'], 
                                               a['end']) 
                          or 

                          token[1] in range(a['start'], 
                                            a['end'])]) for token in tokens]
        #intersecting = 
        # for ann_type in ann_types:
        #     annotations_of_type = [a for a in annotations if a['mention'] == ann_type]
        #     intersecting += [a for a in annotations_of_type if token[0] in range(a['start'], a['end']) 
        #                                                        or 
        #                                                        token[1] in range(a['start'], a['end'])]
        #tags.append(create_bio_tag(token, intersecting))

    assert len(tags) == len(tokens)
    # else:
    #     tags = [tag_column] * len(tokens)

    # for tok, tag in zip(tokens, tags):
    #     # if tag_column == 'none':
    #     #     string_out += '{}\n'.format(tok[2])
    #     #else:
    #     list_out.append('{}{}{}\n'.format(tok[2], delimiter, tag))


    return ['{}{}{}\n'.format(tok[2], delimiter, tag) for tok, tag in zip(tokens, tags)]

def compare(key_text, key_annotations, resp_text, resp_annotations, ent_types):
    
    assert key_text == resp_text, 'text differences found between the documents'


    key_tokens = tokenizer.tokenizer(key_text)
    resp_tokens = tokenizer.tokenizer(resp_text)

    results = {}

    confusion_matrix = [[0,0],[0,0]]
    
    
    for ent_type in ent_types:
        key_bio = transform_to_bio(key_tokens, key_annotations, [ent_type])
        resp_bio = transform_to_bio(resp_tokens, resp_annotations, [ent_type])
        assert len(key_bio) == len(resp_bio), 'lists differ in length'
        key_label_distribution = [camelcase(ent_type) 
                                  if camelcase(ent_type) in item 
                                  else 'O' 
                                  for item in key_bio]

        resp_label_distribution = [camelcase(ent_type) 
                                   if camelcase(ent_type) in item 
                                   else 'O' 
                                   for item in resp_bio]

        assert len(key_label_distribution) == len(resp_label_distribution), 'lists differ in length'

        cm = compute_confusion_matrix(key_label_distribution, 
                                      resp_label_distribution)

        confusion_matrix[0,0] = cm[0,0]
        confusion_matrix[0,1] = cm[0,1]
        confusion_matrix[1,0] = cm[1,0]
        confusion_matrix[1,1] = cm[1,1]
        

    results['confusion_matrix'] = confusion_matrix
    results['pre'], results['rec'], results['acc'], results['f_score'] = acc_precision_recall_f1(confusion_matrix)                                        
    return results

    # results['confusion_matrix'] = [[0,0],[0,0]]
    # results['pre'], results['rec'], results['acc'], results['f_score'] =0,0,0,0
    # return results

