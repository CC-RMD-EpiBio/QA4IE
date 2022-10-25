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
import configparser
from load_data import schema_framework, config_check
from pathlib import Path
from validation import annotation_validations

def determine_entity_relations(corpus, set_names):

    # gather annotation types
    annotation_types = []
    for file, annotators in corpus.items():
        for annotator_name, contents in annotators.items():
            for s_name, annotations in contents['annotation_sets'].items():
                for annotation in annotations:
                    annotation_types.append(annotation['mention'])

    annotation_types = list(set(annotation_types))   

    relationships = {} 
    for annotation_type in annotation_types:  
        for file, annotators in corpus.items():
                for annotator_name, contents in annotators.items():
                    for s_name, annotations in contents['annotation_sets'].items():
                        if s_name in set_names:
                            test = annotation_validations.annotation_overlaps(annotations, 
                                {annotation_type:[x for x in annotation_types if not x == annotation_type]})
                            for x, y in test.items():
                                for z in y:
                                    for u in z:
                                        if not x == u['mention']:
                                            a = '{}-{}'.format(x, u['mention'])
                                            a = a.split('-')
                                            a.sort()
                                            a = '-'.join(a)
                                            try:
                                                relationships[a] += 1
                                            except:
                                                relationships[a] = 1
    counter = {}

    for t in annotation_types:
        counter[t] = 0
    for a, b in relationships.items():
        a = a.split('-')
        
        if b:
            counter[a[0]] += b
            counter[a[1]] += b
    #print(counter)
    #raise ValueError('hey! Listen!')
    try:
        schema = {max(counter, key=counter.get): {'sub_entities':[]}}
    except ValueError:
        return None
    for c in counter:
        if counter[c] == 0:
            schema[c] = {'sub_entities':[]}
            
        else:
            if not c in list(schema.keys()):
                schema[max(counter, key=counter.get)]['sub_entities'].append(c)
                schema[c] = None

    automatic_schema = schema_framework.Schema(name = 'automatic_annotation_schema')
    for ent in schema:
        entity = schema_framework.Entity(name=ent)
        # print(ent)
        try:
            if 'sub_entities' in schema[ent].keys():
                for sub_ent in schema[ent]['sub_entities']:
                    sub_entity = schema_framework.Entity(name=sub_ent)
                    entity.sub_entities[sub_ent] = sub_entity
           
        except AttributeError:
            pass

        # for y in schema:
        #     if entity.has_parent_entity():
        #         if not y in entity.sub_entities.keys():
        #             entity.overlaps[y] = schema_framework.Entity(name=y)
                
        automatic_schema.add_entry(entity)

    for file, annotators in corpus.items():
        for annotator_name, contents in annotators.items():
            for s_name, annotations in contents['annotation_sets'].items():
                if s_name in set_names:
                    for annotation in annotations:
                        current_mention = annotation['mention']
                        current_features = annotation['features']

                        for k, v in current_features.items():
                            try:
                                if not v in automatic_schema.entities[current_mention].features[k]:
                                    automatic_schema.entities[current_mention].features[k].append(v)
                            except KeyError:
                                automatic_schema.entities[current_mention].features[k] = [v]

    for n, obj in automatic_schema.entities.items():
        if obj.is_parent_entity():
            for x, objc in automatic_schema.entities.items():
                if not n == x:
                    obj.overlaps[x] = schema_framework.Entity(name=x) 

    return automatic_schema
    

def create_schema(annotation_sections, parser):

    #assert annotation_sections, 'please provide section names'

    schema = schema_framework.Schema(name = 'annotation_schema')

    for section in annotation_sections:
        
        annotation = parser[section.strip()]
        entity = schema_framework.Entity(name=section.strip().replace('-', '').replace('/', '').replace(' ', '').lower())
        try:
            #entity.alt_names.append(annotation['alt_names'].strip().replace('-', '').replace('/', '').replace(' ', '').lower())
            for alt_name in annotation['alt_names'].split('|'):
                entity.alt_names.append(alt_name.strip().replace('-', '').replace('/', '').replace(' ', '').lower())
        except KeyError as e:
            pass

        if 'sub_entities' in annotation.keys():
            for x in annotation['sub_entities'].split('|'):
                entity.sub_entities[x.strip().replace('-', '').replace('/', '').replace(' ', '').lower()] = schema_framework.Entity(name=x.strip().replace('-', '').replace('/', '').replace(' ', '').lower()) 
        
        if 'overlaps' in annotation.keys():
            if annotation['overlaps']:
                for x in annotation['overlaps'].split('|'):
                    entity.overlaps[x.strip().replace('-', '').replace('/', '').replace(' ', '').lower()] = schema_framework.Entity(name=x.strip().replace('-', '').replace('/', '').replace(' ', '').lower()) 
        if 'features' in annotation.keys():
            if annotation['features']:
                for feature in annotation['features'].split('||'):
                    entity.features[feature.split(':=:')[0]] = feature.split(':=:')[1].split('|') 

        schema.add_entry(entity)

    return schema


def read_config_file_information(path_to_config=None):


    path_to_config = Path() if path_to_config is None else Path(path_to_config)
    
    if not path_to_config.is_file():
        raise ValueError('file does not exist')
    
    parser = configparser.RawConfigParser()   
    
    parser.read(path_to_config)

    config_check.config_check(parser)

    config_sections = parser.sections()
    
    config_annotation_sections = [x for x in config_sections if x not in ['required', 'optional']]


    
    annotations_dir = Path(parser['required']['annotations_dir'])
    output_dir = Path(parser['required']['output_dir'])

    task = parser['required']['task']

    
    if 'optional' in list(parser.keys()):
        #try:


        try:
            set_names = parser['optional']['set_names']
            set_names = set_names.split('|')
            #print(set_names)
            if type(set_names) == str:
                set_names = [set_names]
        except KeyError:
            set_names = []
        try:
            merge_set_names = parser['optional']['merge_sets_as']

        except KeyError:
            merge_set_names = False

    

    else:
        set_names = []
        merge_set_names = False

    encoding = parser['required']['encoding'] # encoding to put into a required section


    if len(config_annotation_sections) == 0:

        annotation_schema = None
    else:
        annotation_schema = create_schema(config_annotation_sections, parser)
    


    

    return {'annotation_dir' : annotations_dir, 
            'output_dir':output_dir, 
            'task':task,
            'merge_set_names':merge_set_names,
            'encoding':encoding,
            'set_names':set_names,
            'schema':annotation_schema}

