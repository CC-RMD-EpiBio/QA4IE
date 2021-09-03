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
    Functions for loading annotations and schemas generated using GATE
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

def read_gate_xml(file_path, exclude_sets = [], annotator = None):
    """
    Given a a path to an gate xml, generate a object representation of it

    :param file_path: a pathlib object that points to the annotation file
    :type Path:

    :param exclude_sets: a list of annotation sets to ignoree
    :type list:

    :param annotator: the name of the current annotator
    :type name:


    :return document_content: a dictionary containing the contents of the annotated document
    :param dict

    """

    document_content = {}
    tree = etree.parse(str(file_path))
    root = tree.getroot()
    document_content['text'] = etree.tostring(tree.find('TextWithNodes'), encoding='utf-8', 
                                                                          method="text", 
                                                                          with_tail = False).decode()
    document_content['annotation_sets'] = {}

    for annotation_set in tree.findall("./AnnotationSet"):
        if annotation_set.attrib == "":
            set_name = 'default_annotation_set'
        else:
            set_name = annotation_set.attrib['Name']

        if set_name in exclude_sets:
            continue # skip this section

        document_content['annotation_sets'][set_name] = []

        for annotation in annotation_set.findall(".Annotation"):
            annotation_dict = {}
            attributes = annotation.attrib
            
            annotation_dict['mention'] = attributes['Type']
            annotation_dict['start'] = int(attributes['StartNode'])
            annotation_dict['end'] = int(attributes['EndNode'])
            annotation_dict['id'] = attributes['Id']
            annotation_dict['text_span'] = document_content['text'][annotation_dict['start']:annotation_dict['end']]

            features = {}
            for att, val in zip(annotation.findall("./Feature/Name"), annotation.findall("./Feature/Value")):
                features[att.text] = val.text

            annotation_dict['features'] = features
            annotation_dict['annotator'] = annotator

            document_content['annotation_sets'][set_name].append(annotation_dict)

    return document_content

def create_corpus(annotations_dir = None, strict_matches=False):
    '''
    Creates a corpus structure using nested dictionaries

    :param annotations_dir: the path object to the annotated files
    :type Pathlib

    :param strict_matches: will match the documents that the annotators have in common, 
                           if false this would grab all annotations in the dir
    :type bool

    :return corpus
    :type dict
    '''

    assert annotations_dir, 'please provide a directory for the annotation'

    assert annotations_dir.is_dir(), 'please provide a valid directory'

    annotations = match_file_ids(files=[x for x in annotations_dir.glob('**/*.xml')], strict_matches=strict_matches)
    corpus = {}
    # for loop to populate the entire corpus into a nested dictionary using the glob approach 
    for file_name, paths in annotations.items():
        content = {}
        for path in paths:
            current_annotator = path.parts[len(annotations_dir.parts)] # getting the annotator's name
            content[current_annotator] = read_gate_xml(file_path = path, annotator=current_annotator) 

        corpus[file_name] = dict(sorted(content.items(), key=lambda x: x[0].lower()))



    return corpus

def match_file_ids(files, strict_matches = True, filter_documents = []):
    """
    Given a list of document paths, match all documents by their file id

    :param files: list of document paths
    :type list:

    :strict_matches: used to test if the function shoulf return the complete set of documents or only those that had
    a pair
    :type boolean

    :filter_documents: list of document ids to keep
    :type list

    
    :return a dictionary that contains the file names as keys and all it's matching files as values
    :type dict

    """
    temp = {}

    for file in files:
        try:
            temp[file.stem].append(file)
        except KeyError as e:
            temp[file.stem] = [file]

    # filtering out documents that did not match
    if strict_matches:
        matches = {x[0].stem : x for x in temp.values() if len(x) > 1}
    else:
        matches = {x[0].stem : x for x in temp.values()}

    if filter_documents:
        matches = {k : v for k, v in matches.items() if v in filter_out}


    return(matches)







