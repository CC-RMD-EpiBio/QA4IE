#!/usr/bin/env python3
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
from collections import Counter
import numpy as np
from sklearn.metrics import confusion_matrix

def cohens_kappa(key, response, lbs):

  cm = confusion_matrix(key, response, labels = lbs)

  true_positives = cm[0,0]
  false_postives = cm[1,0]
  false_negatives = cm[0,1]
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
  
  cohens_kappa = (a_0 - a_e) / (1 - a_e)

 


  return {'confusion_matrix':cm,
          'observed_agreement':round(total_true /total, 4), 
          'positive_specific_agreement':round(cat_2, 4), 
          'negative_specific_agreement':round(cat_1, 4), 
          'chance_agreement':round(a_e, 4), 
          'cohens_kappa':cohens_kappa}

def pretty_print_cm(cm, key_labels, response_labels):
  '''

    formats a confusion matrix into a printable version

    :param cm: a nested list that represents a matrix
    :type list

    :returns: a string containing the output to be printed in the screen
    :type str


  '''
  out = ''
  longest_label = max([y for x in [key_labels, response_labels] for y in x], key = len)
  out += '{}\n'.format('---' * (len(longest_label) - 2))
  #out += '{}'.format('\t')
  out += '{}'.format('{}{}'.format(' ' * len(key_labels[0]), ' '.join([x for x in response_labels])))
  out += '\n'

  # Print rows
  for i, label1 in enumerate(key_labels):
      out += '{}\t'.format(label1)
      for j in range(len(key_labels)):
          cell = '{}\t'.format(cm[i, j])
          out += '{}{}'.format(cell, '\t\t\t')
      out += '\n'
  out += '\n'
  out += '{}\n'.format('---' * (len(longest_label) - 2))
  return out

def calculate_token_performance(cm):
  '''

    calculates precision, recall and f1 score for a confusion matrix

    :param cm: a nested list that represents a matrix
    :type list

    :returns: a dictionary containing precision, recall and f1 score
    :type dict

  '''

  assert not cm is None, 'please provide a confusion matrix'

  # only works for a 2 class matrix
  

  tn, fp, fn, tp = cm.ravel()

  precision = 0 if (tp + fp) == 0 else tp / (tp + fp)
  recall = 0 if (tp + fn) == 0 else tp / (tp + fn)
  f1 = 0 if (precision + recall) == 0 else (2 * precision * recall) / (precision + recall)


  return {
          'precision':precision,
          'recall':recall,
          'f1':f1
          }

def transform_to_bio(tokens, annotations, ann_types, delimiter='\t'):

    '''
      creates a bio like representation of a list of annotations based on a list of annotations types

      :param tokens: a list of tokens
      :type list

      :param annotations: a list of annotations
      :type list

      :param ann_types: a list of annotation types
      :type list

      :param delimiter: a char that represents how the tags will be separated
      :type str

      :returns: a list that represents an entire bio conversion
      :type list


    '''

    def create_bio_tag(token, anns, concatenation_char='-'):
      '''
        creates a line for a bio representation based on a token and the annotations associated with it
        :param token: token tupple containing the ofsets and the tokenized text
        :type tupple

        :param ans: A list containing annotations
        :type list

        :param concatenation_char: a string containing the char used for dividing each tag of a row
                                   in the bio representaion
        :type str

        :returns: a string that represents a row's tag in a bio like format
        :type str



      '''
      def camelcase(s):
        '''
          Camelcase tag names to remove spaces.
          This would also change lowercased or uppercased tags without spaces in them.
        '''
        return ''.join(part.capitalize() for part in s.split())

      if not anns:
          return 'O'
      tag_parts = ['B-{}'.format(ann['mention'])
                          if ann['start'] in range(token[0], token[1]) 
                          else 'I-{}'.format(ann['mention'])
                          for ann in anns]

      return concatenation_char.join(tag_parts)

    list_out = []
    bio_list = []
    
    tags = [create_bio_tag(token, [a  for ann_type in ann_types   
                                      for a in [a for a in annotations 
                                                  if a['mention'] == ann_type] 
                                      if token[0] in range(a['start'], 
                                                           a['end']) 
                                      or 

                                      token[1] in range(a['start'], 
                                                        a['end'])]) for token in tokens]

    assert len(tags) == len(tokens)


    return ['{}{}{}\n'.format(tok[2], delimiter, tag) for tok, tag in zip(tokens, tags)]

