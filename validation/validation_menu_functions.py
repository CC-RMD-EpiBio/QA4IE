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
from pathlib import Path
import pandas as pd


def validate_overlaps(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    overlaps_to_validate = {}

    for n, ovlps in settings.schema.get_overlaps().items():
        ovlps = [str(o) for o in ovlps]
        ovlps = [str(e) for e in settings.schema.get_entity_names() if not e in ovlps]
        overlaps_to_validate[n] = ovlps

    if annotation_type == 'all_types': # all annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)


                          for x,y in overlaps.items():
                              if y:
                                  count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                else: # individual annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)



                          for x,y in overlaps.items():
                              if y:
                                  count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)

                          

                          for x,y in overlaps.items():
                              if y:
                                  count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'                  
                else: # individual annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)


                          for x,y in overlaps.items():
                              if y:
                                  count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          overlaps_to_validate)
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          overlaps_to_validate)
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          overlaps_to_validate)
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'                                                        
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          overlaps_to_validate)
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'

                    

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)

                          
                          
                          for x, y in overlaps.items():
                            if y:

                                count += 1
                     
                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                else: # individual annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)

                         
                          for x,y in overlaps.items():
                              if y:
                                  count += 1


                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)

                         
                          for x,y in overlaps.items():
                              if y:
                                  count += 1


                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                else: # individual annotation sets
                    count = 0
                    for f, a_c in settings.corpus.items():
                      for a_name, d_c in a_c.items():
                        for s, annotations in d_c['annotation_sets'].items():

                          overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                                overlaps_to_validate)

                               
                          for x,y in overlaps.items():
                              if y:
                                  count += 1


                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    count = 0
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          {annotation_type:overlaps_to_validate[annotation_type]})
                    

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          {annotation_type:overlaps_to_validate[annotation_type]})
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          {annotation_type:overlaps_to_validate[annotation_type]})
                    count = 0

                    for x,y in overlaps.items():
                        if y:
                            count += 1

                    if count:
                        return 'Annotation overlaps found'

                    else:
                        return 'No annotation overlaps found'

                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    overlaps = annotation_validations.annotation_overlaps(annotations, 
                                                                          {annotation_type:overlaps_to_validate[annotation_type]})
                    count = 0
                    output = ''
                    overlap_count = 1
                    for x, y in overlaps.items():
                        if y:
                            count +=1
                            for overlap in y:
                                output += 'overlap cluster: {}\n{}\n'.format(overlap_count, '-' * 18)
                                overlap_count += 1
                                for annotation in overlap:
                               
                                    output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                                                                          annotation['start'],
                                                                          annotation['end'],
                                                                          annotation['text_span'])

                    if count:
                        return 'Annotation overlaps found'
                   
                    else:
                        return 'No annotation overlaps found'
                        
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
                
                    #sub_entities = [e for e in settings.schema.entities if e.is_subentity()]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1


                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1


                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]


                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.outbound_subentities(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                       
                        output = ''
                       
                        if conflicts:
                            count+= 1
                        for n, conflict in conflicts.items():
                            
                            for annotation in conflict:
                                   
                                output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                                                                      annotation['start'],
                                                                      annotation['end'],
                                                                      annotation['text_span'])
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1
                        for n, conflict in conflicts.items():
                          
                          for annotation in conflict:
                                 
                              output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                                                                    annotation['start'],
                                                                    annotation['end'],
                                                                    annotation['text_span'])


                    if count:
                        return 'Out of bounds sub-entities found'
                    else:
                        return 'No out of bounds sub-entities found'

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

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1
                    #print(conflicts)
                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #print(conflicts)
                        if conflicts:
                            count += 1

                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if 
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    count = 0
                    for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                        conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                         main_type = e.name, 
                                                         sub_entities = e.get_sub_entity_names())
                        #conflict_count = 0
                        output = ''
                        if annotation_type in list(conflicts.keys()):
                            conflicts = {annotation_type:conflicts[annotation_type]}
                        else:
                            conflicts = {}
                        if conflicts:
                            count+= 1
                        for n, conflict in conflicts.items():
                            
                            for annotation in conflict:
                                   
                                output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                                                                      annotation['start'],
                                                                      annotation['end'],
                                                                      annotation['text_span'])


                    if count:
                        return 'Sub-entity partial overlaps found'
                    else:
                        return 'No sub-entity partial overlaps found'

