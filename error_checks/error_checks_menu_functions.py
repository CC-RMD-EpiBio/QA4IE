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
from error_checks import document_errors
from pathlib import Path


def check_text_differences(filters=[]):

    # 1) filter data based on filters
    #   -   possible filters
    #       files = ['all_files', list of individual files]
    #       pairs = ['all annotators', list of pairs]
    #       filters = [file, pair]
    # 2) run THIS qa function
    # 3) return string of output
    #
    
    # total_text_section_differences = []

    if filters[0].title == 'corpus':
        count = 0
        if filters[1].title == 'team':

            
            for file_name, annotators in settings.corpus.items():
                for anno_1, anno_2 in combinations(annotators, 2):
                    text_conflicts = document_errors.compare_texts(annotators[anno_1]['text'], 
                                                                   annotators[anno_2]['text'])
                    if text_conflicts:
                        count += 1
            if count:
                return 'Text differences found'
            else:
                return 'No text differences found'

            
        else:
            
            for file_name, annotators in settings.corpus.items():
                anno_1, anno_2 = filters[1].title.split('-')
                text_conflicts = document_errors.compare_texts(annotators[anno_1]['text'], 
                                                               annotators[anno_2]['text'])
                if text_conflicts:
                    count += 1

            if count:
                return 'Text differences found'
            else:
                return 'No text differences found'
                        
    else:
        if filters[1].title == 'team':
            count = 0
            for anno_1, anno_2 in combinations(settings.corpus[filters[0].title],2):
                text_conflicts = document_errors.compare_texts(settings.corpus[filters[0].title][anno_1]['text'], 
                                                               settings.corpus[filters[0].title][anno_2]['text'])
                if text_conflicts:
                    count += 1
            if count:
                return 'Text differences found'
            else:
                return 'No text differences found'
        else:
            anno_1, anno_2 = filters[1].title.split('-')
            text_conflicts = document_errors.compare_texts(settings.corpus[filters[0].title][anno_1]['text'], 
                                                           settings.corpus[filters[0].title][anno_2]['text'])

            if text_conflicts:
           
                return 'Text differences found'
            else:
                return 'No text differences found'


def check_set_name_differences(filters=[]):

    # 1) filter data based on filters
    #   -   possible filters
    #       files = ['all_files', list of individual files]
    #       pairs = ['all annotators', list of pairs]
    #       filters = [file, pair]
    # 2) run THIS qa function
    # 3) return string of output
    if filters[0].title == 'corpus':
        count = 0
        if filters[1].title == 'team':
            for file_name, annotators in settings.corpus.items():
                for anno_1, anno_2 in combinations(annotators, 2):

                    set_name_conflicts = document_errors.compare_set_names(annotators[anno_1]['annotation_sets'].keys(), 
                                                                           annotators[anno_2]['annotation_sets'].keys())

                    if set_name_conflicts:
                        count += 1

            if count:
                return 'Set name differences found'
            else:
                return 'No set name differences found'

            
        else:
            
            for file_name, annotators in settings.corpus.items():
                anno_1, anno_2 = filters[1].title.split('-')
                set_name_conflicts = document_errors.compare_set_names(annotators[anno_1]['annotation_sets'].keys(), 
                                                                       annotators[anno_2]['annotation_sets'].keys())

                if set_name_conflicts:
                    count += 1

            if count:
                return 'Set name differences found'
            else:
                return 'No set name differences found'
                        
    else:
        count = 0
        if filters[1].title == 'team':
            for anno_1, anno_2 in combinations(settings.corpus[filters[0].title],2):
                set_name_conflicts = document_errors.compare_set_names(settings.corpus[filters[0].title][anno_1]['annotation_sets'].keys(), 
                                                                       settings.corpus[filters[0].title][anno_2]['annotation_sets'].keys())

                if set_name_conflicts:
                    count += 1
            if count:
                return 'Set name differences found'
            else:
                return 'No set name differences found'
        else:
            anno_1, anno_2 = filters[1].title.split('-')
            set_name_conflicts = document_errors.compare_set_names(settings.corpus[filters[0].title][anno_1]['annotation_sets'].keys(), 
                                                                   settings.corpus[filters[0].title][anno_2]['annotation_sets'].keys())

            if set_name_conflicts:
                return 'Set name differences found'
            else:
                return 'No set name differences found'


def generate_error_checks_report():

    # 1) run this error check report
    # 3) return string of output

    
    error_checks_path = Path(settings.output_dir / 'document_validations')
    error_checks_path.mkdir(parents=True, exist_ok=True)
    try:
        for file_name, annotators in settings.corpus.items():
            for anno_1, anno_2 in combinations(annotators, 2):
                text_conflicts = document_errors.compare_texts(annotators[anno_1]['text'], 
                                                               annotators[anno_2]['text'])

                if text_conflicts:
                    txt_path = error_checks_path / 'txt_differences' 
                    txt_path.mkdir(parents=True, exist_ok=True)
                    with open(txt_path / '{}_{}-{}.txt'.format(file_name, anno_1, anno_2), 'w') as txt_file:
                        print('\n'.join([t for t in text_conflicts]), file=txt_file)

        for file_name, annotators in settings.corpus.items():
            for anno_1, anno_2 in combinations(annotators, 2):
                set_name_conflicts = document_errors.compare_set_names(annotators[anno_1]['annotation_sets'].keys(), 
                                                                       annotators[anno_2]['annotation_sets'].keys())
                
                if set_name_conflicts:
                    txt_path = error_checks_path / 'set_name_differences' 
                    txt_path.mkdir(parents=True, exist_ok=True)
                    with open(txt_path / '{}_{}-{}.txt'.format(file_name, anno_1, anno_2), 'w') as txt_file:
                        print(', '.join([s for s in set_name_conflicts]), file=txt_file)

    except BlockingIOError as e:
        return '{}'.format(str(e))



    return 'report generated in {}'.format(settings.output_dir)
    
