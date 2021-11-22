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
  Validation functions for config file inputs
'''



def validate_config_schema(loaded_schema, config_schema):

    '''
        Validates the schema information written in the config file againts the information found in the Gate xml schema files.
        Generates assertion errors if issues are found

        :param loaded_schema: information loaded from the Gate xml files
        :type dict:

        :param config_schema: schemainformation added into the configuration file
        :type dict:

    '''

    types_in_config_schema = []
    overlaps_in_config_schema = []

    for t in config_schema.keys():
        types_in_config_schema.append(t)
        overlaps_in_config_schema.append(config_schema[t]['overlap'])
        try:

            for sub_t in config_schema[t]['sub_entities'].keys():
                types_in_config_schema.append(sub_t)
                overlaps_in_config_schema.append(config_schema[t]['sub_entities'][sub_t]['overlap'])
        except KeyError:
            pass
    types_in_config_schema.sort()
    schema_keys = list(loaded_schema.keys())
    schema_keys.sort()

    overlaps_in_config_schema = [y for x in overlaps_in_config_schema for y in x]
    overlaps_in_config_schema = list(set(overlaps_in_config_schema))

    assert not [x for x in overlaps_in_config_schema if not x in types_in_config_schema], 'inconsistent overlap types in config schema'
    assert not [x for x in types_in_config_schema if not x in schema_keys], 'inconsistent type in config schema'
