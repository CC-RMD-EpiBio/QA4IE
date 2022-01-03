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
from load_data import settings
from itertools import combinations
import collections
from stats import annotation_statistics
from pathlib import Path
import pandas as pd


def count_entities(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    stat_mention_count_print = {}
    total_mention_counts = []
    output = ''

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]


                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]



            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]


                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                                                                        

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]


    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]




    counts = annotation_statistics.count_mentions(annotations=annotations,
                                                 schema=settings.schema.get_simple_schema(),
                                                 include_features = False)

    for t, stats in counts.items():

        try:
            stat_mention_count_print[annotator_name][t] += stats['count']

        except KeyError:
            try:
                stat_mention_count_print[annotator_name].update({t : stats['count']})

            except KeyError:
                stat_mention_count_print[annotator_name] = {t : stats['count']}

   
    for anno, counts in stat_mention_count_print.items():
        output += '{}\n'.format( 
                            ''.join(['{} : {}\n'.format(k, v) for k, v in counts.items()]))

    return output


def count_entities_with_features(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    stat_mention_count_print = {}
    total_mention_counts = []
    output = ''

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]


                        # total_mention_counts.append([file, annotator_name, annotation_set, 
                        #                             t,
                        #                             stats['count'],

                        #                             stats['char_length_arithmetic_mean'],
                        #                             stats['char_length_median'],
                        #                             stats['char_length_var'],
                        #                             stats['char_length_sd'],
                        #                             stats['char_length_min'],
                        #                             stats['char_length_max'],

                        #                             stats['token_length_arithmetic_mean'],
                        #                             stats['token_length_median'],
                        #                             stats['token_length_var'],
                        #                             stats['token_length_sd'],
                        #                             stats['token_length_min'],
                                                    # stats['token_length_max']])




                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]



            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]


                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                                                                        

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]


    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]




    counts = annotation_statistics.count_mentions(annotations=annotations,
                                                 schema=settings.schema.get_simple_schema(),
                                                 include_features = True)

    for t, stats in counts.items():

        try:

            stat_mention_count_print[annotator_name][t] += stats['count']

        except KeyError:
            try:
                stat_mention_count_print[annotator_name].update({t : stats['count']})

            except KeyError:
                stat_mention_count_print[annotator_name] = {t : stats['count']}

    for anno, counts in collections.OrderedDict(sorted(stat_mention_count_print.items())).items():
        output += '{}\n'.format(
                            ''.join(['{} : {}\n'.format(k, v) for k, v in counts.items()]))

    return output


def entity_token_stats(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    stat_mention_count_print = {}
    total_mention_counts = []
    output = ''

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]



            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]


                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                                                                        

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]


    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]




    counts = annotation_statistics.count_mentions(annotations=annotations,
                                                 schema=settings.schema.get_simple_schema(),
                                                 include_features = False)

    for t, stats in counts.items():

        try:
            token_summary = 'mean ({}) median ({}) sd ({}) min ({}) max ({})'.format(round(stats['token_length_arithmetic_mean']),
                                                                               round(stats['token_length_median']),
                                                                               round(stats['token_length_sd']),
                                                                               round(stats['token_length_min']),
                                                                               round(stats['token_length_max']))
            stat_mention_count_print[annotator_name][t] = token_summary

        except KeyError:
            try:
                stat_mention_count_print[annotator_name].update({t : token_summary})

            except KeyError:
                stat_mention_count_print[annotator_name] = {t : token_summary}

    for anno, counts in collections.OrderedDict(sorted(stat_mention_count_print.items())).items():
        output += '{}\n'.format(
                            ''.join(['{} : {}\n'.format(k, v) for k, v in counts.items()]))

    return output

