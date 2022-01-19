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
from pathlib import Path
import pandas as pd

from itertools import combinations
import sys, os
from evaluation import annotation_evaluation
from load_data import settings
from sklearn.metrics import confusion_matrix

def entity_eval(filters=[]):
    
    document_name = filters[0].title
    set_name = filters[1].title
    key_name = filters[2].title
    response_name = filters[3].title
    entity_type = filters[4].title
    measure = filters[5].title

    classifications = {
                       'correct':0, # exact match
                       'partial':0, # partial match
                       'missing':0, # annotation exist in key but not in response
                       'false_positive':0 # annotation exists in response but not in key
                      }
    
    if document_name == 'corpus':
      #return ''
      if key_name == 'team':
          return ''
      else: #individual keys
          if response_name == 'team':
              return ''
          else: # individual response
            
            for file_name, annotators in settings.corpus.items():

              key_file = settings.corpus[file_name][key_name]
              response_file = settings.corpus[file_name][response_name]

              if entity_type == 'all_types':
                if set_name == 'all_sets':

                  for ent_type in list(settings.schema.entities.keys()):
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == ent_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == ent_type
                                       ]

                    
                    temp_classifications = annotation_evaluation.determine_entity_classification( key_annotations, 
                                                                                                  response_annotations, 
                                                                                                  key_name, 
                                                                                                  response_name)
                    for x in temp_classifications:
                      classifications[x] += temp_classifications[x]

                else: # individual sets
                  
                  for ent_type in list(settings.schema.entities.keys()):
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == ent_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if  a['mention'] == ent_type
                                       ]

                                          # with tokens create a 'bio' like representation
                    temp_classifications = annotation_evaluation.determine_entity_classification(key_annotations, 
                                                                                            response_annotations, 
                                                                                            key_name, 
                                                                                            response_name)
                    for x in temp_classifications:
                      classifications[x] += temp_classifications[x]

                  
              else: # individual annotations
                  if set_name == 'all_sets':
                    key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == entity_type
                                       ]

                   
                    temp_classifications = annotation_evaluation.determine_entity_classification( key_annotations, 
                                                                                                  response_annotations, 
                                                                                                  key_name, 
                                                                                                  response_name)
                    for x in temp_classifications:
                      classifications[x] += temp_classifications[x]

                  else: # individual sets
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == entity_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == entity_type
                                       ]

                                          # with tokens create a 'bio' like representation
                    temp_classifications = annotation_evaluation.determine_entity_classification( key_annotations, 
                                                                                                  response_annotations, 
                                                                                                  key_name, 
                                                                                                  response_name)
                    for x in temp_classifications:
                      classifications[x] += temp_classifications[x]
                    
    else: #individual files
        if key_name == 'team':
            return ''
        else: #individual keys
            if response_name == 'team':
                return ''
            else: # individual response
                key_file = settings.corpus[document_name][key_name]
                response_file = settings.corpus[document_name][response_name]


                if entity_type == 'all_types':
                  if set_name == 'all_sets':
                    for ent_type in list(settings.schema.entities.keys()):
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == ent_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == ent_type
                                         ]

                      temp_classifications = annotation_evaluation.determine_entity_classification( key_annotations, 
                                                                                                    response_annotations, 
                                                                                                    key_name, 
                                                                                                    response_name)
                      for x in temp_classifications:
                        classifications[x] += temp_classifications[x]

                  else: # individual sets
                    
                    for ent_type in list(settings.schema.entities.keys()):
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == ent_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if  a['mention'] == ent_type
                                         ]

                                            # with tokens create a 'bio' like representation
                      temp_classifications = annotation_evaluation.determine_entity_classification(key_annotations, 
                                                                                              response_annotations, 
                                                                                              key_name, 
                                                                                              response_name)
                      for x in temp_classifications:
                        classifications[x] += temp_classifications[x]


                      #entity_performance = annotation_evaluation.calculate_entity_performance(classifications)
                else: # individual annotation types

                    if set_name == 'all_sets':
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                      classifications = annotation_evaluation.determine_entity_classification(key_annotations, 
                                                                                              response_annotations, 
                                                                                              key_name, 
                                                                                              response_name)


                      #entity_performance = annotation_evaluation.calculate_entity_performance(classifications)
#
                      #cm = confusion_matrix(key_labels, response_labels, labels=[entity_type, 'O'])
                    else: # individual sets
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == entity_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == entity_type
                                         ]

                      classifications = annotation_evaluation.determine_entity_classification(key_annotations, 
                                                                                              response_annotations, 
                                                                                              key_name, 
                                                                                              response_name)

    out = ''
                  

    results = annotation_evaluation.calculate_entity_performance(classifications, measure.lower())

    out += '\n'.join(['{} : {}\n'.format(x, y) for x, y in classifications.items()])
    out += '\n'.join(['{} : {:.3f}\n'.format(x, y) for x, y in results.items()])

    return out


