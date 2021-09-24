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
    #       files = [all_files, list of individual files]
    #       annotators = [all_annotators, list of individual annotators]
    #       annotation_type = [all_types, list of individual types]
    #       filters = [file, annotator, annotation_type]
    # 2) run THIS qa function
    # 3) return string of output
    overlaps_to_validate = {}
    for ent, values in settings.schema.items():
        overlaps_to_validate[ent] = values['overlaps']

        for e in values['overlaps']:
            if e in settings.schema.keys():
                if 'sub_entities' in settings.schema[e].keys():
                    overlaps_to_validate[ent] += list(settings.schema[e]['sub_entities'].keys())

        if 'sub_entities' in values.keys():
            overlaps_to_validate[ent] += list(values['sub_entities'].keys())
            for sub_ent, sub_values in values['sub_entities'].items():
                overlaps_to_validate[sub_ent] = [ent] + values['overlaps'] +sub_values['overlaps']


    for k, v in overlaps_to_validate.items():
        overlaps_to_validate[k] = list(set(overlaps_to_validate.keys()) - set(overlaps_to_validate[k]))


    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title

    # 'all_sets' + individual sets
    if file == 'corpus':
        count = 0
        if annotator_name == 'team':

            if annotation_set == 'all_sets':
                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        for set_name, annotations in document['annotation_sets'].items():
                            overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                  annotation_types = overlaps_to_validate)

                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            
                            else:
                                if [o for t,o in overlaps.items() if o]:
                                    count += 1
                if annotation_type == 'all_types':             
                    if count:
                        return 'overlap issues found in all sets between all annotators in corpus'
                    else:
                        return 'no overlap issues found all sets between all annotators in corpus'
                else:
                    if count:
                        return '{} overlap issues found in all sets between all annotators in corpus'.format(annotation_type)
                    else:
                        return 'no {} overlap issues found all sets between all annotators in corpus'.format(annotation_type)
            else:

                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        if annotation_set in settings.corpus[file_name][annotator]['annotation_sets'].keys():
                            annotations = document['annotation_sets'][annotation_set]
                            overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                  annotation_types = overlaps_to_validate)


                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            else:
                                if [o for t,o in overlaps.items() if o]:
                                    count += 1
                            
        
                if annotation_type == 'all_types':             
                    if count:
                        return 'overlap issues found in {} between all annotators in corpus'.format(annotation_set)
                    else:
                        return 'no overlap issues found {} between all annotators in corpus'.format(annotation_set)
                else:
                    if count:
                        return '{} overlap issues found in {} between all annotators in corpus'.format(annotation_type,
                                                                                                       annotation_set)
                    else:
                        return 'no {} overlap issues found {} between all annotators in corpus'.format(annotation_type,
                                                                                                       annotation_set)

        else:
            count = 0
            if annotation_set == 'all_sets':
                for file_name, annotators in settings.corpus.items():
                    for set_name, annotations in annotators[annotator_name]['annotation_sets'].items():
                            overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                  annotation_types = overlaps_to_validate)

                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            else:
                                if [ o for t,o in overlaps.items() if o]:
                                    count += 1
                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found for {} in corpus'.format(annotation_type, 
                                                                                 annotator_name)
                    else:
                        return 'overlap issues found for {} in corpus'.format(annotator_name)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found for {} in corpus'.format(annotation_type, 
                                                                                    annotator_name)
                    else:
                        return 'no overlap issues found for {} in corpus'.format(annotator_name)

            else:
                
                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        if annotation_set in settings.corpus[file_name][annotator_name]['annotation_sets'].keys():
                            if annotation_set in settings.corpus[file_name][annotator_name]['annotation_sets'].keys():
                                annotations = annotators[annotator_name]['annotation_sets'][annotation_set]
                                overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                      annotation_types = overlaps_to_validate)

                                if not annotation_type == 'all_types':
                                    overlaps = overlaps[annotation_type]
                                    if overlaps:
                                        count += 1
                                else:
                                    if [o for t,o in overlaps.items() if o]:
                                        count += 1
                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found for {} on set {} in corpus'.format(annotation_type, 
                                                                                           annotator_name, 
                                                                                           annotation_set)
                    else:
                        return 'overlap issues found for {} on set {} in corpus'.format(annotator_name, 
                                                                                        annotation_set)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found for {} on set {} in corpus'.format(annotation_type, 
                                                                                              annotator_name, 
                                                                                              annotation_set)
                    else:
                        return 'no overlap issues found for {} on set {} in corpus'.format(annotator_name, 
                                                                                           annotation_set)
    else:
        count = 0
        if annotator_name == 'team':
            if annotation_set == 'all_sets':
                for annotator, document in settings.corpus[file].items():
                    for set_name, annotations in document['annotation_sets'].items():
                        overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                              annotation_types = overlaps_to_validate)

                        if not annotation_type == 'all_types':
                            overlaps = overlaps[annotation_type]
                            if overlaps:
                                count += 1
                        else:
                            if [o for t,o in overlaps.items() if o]:
                                count += 1

                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found between all annotators in file {}'.format(annotation_type, 
                                                                                                  file)
                    else:
                        return 'overlap issues found between all annotators in file {}'.format(file)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found between all annotators in file {}'.format(annotation_type, 
                                                                                                     file)
                    else:
                        return 'no overlap issues found between all annotators in file {}'.format(file)
            else:
                for annotator, document in settings.corpus[file].items():
                    if annotation_set in document['annotation_sets'].keys():
                        annotations = settings.corpus[file][annotator]['annotation_sets'][annotation_set]

                        overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                              annotation_types = overlaps_to_validate)

                        if not annotation_type == 'all_types':
                            overlaps = overlaps[annotation_type]
                            if overlaps:
                                count += 1
                        else:
                            if [o for t,o in overlaps.items() if o]:
                                count += 1

                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found between all annotators for the set {} in file {}'.format(annotation_type, 
                                                                                                                annotation_set,
                                                                                                                file)
                    else:
                        return 'overlap issues found between all annotators for the set {} in file {}'.format(file, 
                                                                                                              annotation_set)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found between all annotators for the set {} in file {}'.format(annotation_type, 
                                                                                                                    annotation_set,
                                                                                                                    file)
                    else:
                        return 'no overlap issues found between all annotators for the set {} in file {}'.format(file, 
                                                                                                                 annotation_set)
        else:

            if not annotation_set == 'all_sets':
                
                if annotation_set in settings.corpus[file][annotator_name]['annotation_sets'].keys():
                    annotations = settings.corpus[file][annotator_name]['annotation_sets'][annotation_set]
                    overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                          annotation_types = overlaps_to_validate)
                        
                    if not annotation_type == 'all_types':
                        overlaps = overlaps[annotation_type]
                        count = 1
                        out = ''
                        if overlaps:
                            for overlaping_annotations in overlaps:
                                out += 'overlap group ({})\n'.format(count)
                                out += '-'*20
                                out += '\n'
                                for overlap in overlaping_annotations:
                                    out += '{}  ({}-{})\n\n'.format(overlap['text_span'], 
                                                                    overlap['start'], 
                                                                    overlap['end'])
                                out += '-'*20
                                count += 1
                            return out
                        else:
                            return 'no {} overlaps found for {} in set {} in file {}'.format(annotation_type, 
                                                                                             annotator_name, 
                                                                                             annotation_set, 
                                                                                             file)
                    else:
                        if [o for t,o in overlaps.items() if o]:
                            return 'overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                       annotation_set, 
                                                                                       file)
                        else:
                            return 'no overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                          annotation_set, 
                                                                                          file)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlaps found for {} in set {} in file {}'.format(annotation_type, 
                                                                                         annotator_name, 
                                                                                         annotation_set, 
                                                                                         file)
                    else:
                        return 'no overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                      annotation_set, 
                                                                                      file)

            else: 

                for set_name, annotations in settings.corpus[file][annotator_name]['annotation_sets'].items():
                    overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                          annotation_types = overlaps_to_validate)

                    if not annotation_type == 'all_types':
                        overlaps = overlaps[annotation_type]
                        if overlaps:
                            count += 1
                    else:
                        if [o for t, o in overlaps.items() if o]:
                            count += 1

                if annotation_type == 'all_types':
                    if count:
                        return 'overlaps found for annotator {} in file {}'.format(annotator_name,  
                                                                                   file)
                    else:
                        return 'no overlaps found for annotator {} in file {}'.format(annotator_name, 
                                                                                      file)
                else:
                    if count:
                        return '{} overlaps found for annotator {} in file {}'.format(annotation_type, 
                                                                                      annotator_name,  
                                                                                      file)
                    else:
                        return 'no {} overlaps found for annotator {} in file {}'.format(annotation_type, 
                                                                                         annotator_name, 
                                                                                         file)
                            
                            
                        