def validate_annotation_scope(filters=[]):

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
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                        if conflicts:
                            count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        if s == annotation_set:
                          conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                          if conflicts:
                              count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                          if conflicts:
                              count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                       
                        for s, ans in d_c['annotation_sets'].items():
                          
                          conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                          if conflicts:
                              count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                          
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          ans = [a for a in ans if a['mention'] == annotation_type]
                          conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                          if conflicts:
                              count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                      
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                            if conflicts:
                                count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items():
                    if f == file:
                      for a_name, d_c in a_c.items():
                        
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              if s == annotation_set:
                                ans = [a for a in ans if a['mention'] == annotation_type]
                                conflicts = annotation_validations.validate_annotation_scope(ans, d_c['text'])
                                if conflicts:
                                    count += 1

                  if count:
                      return 'Document Scope Issues found'
                  else:
                      return 'No document Scope Issues found'
                        #conflict_count = 0
                    #     output = ''
                    #     if annotation_type in list(conflicts.keys()):
                    #         conflicts = {annotation_type:conflicts[annotation_type]}
                    #     else:
                    #         conflicts = {}
                    #     if conflicts:
                    #         count+= 1
                    #     for n, conflict in conflicts.items():
                            
                    #         for annotation in conflict:
                                   
                    #             output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                    #                                                   annotation['start'],
                    #                                                   annotation['end'],
                    #                                                   annotation['text_span'])


                    # if count:
                    #     return 'Sub-entity partial overlaps found'
                    # else:
                    #     return 'No sub-entity partial overlaps found'
  
def validate_annotation_zero_length(filters=[]):

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
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        conflicts = annotation_validations.validate_zero_length(ans)
                        if conflicts:
                            count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        if s == annotation_set:
                          conflicts = annotation_validations.validate_zero_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          conflicts = annotation_validations.validate_zero_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                       
                        for s, ans in d_c['annotation_sets'].items():
                          
                          conflicts = annotation_validations.validate_zero_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                          
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              conflicts = annotation_validations.validate_zero_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          ans = [a for a in ans if a['mention'] == annotation_type]
                          conflicts = annotation_validations.validate_zero_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_zero_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                      
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_zero_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items():
                    if f == file:
                      for a_name, d_c in a_c.items():
                        
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_zero_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_zero_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              if s == annotation_set:
                                ans = [a for a in ans if a['mention'] == annotation_type]
                                conflicts = annotation_validations.validate_zero_length(ans)
                                if conflicts:
                                    count += 1

                  if count:
                      return 'Zero length issues found'
                  else:
                      return 'No zero length issues found'
                        #conflict_count = 0
                    #     output = ''
                    #     if annotation_type in list(conflicts.keys()):
                    #         conflicts = {annotation_type:conflicts[annotation_type]}
                    #     else:
                    #         conflicts = {}
                    #     if conflicts:
                    #         count+= 1
                    #     for n, conflict in conflicts.items():
                            
                    #         for annotation in conflict:
                                   
                    #             output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                    #                                                   annotation['start'],
                    #                                                   annotation['end'],
                    #                                                   annotation['text_span'])


                    # if count:
                    #     return 'Sub-entity partial overlaps found'
                    # else:
                    #     return 'No sub-entity partial overlaps found'
    