def token_eval(filters=[]):
    
    document_name = filters[0].title
    set_name = filters[1].title
    key_name = filters[2].title
    response_name = filters[3].title
    entity_type = filters[4].title


    
    # defaults
    #   File : corpus Set Name : all_sets Key : team Response : team Entity : all_types

    if document_name == 'corpus':
      #return ''
      if key_name == 'team':
          return ''
      else: #individual keys
          if response_name == 'team':
              return ''
          else: # individual response
            cm = None
            for file_name, annotators in settings.corpus.items():

              key_file = settings.corpus[file_name][key_name]
              response_file = settings.corpus[file_name][response_name]

              key_text = key_file['text']
              key_tokens = tokenizer.tokenizer(key_text)

              response_text = response_file['text']
              response_tokens =  tokenizer.tokenizer(response_text)


              if entity_type == 'all_types':
                if set_name == 'all_sets':
                  
                  for ent_type in list(settings.schema.entities.keys()):
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == ent_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == ent_type
                                       ]

                    # with tokens create a 'bio' like representation
                    key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [ent_type])
                    key_labels = [ent_type if ent_type in x else 'O' for x in key_bio]
                    response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [ent_type])
                    response_labels = [ent_type if ent_type in x else 'O' for x in response_bio]

                    if not len(key_labels) == len(response_labels):
                      if len(key_labels) > len(response_labels):
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          response_labels.append('O')
                      else:
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          key_labels.append('O')
                    temp_cm = confusion_matrix(key_labels, response_labels, labels=[ent_type, 'O'])
                    if cm is None:
                      cm = temp_cm
                    else:
                      cm += temp_cm
                else: # individual sets
                  
                  for ent_type in list(settings.schema.entities.keys()):
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == ent_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if  a['mention'] == ent_type
                                       ]

                                          # with tokens create a 'bio' like representation
                    key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [ent_type])
                    key_labels = [ent_type if ent_type in x else 'O' for x in key_bio]
                    response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [ent_type])
                    response_labels = [ent_type if ent_type in x else 'O' for x in response_bio]

                    if not len(key_labels) == len(response_labels):
                      if len(key_labels) > len(response_labels):
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          response_labels.append('O')
                      else:
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          key_labels.append('O')
                    temp_cm = confusion_matrix(key_labels, response_labels, labels=[ent_type, 'O'])
                    if cm is None:
                      cm = temp_cm
                    else:
                      cm += temp_cm
                  
              else: # individual annotation types
                  if set_name == 'all_sets':

                    key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if  a['mention'] == entity_type
                                       ]

                    # with tokens create a 'bio' like representation
                    key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [entity_type])

                    key_labels = [entity_type if entity_type in x else 'O' for x in key_bio]
                    response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [entity_type])
                    response_labels = [entity_type if entity_type in x else 'O' for x in response_bio]
                   
                    if not len(key_labels) == len(response_labels):
                      if len(key_labels) > len(response_labels):
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          response_labels.append('O')
                      else:
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          key_labels.append('O')

                    cm = confusion_matrix(key_labels, response_labels, labels=[entity_type, 'O'])
                  else: # individual sets
                    key_annotations = [  
                                        a 
                                        for set_n, annotations in key_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == entity_type
                                       ]

                    response_annotations = [  
                                        a 
                                        for set_n, annotations in response_file['annotation_sets'].items() 
                                        for a in annotations 
                                        if set_n == set_name
                                        if a['mention'] == entity_type
                                       ]

                                          # with tokens create a 'bio' like representation
                    key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [entity_type])
                    key_labels = [entity_type if entity_type in x else 'O' for x in key_bio]
                    response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [entity_type])
                    response_labels = [entity_type if entity_type in x else 'O' for x in response_bio]

                    if not len(key_labels) == len(response_labels):
                      if len(key_labels) > len(response_labels):
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          response_labels.append('O')
                      else:
                        for i in range(abs(len(key_labels) - len(response_labels))):
                          key_labels.append('O')
                    cm = confusion_matrix(key_labels, response_labels, labels=[entity_type, 'O'])
 
                    
    else: #individual files
        if key_name == 'team':
            return ''
        else: #individual keys
            if response_name == 'team':
                return ''
            else: # individual response
                key_file = settings.corpus[document_name][key_name]
                response_file = settings.corpus[document_name][response_name]

                key_text = key_file['text']
                key_tokens = tokenizer.tokenizer(key_text)
  
                response_text = response_file['text']
                response_tokens =  tokenizer.tokenizer(response_text)


                if entity_type == 'all_types':
                  if set_name == 'all_sets':
                    cm = None
                    for ent_type in list(settings.schema.entities.keys()):
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == ent_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == ent_type
                                         ]

                      # with tokens create a 'bio' like representation
                      key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [ent_type])
                      key_labels = [ent_type if ent_type in x else 'O' for x in key_bio]
                      response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [ent_type])
                      response_labels = [ent_type if ent_type in x else 'O' for x in response_bio]

                      if not len(key_labels) == len(response_labels):
                        if len(key_labels) > len(response_labels):
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            response_labels.append('O')
                        else:
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            key_labels.append('O')
                      temp_cm = confusion_matrix(key_labels, response_labels, labels=[ent_type, 'O'])
                      if cm is None:
                        cm = temp_cm
                      else:
                        cm += temp_cm
                  else: # individual sets
                    cm = None
                    for ent_type in list(settings.schema.entities.keys()):
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == ent_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if  a['mention'] == ent_type
                                         ]

                                            # with tokens create a 'bio' like representation
                      key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [ent_type])
                      key_labels = [ent_type if ent_type in x else 'O' for x in key_bio]
                      response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [ent_type])
                      response_labels = [ent_type if ent_type in x else 'O' for x in response_bio]

                      if not len(key_labels) == len(response_labels):
                        if len(key_labels) > len(response_labels):
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            response_labels.append('O')
                        else:
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            key_labels.append('O')
                      temp_cm = confusion_matrix(key_labels, response_labels, labels=[ent_type, 'O'])
                      if cm is None:
                        cm = temp_cm
                      else:
                        cm += temp_cm
                else: # individual annotation types

                    if set_name == 'all_sets':
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if  a['mention'] == entity_type
                                         ]

                      # with tokens create a 'bio' like representation
                      key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [entity_type])
                      key_labels = [entity_type if entity_type in x else 'O' for x in key_bio]
                      response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [entity_type])
                      response_labels = [entity_type if entity_type in x else 'O' for x in response_bio]

                      if not len(key_labels) == len(response_labels):
                        if len(key_labels) > len(response_labels):
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            response_labels.append('O')
                        else:
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            key_labels.append('O')
                      cm = confusion_matrix(key_labels, response_labels, labels=[entity_type, 'O'])
                    else: # individual sets
                      key_annotations = [  
                                          a 
                                          for set_n, annotations in key_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == entity_type
                                         ]

                      response_annotations = [  
                                          a 
                                          for set_n, annotations in response_file['annotation_sets'].items() 
                                          for a in annotations 
                                          if set_n == set_name
                                          if a['mention'] == entity_type
                                         ]

                                            # with tokens create a 'bio' like representation
                      key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [entity_type])
                      key_labels = [entity_type if entity_type in x else 'O' for x in key_bio]
                      response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [entity_type])
                      response_labels = [entity_type if entity_type in x else 'O' for x in response_bio]

                      if not len(key_labels) == len(response_labels):
                        if len(key_labels) > len(response_labels):
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            response_labels.append('O')
                        else:
                          for i in range(abs(len(key_labels) - len(response_labels))):
                            key_labels.append('O')
                      cm = confusion_matrix(key_labels, response_labels, labels=[entity_type, 'O'])
    out = ''
                  

    cm_print = annotation_evaluation.pretty_print_cm(cm, ['true_key', 'false_key'], ['true_response', 'false_response'])

    results = annotation_evaluation.calculate_token_performance(cm)
    out += '{}\n\n'.format(cm_print)
    out += '\n\n'
    out += '\n'.join(['{} : {:.3f}'.format(x, y) for x, y in results.items()])

    return out

