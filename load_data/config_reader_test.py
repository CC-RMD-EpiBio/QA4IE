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
from pathlib import Path


def create_annotation_relationships(annotation_sections, parser):

    assert annotation_sections, 'please provide section names'


    schema = {}
    previous_sections = []

    for section in annotation_sections:
        section_keys = list(parser[section].keys())
        if 'sub_entities' in section_keys:
            features = {}
            try:
                try:
                    x = parser[section.strip()]['features']
                    for feature in x.split('||'):
                        features[feature.split(':')[0]] = feature.split(':')[1].split('|') 
                except IndexError as e:
                    pass

            except KeyError as e:
                pass

            schema[section] = {
                            'overlaps': 
                                      [x.strip() for x in parser[section.strip()]['overlaps'].split('|')],
                            'sub_entities': 
                                          {
                                          x.strip():{
                                                     'overlaps':
                                                               [y.strip() for y in parser[x.strip()]['overlaps'].split('|')]
                                                     } 
                                                       for x in parser[section.strip()]['sub_entities'].split('|')
                                           }
                                }
            schema[section]['features'] = features
            
            previous_sections = previous_sections + [section.strip()] + list(schema[section]['sub_entities'].keys())

            for s in schema[section]['sub_entities'].keys():
                if s in schema.keys():
                    schema[section]['sub_entities'][s] = schema[s]
                    del schema[s]

        else:# types without subtypes
            features = {}
            try:
                try:
                    x = parser[section.strip()]['features']
                    for feature in x.split('||'):
                        features[feature.split(':')[0]] = feature.split(':')[1].split('|') 
                except IndexError as e:
                    pass

            except KeyError as e:
                pass

            if not section in previous_sections:
                schema[section.strip()] = {
                                        'overlaps': 
                                                  [x.strip() for x in parser[section.strip()]['overlaps'].split('|')]
                                        }
                schema[section.strip()]['features'] = features
    return schema


def read_config_file_information(path_to_config=None):


    path_to_config = Path() if path_to_config is None else Path(path_to_config)
    
    assert path_to_config.is_file(), 'file does not exist'

    parser = configparser.RawConfigParser()   
    
    parser.read(path_to_config)
    config_sections = parser.sections()
    
    config_annotation_sections = [x for x in config_sections if x not in ['required', 'optional']]

    annotations_dir = Path(parser['required']['annotations_dir'])
    output_dir = Path(parser['required']['output_dir'])

    # schema dir option no longer necessary if we add the info directly into the config file
    # schema_dir = Path(parser['required']['output_dir']) 
    especified_set_name = parser['required']['especified_set_name']
    key_annotator = parser['required']['key_annotator']

    task = parser['required']['task']
    encoding = parser['required']['encoding'] # encoding to put into a required section

    annotation_schema = create_annotation_relationships(config_annotation_sections, parser)

    return {'annotation_dir' : annotations_dir, 
            'output_dir':output_dir, 
            'key_annotator':key_annotator,
            'task':task,
            'encoding':encoding,
            'schema':annotation_schema}


    