def validate_annotation_negative_length(filters=[]):

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
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        conflicts = annotation_validations.validate_negative_length(ans)
                        if conflicts:
                            count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      for s, ans in d_c['annotation_sets'].items():
                        if s == annotation_set:
                          conflicts = annotation_validations.validate_negative_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          conflicts = annotation_validations.validate_negative_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    for a_name, d_c in a_c.items(): 
                      if a_name == annotator_name:
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                  
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                       
                        for s, ans in d_c['annotation_sets'].items():
                          
                          conflicts = annotation_validations.validate_negative_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        
                        for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                          
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              conflicts = annotation_validations.validate_negative_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          ans = [a for a in ans if a['mention'] == annotation_type]
                          conflicts = annotation_validations.validate_negative_length(ans)
                          if conflicts:
                              count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      
                      for s, ans in d_c['annotation_sets'].items():
                          if s == annotation_set:
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                  
                    for a_name, d_c in a_c.items(): 
                      if annotator_name == a_name:
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_negative_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                      
                        for s, ans in d_c['annotation_sets'].items():
                            ans = [a for a in ans if a['mention'] == annotation_type]
                            conflicts = annotation_validations.validate_negative_length(ans)
                            if conflicts:
                                count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items():
                    if f == file:
                      for a_name, d_c in a_c.items():
                        
                        for s, ans in d_c['annotation_sets'].items():
                            if s == annotation_set:
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_negative_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              ans = [a for a in ans if a['mention'] == annotation_type]
                              conflicts = annotation_validations.validate_negative_length(ans)
                              if conflicts:
                                  count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                else: # individual annotation sets
                  count = 0
                  for f, a_c in settings.corpus.items(): 
                    if f == file:
                      for a_name, d_c in a_c.items(): 
                        if a_name == annotator_name:
                          for s, ans in d_c['annotation_sets'].items():
                              if s == annotation_set:
                                ans = [a for a in ans if a['mention'] == annotation_type]
                                conflicts = annotation_validations.validate_negative_length(ans)
                                if conflicts:
                                    count += 1

                  if count:
                      return 'Negative length issues found'
                  else:
                      return 'No negative length issues found'
                        #conflict_count = 0
                    #     output = ''
                    #     if annotation_type in list(conflicts.keys()):
                    #         conflicts = {annotation_type:conflicts[annotation_type]}
                    #     else:
                    #         conflicts = {}
                    #     if conflicts:
                    #         count+= 1
                    #     for n, conflict in conflicts.items():
                            
                    #         for annotation in conflict:
                                   
                    #             output += '\n{} ({}-{})\n{}\n'.format(annotation['mention'],
                    #                                                   annotation['start'],
                    #                                                   annotation['end'],
                    #                                                   annotation['text_span'])


                    # if count:
                    #     return 'Sub-entity partial overlaps found'
                    # else:
                    #     return 'No sub-entity partial overlaps found'

def validate_annotation_boundaries(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    sets_with_types = {}
    all_sets = list(set([s for f, a_c in settings.corpus.items() 
                  for a_name, d_c in a_c.items() 
                  for s, ans in d_c['annotation_sets'].items()
                  ]))

    # for set_ in all_sets:
    #   sets_with_types[set_] = []
    count = 0
    out = ''
    if file == 'corpus':
      for f, a_c in settings.corpus.items(): 
        for a_name, d_c in a_c.items():
          temp = []

          for s, ans in d_c['annotation_sets'].items():
            if s == 'default_annotation_set':
              if len(ans) > 0:
                count += 1
            
            temp.append(list(set([a['mention'] for a in ans])))

          for x in temp[0]:
            
              # out += '{}\n'.format(' '.join([y for x in temp[1:] for y in x]))
            if x in [y for x in temp[1:] for y in x]:
              count += 1
    else:
        for f, a_c in settings.corpus.items(): 
          if f == file:
            for a_name, d_c in a_c.items():
              temp = []
              for s, ans in d_c['annotation_sets'].items():
                if s == 'default_annotation_set':
                  if len(ans) > 0:
                    count += 1
                temp.append(list(set([a['mention'] for a in ans])))

              for x in temp[0]:
                
                  # out += '{}\n'.format(' '.join([y for x in temp[1:] for y in x]))
                if x in [y for x in temp[1:] for y in x]:
                  count += 1

    if count:
      out += 'Annotation boundaries found\n'
    else:
      out += 'No annotation boundaries found\n'

    return out


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

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if s == annotation_set]


                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans  if a_name == annotator_name]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans     if a_name == annotator_name and
                                                         s == annotation_set]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if f == file]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans        if f == file and
                                                            s == annotation_set]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if f == file and
                                                               a_name == annotator_name]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans    if f == file and
                                                        a_name == annotator_name and
                                                        s == annotation_set]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'

    else: # individual annotation types
        if file == 'corpus': # all notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans if a['mention'] == annotation_type]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            s == annotation_set]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans           if a['mention'] == annotation_type and
                                                               a_name == annotator_name]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans        if a['mention'] == annotation_type and
                                                            a_name == annotator_name and
                                                            s == annotation_set]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                
        else: # individual notes
            if annotator_name == 'team': # all annotators
                if annotation_set == 'all_sets': # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() 
                                     for a in ans               if a['mention'] == annotation_type and
                                                                f == file and
                                                                s == annotation_set]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
            else: # individual annotators
                if annotation_set == 'all_sets':  # all annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items() \
                                     for a in ans    if a['mention'] == annotation_type and
                                                        f == file and
                                                        a_name == annotator_name]
                    count = 0
                    schema = settings.schema.get_simple_schema()
                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    #print(conflicts)
                    if conflicts:
                        count += 1

                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'
                else: # individual annotation sets
                    annotations = [a for f, a_c in settings.corpus.items() 
                                     for a_name, d_c in a_c.items() 
                                     for s, ans in d_c['annotation_sets'].items()
                                     for a in ans                if a['mention'] == annotation_type and
                                                                    f == file and
                                                                    a_name == annotator_name and 
                                                                    s == annotation_set]

                    count = 0
                    schema = settings.schema.get_simple_schema()

                    conflicts = annotation_validations.validate_schema(annotations, schema)
                                                                        
                    output = ''
                    if annotation_type in list(conflicts.keys()):
                        conflicts = {annotation_type:conflicts[annotation_type]}
                    else:
                        conflicts = {}
                    if conflicts:
                        count+= 1
                    for n, conflict in conflicts.items():
                        
                        for annotation in conflict:
                               
                            output += '\n{} ({}-{})\n{}\n{}\n'.format(annotation['mention'],
                                                                  annotation['start'],
                                                                  annotation['end'],
                                                                  annotation['text_span'],
                                                                  annotation['features'])


                    if count:
                        return 'Invalid annotations found'
                    else:
                        return 'No invalid annotations found'


