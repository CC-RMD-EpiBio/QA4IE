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
from pathlib import Path
import curses
import locale
from functools import reduce



def print_document(filters=[]):

    file = filters[0].title
    annotator_name = filters[1].title


    document = settings.corpus[file][annotator_name]['text']

    filecontent = document

    encoding = 'utf-8'
    filename = file 
    
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    rows, columns = stdscr.getmaxyx()
    stdscr.border()
    bottom_menu = u"(↓) Next line | (↑) Previous line | (→) Next page | (←) Previous page | (q) Quit".encode(encoding).center(columns - 4)
    stdscr.addstr(rows - 1, 2, bottom_menu, curses.A_REVERSE)
    out = stdscr.subwin(rows - 2, columns - 2, 1, 1)
    out_rows, out_columns = out.getmaxyx()
    out_rows -= 1
    lines = map(lambda x: x + " " * (out_columns - len(x)), reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in range(0, len(x), out_columns)] for x in filecontent.expandtabs(4).splitlines()]))
    stdscr.refresh()
    line = 0
    while True:
        top_menu = (u"Lines %d to %d of %d of %s" % (line + 1, min(len(lines), line + out_rows), len(lines), filename)).encode(encoding).center(columns - 4)
        stdscr.addstr(0, 2, top_menu, curses.A_REVERSE)
        out.addstr(0, 0, "".join(lines[line:line+out_rows]))
        stdscr.refresh()
        out.refresh()
        c = stdscr.getch()
        if c == ord("q"):
            break
        elif c == curses.KEY_DOWN:
            if len(lines) - line > out_rows:
                line += 1
        elif c == curses.KEY_UP:
            if line > 0:
                line -= 1
        elif c == curses.KEY_RIGHT:
            if len(lines) - line >= 2 * out_rows:
                line += out_rows
        elif c == curses.KEY_LEFT:
            if line >= out_rows:
                line -= out_rows

    return document
