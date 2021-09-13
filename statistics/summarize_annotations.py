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



from tokenizer.tokenizer import tokenizer
from collections import defaultdict
import numpy as np
from discrepancy_analysis.hierarchical_structure import apply_hierarchical_structure


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))


def count_annotation_types(annotations = [], schema = {}, include_features=False):

    '''
        counts the amount of annotations found in each file
        :param annotators_content: a dictionary that contains the text and annotated sections of each annotator
        :type dict

        :param ignore_sets: a list of set names to ignore
        :type list

        :param include_features: include the annotation features
        :type bool

        :return count_dict: annotation counts

    '''
    counts = nested_dict(2, list)

    for annotation in annotations:
        if annotation['mention'] in list(schema.keys()):
            values = [annotation['mention']]
            if include_features:
                values += [x if x is not None else '' for x in list(annotation['features'].values())]
            values = '_'.join(values)

            counts[values]['count'].append(1)
            counts[values]['char_length'].append(annotation['end'] - annotation['start'])
            counts[values]['token_length'].append(len(tokenizer(annotation['text_span'])))

    return counts


def summarize_counts(count_dict):

    '''
        summarizes counts in the dictionary
        :param count_dict: counts dictionary derived from
        :type dict

        :return count_dict: summarized counts

    '''

    for annotation_type, annotation_summary in count_dict.items():
        annotation_summary['count'] = sum(annotation_summary['count'])
        annotation_summary['char_length_arithmetic_mean'] = np.mean(annotation_summary['char_length'])
        annotation_summary['char_length_median'] = np.median(annotation_summary['char_length'])
        annotation_summary['char_length_var'] = np.var(annotation_summary['char_length'])
        annotation_summary['char_length_sd'] = np.std(annotation_summary['char_length'])
        annotation_summary['char_length_min'] = min(annotation_summary['char_length'])
        annotation_summary['char_length_max'] = max(annotation_summary['char_length'])

        annotation_summary['token_length_arithmetic_mean'] = np.mean(annotation_summary['token_length'])
        annotation_summary['token_length_median'] = np.median(annotation_summary['token_length'])
        annotation_summary['token_length_var'] = np.var(annotation_summary['token_length'])
        annotation_summary['token_length_sd'] = np.std(annotation_summary['token_length'])
        annotation_summary['token_length_min'] = min(annotation_summary['token_length'])
        annotation_summary['token_length_max'] = max(annotation_summary['token_length'])   

        del annotation_summary['char_length']
        del annotation_summary['token_length']

    return count_dict

def count_hierarchical_overlaps(annotations = [], structure = {}, include_features=False):

    counts = nested_dict(3, list)

    annotations = apply_hierarchical_structure(annotations=annotations, structure=structure)
   
    for annotation in annotations:
        val = [annotation['entity']['mention']]

        if include_features:
            val += [x if x is not None else '' for x in list(annotation['features'].values())]
        val = '_'.join(val)
        try:
            for k, v in annotation['sub_entities'].items():
                
                for s in v:
                    sub_val = [s['mention']]
                    if include_features:
                        sub_val += [x if x is not None else '' for x in list(s['features'].values())]
                    sub_val = '_'.join(sub_val)
                    counts[val][sub_val]['counts'].append(1)

                    counts[val][sub_val]['char_length'].append(s['end'] - s['start'])
                    counts[val][sub_val]['token_length'].append(len(tokenizer(s['text_span'])))
        except KeyError:
            pass

    return counts
