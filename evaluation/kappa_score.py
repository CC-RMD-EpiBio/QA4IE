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

def calculate_kappa(key, response):

    cm = compute_confusion_matrix(key, response)

    true_positives = cm[0,0]
    false_postives = cm[0,1]
    false_negatives = cm[1,0]
    true_negatives = cm[1,1]

    total_true = true_positives + true_negatives
    total_false = false_postives + false_negatives
    total = total_true + total_false

    a_0 = (true_positives + true_negatives) / total
    cat_1 = (2 * true_positives) / ((2 * true_positives) + false_postives + false_negatives)
    cat_2 = (2 * true_negatives) / (false_postives + false_negatives + (2 * true_negatives))

    expected_matrix = np.array([[sum(cm[0,:])/total, sum(cm[:,0])/total],
                                [sum(cm[1,:])/total, sum(cm[:,1])/total]])

    a_e = (expected_matrix[0,0] * expected_matrix[0,1]) + (expected_matrix[1,0] * expected_matrix[1,1])
    
    cohens_kappa = round((a_0 - a_e) / (1 - a_e), 4)
    results = {}
    results['confusion_matrix'] = cm
    results['observed_agreement'] = round(total_true /total, 4)
    results['positive_specific_agreement'] = round(cat_2, 4)
    results['negative_specific_agreement'] = round(cat_1, 4)
    results['chance_agreement'] = round(a_e, 4)
    results['cohens_kappa'] = cohens_kappa

    return results

def compute_confusion_matrix(actual, predicted, normalize = False):

    unique = sorted(set(actual+predicted))
    matrix = [[0 for _ in unique] for _ in unique]
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
    except IndexError as e:
        temp_matrix = [[0,0], [0,0]]
        if 0 in unique:
            temp_matrix[1][1] = matrix[0][0]
        else:
            temp_matrix[0][0] = matrix[0][0]

        matrix = temp_matrix
    return matrix


def compare(key_text, key_annotations, resp_text, resp_annotations, ent_type):
    
    assert key_text == resp_text, 'text differences found between the documents'

   

    k = [a['mention'] for a in key_annotations]
    r = [a['mention'] for a in resp_annotations]

    assert len(k) == len(r), 'Different annotation lengths'

    results=calculate_kappa(k, r)

                                             
    return results



