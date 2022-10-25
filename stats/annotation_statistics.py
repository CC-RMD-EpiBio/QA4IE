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
from tokenizer import tokenizer
import numpy as np

def count_mentions(annotations = [], schema = {}, include_features = True):

    '''
        counts the amount of annotations found in each file
        :param annotators_content: a dictionary that contains the text and annotated sections of each annotator
        :type dict

        :param ignore_sets: a list of set names to ignore
        :type list

        :return conflicts: the conflicts found for this check

    '''
    counts = {}
    annotations.sort(key=lambda x: x['mention'], reverse=False)
    for annotation in annotations:
        if not annotation['mention'] in schema.keys():
            continue
        if include_features:
            values = '_'.join([annotation['mention']] + [x if x is not None else '' for x in list(annotation['features'].values())])
        else:
            values = annotation['mention']

        try:
            counts[values]['count'] += 1

            counts[values]['char_length'].append(annotation['end'] - annotation['start'])

            counts[values]['token_length'].append(len(tokenizer.tokenizer(annotation['text_span'])))
        except KeyError as e:
            
            counts[values] = {
                            'count' : 1,
                            'char_length' : [annotation['end'] - annotation['start']],
                            'token_length' : [len(tokenizer.tokenizer(annotation['text_span']))]
                            }
          
    for annotation_type, annotation_summary in counts.items():
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


    return counts


def count_hierarchical_relationships(annotations = [], current_type = None):
    def overlap(a, l):
        '''
            finds overlaps between a list of annotations and a single annotation
            :param a: a single annotation
            :type dict

            :param b: a list of annotations
            type list

            :return conflicts: the conflicts found for this check       
        '''
        #assert a, 'please provide an annotationn'
        #assert l, 'please provide a list of annotations'
        
        res = []
        for t in l:
            if(t['end'] > a['start'] and t['start'] < a['end'] 
                                     and not (t['id'] == a['id']) 
                                     and (t['annotator'] == a['annotator'])):
                res.append(t)
        return res

    out = {}

    # current_type = schema[annotation_type]
    if current_type.is_parent_entity():
        #return '{}'.format(current_type.name)
        out[current_type.name] = {}
       
        for sub in list(current_type.sub_entities.keys()):
            
        #     # get subentities of this type


            out[current_type.name][sub] = 0
            
            subs_of_type = [s for s in annotations if s['mention'] == sub]

            #return '{}'.format([s['mention'] for s in annotations])
            filtered_annotations = [a for a in annotations if a['mention'] == current_type.name]
            
            for sub_entity in subs_of_type:
                if overlap(sub_entity, filtered_annotations):
                    out[current_type.name][sub] +=1
            try:
                out[current_type.name][sub] = out[current_type.name][sub] / len(filtered_annotations)
            except ZeroDivisionError:
                out[current_type.name][sub] = 0

    
        return out




        
    if current_type.is_sub_entity():
        main_type = current_type.get_parent_entity().name
        out[main_type] = {}
       
        sub = current_type.name
            
        #     # get subentities of this type


        out[main_type][sub] = 0
        
        subs_of_type = [s for s in annotations if s['mention'] == sub]

        #return '{}'.format([s['mention'] for s in annotations])
        filtered_annotations = [a for a in annotations if a['mention'] == main_type]
        
        for sub_entity in subs_of_type:
            if overlap(sub_entity, filtered_annotations):
                out[main_type][sub] +=1
        try:
            out[main_type][sub] = out[main_type][sub] / len(filtered_annotations)
        except ZeroDivisionError:
            out[main_type][sub] = 0

    
        return out


    else:
        return {}










