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

'''
    Funtions that represent a series of steps for validating annotations, based on constrains in the configuration file

'''

def annotation_overlaps(annotations = [], annotation_types = {}):
    '''
        looks for overlaps of annotations that are not allowed in the guidelines

        :param annotators_content: a dictionary that contains the text and annotated sections of each annotator
        :type dict

        :param annotation_types: a list of annotations types to check for overlaps
        :type list

        :param ignore_sets: a list of set names to ignore 
        :type list

        :return conflicts: the conflicts found for this check

    '''
    #print(annotations)
    #assert annotations, 'please provide a list of annotations'
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
            if(t['end'] >= a['start'] and t['start'] <= a['end'] and not t['id'] == a['id']):
                res.append(t)
        return res

    conflict_types = {}

    for _type, invalid_overlaps in annotation_types.items():
        if invalid_overlaps:
            annotations_of_type = [a for a in annotations if a['mention'] == _type]
            annotations_of_types = [a for a in annotations if a['mention'] in invalid_overlaps]
            conflict_types[_type] = []
            for annotation in annotations_of_type:
                current_overlaps = overlap(annotation, annotations_of_types)
                if current_overlaps:
                    current_overlaps.append(annotation)
                    current_overlaps = sorted(current_overlaps, key=lambda x: x['start'])
                    if not current_overlaps in conflict_types[_type]:
                        conflict_types[_type].append(current_overlaps)

    return conflict_types


def outbound_subentities(annotations, main_type = '', sub_entities = []):
    '''
        looks for subentities that are not contained inside of an entity as stablished by the guideline

        :param annotattions: a list of annotations
        :type list

        :return conflicts: the conflicts found for this check

    '''
    #assert annotations, 'please provide a list of annotations'
    conflicts = {}

    # get all entities/subentities in current file
    sub_entities_in_file = [a for a in annotations if a['mention'] in sub_entities]
    entities_in_file = [a for a in annotations if a['mention'] == main_type]

    for s_e in sub_entities_in_file:
        res = []
        for e in entities_in_file:
            if(e['end'] >= s_e['start'] and e['start'] <= s_e['end']):
                res.append(e)                                           

        if not res:
            try:
                conflicts[s_e['mention']].append(s_e)
            except KeyError as e:
                conflicts[s_e['mention']] = [s_e]


    return conflicts

def partial_subentity_overlap(annotations, main_type = '', sub_entities = []):

    '''
    looks for subentities that are partially overlaped with their respective entity

    :param annotatoins: a list of annotations
    :type list

    :param hierarchy: an object representation of a hierarchical structure
    :type dict

    :return conflicts: the conflicts found for this check

    '''
    #assert annotations, 'please provide a list of annotations'
    conflicts = {}
    

    # get all subentities in current file
    sub_entities_in_file = [a for a in annotations if a['mention'] in sub_entities]
    entities_in_file = [a for a in annotations if a['mention'] == main_type]
    

    for s_e in sub_entities_in_file:
        #print(s_e)
        for e in entities_in_file:
            
            if(s_e['start'] < e['start'] and s_e['end'] > e['start'] or 
                s_e['start'] < e['end'] and s_e['end'] > e['end']): 
                    try:
                        conflicts[s_e['mention']].append(s_e)

                    except KeyError as e:
                        conflicts[s_e['mention']] = [s_e]

    return conflicts



def outbound_annotations(annotations, all_types= {}):
    '''

        looks for annotations that exist in specific annotation sets

        :param annotations: a list of annotations
        :type list

        :param all_types: a list of all annotation types for the current schema
        :type list


        :return conflicts: the conflicts found for this check

    '''
    assert annotations, 'please provide a list of annotations'

    conflicts = {}
    for _type in all_types:
        conflicts[_type] = [a for a in annotations if a['mention'] == _type]

    return conflicts
                 

def validate_schema(annotations = [], schema = {}):
    '''

        looks for annotations that violate the contents of a given schema

        :param annotations: a list of annotations
        :type list

        :param schema: an object representation of the annotation schema
        :type dict

        :return conflicts: the conflicts found for this check

    '''

    assert schema, 'please provide a valid schema representation'
    #assert annotations, 'please provide a list of annotations'

    conflicts = {}
    for annotation in annotations:

        try:    
            schema_features = schema[annotation['mention']]
            key_diff = set(annotation['features'].keys()) - set(schema_features.keys())

            current_values = list(annotation['features'].values())
            flat_schema_values = [v for l in list(schema_features.values()) for v in l]

            value_diff = set(current_values) - set(flat_schema_values)

            if value_diff or key_diff:
                try:
                    conflicts[annotation['mention']].append(annotation)
                except KeyError as e:
                    conflicts[annotation['mention']] = [annotation]
                                         


            
        except KeyError as e:
            # annotation not in schema
            pass
                
    return conflicts



                                                                                    
                    




