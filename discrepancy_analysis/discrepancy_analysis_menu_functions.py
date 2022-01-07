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
from load_data import settings
from itertools import combinations
from collections import Counter
import collections
from discrepancy_analysis import discrepancy_analysis
from pathlib import Path
import pandas as pd


def compare_annotations(filters=[]):
    # 1) filter data based on filters
    # 2) run THIS qa function
    # 3) return string of output
    
    file = filters[0].title
    annotator_pair = filters[1].title

    output = ''

    if file == 'corpus': # all notes
        if annotator_pair == 'team': # all annotators
            document_annotations = {}
            aligned_discrepancies = {}
            for file_name, annotators in settings.corpus.items():
                for annotator_name, annotator_contents in annotators.items():
                    ans = []
                    for set_name, annotations in annotator_contents['annotation_sets'].items():
                        for annotation in annotations:
                            if annotation['mention'] in settings.schema.entities:
                                ans.append(annotation)
                    document_annotations[annotator_name] = ans
                        

                temp_annotation_container = []
                annotator_names = []
                for a, b in document_annotations.items():
                    annotator_names.append(a)
                    temp_annotation_container.append(discrepancy_analysis.apply_hierarchical_structure(settings.schema.entities, b))
                    #output += '{}\n'.format(b)


                
                                                                                          
            
                temp_annotation_container = [y for x in temp_annotation_container for y in x]
                clusters = discrepancy_analysis.cluster_annotations(temp_annotation_container)



                temp = discrepancy_analysis.align_all_clusters(clusters, settings.schema.get_main_entity_names(), 
                                                                file = file_name, all_annotators=annotator_names)

                for k in temp:
                    if k in aligned_discrepancies.keys():
                        aligned_discrepancies[k] += temp[k]
                    else:
                        aligned_discrepancies[k] = temp[k]

            text_disc_distribution, feature_disc_distribution = discrepancy_analysis.determine_discrepancies(aligned_discrepancies)

            output += 'text discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(text_disc_distribution)).items()])
            output += '\nfeature discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(feature_disc_distribution)).items()])

               
        else: # pairs
            aligned_discrepancies = {}
            for file_name, annotators in settings.corpus.items():
                anno1 = annotator_pair.split('-')[0]
                anno2 = annotator_pair.split('-')[1]

                anno1_annotations = [a for set_name, ans in annotators[anno1]['annotation_sets'].items() for a in ans]
                anno2_annotations = [a for set_name, ans in annotators[anno2]['annotation_sets'].items() for a in ans]

                document_annotations = [discrepancy_analysis.apply_hierarchical_structure(settings.schema.entities, x) 
                                                                                         for x in [anno1_annotations, anno2_annotations]]

                document_annotations = [y for x in document_annotations for y in x]

                clusters = discrepancy_analysis.cluster_annotations(document_annotations)

                temp = discrepancy_analysis.align_all_clusters(clusters, settings.schema.get_main_entity_names(), 
                                                               file = file_name, all_annotators=[anno1, anno2])

                for k in temp:
                    if k in aligned_discrepancies.keys():
                        aligned_discrepancies[k] += temp[k]
                    else:
                        aligned_discrepancies[k] = temp[k]

            text_disc_distribution, feature_disc_distribution = discrepancy_analysis.determine_discrepancies(aligned_discrepancies)

            output += 'text discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(text_disc_distribution)).items()])
            output += '\nfeature discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(feature_disc_distribution)).items()])

    else: # single notes
        if annotator_pair == 'team':  # all annotators
            document_annotations = {}
            aligned_discrepancies = {}
            for annotator_name, annotator_contents in settings.corpus[file].items():
                ans = []
                for set_name, annotations in annotator_contents['annotation_sets'].items():
                    for annotation in annotations:
                        if annotation['mention'] in settings.schema.entities:
                            ans.append(annotation)
                document_annotations[annotator_name] = ans
                    

            temp_annotation_container = []
            annotator_names = []
            for a, b in document_annotations.items():
                annotator_names.append(a)
                temp_annotation_container.append(discrepancy_analysis.apply_hierarchical_structure(settings.schema.entities, b))
                #output += '{}\n'.format(b)


            
                                                                                      
        
            temp_annotation_container = [y for x in temp_annotation_container for y in x]
            clusters = discrepancy_analysis.cluster_annotations(temp_annotation_container)



            temp = discrepancy_analysis.align_all_clusters(clusters, settings.schema.get_main_entity_names(), 
                                                            file = file, all_annotators=annotator_names)

            for k in temp:
                if k in aligned_discrepancies.keys():
                    aligned_discrepancies[k] += temp[k]
                else:
                    aligned_discrepancies[k] = temp[k]

            text_disc_distribution, feature_disc_distribution = discrepancy_analysis.determine_discrepancies(aligned_discrepancies)

            output += 'text discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(text_disc_distribution)).items()])
            output += '\nfeature discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(feature_disc_distribution)).items()])
        else: # pairs
            anno1 = annotator_pair.split('-')[0]
            anno2 = annotator_pair.split('-')[1]

            current_document = settings.corpus[file]

            anno1_annotations = [a for set_name, ans in current_document[anno1]['annotation_sets'].items() for a in ans]
            anno2_annotations = [a for set_name, ans in current_document[anno2]['annotation_sets'].items() for a in ans]

            document_annotations = [discrepancy_analysis.apply_hierarchical_structure(settings.schema.entities, x) for x in [anno1_annotations, anno2_annotations]]

            document_annotations = [y for x in document_annotations for y in x]

            clusters = discrepancy_analysis.cluster_annotations(document_annotations)

            aligned_discrepancies = discrepancy_analysis.align_all_clusters(clusters, settings.schema.get_main_entity_names(), file = file, all_annotators=[anno1, anno2])

            text_disc_distribution, feature_disc_distribution = discrepancy_analysis.determine_discrepancies(aligned_discrepancies)

            output += 'text discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(text_disc_distribution)).items()])
            output += '\nfeature discrepancies\n'
            output += ''.join(['  {} : {}\n'.format(k,v) for k, v in dict(Counter(feature_disc_distribution)).items()])

    return output
 

