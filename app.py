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
import curses
import locale
from itertools import combinations
from load_data import settings
from menu import menu_system
from validation import validation_menu_functions 
from error_checks import error_checks_menu_functions
from stats import statistics_menu_functions
from evaluation import evaluation_menu_functions


sys.setrecursionlimit(10**6)

def run_app(stdscr):
    if len(list(settings.corpus.keys())) == 1:
        file_names = list(settings.corpus.keys())
    else:
        file_names = ['corpus'] + list(settings.corpus.keys())

    if len(list(set([n for f, c in settings.corpus.items() 
                                           for a, b in c.items() 
                                           for n in b['annotation_sets']]))) == 1:
        set_names = list(set([n for f, c in settings.corpus.items() 
                                               for a, b in c.items() 
                                               for n in b['annotation_sets']]))
    else:
        set_names = ['all_sets'] + list(set([n for f, c in settings.corpus.items() 
                                               for a, b in c.items() 
                                               for n in b['annotation_sets']]))

   
    if len(list(set([a for k, v in settings.corpus.items()
                                        for a in v.keys()]))) == 1:
        annotators = list(set([a for k, v in settings.corpus.items() 
                                            for a in v.keys()]))
    else:
        annotators = ['team'] + list(set([a for k, v in settings.corpus.items() 
                                            for a in v.keys()]))

    if len(['{}-{}'.format(x, y) for x, y in combinations(annotators[1:], 2)]) == 1:
        annotator_pairs = ['{}-{}'.format(x, y) for x, y in combinations(annotators[1:], 2)]
    else:
        annotator_pairs = ['team'] +  ['{}-{}'.format(x, y) for x, y in combinations(annotators[1:], 2)]

    if len(settings.schema.get_entity_names()) == 1:
        annotation_types = settings.schema.get_entity_names()
    else:
        annotation_types = ['all_types'] + settings.schema.get_entity_names()



    file_name_options = menu_system.MenuToolBarOptions(option_rack=file_names)
    set_name_options = menu_system.MenuToolBarOptions(option_rack=set_names)
    if len(file_names) > 1:
      file_name_options_no_general = menu_system.MenuToolBarOptions(option_rack=file_names[1:])
    else:
      file_name_options_no_general = menu_system.MenuToolBarOptions(option_rack=file_names)
    if len(set_names) > 1:
      set_name_options_no_general = menu_system.MenuToolBarOptions(option_rack=set_names[1:])
    else:
      set_name_options_no_general = menu_system.MenuToolBarOptions(option_rack=set_names)
    annotator_options = menu_system.MenuToolBarOptions(option_rack=annotators)
    if len(annotators) > 1:
      annotator_options_no_general = menu_system.MenuToolBarOptions(option_rack=annotators[1:])
    else:
      annotator_options_no_general = menu_system.MenuToolBarOptions(option_rack=annotators)
    annotator_pair_options = menu_system.MenuToolBarOptions(option_rack=annotator_pairs)
    annotation_types_options = menu_system.MenuToolBarOptions(option_rack=annotation_types)
    if len(annotation_types) > 1:
      annotation_types_options_no_general = menu_system.MenuToolBarOptions(option_rack=annotation_types[1:])
    else:
      annotation_types_options_no_general = menu_system.MenuToolBarOptions(option_rack=annotation_types)
    measure_options = menu_system.MenuToolBarOptions(option_rack=['Average', 'Strict', 'Lenient'])

    error_checks_tool_bar = menu_system.MenuToolBar(title = 'Error Checks Menu Tool Bar',
                             options=[menu_system.MenuAction(file_name_options.title, 
                                                             file_name_options.return_options),
                                      menu_system.MenuAction(annotator_pair_options.title, 
                                                             annotator_pair_options.return_options)],
                             slots = ['File', 'Annotator Pair'])


    corpus_viewer_tool_bar = menu_system.MenuToolBar(title = 'Corpus Viewer Tool Bar',
                           options=[menu_system.MenuAction(file_name_options_no_general.title, 
                                                           file_name_options_no_general.return_options),
                                    menu_system.MenuAction(annotator_options_no_general.title, 
                                                           annotator_options_no_general.return_options),
                                    menu_system.MenuAction(set_name_options_no_general.title,
                                                           set_name_options_no_general.return_options),
                                    menu_system.MenuAction(annotation_types_options_no_general.title, 
                                                           annotation_types_options_no_general.return_options)],
                           slots = ['File', 'Annotator', 'Set Name', 'Annotation Type'])


    validation_tool_bar = menu_system.MenuToolBar(title = 'Validation Menu Tool Bar',
                             options=[menu_system.MenuAction(file_name_options.title, 
                                                             file_name_options.return_options),
                                      menu_system.MenuAction(set_name_options.title,
                                                             set_name_options.return_options),
                                      menu_system.MenuAction(annotator_options.title, 
                                                             annotator_options.return_options),
                                      menu_system.MenuAction(annotation_types_options.title, 
                                                             annotation_types_options.return_options)],
                             slots = ['File', 'Set Name', 'Annotator', 'Entity'])

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
                             slots = ['File', 'Set Name', 'Key', 'Response', 'Entity', 'Measure'])

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
                             slots = ['File', 'Set Name', 'Key', 'Response', 'Entity'])

    cohens_kappa_tool_bar = menu_system.MenuToolBar(title = 'Cohens Kappa Menu Tool Bar',
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
                             slots = ['File', 'Set Name', 'Key', 'Response', 'Entity'])

    discrepancy_tool_bar = menu_system.MenuToolBar(title = 'Discrepancy Menu Tool Bar',
                             options=[menu_system.MenuAction(file_name_options.title, 
                                                             file_name_options.return_options),
                                      menu_system.MenuAction(annotator_pair_options.title, 
                                                             annotator_pair_options.return_options)],
                             slots = ['File', 'Annotator Pair'])

    statistics_tool_bar = menu_system.MenuToolBar(title = 'Validation Menu Tool Bar',
                             options=[menu_system.MenuAction(file_name_options.title, 
                                                             file_name_options.return_options),
                                      menu_system.MenuAction(set_name_options.title,
                                                             set_name_options.return_options),
                                      menu_system.MenuAction(annotator_options.title, 
                                                             annotator_options.return_options),
                                      menu_system.MenuAction(annotation_types_options.title, 
                                                             annotation_types_options.return_options)],
                             slots = ['File', 'Set Name', 'Annotator', 'Entity'])


    error_checks_menu = menu_system.Menu(title='Document Validations', 
                      options=[menu_system.MenuAction('Text Differences', 
                                                      error_checks_menu_functions.check_text_differences),
                               menu_system.MenuAction('Set Name Differences', 
                                                      error_checks_menu_functions.check_set_name_differences,),
                               menu_system.MenuAction('Generate Report', 
                                                      error_checks_menu_functions.generate_error_checks_report)], 
                      tool_bar=error_checks_tool_bar,
                      screen=stdscr,
                      inherit_settings=True)
    if [y for x, y in settings.schema.entities.items() if y.is_sub_entity()]:
        validation_menu = menu_system.Menu(title='Annotation Validations', 
                          options=[menu_system.MenuAction('Annotation Overlaps', 
                                              validation_menu_functions.validate_overlaps),
                                   menu_system.MenuAction('Subentity Boundaries', 
                                              validation_menu_functions.validate_subentity_boundaries),
                                   menu_system.MenuAction('Annotation Boundaries (TODO)', 
                                              validation_menu_functions.validate_annotation_boundaries),
                                   menu_system.MenuAction('Negative Length Annotations (TODO)'),
                                   menu_system.MenuAction('Zero Length Annotations (TODO)'),
                                   menu_system.MenuAction('Document Scope',
                                    validation_menu_functions.validate_annotation_scope),
                                   menu_system.MenuAction('Validate Schema', 
                                              validation_menu_functions.validate_schema_values),
                                   menu_system.MenuAction('Generate Report', 
                                              validation_menu_functions.generate_validation_report)], 
                          tool_bar=validation_tool_bar,
                          screen=stdscr,
                          inherit_settings=True)
    else:
        validation_menu = menu_system.Menu(title='Annotation Validations', 
                  options=[menu_system.MenuAction('Annotation Overlaps', 
                                      validation_menu_functions.validate_overlaps),
                           menu_system.MenuAction('Annotation Boundaries (TODO)', 
                                      validation_menu_functions.validate_annotation_boundaries),
                           menu_system.MenuAction('Negative Length Annotations (TODO)'),
                           menu_system.MenuAction('Zero Length Annotations (TODO)'),
                           menu_system.MenuAction('Document Scope',
                            validation_menu_functions.validate_annotation_scope),
                           menu_system.MenuAction('Validate Schema', 
                                      validation_menu_functions.validate_schema_values),
                           menu_system.MenuAction('Generate Report', 
                                      validation_menu_functions.generate_validation_report)], 
                  tool_bar=validation_tool_bar,
                  screen=stdscr,
                  inherit_settings=True)




    if settings.task == 'sequence_labelling':
      entity_level_menu = menu_system.Menu(title='Entity Level', 
                                    options=[menu_system.MenuAction('Evaluate')], 
                                    tool_bar = entity_lvl_tool_bar,
                                    screen=stdscr,
                                    inherit_settings=True)

      token_level_menu = menu_system.Menu(title='Token Level', 
                                          options=[menu_system.MenuAction('Evaluate', 
                                                  evaluation_menu_functions.token_eval)], 
                                          tool_bar = token_lvl_tool_bar,
                                          screen=stdscr,
                                          inherit_settings=True)
      evaluation_menu = menu_system.Menu(title='Evaluation', 
                                         options=[entity_level_menu, token_level_menu], 
                                         screen=stdscr,
                                         inherit_settings=True)
    if settings.task == 'classification':
      cohens_kappa_menu = menu_system.Menu(title='Cohens Kappa', 
                                          options=[menu_system.MenuAction('Evaluate',
                                            evaluation_menu_functions.cohens_kappa)], 
                                          tool_bar = cohens_kappa_tool_bar,
                                          screen=stdscr,
                                          inherit_settings=True)
      evaluation_menu = menu_system.Menu(title='Evaluation', 
                                         options=[cohens_kappa_menu], 
                                         screen=stdscr,
                                         inherit_settings=True)

    discrepancy_menu = menu_system.Menu(title='Discrepancy Analysis', 
                                       options=[menu_system.MenuAction('Compare')], 
                                       tool_bar = discrepancy_tool_bar,
                                       screen=stdscr,
                                       inherit_settings=True)

    statistics_menu = menu_system.Menu(title='Statistics', 
                                       options=[menu_system.MenuAction('Entity Distribution',
                                                statistics_menu_functions.count_entities),
                                                menu_system.MenuAction('Entity/Features Distribution',
                                                statistics_menu_functions.count_entities_with_features),
                                                menu_system.MenuAction('Entity Token Length Distribution',
                                                statistics_menu_functions.entity_token_stats),
                                                menu_system.MenuAction('Entity/Features Token Length Distribution',
                                                statistics_menu_functions.entity_with_features_token_stats),
                                                menu_system.MenuAction('Generate Report',
                                                statistics_menu_functions.generate_statistics_report)], 
                                       tool_bar = statistics_tool_bar,
                                       screen=stdscr,
                                       inherit_settings=True)


    help_menu = menu_system.HelpMenu(title='Help',
                                     screen=stdscr,
                                     inherit_settings=True)




    schema_viewer = menu_system.SchemaMenu(title='Annotation Schema',
                                           options=[],
                                           screen=stdscr,
                                           inherit_settings=True)


    corpus_viewer = menu_system.CorpusViewerMenu(title='Corpus Viewer',
                                     options=[],
                                     screen=stdscr,
                                     tool_bar = corpus_viewer_tool_bar,
                                     inherit_settings=True)


    main_menu =  menu_system.Menu(title='QA4IE Main Menu', 
                      options=[error_checks_menu, 
                               validation_menu, 
                               statistics_menu,
                               evaluation_menu, 
                               discrepancy_menu, 
                               menu_system.MenuAction('Generate Reports', generate_all_reports),
                               corpus_viewer,
                               schema_viewer,
                               help_menu], 
                      screen=stdscr)

    try:
      try:
        curses.noecho()
        curses.curs_set(0)

        main_menu.run_menu()
      except curses.error as e:
        print(e)
    finally:
      curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.curs_set(1)
      curses.endwin() 

def generate_all_reports():
    error_checks_menu_functions.generate_error_checks_report()
    validation_menu_functions.generate_validation_report()
    statistics_menu_functions.generate_statistics_report()

    return 'report generated in {}'.format(settings.output_dir)


def main():
  try:
    if len(sys.argv) == 1:
      path = sys.argv[1]
    else:
      path = ' '.join([x for x in sys.argv[1:]])
    
    settings.init(path)
  except IndexError as e:
      print('Usage: python {} <path_to_file>'.format( __file__))

  else:
    try:

        curses.wrapper(run_app)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(0)
    except:
      # curses.nocbreak()
      # curses.keypad(0)
      
      # curses.echo()
      # curses.endwin()
      #curses.wrapper(run_app)
      raise
    

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    encoding = locale.getpreferredencoding()

    main()
    
    


