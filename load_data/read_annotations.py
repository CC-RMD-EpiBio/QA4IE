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
    Functions for loading annotations generated using GATE
'''

from lxml import etree


def read_gate_xml(file_path, exclude_sets = [], annotator = None, encoding = 'utf-8'):
    """
    Given a a path to an gate xml, generate a object representation of it
    :param file_path: a pathlib object that points to the annotation file
    :type Path:
    :param exclude_sets: a list of annotation sets to ignoree
    :type list:
    :param annotator: the name of the current annotator
    :type name:
    :return document_contents: a dictionary containing the contents of the annotated document
    :param dict
    """

    document_contents = {}
    tree = etree.parse(str(file_path))
    root = tree.getroot()
    document_contents['text'] = etree.tostring(tree.find('TextWithNodes'), encoding=encoding, 
                                                                           method='text', 
                                                                           with_tail = False).decode()
    document_contents['annotation_sets'] = {}

    for annotation_set in tree.findall("./AnnotationSet"):
        if annotation_set.attrib == "":
            set_name = 'default_annotation_set'
        else:
            set_name = annotation_set.attrib['Name']

        if set_name in exclude_sets:
            continue # skip this section

        document_contents['annotation_sets'][set_name] = []

        for annotation in annotation_set.findall(".Annotation"):
            annotation_dict = {}
            attributes = annotation.attrib
            
            annotation_dict['mention'] = attributes['Type']
            annotation_dict['start'] = int(attributes['StartNode'])
            annotation_dict['end'] = int(attributes['EndNode'])
            annotation_dict['id'] = attributes['Id']
            annotation_dict['text_span'] = document_contents['text'][annotation_dict['start']:annotation_dict['end']]

            features = {}
            for att, val in zip(annotation.findall("./Feature/Name"), annotation.findall("./Feature/Value")):
                features[att.text] = val.text

            annotation_dict['features'] = features
            annotation_dict['annotator'] = annotator

            document_contents['annotation_sets'][set_name].append(annotation_dict)

    return document_contents