def generate_discrepancy_report(filters=[]):

    discrepancy_analisys_path = Path(settings.output_dir / 'discrepancy_analysis')
    discrepancy_analisys_path.mkdir(parents=True, exist_ok=True)
    document_annotations = {}
    aligned_discrepancies = {}
    total_discrepancies = {}
    df_list = []
    for file_name, annotators in settings.corpus.items():
        for annotator_name, annotator_contents in annotators.items():
            ans = []
            for set_name, annotations in annotator_contents['annotation_sets'].items():
                for annotation in annotations:
                    if annotation['mention'] in settings.schema.entities:
                        ans.append(annotation)
            document_annotations[annotator_name] = ans
                

        temp_annotation_container = []
        annotator_names = []
        for a, b in document_annotations.items():
            annotator_names.append(a)
            temp_annotation_container.append(discrepancy_analysis.apply_hierarchical_structure(settings.schema.entities, b))
            #output += '{}\n'.format(b)


        
                                                                                  
    
        temp_annotation_container = [y for x in temp_annotation_container for y in x]
        clusters = discrepancy_analysis.cluster_annotations(temp_annotation_container)



        temp = discrepancy_analysis.align_all_clusters(clusters, settings.schema.get_main_entity_names(), 
                                                        file = file_name, all_annotators=annotator_names)

        for k in temp:
            if k in aligned_discrepancies.keys():
                aligned_discrepancies[k] += temp[k]
            else:
                aligned_discrepancies[k] = temp[k]

        temp_text_disc, temp_feature_disc = discrepancy_analysis.determine_discrepancies(temp)
        for x in temp_text_disc:
            try:
                total_discrepancies['text_discrepancies'].append(x)
            except KeyError as e:
                total_discrepancies['text_discrepancies'] = [x]
        for x in temp_feature_disc:
            try:
                total_discrepancies['feature_discrepancies'].append(x)
            except KeyError as e:
                total_discrepancies['feature_discrepancies'] = [x]

        discrepancy_analysis.format_cells(temp)
        df = discrepancy_analysis.create_df(temp)
        df_list.append(df)

    df = pd.concat(df_list)

    with open(discrepancy_analisys_path  / 'discrepancy_summary.txt', 'w') as text_file:
        for x in total_discrepancies:
          text_file.write('{}\n'.format(x))
          for y, z in dict(Counter(total_discrepancies[x])).items():
            text_file.write('\t{} : {}\n'.format(y, z))
  
    
    df.to_csv(discrepancy_analisys_path / 'discrepancy_analysis.csv', index=False)


    return 'report generated in {}'.format(settings.output_dir)
