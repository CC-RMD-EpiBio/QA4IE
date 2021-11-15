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
                                     for a in ans       if a['mention'] == annotation_type and
                                                           f == file]

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
                        #conflict_count = 0
                        output = ''
                       
                        if conflicts:
                            count+= 1
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

    validation_path = Path(settings.output_dir / 'validations')
    validation_path.mkdir(parents=True, exist_ok=True)
    overlaps_to_validate = {}
    total_overlaps = []
    total_outbound_subentities = []
    total_subentity_partial_overlaps = []
    total_invalid_annotations = []

    for n, ovlps in settings.schema.get_overlaps().items():
        ovlps = [str(o) for o in ovlps]
        ovlps = [str(e) for e in settings.schema.get_entity_names() if not e in ovlps]
        overlaps_to_validate[n] = ovlps

    for file_name, annotators in settings.corpus.items():
        for annotator, document in annotators.items():
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

                schema = settings.schema.get_simple_schema()
                conflicts = annotation_validations.validate_schema(annotations, schema)
                for n, e in conflicts.items():
                    total_invalid_annotations.append([file_name, annotator, set_name, n, e])
                        
    overlap_report = pd.DataFrame(total_overlaps, columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'overlaps'])

    sub_entity_outbound_report = pd.DataFrame(total_outbound_subentities, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'overlaps'])

    sub_entity_partial_overlap_report = pd.DataFrame(total_subentity_partial_overlaps, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'overlaps'])

    invalid_annotations_report = pd.DataFrame(total_invalid_annotations, 
                                                  columns = ['file_name', 'annotator', 
                                                             'set_name', 'annotation_type',
                                                             'overlaps'])

    # #out_of_bounds_annotations_report = out_bound_annotation(print_results=False)


   
    writer = pd.ExcelWriter(validation_path / 'validation_report.xlsx', engine='xlsxwriter')

    
    overlap_report.to_excel(writer, sheet_name='overlaps', index=False)
    sub_entity_outbound_report.to_excel(writer, sheet_name='outbounds_sub_entity', index=False)
    sub_entity_partial_overlap_report.to_excel(writer, sheet_name='sub_entity_partial_overlap', index=False)
    invalid_annotations_report.to_excel(writer, sheet_name='invalid_annotations', index=False)
    writer.save()

    return 'report generated in {}'.format(settings.output_dir)


