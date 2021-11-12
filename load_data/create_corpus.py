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
    Functions for creating a representation of a corpus
'''

from load_data.read_annotations import read_gate_xml


def create_corpus(annotations_dir = None, strict_matches=False, encoding='utf-8'):
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
            content[current_annotator] = read_gate_xml(file_path = path, annotator=current_annotator, encoding=encoding) 

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
