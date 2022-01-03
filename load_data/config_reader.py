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
from load_data import schema_framework 
from pathlib import Path


def create_schema(annotation_sections, parser):

    #assert annotation_sections, 'please provide section names'

    schema = schema_framework.Schema(name = 'annotation_schema')

    for section in annotation_sections:
        
        annotation = parser[section.strip()]
        entity = schema_framework.Entity(name=section.strip())

        if 'sub_entities' in annotation.keys():
            for x in annotation['sub_entities'].split('|'):
                entity.sub_entities[x.strip()] = schema_framework.Entity(name=x.strip()) 
        
        if 'overlaps' in annotation.keys():
            if annotation['overlaps']:
                for x in annotation['overlaps'].split('|'):
                    entity.overlaps[x.strip()] = schema_framework.Entity(name=x.strip()) 
        if 'features' in annotation.keys():
            if annotation['features']:
                for feature in annotation['features'].split('||'):
                    entity.features[feature.split(':=:')[0]] = feature.split(':=:')[1].split('|') 

        schema.add_entry(entity)

    return schema


def read_config_file_information(path_to_config=None):


    path_to_config = Path() if path_to_config is None else Path(path_to_config)
    
    #assert path_to_config.is_file(), 'file does not exist'

    parser = configparser.RawConfigParser()   
    
    parser.read(path_to_config)
    config_sections = parser.sections()
    
    config_annotation_sections = [x for x in config_sections if x not in ['required', 'optional']]

    annotations_dir = Path(parser['required']['annotations_dir'])
    output_dir = Path(parser['required']['output_dir'])

    task = parser['required']['task']
    encoding = parser['required']['encoding'] # encoding to put into a required section

    annotation_schema = create_schema(config_annotation_sections, parser)

    

    return {'annotation_dir' : annotations_dir, 
            'output_dir':output_dir, 
            'task':task,
            'encoding':encoding,
            'schema':annotation_schema}

