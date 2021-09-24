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
from itertools import combinations
from load_data import settings
from visualization import menu_system
from validation import validation_menu_functions 
from error_checks import error_checks_menu_functions


settings.init() 

file_names = ['corpus'] + list(settings.corpus.keys())

set_names = ['all_sets'] + list(set([n for f, c in settings.corpus.items() 
                                       for a, b in c.items() 
                                       for n in b['annotation_sets']]))

annotators = ['team'] + list(set([a for k, v in settings.corpus.items() 
                                    for a in v.keys()]))

annotator_pairs = ['team'] +  ['{}-{}'.format(x, y) for x, y in combinations(annotators[1:], 2)]
annotation_types = ['all_types']

for k, v in settings.schema.items():
    annotation_types.append(k)
    try:
        for s in v['sub_entities']:
            annotation_types.append(s)
    except KeyError as e:
        pass 

file_name_options = menu_system.MenuToolBarOptions(option_rack=file_names)
set_name_options = menu_system.MenuToolBarOptions(option_rack=set_names)
annotator_options = menu_system.MenuToolBarOptions(option_rack=annotators)
annotator_pair_options = menu_system.MenuToolBarOptions(option_rack=annotator_pairs)
annotation_types_options = menu_system.MenuToolBarOptions(option_rack=annotation_types)
measure_options = menu_system.MenuToolBarOptions(option_rack=['Average', 'Strict', 'Lenient'])

error_checks_tool_bar = menu_system.MenuToolBar(title = 'Error Checks Menu Tool Bar',
                         options=[menu_system.MenuAction(file_name_options.title, 
                                                         file_name_options.return_options),
                                  menu_system.MenuAction(annotator_pair_options.title, 
                                                         annotator_pair_options.return_options)],
                         slots = ['File', 'Annotator Pair'],
                         selection_settings=menu_system.MenuSettings(color='green'))

error_checks_menu = menu_system.Menu(title='Error Checks Menu', 
                  options=[menu_system.MenuAction('Text Differences', 
                                                  error_checks_menu_functions.check_text_differences),
                           menu_system.MenuAction('Set Name Differences', 
                                                  error_checks_menu_functions.check_set_name_differences)], 
                  tool_bar=error_checks_tool_bar,
                  inherit_settings=True)


validation_tool_bar = menu_system.MenuToolBar(title = 'Validation Menu Tool Bar',
                         options=[menu_system.MenuAction(file_name_options.title, 
                                                         file_name_options.return_options),
                                  menu_system.MenuAction(set_name_options.title,
                                                         set_name_options.return_options),
                                  menu_system.MenuAction(annotator_options.title, 
                                                         annotator_options.return_options),
                                  menu_system.MenuAction(annotation_types_options.title, 
                                                         annotation_types_options.return_options)],
                         slots = ['File', 'Set Name', 'Annotator', 'Entity'],
                         selection_settings=menu_system.MenuSettings(color='green'))

entity_lvl_tool_bar = menu_system.MenuToolBar(title = 'Entity Level Menu Tool Bar',
                         options=[menu_system.MenuAction(file_name_options.title, 
                                                         file_name_options.return_options),
                                  menu_system.MenuAction(set_name_options.title,
                                                         set_name_options.return_options),
                                  menu_system.MenuAction(annotator_options.title, 
                                                         annotator_options.return_options),
                                  menu_system.MenuAction(annotator_options.title, 
                                                         annotator_options.return_options),
                                  menu_system.MenuAction(annotation_types_options.title, 
                                                         annotation_types_options.return_options),
                                  menu_system.MenuAction(measure_options.title, 
                                                         measure_options.return_options)],
                         slots = ['File', 'Set Name', 'Key', 'Response', 'Entity', 'Measure'],
                         selection_settings=menu_system.MenuSettings(color='green'))

token_lvl_tool_bar = menu_system.MenuToolBar(title = 'Token Level Menu Tool Bar',
                         options=[menu_system.MenuAction(file_name_options.title, 
                                                         file_name_options.return_options),
                                  menu_system.MenuAction(set_name_options.title,
                                                         set_name_options.return_options),
                                  menu_system.MenuAction(annotator_options.title, 
                                                         annotator_options.return_options),
                                  menu_system.MenuAction(annotator_options.title, 
                                                         annotator_options.return_options),
                                  menu_system.MenuAction(annotation_types_options.title, 
                                                         annotation_types_options.return_options)],
                         slots = ['File', 'Set Name', 'Key', 'Response', 'Entity'],
                         selection_settings=menu_system.MenuSettings(color='green'))

discrepancy_tool_bar = menu_system.MenuToolBar(title = 'Discrepancy Menu Tool Bar',
                         options=[menu_system.MenuAction(file_name_options.title, 
                                                         file_name_options.return_options),
                                  menu_system.MenuAction(annotator_pair_options.title, 
                                                         annotator_pair_options.return_options)],
                         slots = ['File', 'Annotator Pair'],
                         selection_settings=menu_system.MenuSettings(color='green'))

validation_menu = menu_system.Menu(title='Validation Menu', 
                  options=[menu_system.MenuAction('Validate Overlaps', 
                                      validation_menu_functions.validate_overlaps),
                           menu_system.MenuAction('Validate Subentity Boundaries', 
                                      validation_menu_functions.validate_subentity_boundaries),
                           menu_system.MenuAction('Validate Subentity Partial Overlaps', 
                                      validation_menu_functions.validate_subentity_partial_overlap),
                           menu_system.MenuAction('Validate Annotation Boundaries', 
                                      validation_menu_functions.validate_annotation_boundaries),
                           menu_system.MenuAction('Validate Schema', 
                                      validation_menu_functions.validate_schema_values)], 
                  tool_bar=validation_tool_bar,
                  inherit_settings=True)


entity_level_menu = menu_system.Menu(title='Entity Level', 
                                    options=[menu_system.MenuAction('Evaluate')], 
                                    tool_bar = entity_lvl_tool_bar,
                                    inherit_settings=True)

token_level_menu = menu_system.Menu(title='Token Level', 
                                    options=[menu_system.MenuAction('Evaluate')], 
                                    tool_bar = token_lvl_tool_bar,
                                    inherit_settings=True)

evaluation_menu = menu_system.Menu(title='Evaluation Menu', 
                                   options=[entity_level_menu, token_level_menu], 
                                   inherit_settings=True)

discrepancy_menu = menu_system.Menu(title='Discrepancy Menu', 
                                   options=[menu_system.MenuAction('Compare')], 
                                   tool_bar = discrepancy_tool_bar,
                                   inherit_settings=True)


main_menu =  menu_system.Menu(title='QA4IE Main Menu', 
                  options=[error_checks_menu, 
                           validation_menu, 
                           evaluation_menu, 
                           discrepancy_menu, 
                           menu_system.MenuAction('Generate Report')], 
                  selection_settings=menu_system.MenuSettings(color='green'))

main_menu.run_menu()


