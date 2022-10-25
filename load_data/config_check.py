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

import os
from pathlib import Path

# configuration = {}
# config_path = r'config.config'
# configuration = read_config_file_information(config_path)
# schema = schema_framework
#Check if configuration is readable


def config_check(configuration):


    if 'required' not in configuration.sections():
        raise ValueError('Config file Missing Required Section')

    # if len(configuration.sections()) == 2:
    #     if 'required' in configuration.sections() and 'optional' in configuration.sections():
    #         raise ValueError('Config File Missing Schema Section')

    if len(configuration.sections()) == 1:
        if 'optional' in configuration.sections():
            raise ValueError('Config File Missing Schema and Required Sections')
        if 'required' in configuration.sections():
            raise ValueError('Config File Missing Schema Section')

    # ['annotations_dir', 'output_dir', 'task', 'encoding']
    if not len(list(configuration['required'])) == 4:
        raise ValueError('''Errors in Required Section of the Config File
                            \nRequired Section Should Only Contain {}'''.format(', '.join(['annotations_dir', 'output_dir', 
    
                                                                                          'task', 'encoding'])))
    
   
    if not configuration['required']['task'] in ['sequence_labelling', 'classification']:
        raise ValueError('{} is Not A Valid Task\n Please Use {}'.format(configuration['required']['task'],
                                                                        ', '.join(['sequence_labelling', 'classification'])))

    if not configuration['required']['encoding'] in ['UTF-8', 'Windows-1252']: 
        raise ValueError('{} is Not A Valid Encoding\n Please Use {}'.format(configuration['required']['encoding'],
                                                                        ', '.join(['UTF-8', 'Windows-1252'])))


    if not Path(configuration['required']['annotations_dir']).is_dir():
        raise ValueError('{} Is Not A Valid Path'.format(configuration['required']['annotations_dir']))

    if not Path(configuration['required']['output_dir']).is_dir():
        raise ValueError('{} Is Not A Valid Path'.format(configuration['required']['output_dir']))



    try:
        if len(list(configuration['optional'])) > 2:
            raise ValueError('''Errors in Optional Section of the Config File
                                \nOptional Section Should Only Contain {}'''.format(', '.join(['set_names', 'merge_sets_as'])))
    except KeyError:
        pass

    config_annotation_sections = [x for x in configuration.sections() if x not in ['required', 'optional']]

    annotation_type_values = {'overlaps':None,
                              'sub_entities':None,
                              'features':None,
                              'alt_names':None}

    for x in config_annotation_sections:
        if len(list(configuration[x])) >= 1:
            for y in list(configuration[x]):
                try:
                    annotation_type_values[y]
                except KeyError:
                    raise ValueError('{} is Not A Valid Option For Annotation Types'.format(y))

                try:
                    overlaps = configuration[x]['overlaps']
                    if type(overlaps) == str:
                        overlaps = [overlaps]
                    #if not overlaps == ['']:
                        #for overlap in overlaps:
                            #if not overlap in config_annotation_sections:
                                #raise ValueError('Type {} Is Not Defined In The Schema'.format(overlap))
                    
                except KeyError:
                    pass
                try:
                    sub_entities = configuration[x]['sub_entities'].split('|')
                    if type(sub_entities) == str:
                        sub_entities = [sub_entities]
                    if not sub_entities == ['']:
                        if x in sub_entities:
                            raise ValueError('Type Can\'t Be It\'s Own Sub Entity')
                        for sub_entity in sub_entities:
                            if not sub_entity in config_annotation_sections:
                                raise ValueError('Type {} Is Not Defined In The Schema'.format(sub_entity))
                except KeyError:
                    pass               



                


    

    #raise ValueError('im config check')
 