def generate_validation_report():

    validation_path = Path(settings.output_dir / 'annotation_validations')
    validation_path.mkdir(parents=True, exist_ok=True)
    overlaps_to_validate = {}
    total_overlaps = []
    total_annotation_boundaries = []
    total_outbound_subentities = []
    total_subentity_partial_overlaps = []
    total_invalid_annotations = []
    total_document_scope = []
    total_negative_length = []
    total_zero_length = []
    total_document_scope = []

    for n, ovlps in settings.schema.get_overlaps().items():
        ovlps = [str(o) for o in ovlps]
        ovlps = [str(e) for e in settings.schema.get_entity_names() if not e in ovlps]
        overlaps_to_validate[n] = ovlps

    for file_name, annotators in settings.corpus.items():
        for annotator, document in annotators.items():
                          # for set_ in all_sets:
                #   sets_with_types[set_] = []
          

          temp = []
          for s, ans in document['annotation_sets'].items():
            
            temp.append(list(set([a['mention'] for a in ans])))

            if s == 'default_annotation_set':
              if len(ans) > 0:
                for x in ans:
                  total_annotation_boundaries.append([file_name, annotator, s, x['mention']])



          for x in temp[0]:
            
              # out += '{}\n'.format(' '.join([y for x in temp[1:] for y in x]))

            if x in [y for x in temp[1:] for y in x]:
              if not [file_name, annotator, set_name, x] in total_annotation_boundaries:
                total_annotation_boundaries.append([file_name, annotator, set_name, x])

              
          

          for set_name, annotations in document['annotation_sets'].items():
              overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                    annotation_types = overlaps_to_validate)
              
              for t, o in overlaps.items():
                  if o:
                      for x in o:
                          total_overlaps.append([file_name, annotator, set_name, t, x])

              for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                      conflicts = annotation_validations.outbound_subentities(annotations, 
                                                       main_type = e.name, 
                                                       sub_entities = e.get_sub_entity_names())
                      for n, e in conflicts.items():
                          total_outbound_subentities.append([file_name, annotator, set_name, n, e])

              for e in [e for n, e in settings.schema.entities.items() if e.is_parent_entity()]:
                      conflicts = annotation_validations.partial_subentity_overlap(annotations, 
                                                       main_type = e.name, 
                                                       sub_entities = e.get_sub_entity_names())
                      for n, e in conflicts.items():
                          total_subentity_partial_overlaps.append([file_name, annotator, set_name, n, e])


              conflicts = annotation_validations.validate_annotation_scope(annotations, document['text'])

              for n, e in conflicts.items():
                  total_document_scope.append([file_name, annotator, set_name, n, e])

              
              conflicts = annotation_validations.validate_negative_length(annotations)

              for n, e in conflicts.items():
                  total_negative_length.append([file_name, annotator, set_name, n, e])

              conflicts = annotation_validations.validate_zero_length(annotations)

              for n, e in conflicts.items():
                  total_zero_length.append([file_name, annotator, set_name, n, e])


              all_sets = list(set([s for f, a_c in settings.corpus.items() 
                            for a_name, d_c in a_c.items() 
                            for s, ans in d_c['annotation_sets'].items()
                            ]))


                      

              schema = settings.schema.get_simple_schema()
              conflicts = annotation_validations.validate_schema(annotations, schema)
              for n, e in conflicts.items():
                  total_invalid_annotations.append([file_name, annotator, set_name, n, e])

      
    overlap_report = pd.DataFrame(total_overlaps, columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'overlaps'])

    outbound_report = pd.DataFrame(total_annotation_boundaries, columns = ['file_name', 'annotator', 
                                                         'set_name', 'annotation_type'])

    sub_entity_outbound_report = pd.DataFrame(total_outbound_subentities, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'outbound_subentities'])

    document_scope_report = pd.DataFrame(total_document_scope, 
                                              columns = ['file_name', 'annotator', 
                                                         'set_name', 'annotation_type',
                                                         'document_scope'])

    sub_entity_partial_overlap_report = pd.DataFrame(total_subentity_partial_overlaps, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'sub_entity_partial_overlap'])

    invalid_annotations_report = pd.DataFrame(total_invalid_annotations, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'invalid_annotations'])

    zero_length_report = pd.DataFrame(total_zero_length, 
                                              columns = ['file_name', 'annotator', 
                                                         'set_name', 'annotation_type',
                                                         'zero_length'])
    negative_length_report = pd.DataFrame(total_negative_length, 
                                              columns = ['file_name', 'annotator', 
                                                         'set_name', 'annotation_type',
                                                         'negative_length'])
    try:
      with open(validation_path / 'annotation_validation_summary.txt', 'w') as text_file:
        text_file.write('{} : {} \n'.format('overlaps', len(total_overlaps)))
        text_file.write('{} : {} \n'.format('sub entity boundaries', len(total_outbound_subentities)))
        text_file.write('{} : {} \n'.format('document scope', len(total_document_scope)))
        text_file.write('{} : {} \n'.format('sub entity partial overlaps', len(total_subentity_partial_overlaps)))
        text_file.write('{} : {} \n'.format('invalid annotations', len(total_invalid_annotations)))
        text_file.write('{} : {} \n'.format('zero length annotations', len(total_zero_length)))
        text_file.write('{} : {} \n'.format('negative length annotations', len(total_negative_length)))    
        text_file.write('{} : {} \n'.format('annotation boundaries', len(total_annotation_boundaries)))  
      overlap_report.to_csv(validation_path  / 'overlap_report.csv', index=False)
      outbound_report.to_csv(validation_path  / 'out_of_bound_annotations_report.csv', index=False)
      zero_length_report.to_csv(validation_path  / 'zero_length_report.csv', index=False)
      negative_length_report.to_csv(validation_path  / 'negative_length_report.csv', index=False)
      document_scope_report.to_csv(validation_path  / 'document_scope_report.csv', index=False)
      sub_entity_outbound_report.to_csv(validation_path  / 'out_of_boundary_sub_entity_report.csv', index=False)
      sub_entity_partial_overlap_report.to_csv(validation_path  / 'sub_entity_partial_overlap_report.csv', index=False)
      invalid_annotations_report.to_csv(validation_path  / 'invalid_annotation_report.csv', index=False)

      return 'report generated in {}'.format(settings.output_dir)
    except BlockingIOError as e:
        return '{}'.format(str(e))
    


