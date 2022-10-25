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
from pathlib import Path
from load_data import config_reader, create_corpus, config_check


def init(config_path=None):

    global task 
    global corpus
    global schema
    global merge_sets
    global output_dir
    global logger

    # load config file
    #base_dir = Path(__file__)
    
    try:
        #print(config_path)
        config_info = config_reader.read_config_file_information(config_path)
        
        
        
        schema = config_info['schema']
        set_names = config_info['set_names']
        merge_sets = config_info['merge_set_names']
        encoding = config_info['encoding']
        task = config_info['task']
        output_dir = Path(config_info['output_dir'])
        annotations_dir = config_info['annotation_dir']

        try:
            corpus = create_corpus.create_corpus(annotations_dir=Path(annotations_dir),
                                                 strict_matches=True,
                                                 encoding = encoding,
                                                 filter_sets=set_names,
                                                 schema=schema,
                                                 merge_sets=merge_sets)

            if not schema:
                
                if not set_names:
                    raise ValueError('Set Name Required')
                #if len(set_names) > 1:
                    #raise ValueError('Only One Set Name Can Be Used If Schema Types Are Absent')
                #raise ValueError('Schema Not Found In Config File')
                schema = config_reader.determine_entity_relations(corpus, set_names)
            
                #raise ValueError('Schema Not Found In Config File')
            
        except LookupError as e:
            raise ValueError('Data Not Structured Properly')

    except AssertionError as e:
        raise ValueError('Config File Not Found')

  



    