def calculate_entity_performance(counts = {}, method = 'average'):

  '''
      outputs the recall precision and f1 score based on a given method

      :param counts: dict that contains the the counts of matching categories
      :type dict
      :param method: the method to be used for calculating the performance
      :type str

      :returns dictionary of counts precision, recall and f1 score
      :type dict

  '''
  assert method in ['average', 'strict', 'lenient'], 'please provide a valid method'
  assert counts, 'please provide a dictionary of counts'

  if (counts['correct'] + counts['false_positive'] + counts['missing'] + counts['partial']) == 0:
    return {
          'precision':1.00,
          'recall':1.00,
          'f1':1.00
          }

  constants = {'strict':0, 'average':0.5, 'lenient': 1}

  tp = counts['correct'] + (constants[method] * counts['partial'])

  fp = counts['false_positive'] + ((1-constants[method]) * counts['partial'])

  fn = counts['missing'] + ((1-constants[method]) * counts['partial'])

  precision = 0 if tp + fp == 0 else tp/(tp+fp)
  recall = 0 if tp + fn == 0 else tp/(tp+fn)
  f1 = 0 if precision + recall == 0 else 2 * ((precision*recall)/(precision+recall))


  return {
          'precision':precision,
          'recall':recall,
          'f1':f1
          }

def determine_entity_classification(key_annotations = [], response_annotations = [], key_name='', resp_name=''):

  def coextensive(k, r):
    return k['start'] == r['start'] and k['end'] == r['end']

  def compatible(k, r):
    # if len(k['features']) == len(r['features']):
    #   return k['features'] == r['features']
    # else:
    return any(i in k['features'].values() for i in r['features'].values())

  def overlaps(a, t):
    return(t['end'] > a['start'] and t['start'] < a['end'])

  flat_list = [item for sublist in [key_annotations, response_annotations] for item in sublist]

  clusters = create_clusters(flat_list, hierarchy_present = False) # gets both annotators annotation sets into the same list



  results = {
           'correct':0, # exact match
           'partial':0, # partial match
           'missing':0, # annotation exist in key but not in response
           'false_positive':0 # annotation exists in response but not in key

          }


  for i in range(len(key_annotations)):
      for j in range(len(response_annotations)):
        key_annotation = key_annotations[i]
        response_annotation = response_annotations[j]

        choice = None
        # Coextensive
        # Two annotations are coextensive if they hit the same span of text in a document. 
        # Basically, both their start and end oﬀsets are equal.

        if coextensive(key_annotation, response_annotation):
          # full overlap found
          #if compatible(key_annotation, response_annotation):
            # if compatible, we have a full match 
          results['correct'] += 1
        elif overlaps(key_annotation, response_annotation):

          #if compatible(key_annotation, response_annotation): # if partially compatible
          results['partial'] += 1


  for cluster in clusters:
  
    hits = determine_hit_type(cluster, key_name, resp_name)
  
    for hit in hits:
        results[hit] += 1
  return results

def determine_hit_type(annotations, key_name, resp_name):
    """
        determines the type of match

        param:
            annotations: list of annotations
            key_name: string representation of the annotator that will be used as the key
            resp_name: string representation of the annotator that will be used as the response
    """

    def overlaps(search, tuples):
        res = []
        for t in tuples:
            if(t[1]>search[0] and t[0]<search[1]):
                res.append(t)
        return res

    annotator_freq = Counter([a['annotator'] for a in annotations])
    offset_dict = {}

    hits = []

    if annotator_freq[resp_name] > annotator_freq[key_name] :
        hits.extend(['false_positive'] * (annotator_freq[resp_name] - annotator_freq[key_name]))

    if annotator_freq[key_name] > annotator_freq[resp_name]:

        hits.extend(['missing'] * (annotator_freq[key_name] - annotator_freq[resp_name]))

    return(hits)

def create_clusters(l = [], exclude = [], hierarchy_present = True):

    """
        clustering algorithm. Groups related annotations together

        param:
            l: list of all annotations for a single document

        return:
            a list containing annotations related to a specific cluster
    """
    if hierarchy_present:
        if exclude:
            l = [i for i in l if i['entity']['mention'] in exclude]

        if l:
            l.sort(key = lambda x: x['entity']['start'])
            
            union_left = l[0]['entity']['start']
            union_right = l[0]['entity']['end']
            result = []
            group = [l[0]]

            for interval in l[1:]:
                current_left = interval['entity']['start']
                current_right = interval['entity']['end']
                if current_left > union_right:
                    result.append(group)
                    group = [interval]
                    union_left = interval['entity']['start']
                    union_right = interval['entity']['end']
                else:
                    group.append(interval)
                    union_right = max(current_right, union_right)
            result.append(group)

            return result
    else:

        if exclude:
            l = [i for i in l if i['mention'] in exclude]

        if l:
            l.sort(key = lambda x: x['start'])
            
            union_left = l[0]['start']
            union_right = l[0]['end']
            result = []
            group = [l[0]]

            for interval in l[1:]:
                current_left = interval['start']
                current_right = interval['end']
                if current_left > union_right:
                    result.append(group)
                    group = [interval]
                    union_left = interval['start']
                    union_right = interval['end']
                else:
                    group.append(interval)
                    union_right = max(current_right, union_right)
            result.append(group)

            return result

    return []