def validate_subentity_boundaries(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    file = filters[0].title
    annotation_set = filters[1].title
    annotator_name = filters[2].title
    annotation_type = filters[3].title
    if file == 'corpus':
        count = 0
        if annotator_name == 'team':

            if annotation_set == 'all_sets':
                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        for set_name, annotations in document['annotation_sets'].items():
                            overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                  annotation_types = overlaps_to_validate)

                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            
                            else:
                                if [o for t,o in overlaps.items() if o]:
                                    count += 1
                if annotation_type == 'all_types':             
                    if count:
                        return 'overlap issues found in all sets between all annotators in corpus'
                    else:
                        return 'no overlap issues found all sets between all annotators in corpus'
                else:
                    if count:
                        return '{} overlap issues found in all sets between all annotators in corpus'.format(annotation_type)
                    else:
                        return 'no {} overlap issues found all sets between all annotators in corpus'.format(annotation_type)
            else:

                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        if annotation_set in settings.corpus[file_name][annotator]['annotation_sets'].keys():
                            annotations = document['annotation_sets'][annotation_set]
                            overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                                  annotation_types = overlaps_to_validate)


                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            else:
                                if [o for t,o in overlaps.items() if o]:
                                    count += 1
                            
        
                if annotation_type == 'all_types':             
                    if count:
                        return 'overlap issues found in {} between all annotators in corpus'.format(annotation_set)
                    else:
                        return 'no overlap issues found {} between all annotators in corpus'.format(annotation_set)
                else:
                    if count:
                        return '{} overlap issues found in {} between all annotators in corpus'.format(annotation_type,
                                                                                                       annotation_set)
                    else:
                        return 'no {} overlap issues found {} between all annotators in corpus'.format(annotation_type,
                                                                                                       annotation_set)

        else:
            count = 0
            if annotation_set == 'all_sets':
                for file_name, annotators in settings.corpus.items():
                    for set_name, annotations in annotators[annotator_name]['annotation_sets'].items():
                            # execute function

                            if not annotation_type == 'all_types':
                                overlaps = overlaps[annotation_type]
                                if overlaps:
                                    count += 1
                            else:
                                if [ o for t,o in overlaps.items() if o]:
                                    count += 1
                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found for {} in corpus'.format(annotation_type, 
                                                                                 annotator_name)
                    else:
                        return 'overlap issues found for {} in corpus'.format(annotator_name)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found for {} in corpus'.format(annotation_type, 
                                                                                    annotator_name)
                    else:
                        return 'no overlap issues found for {} in corpus'.format(annotator_name)

            else:
                
                for file_name, annotators in settings.corpus.items():
                    for annotator, document in annotators.items():
                        if annotation_set in settings.corpus[file_name][annotator_name]['annotation_sets'].keys():
                            if annotation_set in settings.corpus[file_name][annotator_name]['annotation_sets'].keys():
                                annotations = annotators[annotator_name]['annotation_sets'][annotation_set]
                                # execute function

                                if not annotation_type == 'all_types':
                                    overlaps = overlaps[annotation_type]
                                    if overlaps:
                                        count += 1
                                else:
                                    if [o for t,o in overlaps.items() if o]:
                                        count += 1
                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found for {} on set {} in corpus'.format(annotation_type, 
                                                                                           annotator_name, 
                                                                                           annotation_set)
                    else:
                        return 'overlap issues found for {} on set {} in corpus'.format(annotator_name, 
                                                                                        annotation_set)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found for {} on set {} in corpus'.format(annotation_type, 
                                                                                              annotator_name, 
                                                                                              annotation_set)
                    else:
                        return 'no overlap issues found for {} on set {} in corpus'.format(annotator_name, 
                                                                                           annotation_set)
    else:
        count = 0
        if annotator_name == 'team':
            if annotation_set == 'all_sets':
                for annotator, document in settings.corpus[file].items():
                    for set_name, annotations in document['annotation_sets'].items():
                        # execute function

                        if not annotation_type == 'all_types':
                            overlaps = overlaps[annotation_type]
                            if overlaps:
                                count += 1
                        else:
                            if [o for t,o in overlaps.items() if o]:
                                count += 1

                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found between all annotators in file {}'.format(annotation_type, 
                                                                                                  file)
                    else:
                        return 'overlap issues found between all annotators in file {}'.format(file)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found between all annotators in file {}'.format(annotation_type, 
                                                                                                     file)
                    else:
                        return 'no overlap issues found between all annotators in file {}'.format(file)
            else:
                for annotator, document in settings.corpus[file].items():
                    if annotation_set in document['annotation_sets'].keys():
                        # execute function

                        overlaps = annotation_validations.annotation_overlaps(annotations=annotations, 
                                                                              annotation_types = overlaps_to_validate)

                        if not annotation_type == 'all_types':
                            overlaps = overlaps[annotation_type]
                            if overlaps:
                                count += 1
                        else:
                            if [o for t,o in overlaps.items() if o]:
                                count += 1

                if count:
                    if not annotation_type == 'all_types':
                        return '{} overlap issues found between all annotators for the set {} in file {}'.format(annotation_type, 
                                                                                                                annotation_set,
                                                                                                                file)
                    else:
                        return 'overlap issues found between all annotators for the set {} in file {}'.format(file, 
                                                                                                              annotation_set)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlap issues found between all annotators for the set {} in file {}'.format(annotation_type, 
                                                                                                                    annotation_set,
                                                                                                                    file)
                    else:
                        return 'no overlap issues found between all annotators for the set {} in file {}'.format(file, 
                                                                                                                 annotation_set)
        else:

            if not annotation_set == 'all_sets':
                
                if annotation_set in settings.corpus[file][annotator_name]['annotation_sets'].keys():
                    annotations = settings.corpus[file][annotator_name]['annotation_sets'][annotation_set]
                    # execute function
                        
                    if not annotation_type == 'all_types':
                        overlaps = overlaps[annotation_type]
                        count = 1
                        out = ''
                        if overlaps:
                            for overlaping_annotations in overlaps:
                                out += 'overlap group ({})\n'.format(count)
                                out += '-'*20
                                out += '\n'
                                for overlap in overlaping_annotations:
                                    out += '{}  ({}-{})\n\n'.format(overlap['text_span'], 
                                                                    overlap['start'], 
                                                                    overlap['end'])
                                out += '-'*20
                                count += 1
                            return out
                        else:
                            return 'no {} overlaps found for {} in set {} in file {}'.format(annotation_type, 
                                                                                             annotator_name, 
                                                                                             annotation_set, 
                                                                                             file)
                    else:
                        if [o for t,o in overlaps.items() if o]:
                            return 'overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                       annotation_set, 
                                                                                       file)
                        else:
                            return 'no overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                          annotation_set, 
                                                                                          file)
                else:
                    if not annotation_type == 'all_types':
                        return 'no {} overlaps found for {} in set {} in file {}'.format(annotation_type, 
                                                                                         annotator_name, 
                                                                                         annotation_set, 
                                                                                         file)
                    else:
                        return 'no overlaps found for {} in set {} in file {}'.format(annotator_name, 
                                                                                      annotation_set, 
                                                                                      file)

            else: 

                for set_name, annotations in settings.corpus[file][annotator_name]['annotation_sets'].items():
                    # execute function

                    if not annotation_type == 'all_types':
                        # if annotation_type in settings.schema.keys():
                        overlaps = overlaps[annotation_type]
                        if overlaps:
                            count += 1
                    else:
                        if [o for t, o in overlaps.items() if o]:
                            count += 1

                if annotation_type == 'all_types':
                    if count:
                        return 'overlaps found for annotator {} in file {}'.format(annotator_name,  
                                                                                   file)
                    else:
                        return 'no overlaps found for annotator {} in file {}'.format(annotator_name, 
                                                                                      file)
                else:
                    if count:
                        return '{} overlaps found for annotator {} in file {}'.format(annotation_type, 
                                                                                      annotator_name,  
                                                                                      file)
                    else:
                        return 'no {} overlaps found for annotator {} in file {}'.format(annotation_type, 
                                                                                         annotator_name, 
                                                                                         file)


    # if not (file == 'all_files' and annotation_set == 'all_sets' and annotator_name == 'all_annotators'):
    #     if not annotation_type == 'all_types':
    #         if annotation_type in settings.schema.keys():
    #             #print('{} is entity'.format(annotation_type))
    #             if 'sub_entities' in settings.schema[annotation_type].keys():
    #                 sub_entities = list(settings.schema[annotation_type]['sub_entities'].keys())
    #                 #print('will validate boundaries for {}'.format(sub_entities))
    #                 try:
                        
    #                     annotations = settings.corpus[file][annotator_name]['annotation_sets'][annotation_set]
    #                     if annotations:
    #                         out = ''
    #                         conflicts = annotation_validations.outbound_subentities(annotations,
    #                                                                                 annotation_type, 
    #                                                                                 sub_entities)
    #                         for k, v in conflicts.items():
    #                             out += '{}\n'.format(k)
    #                             for x in v:
    #                                 out += '\t{}  ({}-{})\n'.format(x['text_span'], x['start'], x['end'])
    #                         return out
    #                     else: 
    #                         return 'no {} overlap issues found in set {} for annotator {} file {}'.format(annotation_type,
    #                                                                                                     annotation_set, 
    #                                                                                                   annotator_name,
    #                                                                                                   file)

    #                 except KeyError as e:
    #                     return 'no {} overlap issues found in set {} for annotator {} file {}'.format(annotation_type,
    #                                                                                                     annotation_set, 
    #                                                                                                   annotator_name,
    #                                                                                                   file)
    #             else:
    #                 return 'annotation type {} does not contain any sub_entities.'.format(annotation_type)
    #         else:
    #             temp = []
    #             for a in settings.schema.keys():
    #                 if 'sub_entities' in settings.schema[a]:
    #                     if annotation_type in settings.schema[a]['sub_entities']:
    #                         temp.append(a)

    #             try:
    #                 annotations = settings.corpus[file][annotator_name]['annotation_sets'][annotation_set]
    #                 if annotations:
    #                     out = ''
    #                     conflicts = annotation_validations.outbound_subentities(annotations,
    #                                                                             temp[0], 
    #                                                                             [annotation_type])
    #                     for k, v in conflicts.items():
    #                         out += '{}\n'.format(k)
    #                         for x in v:
    #                             out += '\t{}  ({}-{})\n'.format(x['text_span'], x['start'], x['end'])
    #                     return out
    #                 else: 
    #                     return 'no {} overlap issues found in set {} for annotator {} file {}'.format(annotation_type,
    #                                                                                                   annotation_set, 
    #                                                                                                   annotator_name,
    #                                                                                                   file)
    #             except KeyError as e:
    #                 return 'no {} overlap issues found in set {} for annotator {} file {}'.format(annotation_type,
    #                                                                                                 annotation_set, 
    #                                                                                                   annotator_name,
    #                                                                                                   file)

    #     else:
    #         return 'looking at all types'
    # else:
    #     pass




def validate_subentity_partial_overlap(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    file = filters[0].title
    annotation_set = filters[1].title
    annotator = filters[2].title
    annotation_type = filters[3].title
    out_string = ''
    out_string += 'validating subentity partial overlap with the following filters {} {} {} {}'.format(file, 
                                                                                                    annotation_set,
                                                                                                    annotator, 
                                                                                                    annotation_type)
    return out_string

def validate_annotation_boundaries(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    file = filters[0].title
    annotation_set = filters[1].title
    annotator = filters[2].title
    annotation_type = filters[3].title
    out_string = ''
    out_string += 'validating annotation boundaries with the following filters {} {} {} {}'.format(file, 
                                                                                                annotation_set,
                                                                                                annotator, 
                                                                                                annotation_type)
    return out_string


def validate_schema_values(filters=[]):

    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    file = filters[0].title
    annotation_set = filters[1].title
    annotator = filters[2].title
    annotation_type = filters[3].title
    out_string = ''
    out_string += 'validating schema values with the following filters {} {} {} {}'.format(file, 
                                                                                        annotation_set,
                                                                                        annotator, 
                                                                                        annotation_type)
    return out_string


def generate_validation_report():

    # 1) run this qa report
    # 3) return string of output
    pass