def entity_with_features_token_stats(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    stat_mention_count_print = {}
    total_mention_counts = []
    output = ''

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]



            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]


                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                                                                        

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]


    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]




    counts = annotation_statistics.count_mentions(annotations=annotations,
                                                 schema=settings.schema.get_simple_schema(),
                                                 include_features = True)

    for t, stats in counts.items():

        try:
            token_summary = 'mean ({}) median ({}) sd ({}) min ({}) max ({})'.format(round(stats['token_length_arithmetic_mean']),
                                                                               round(stats['token_length_median']),
                                                                               round(stats['token_length_sd']),
                                                                               round(stats['token_length_min']),
                                                                               round(stats['token_length_max']))
            stat_mention_count_print[annotator_name][t] = token_summary

        except KeyError:
            try:
                stat_mention_count_print[annotator_name].update({t : token_summary})

            except KeyError:
                stat_mention_count_print[annotator_name] = {t : token_summary}

    for anno, counts in collections.OrderedDict(sorted(stat_mention_count_print.items())).items():
        output += '{}\n'.format(
                            ''.join(['{} : {}\n'.format(k, v) for k, v in counts.items()]))

    return output

def hierarchical_relationship_counts(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    stat_mention_count_print = {}
    total_mention_counts = []
    output = ''

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]


                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]



            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]


                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                                                                        

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                                                                        

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]


    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]

            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]
    if not annotation_type == 'all_types':
        schema = settings.schema.get_type(annotation_type)
    else:
        schema = settings.schema


    counts = annotation_statistics.count_hierarchical_relationships(annotations, schema)

    output = counts
    # for anno, counts in stat_mention_count_print.items():
    #     output += '{}\n{}\n'.format(anno, 
    #                         ''.join(['  {} : {}\n'.format(k, v) for k, v in counts.items()]))

    return output


def generate_statistics_report(filters=[]):

    statistics_path = Path(settings.output_dir / 'statistics')
    statistics_path.mkdir(parents=True, exist_ok=True)

    total_mention_counts = []

    output = ''
    stat_mention_count_print = {}

    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

    counts = annotation_statistics.count_mentions(annotations=annotations,
                                                  schema=settings.schema.get_simple_schema(),
                                                  include_features = False)

    for t, stats in counts.items():

        try:
            token_summary = 'mean ({}) median ({}) sd ({}) min ({}) max ({})'.format(round(stats['token_length_arithmetic_mean']),
                                                                               round(stats['token_length_median']),
                                                                               round(stats['token_length_sd']),
                                                                               round(stats['token_length_min']),
                                                                               round(stats['token_length_max']))
            stat_mention_count_print[t] = token_summary

        except KeyError:
            
            stat_mention_count_print = {t : token_summary}

    for anno, counts in collections.OrderedDict(sorted(stat_mention_count_print.items())).items():
        output += '{} : {}\n'.format(anno,
                            ''.join(['{} \n'.format(counts)]))

    with open(statistics_path / 'statistics_summary.txt', 'w') as text_file:
        text_file.write('{}'.format(output))

    


    for file_name, annotators in settings.corpus.items():
        for annotator, document in annotators.items():
            for set_name, annotations in document['annotation_sets'].items():
                counts = annotation_statistics.count_mentions(annotations=annotations,
                                                             schema=settings.schema.get_simple_schema(),
                                                             include_features = False)

                for t, stats in counts.items():

                    total_mention_counts.append([file_name, annotator, set_name, 
                                                t,
                                                stats['count'],
                                                stats['char_length_arithmetic_mean'],
                                                stats['char_length_median'],
                                                stats['char_length_var'],
                                                stats['char_length_sd'],
                                                stats['char_length_min'],
                                                stats['char_length_max'],
                                                stats['token_length_arithmetic_mean'],
                                                stats['token_length_median'],
                                                stats['token_length_var'],
                                                stats['token_length_sd'],
                                                stats['token_length_min'],
                                                stats['token_length_max']])

    mention_features_counts_report = pd.DataFrame(total_mention_counts, 
                                           columns = ['file_name', 'annotator', 'set_name',
                                                      'annotation_type',
                                                      'count',
                                                      'char_length_arithmetic_mean',
                                                      'char_length_median',
                                                      'char_length_var',
                                                      'char_length_sd',
                                                      'char_length_min',
                                                      'char_length_max',
                                                      'token_length_arithmetic_mean',
                                                      'token_length_median',
                                                      'token_length_var',
                                                      'token_length_sd',
                                                      'token_length_min',
                                                      'token_length_max'])

    mention_features_counts_report.to_csv(statistics_path / 'statistics_report.csv', index=False)



    return 'report generated in {}'.format(settings.output_dir)