def generate_token_level_report(filters=[]):

  token_level_path = Path(settings.output_dir / 'evaluation')
  token_level_path.mkdir(parents=True, exist_ok=True)
  out = []
  total_cm_dictionary = {}
  
  for file_name, annotators in settings.corpus.items():
    for key_name, response_name in combinations(list(annotators.keys()),2):
      #cm_total = None

      key_file = settings.corpus[file_name][key_name]
      response_file = settings.corpus[file_name][response_name]

      key_text = key_file['text']
      key_tokens = tokenizer.tokenizer(key_text)

      response_text = response_file['text']
      response_tokens =  tokenizer.tokenizer(response_text)

      for ent_type in list(settings.schema.entities.keys()):
        key_annotations = [  
                            a 
                            for set_n, annotations in key_file['annotation_sets'].items() 
                            for a in annotations 
                            if  a['mention'] == ent_type
                           ]

        response_annotations = [  
                            a 
                            for set_n, annotations in response_file['annotation_sets'].items() 
                            for a in annotations 
                            if  a['mention'] == ent_type
                           ]

        # with tokens create a 'bio' like representation
        key_bio = annotation_evaluation.transform_to_bio(key_tokens, key_annotations, [ent_type])
        key_labels = [ent_type if ent_type in x else 'O' for x in key_bio]
        response_bio = annotation_evaluation.transform_to_bio(response_tokens, response_annotations, [ent_type])
        response_labels = [ent_type if ent_type in x else 'O' for x in response_bio]

        if not len(key_labels) == len(response_labels):
          if len(key_labels) > len(response_labels):
            for i in range(abs(len(key_labels) - len(response_labels))):
              response_labels.append('O')
          else:
            for i in range(abs(len(key_labels) - len(response_labels))):
              key_labels.append('O')
        cm = confusion_matrix(key_labels, response_labels, labels=[ent_type, 'O'])
        try:
          total_cm_dictionary['{}_{}'.format(key_name, response_name)] += cm
        except KeyError as e:
          total_cm_dictionary['{}_{}'.format(key_name, response_name)] = cm
        tn, fp, fn, tp = cm.ravel()
        results = annotation_evaluation.calculate_token_performance(cm)
        out.append([file_name, key_name, response_name, ent_type, tp, tn, fp, fn, results['precision'], results['recall'], results['f1']])



  with open(token_level_path  / 'token_level_eval_summary.txt', 'w') as text_file:
    
    for x in total_cm_dictionary:
      cm_total = total_cm_dictionary[x]
      tn, fp, fn, tp = cm_total.ravel()
      results = annotation_evaluation.calculate_token_performance(cm_total)

      text_file.write('{}\n'.format(x))
      text_file.write('\ttn : {}\n\tfp : {}\n\tfn : {}\n\ttp: {}\n'.format(tn, fp, fn, tp))
      for i, j in results.items():
        text_file.write('\t{} : {} \n'.format(i, j))



  df = pd.DataFrame(out, columns=['file_name', 'key', 'response', 'type', 'tp', 'tn', 'fp', 'fn', 'precision', 'recall', 'f1'])      

  df.to_csv(token_level_path / 'token_level_eval.csv', index=False)
  return 'report generated in {}'.format(settings.output_dir)


