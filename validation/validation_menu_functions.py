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
from validation import annotation_validations



def validate_overlaps(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    return ''

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    # h = settings.schema.get_type(annotation_type)    
                    # if annotations:                                           

                    #     if h.has_sub_entities():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.name,
                    #                                                                             h.get_sub_entity_names())
                    #         print(partial_overlaps)
                    #     elif h.has_parent_entity():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.get_parent_entity_name(),
                    #                                                                             [h.name])
                    #         print(partial_overlaps)
                    return ''
                        
def validate_subentity_boundaries(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    return ''

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    # h = settings.schema.get_type(annotation_type)    
                    # if annotations:                                           

                    #     if h.has_sub_entities():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.name,
                    #                                                                             h.get_sub_entity_names())
                    #         print(partial_overlaps)
                    #     elif h.has_parent_entity():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.get_parent_entity_name(),
                    #                                                                             [h.name])
                    #         print(partial_overlaps)
                    return ''





def validate_subentity_partial_overlap(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    return ''

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    h = settings.schema.get_type(annotation_type)    
                    if annotations:                                           

                        if h.has_sub_entities():
                            partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                                                                                                h.name,
                                                                                                h.get_sub_entity_names())
                            print(partial_overlaps)
                        elif h.has_parent_entity():
                            partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                                                                                                h.get_parent_entity_name(),
                                                                                                [h.name])
                            print(partial_overlaps)
                    return ''


    

def validate_annotation_boundaries(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    return ''

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    # h = settings.schema.get_type(annotation_type)    
                    # if annotations:                                           

                    #     if h.has_sub_entities():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.name,
                    #                                                                             h.get_sub_entity_names())
                    #         print(partial_overlaps)
                    #     elif h.has_parent_entity():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.get_parent_entity_name(),
                    #                                                                             [h.name])
                    #         print(partial_overlaps)
                    return ''


def validate_schema_values(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                    for a_name, d_c in a_c.items() 
                                    for s, ans in d_c['annotation_sets'].items()
                                    for a in ans]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    return ''

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    return ''
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    return ''
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    return ''
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    # h = settings.schema.get_type(annotation_type)    
                    # if annotations:                                           

                    #     if h.has_sub_entities():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.name,
                    #                                                                             h.get_sub_entity_names())
                    #         print(partial_overlaps)
                    #     elif h.has_parent_entity():
                    #         partial_overlaps = annotation_validations.partial_subentity_overlap(annotations, 
                    #                                                                             h.get_parent_entity_name(),
                    #                                                                             [h.name])
                    #         print(partial_overlaps)
                    return ''


def generate_validation_report():

    # 1) run this qa report
    # 3) return string of output
    pass


