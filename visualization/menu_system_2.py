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

import os, sys, tty ,termios
from termcolor import colored


class _Getch:
    def __init__(self, i):
        self.i = i

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(self.i)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Menu():
    """
    A representation of a simple command line menu system.

    :parameter title: a string representation of the menu's name
    :type title: string
    :parameter options: a dictionary containing the options that the user could select from
    :type options: dict
    :parameter parent_menu: the parent menu of a current menu
    :type parent_menu: Menu
    :parameter child_menus: the child menus accesible from the current menu
    :type child_menus: dict

    """

    os.system('clear')
    def __init__(self, title=None, options=None):
        self.title = title
        self.options = options
        self.parent_menu = None
        self.child_menus = {}
        self.previous_execution = None
        self.highlighted_option = {list(self.options.keys())[0]:self.options[list(self.options.keys())[0]]} if not self.options is None else None
        
        # links parents and children based on the contents of the options dict
        self.create_links()

    @property
    def title(self):
        """
        :type: Menu
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @title.deleter
    def title(self):
        """
        :type: Menu
        """
        del self._title

    @property
    def options(self):
        """
        :type: Menu
        """
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @options.deleter
    def options(self):
        """
        :type: Menu
        """
        del self._options

    @property
    def parent_menu(self):
        """
        :type: Menu
        """
        return self._parent_menu

    @parent_menu.setter
    def parent_menu(self, value):
        self._parent_menu = value
        if isinstance(value, Menu) and not value.has_children():
            value.child_menus = [self]

    @parent_menu.deleter
    def parent_menu(self):
        """
        :type: Menu
        """
        del self._parent_menu

    @property
    def child_menus(self):
        """
        :type: Menu
        """
        return self._child_menus

    @child_menus.setter
    def child_menus(self, value):

        self._child_menus = value
        if isinstance(value, Menu) and not value.has_parent():
            value.parent_menu = self

    @child_menus.deleter
    def child_menus(self):
        """
        :type: Menu
        """
        del self._child_menus

    def __repr__(self):
        """
        :type: Menu
        """
        return '{}'.format(self.title.title())

    def has_parent(self):
        """
        :type: Menu
        """
        return not self.parent_menu is None

    def has_children(self):
        return not self.child_menus is None

    def list_parent(self):
        return self.parent_menu.title.title() if self.has_parent() else None

    def list_children(self):
        return list(self.child_menus.keys())

    def is_parent_of(self, other):
        return self.child_menus == other

    def is_child_of(self, other):
        return self.parent_menu == other

    def is_empty(self):
        return len(self.options) < 1

    def add_option(self, new_option):
        assert isinstance(new_option, dict)
        self.options.update(new_option)

    def create_links(self):
        """
        Creates parent/child relationships based on options dictionary
        if an option is another menu, link the menus

        :type: Menu
        """
        for v in self.options.values():
            if isinstance(v, Menu):
                if not v.title in self.child_menus.keys():
                    self.child_menus[v.title] = v
                    v.parent_menu = self

    def generation(self):

        if not self.has_parent():
            return {'1':self}
        root = self.return_root()
        descendants = root.descendants()

        for x, y in descendants.items():
            if self.title in list(y.keys()):
                return {x:y[self.title]}


    def ascendants(self, reverse=False):
        def gather_ascendants(menu, d):

            if not menu.has_parent():
                return d
            else:
                d[menu.parent_menu.title] = menu.parent_menu
                return gather_ascendants(menu.parent_menu, d)

        dict_of_ascendants = gather_ascendants(self, {})

        return {v: k for k, v in dict_of_ascendants.items()} if reverse else dict_of_ascendants

    def descendants(self):
        def gather_descendants(menu,d):
            
            if not menu:
                last_key = list(d.keys())[len(d) - 1]
                del d[last_key] 

                return d
            else: 
                menu_titles =  list(menu.keys())
                menu_contents = list(menu.values())
                sibiling = menu_contents[0]

                last_key = list(d.keys())[len(d) - 1]
                d[last_key] = sibiling.parent_menu.child_menus
                next_key = str(int(last_key) + 1)
                d[next_key] = None
                return gather_descendants(sibiling.child_menus, d)

        return gather_descendants(self.child_menus, {'2':None})

    def sibilings(self):

        return {x:y for x, y in self.parent_menu.child_menus.items() if not self == y} if self.has_parent() else {}


    def return_root(self):

        def root_search(m):

            return m if m.parent_menu is None else root_search(m.parent_menu)

        return root_search(self)
        

    def run_menu(self):
        os.system('clear')
        

        print('{}'.format(self.title.title()))
        print('Please choose an option:\n')

        self.add_option({})
        labels = list(self.options.keys())
        menu_actions = {x+1:self.options[labels[x]] for x in range(len(labels))}

        for option, i in zip(labels, menu_actions.keys()):
            try:
                self.highlighted_option[option]
                print('\x1b[1;30;47m{}){}\x1b[0m'.format(i, option))
            except KeyError as e:
                print('{}){}'.format(i, option))

        if not self.has_parent():
            if self.highlighted_option == {'Exit':None}:
                print('\x1b[1;30;47m{}){}\x1b[0m'.format(0, 'Exit'))
            else:
                print('{}){}'.format(0, 'Exit'))

        print('\n')
        
        if self.has_parent():
            print('Press spacebar to refresh the screen')
            print('Press backspace to go back to {}'.format(self.parent_menu.title.title()))
        else:
            print('Press spacebar to refresh the screen')

        if not self.previous_execution is None:
            if not isinstance(self.previous_execution, Menu):
                self.previous_execution()

        self.read_input()

    def read_input(self):

        def get_user_input():
            key = _Getch(i=1) 
   
            while(True):

                k = key()
                if k == '\x1b':
                    movement = {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[_Getch(i=1)() + _Getch(i=1)()]
                    try:

                        x = {'up':-1, 'down':1}[movement]
                        

                    except KeyError as e:
                        self.refresh()
                        continue

                    current_option_name = list(self.highlighted_option.keys())[0]
                    options_keys = list(self.options.keys())

                    try:
                        current_option_index = options_keys.index(current_option_name)
                    except ValueError as e:
                        current_option_index = len(options_keys) 

                    if current_option_index  == len(options_keys) - 1:
                            if x > 0:
                                current_option_index = 0
                                self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                                if not self.has_parent():
                                    self.highlighted_option = {'Exit':None}
                                self.refresh()
                            elif x < 0:
                                current_option_index += x
                                self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                                self.refresh()
                    if current_option_index == 0:
                        if x < 0:
                            current_option_index = len(options_keys) - 1
                            self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                            if not self.has_parent():
                                self.highlighted_option = {'Exit':None}
                            self.refresh()
                    if current_option_index == len(options_keys):
                        if x > 0:
                            current_option_index = 0
                            self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                            self.refresh()

                        if x < 0:
                            current_option_index = len(options_keys) - 1
                            self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                            self.refresh()


                    if current_option_index + x in range(0, len(options_keys)):
                        current_option_index += x
                        self.highlighted_option = {options_keys[current_option_index]:self.options[options_keys[current_option_index]]}
                        self.refresh()

                elif k == ' ':
                    #print('spacebar') # refresh
                    self.previous_execution = None
                    self.validate_user_input(k)
                    
                elif k == '\t': # exit
                    self.previous_execution = None
                    self.validate_user_input(k)
                elif k == '\x7f':
                    #print('backspace')
                    self.previous_execution = None
                    self.validate_user_input(k)
                elif k == '\r':

                    self.previous_execution = self.validate_user_input(k)
                    if not isinstance(self.previous_execution, Menu):
                        self.refresh()
                    self.previous_execution()
  
                else:
                    pass
                    
        get_user_input()


    def remove_option(self, selection):

        assert selection in list(self.options.keys()), 'Selection not found in the options of this menu'

        if isinstance(self.options[selection], Menu):
            if self.options[selection].has_children:
                if self.options[selection].has_parent:
                    for child_name, child_menu in self.options[selection].child_menus.items():
                        child_menu.parent_menu = self.options[selection].parent_menu
                        child_menu.parent_menu.child_menus[child_name] = child_menu
                        del self.options[selection]
                        del self.child_menus[selection]
        else:
            del self.options[selection]
        

    def validate_user_input(self, i):

        
        if i == '\x7f':
            self.back()

        if i == ' ':
            self.refresh() # refresh

        if i == '\t' and not self.has_parent():
            self.exit()

        if i =='\r':

            if self.highlighted_option == {'Exit': None}:
                self.exit()
            else:

                key = list(self.highlighted_option.keys())[0]
                if isinstance(self.options[key], Menu):
                    self.options[key].run_menu()
                else:
                    return self.options[key]
                self.refresh()
        
                   
    def refresh(self):
        '''
            Refreshes the screen contents

        '''
        self.run_menu()

    def back(self):
        '''
            Goes to the previous menu, if current menu does not have any previous menus then it refreshes the page

        '''
        if self.has_parent():
            self.parent_menu.run_menu()
        else:
            self.refresh()

    def exit(self):
        '''
            Quits the menu
        '''
        sys.exit()