def generate_entity_level_report(filters=[]):

  entity_level_path = Path(settings.output_dir / 'evaluation')
  entity_level_path.mkdir(parents=True, exist_ok=True)
  out = []

  classifications_total = {}

  annotators_total = {}
  for file_name, annotators in settings.corpus.items():
    for key_name, response_name in combinations(list(annotators.keys()),2):
      key_file = settings.corpus[file_name][key_name]
      response_file = settings.corpus[file_name][response_name]

      classifications_total['{}_{}'.format(key_name, response_name)] =  {'correct':0, # exact match
                                                                         'partial':0, # partial match
                                                                         'missing':0, # annotation exist in key but not in response
                                                                         'false_positive':0} # ann
                                                                      

      for ent_type in list(settings.schema.entities.keys()):
        key_annotations = [  
                            a 
                            for set_n, annotations in key_file['annotation_sets'].items() 
                            for a in annotations 
                            if  a['mention'] == ent_type
                           ]

        response_annotations = [  
                            a 
                            for set_n, annotations in response_file['annotation_sets'].items() 
                            for a in annotations 
                            if  a['mention'] == ent_type
                           ]

        # with tokens create a 'bio' like representation
        classifications = annotation_evaluation.determine_entity_classification(key_annotations, 
                                                                        response_annotations, 
                                                                        key_name, 
                                                                        response_name)



        

        results = annotation_evaluation.calculate_entity_performance(classifications)
        for x in classifications:
          try:
            classifications_total['{}_{}'.format(key_name, response_name)][x]+=classifications[x]
          except KeyError as e:
            classifications_total['{}_{}'.format(key_name, response_name)]={x:classifications[x]}
        
        out.append([file_name, key_name, response_name, ent_type, classifications['correct'], 
                    classifications['partial'], classifications['missing'], classifications['false_positive'],
                    results['precision'], results['recall'], results['f1']])

  with open(entity_level_path  / 'entity_level_eval_summary.txt', 'w') as text_file:
    for x in classifications_total:

      text_file.write('{}\n'.format(x))
      for i, j in classifications_total[x].items():
        text_file.write('\t{} : {} \n'.format(i, j))
      for i, j in annotation_evaluation.calculate_entity_performance(classifications_total[x]).items():
        text_file.write('\t{} : {} \n'.format(i, j))

  df = pd.DataFrame(out, columns=['file_name', 'key', 'response', 'type', 'correct', 'partial', 'missing', 'false_positive', 'precision', 'recall', 'f1'])      

  df.to_csv(entity_level_path  / 'entity_level_eval.csv', index=False)
  return 'report generated in {}'.format(settings.output_dir)

