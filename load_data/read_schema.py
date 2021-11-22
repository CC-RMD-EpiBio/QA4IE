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
    Function for reading schemas generated using GATE
'''

from lxml import etree

def read_gate_schema(schema_dir = None, main_schema_file_name = None):
    """
    From a directory of individual gate xml schemas, gets the single xml file that loads all of the other schema xml files
    :param schema_dir: a pathlib object that points to the directory where all the schema files are
    :type Path:
    :param main_schema_file_name: the name of the single xml file that loads all the other schema types
    :type str:
    :return schema_dict: a dictionary containing the schema used to annotate the files
    :type dict
    """

    assert schema_dir, 'please provide a path to the schema files'
    assert main_schema_file_name, 'please provide the name of the main schema file'

    main_schema_file_path = schema_dir / main_schema_file_name

    assert main_schema_file_path.is_file(), '{} does not exist in the schema directory'.format(main_schema_file_name)

    schema_dict = {}

    try:
        tree = etree.parse(str(main_schema_file_path))
    except OSError as e:
        print(e)
        print('Not an annotation schema')
        pass
    
    root = tree.getroot()
    attribute_list = []
    for child in root:
        try:
            file = schema_dir / child.attrib['schemaLocation']
            annotation_type = etree.parse(str(file))
            annotation_type_root = annotation_type.getroot()
            annotation_type_dict = {}
            for _type in annotation_type.iter():
                attribute = dict(_type.attrib)
                values = dict(_type.attrib)
                if(len(attribute)):
                    att = attribute.get('name')
                    val = attribute.get('value')
                    if(att is not None):
                        attribute_list.append(att)
                    if(val is not None and att is None):
                        key = str(attribute_list[-1])
                        if(not key in annotation_type_dict):
                            annotation_type_dict[key] = list()
                        annotation_type_dict[key].append(val)
            schema_dict[attribute_list[0]] = annotation_type_dict         
            value_list = []         
            attribute_list = []
        except OSError as e:
            print(e)
            print('Can\'t parse xml {sub_e}'
                .format(sub_e=child.attrib.values()[0]))
        
    return schema_dict





