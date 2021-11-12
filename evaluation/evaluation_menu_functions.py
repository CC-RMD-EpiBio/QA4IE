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

import sys, os
from evaluation import token_level_eval
from load_data import settings

def token_eval(filters=[]):
    
    document_name = filters[0].title
    set_name = filters[1].title
    key_name = filters[2].title
    response_name = filters[3].title
    entity_type = filters[4].title

    
    # defaults
    #   File : corpus Set Name : all_sets Key : team Response : team Entity : all_types

    if document_name == 'corpus':
        return ''
    else:
        if key_name == 'team':
            return ''
        else:
            if response_name == 'team':
                return ''
            else:
                if entity_type == 'all_types':
                    return ''
                else:
                # (key_text, key_annotations, resp_text, resp_annotations, ent_types)
                    
                    current_document = settings.corpus[document_name]
                    key_document = current_document[key_name]
                    response_document = current_document[response_name]

                    if set_name == 'all_sets':
                        key_annotations = [a for s, ans in key_document['annotation_sets'].items()
                                             for a in ans
                                             if a['mention'] == entity_type]
                        response_annotations = [a for s, ans in response_document['annotation_sets'].items()
                                                  for a in ans
                                                  if a['mention'] == entity_type]
                    else:
                        key_annotations = [a for s, ans in key_document['annotation_sets'].items()
                                             for a in ans if s == set_name
                                             if a['mention'] == entity_type]

                        response_annotations = [a for s, ans in response_document['annotation_sets'].items()
                                                  for a in ans if s == set_name
                                                  if a['mention'] == entity_type]


                    try:
                        results = token_level_eval.compare(key_document['text'],
                                                           key_annotations,
                                                           response_document['text'],
                                                           response_annotations,
                                                           [entity_type])
                    except AssertionError as e:
                        return '{}'.format(e)

                    out = ''
                                  
                    cm_print = '{} {}\n{} {}\n'.format(results['confusion_matrix'][0][0],
                                                    results['confusion_matrix'][1][0],
                                                       results['confusion_matrix'][0][1],
                                                       results['confusion_matrix'][1][1])


                    out += '{}\n\n'.format(cm_print)
                    out += 'Precision: {}\n'.format(round(results['pre'],2))
                    out += 'Reccall: {}\n'.format(round(results['rec'],2))
                    out += 'Accuracy: {}\n'.format(round(results['acc'],2))
                    out += 'F1 Score: {}\n'.format(round(results['f_score'],2))

                    return out






