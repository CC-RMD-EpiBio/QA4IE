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
from load_data import settings
import copy
import string
import curses
import locale
from functools import reduce



class KeyboardReader():
    def __init__(self):
        self.key_mappings = {
                        127:'backspace',
                        10: 'enter',
                        32: 'space',
                        9: 'tab',
                        27: 'esc',
                        259: 'up',
                        258: 'down',
                        261: 'right',
                        260: 'left',
                        114: 'r'
                           }
        
    def read_key(self, scr):
        k =  scr.getch()
        try:
            return self.key_mappings[k]
        except KeyError as e:
            if k == curses.KEY_RESIZE:
                return '--'
            else:
                scr.refresh()

class MenuPrint():

    def __init__(self, output=None, settings=None):
        self.output = '' if output is None else output
        self.settings = settings

    def print_in_console(self):
        print('{}'.format(self.settings.format_str(self.output)))

class MenuToolBarOptions():
    def __init__(self, option_rack = None):
        self.option_rack = option_rack if option_rack else []
        self.title = self.option_rack[0] if self.option_rack else ''

    def show_options(self, x = None):

        if x is None:
            pass
        else:
            l = self.option_rack
            current_option = x.title
            #var = current_option
            if not current_option in l:
                pass
            else:
                current_option_index = l.index(current_option)
                if current_option_index == len(l)-1:
                    next_option_index = 0
                else:
                    next_option_index = current_option_index + 1
                return l[next_option_index]
    def return_options(self):
        return self.option_rack

class MenuToolBar():
    

    def __init__(self, title = None, options = None, previous_execution = None, highlighted_option = None, text_settings = None, selection_settings = None, slots=None):
        
        self.title = title
        self.options = options
        self.slots = string.ascii_lowercase[0: len(self.options)] if slots is None else slots
        self.default_options = copy.deepcopy(options)
        self.previous_execution = MenuAction()
        self.highlighted_option = MenuAction()

        #self.text_settings = MenuSettings(color='white', attributes=[]) if text_settings is None else text_settings
        
        #self.selection_settings = MenuSettings(color='white', attributes=['reverse', 'bold']) if selection_settings is None else selection_settings

    def generate_toolbar(self, scr, color, width):

        height, width = scr.getmaxyx()
        bar = [o.title for o in self.options]
        assert len(self.slots) == len(bar), 'need to add slot names in tool bar {}'.format(self.title)
        # if self.highlighted_option.title == 'Exit':
        #     self.screen.addstr(len(self.options.keys()) + 5, 0, '{}'.format('Exit'), curses.color_pair(1))
        # else:
        #     self.screen.addstr(len(self.options.keys()) + 5, 0, '{}'.format('Exit'))
        x = 0
        try:
            for i, j in zip(range(0, len(self.options)), range(0, len(self.slots))):
                if x >= width:
                    break
                if self.options[i] == self.highlighted_option:
                    scr.addstr(1, x, '{}'.format(self.slots[j]))
                    x += len(self.slots[j]) + 1
                    scr.addstr(1, x, '{}'.format(':'))
                    x += 2
                    scr.addstr(1, x, '{}'.format(self.options[i].title), color)
                    x += len(self.options[i].title) + 1
                else:
                    scr.addstr(1, x, '{}'.format(self.slots[j]))
                    x += len(self.slots[j]) + 1
                    scr.addstr(1, x, '{}'.format(':'))
                    x += 2
                    scr.addstr(1, x, '{}'.format(self.options[i]))
                    x += len(self.options[i].title) + 1
        except curses.error as e:
            pass



        
        # bar = ['{} : {}'.format(self.text_settings.format_str(x), y) for x, y in zip(self.slots, bar)]
        # return '  '.join(bar)

    def reset_toolbar(self):

        if self.previous_execution:
    
            try:
                highlighted_option_index = self.options.index(self.highlighted_option)
                self.options = [MenuAction(do.title, o.action) for o, do in zip(self.options, self.default_options)]
                self.highlighted_option = self.options[highlighted_option_index]
            except ValueError as e:
                self.options = [MenuAction(do.title, o.action) for o, do in zip(self.options, self.default_options)]


    def update_toolbar(self, x=None, scr=None, color=None, width=0):

        if not x is None:
            try:
                current_option_index = self.options.index(self.highlighted_option)

            except ValueError as e:

                current_option_index = 0
            
            if current_option_index == 0:
                if x < 0:
                    self.highlighted_option = self.options[len(self.options) - 1]
                if x > 0:
                    self.highlighted_option = self.options[current_option_index + x]

            if current_option_index == len(self.options) - 1:
                if x < 0:
                    
                    self.highlighted_option = self.options[current_option_index + x]
                if x > 0: 
                    self.highlighted_option = self.options[0]

            if current_option_index + x in range(0, len(self.options)):
                #current_option_index = current_option_index + x
                self.highlighted_option = self.options[current_option_index + x]

            self.generate_toolbar(scr, color, width)
            #self.highlighted_option = MenuAction()

class MenuAction():
    def __init__(self, title=None, action=None):
        self.title = 'default_option_title' if not title else title
        self.action = action
        self.highlighted_option = None

    def __repr__(self):
        """
        :type: MenuAction
        """
        return '{}'.format(self.title)



    @property
    def title(self):
        """
        :type: MenuAction
        """
        return self._title

    @title.setter
    def title(self, value):
        assert isinstance(value, str), 'assigned menu title is not str'
        self._title = value

    @title.deleter
    def title(self):
        """
        :type: MenuAction title
        """
        del self._title

    @property
    def action(self):
        """
        :type: MenuAction
        """
        return self._action

    @action.setter
    def action(self, value):
       
        self._action = value

    @action.deleter
    def action(self):
        """
        :type: MenuAction 
        """
        del self._function

    def execute_action(self, x=None):
        assert hasattr(self.action, '__call__') or self.action is None, 'menu action is not a function'
        if self.action is None:
            pass
        else:
            try:
                return self.action(x)
            except TypeError as e:
                return self.action()



    def highlight_action(self, settings):
        self.title = settings.format_str(self.title)
        self.highlighted_option = True

# class MenuSettings():
#     def __init__(self, color=None, attributes=None):
#         self.color = 'white' if color is None else color
#         self.attributes = [] if attributes is None else attributes

#     def format_str(self, string):
#         return colored(string, color=self.color, attrs=self.attributes)

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
    def __init__(self, title=None, options=None, screen = None, selection_settings=None, text_settings=None, inherit_settings=False, tool_bar=None):
        self.title = title
        self.options = {x.title:x for x in options}
        self.parent_menu = None
        self.child_menus = {}
        self.previous_execution = MenuAction()
        self.inherit_settings = inherit_settings
        #self.selection_settings = MenuSettings(color='white', attributes=['reverse', 'bold']) if selection_settings is None else selection_settings
        #self.text_settings = MenuSettings(color='white', attributes=[]) if text_settings is None else text_settings
        
        self.highlighted_option = self.options[list(self.options.keys())[0]]
        self.tool_bar = tool_bar

        self.create_links()

        self.update_inherited_settings()
        self.screen = screen
        
        #self.screen.clear()
        #self.screen.refresh()
        


    # @property
    # def selection_settings(self):
    #     """
    #     :type: Menu
    #     """
    #     return self._selection_settings

    # @selection_settings.setter
    # def selection_settings(self, value):

    #     self._selection_settings = value

    # @selection_settings.deleter
    # def selection_settings(self):
    #     """
    #     :type: Menu
    #     """
    #     del self._selection_settings  
    # @property
    # def text_settings(self):
    #     """
    #     :type: Menu
    #     """
    #     return self._text_settings 

    # @text_settings.setter
    # def text_settings (self, value):
    #     # for child in self.child_menus.values():
    #     self._text_settings = value

    # @text_settings.deleter
    # def text_settings(self):
    #     """
    #     :type: Menu
    #     """
    #     del self._text_settings  


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
        assert len(value) <= 15, 'option limit exceeded in {}'.format(self.title)
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
        return '{}'.format(self.title)

    def has_parent(self):
        """
        :type: Menu
        """
        return not self.parent_menu is None

    def has_children(self):
        return not self.child_menus is None

    def list_parent(self):
        return self.parent_menu.title if self.has_parent() else None

    def list_children(self):
        return list(self.child_menus.keys())

    def is_parent_of(self, other):
        return self.child_menus == other

    def is_child_of(self, other):
        return self.parent_menu == other

    def is_empty(self):
        return len(self.options) < 1

    def add_option(self, new_option):
        assert isinstance(new_option, MenuAction), 'menu options can only be of type MenuAction'
        self.options.update(new_option)

    def update_inherited_settings(self):
        root = self.return_root()

        def update_children(menu):
            #menu.text_settings = menu.parent_menu.text_settings
            #menu.selection_settings = menu.parent_menu.selection_settings
            return([update_children(child) for child in menu.child_menus.values() if child.inherit_settings])

        [update_children(child) for child in root.child_menus.values() if child.inherit_settings]

    def create_links(self):
        """
        Creates parent/child relationships based on options dictionary
        if an option is another menu, link the menus

        :type: Menu
        """
        def link_menus(menu, sub_menu):

            menu.child_menus[sub_menu.title] = sub_menu
            sub_menu.parent_menu = menu

            [link_menus(sub_menu, o) for o in sub_menu.options.values() if isinstance(o, Menu)]

        [link_menus(self, o) for o in self.options.values() if isinstance(o, Menu)]

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
        
    def run_menu(self, input_ = True):
        '''
            Runs the current menu
        '''
        self.screen.clear()
        #self.screen.refresh()
        try:
            height, width = self.screen.getmaxyx()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            self.screen.addstr(0, 0, '{}'.format(self.title))
            if self.tool_bar:
                self.tool_bar.generate_toolbar(self.screen, curses.color_pair(1), width)
            self.screen.addstr(2, 0, '{}'.format('Please select an option:'))
            
            #print(self.text_settings.format_str('{}'.format(self.title)))

            #curses.endwin()
            # if self.tool_bar:
            #     #print(self.tool_bar.options)
            #     #self.tool_bar.options filters
            #     self.tool_bar.generate_toolbar()
            # print(self.text_settings.format_str('Please select an option:\n'))

            for i in range(0, len(self.options.keys())):
                if list(self.options.keys())[i] == self.highlighted_option.title:
                    self.screen.addstr(4 + i, 0, '{}'.format(list(self.options.keys())[i]), curses.color_pair(1))
                    #print('  {}'.format(self.selection_settings.format_str(option)))
                else:
                    self.screen.addstr(4 + i, 0, '{}'.format(list(self.options.keys())[i]))
            if not self.has_parent():
                if self.highlighted_option.title == 'Exit':
                    self.screen.addstr(len(self.options.keys()) + 5, 0, '{}'.format('Exit'), curses.color_pair(1))
                else:
                    self.screen.addstr(len(self.options.keys()) + 5, 0, '{}'.format('Exit'))

            # for option in self.options.keys():
            #     if option == self.highlighted_option.title:
            #         print('  {}'.format(self.selection_settings.format_str(option)))
            #     else:
            #         print('  {}'.format(self.text_settings.format_str(option)))
            # if not self.has_parent():
            #     if self.highlighted_option.title == 'Exit':
            #         print('\n  {}'.format(self.selection_settings.format_str('Exit')))
            #     else:
            #         print('\n  {}'.format(self.text_settings.format_str('Exit')))

            # print(self.text_settings.format_str('\nUse the up and down arrow keys to move the highlight to your choice.'))

            # if self.has_parent():
            #     print(self.text_settings.format_str('Press enter to execute the option.\n'))
            #     print(self.text_settings.format_str('Press backspace to go back to {}.\n'.format(self.parent_menu.title)))
            # else:
            #     print(self.text_settings.format_str('Press enter to execute the option.\n'))

            height, width = self.screen.getmaxyx()
            if isinstance(self.previous_execution, MenuAction):
                if self.previous_execution.title == 'Exit':
                    self.previous_execution.execute_action()
                # else:
                #     self.screen.addstr(8, 0 , '{}'.format('Executed'))

                if self.tool_bar: 
                    action = self.previous_execution.execute_action(self.tool_bar.options)
                    if not action is None:
                        self.screen.addstr(len(self.options.keys()) + 6, 0, '{}'.format(action))

                    # MenuPrint(, self.text_settings).print_in_console()
                #self.screen.addstr(len(self.options.keys()) + 10, 0, '{}'.format('Executed'))

            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            height, width = self.screen.getmaxyx()

            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            
            corpus_size = len(settings.corpus)
            annotators_in_corpus = len(set([a for t, ans in settings.corpus.items() for a, b in ans.items()]))
            annotations = len([a for f, a_c in settings.corpus.items() 
                            for a_name, d_c in a_c.items() 
                            for s, ans in d_c['annotation_sets'].items()
                            for a in ans if a['mention'] in settings.schema.get_entity_names()])
            if self.has_parent():
                statusbarstr = "Press 'backspace' to return to {} | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(self.parent_menu,corpus_size, annotators_in_corpus, annotations)
            else:
                statusbarstr = "Press 'esc' to exit | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(corpus_size, annotators_in_corpus, annotations)


            if width <= len(statusbarstr):
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(height-1, 0, statusbarstr[:width-len(statusbarstr)-1])
                #self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))
            else:
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(height-1, 0, statusbarstr)
                self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))

            self.screen.refresh()

            if input_:
                self.read_input()
        except curses.error as e:
            print(e)
            #self.screen.addstr(20, 0, '{}'.format(e))

    def read_input(self):
        '''
            Reads user input
        '''
        #while(True):
        key = KeyboardReader().read_key(self.screen)
        self.validate_user_input(key)

    def remove_option(self, selection):
        '''
            Removes an item from the options dictionary
        '''
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

    def update_movement(self, key):

        #self.clear_screen()
        self.screen.keypad(1)
        try:
            try:
                x = {'up':-1, 'down':1}[key]
            except KeyError as e:
                x = 0
            try:
                y = {'left':-1, 'right':1}[key]
            except KeyError as e:
                y= 0

            options_keys = list(self.options.keys())

            if not isinstance(self.highlighted_option, Menu):
                if self.tool_bar:
                    if y in [1, -1] and not self.highlighted_option.action:
                        
                        self.tool_bar.update_toolbar(y,self.screen, curses.color_pair(1)) # moves left and
                        self.run_menu(input_=False)
                    elif y == 0:
                        self.tool_bar.highlighted_option = MenuAction()
                        self.run_menu(input_=False)


            try:
                try:
                    current_option_index = options_keys.index(self.highlighted_option.title)
                except AttributeError as e:
                    current_option_index = 0
            except ValueError as e: # if current option is exit
                current_option_index = len(options_keys) 

            if current_option_index  == len(options_keys) - 1: # last item in the options list
                if x > 0:
                    if self.tool_bar:
                        
                        self.highlighted_option = MenuAction()
                        self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
                        self.refresh()
                    
                    current_option_index = 0
                    self.highlighted_option = self.options[options_keys[current_option_index]]
                    if not self.has_parent():
                        self.highlighted_option = MenuAction('Exit',self.exit)
                    self.refresh()

                elif x < 0:
                    current_option_index += x
                    if self.tool_bar:
                        if current_option_index < 0:
                            
                            current_option_index = 0
                            self.highlighted_option = MenuAction()
                            self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
                            self.refresh()


                        # self.tool_bar.update_toolbar(0)
                        # #self.refresh()
                        # current_option_index = 0

                    self.highlighted_option = self.options[options_keys[current_option_index]]
                    self.refresh()

            if current_option_index == 0: # first item in the options list
                if x < 0:
                    if self.tool_bar:
                        self.highlighted_option = MenuAction()
                        self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
                        self.refresh()
                        
                    current_option_index = len(options_keys) - 1
                    current_menu_action = self.options[options_keys[current_option_index]]
                    self.highlighted_option = self.options[options_keys[current_option_index]]
                    if not self.has_parent():
                        self.highlighted_option = MenuAction('Exit', self.exit)
                    self.refresh()

            if current_option_index == len(options_keys): # if in exit go back to top or bottom
                if x > 0:
                    current_option_index = 0
                    self.highlighted_option = self.options[options_keys[current_option_index]]
                    self.refresh()

                if x < 0:
                    current_option_index = len(options_keys) - 1
                    self.highlighted_option = self.options[options_keys[current_option_index]]
                    self.refresh()

            if current_option_index + x in range(0, len(options_keys)):
                current_option_index += x
                self.highlighted_option = self.options[options_keys[current_option_index]]
                self.refresh()
        except IndexError as e:
            self.refresh()
    def validate_user_input(self, key):
        '''
            Validates the key pressed by the user

        '''
        
        if key in ['up', 'down', 'left', 'right']:
            self.update_movement(key)
            
        elif key == 'space': 
            self.previous_execution = MenuAction()
            if self.tool_bar:
                self.tool_bar.reset_toolbar()
            self.refresh()
        # elif key == 'r':
        #     height, width = self.screen.getmaxyx()
        #     msg = 'restarting tool'
        #     self.screen.addstr(0, width - len(msg), '{}'.format(msg), curses.A_BLINK)
        #     os.execv(sys.executable, ['python3'] + [sys.argv[0]])

        elif key == '--':
            try:
                self.refresh()
            except curses.error as e:
                pass
        elif key == 'tab': 
            self.previous_execution = MenuAction()
                
            self.refresh()
        elif key == 'esc' and not self.has_parent(): 
            self.exit()
        elif key == 'backspace':
            self.previous_execution = MenuAction() # clears the output every time one goes back and forth menus
            self.back()
        elif key == 'enter':
            
            if self.tool_bar:
                if self.tool_bar.highlighted_option.action: 
                    current_option = self.tool_bar.highlighted_option

                    current_option_stack = current_option.execute_action()

                    while(True):
                        key = KeyboardReader().read_key(self.screen)
                        if key == 'enter':
                            self.refresh()
                        if key in ['left', 'right']:
                            x = {'left':-1, 'right':1}[key]
                            # get index number
                            current_option_index = current_option_stack.index(current_option.title)
    
                            if current_option_index == 0:
                                if x < 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[-1]
                                    self.run_menu(input_ = False)
                                if x > 0:
                                    try:
                                        self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]
                                    except IndexError as e:
                                        self.tool_bar.highlighted_option.title = current_option_stack[-1]
                                    self.run_menu(input_ = False)
 
                            elif current_option_index  == len(current_option_stack) - 1:
                                if x > 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[0]
                                    self.run_menu(input_ = False)
                                if x < 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]
                                    self.run_menu(input_ = False)
                            elif x + current_option_index in range(0, len(current_option_stack)):
                                self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]

                                self.run_menu(input_ = False)
            if isinstance(self.highlighted_option, Menu): # checks if selection is menu
                self.screen.clear()
                self.highlighted_option.run_menu()

            self.previous_execution = self.highlighted_option

            self.refresh()
        else:
            pass # if other keys are found, do nothing
                   
    def refresh(self):
        '''
            Refreshes the screen 
        '''
        
        # try:
        # #self.clear_screen()
        self.run_menu()
        # except RecursionError as e:

        #     #self.screen = None
        #     self.screen = curses.initscr()
        #     curses.noecho()
        #     curses.curs_set(0)
        #     #self.highlighted_option = self.previous_execution
            
        #     # self.screen.keypad(0)
        #     # #curses.echo()
        #     # #curses.curs_set(1)
        #     curses.endwin() 
        #     # #curses.cbreak()
        #     # self.screen.clear()
        #     # # #self.screen.refresh()
        #     # print(e)
        #     # self.previous_execution = MenuAction()

        #     # self.highlighted_option = self.options[list(self.options.keys())[0]]
        #     #self.run_menu(input_=False)
        #     # #print(e)# maximum recursion depth exceeded while getting the str of an object
        #     #self.exit()
        #     # #pass
        #     # self.refresh()
        #     # temp_title = self.title
        #     # temp_options = list(self.options.values())
        #     # self.previous_execution = MenuAction()
        #     # self.highlighted_option = self.options[list(self.options.keys())[0]]
        #     # self = None
        #     #print(e)
        #     # temp_new_menu = Menu(title=temp_title,
        #     #                      options=temp_options,
        #     #                      screen=curses.initscr())

        #     # self=temp_new_menu
        #     #self.run_menu()

    def back(self):
        '''
            Goes to the previous menu, if current menu does not have any previous menus then it refreshes the page
        '''
        #self.screen.clear()
        if self.has_parent():
            self.parent_menu.refresh()
        else:
            self.refresh()

    def clear_screen(self):
        '''
            Deletes all contents in screen
        '''
        self.screen.clear()
        #os.system('cls' if os.name == 'nt' else 'clear')

    def exit(self):
        '''
            Quits the menu
        '''
        #self.clear_screen()
        sys.exit()

class HelpMenu(Menu):
    def __init__(self, title=None, text_settings=None, inherit_settings=False, _options={}, screen=None):
        self.title = title
        self.parent_menu = None
        self.child_menus = {}
        self.inherit_settings = inherit_settings
        self._options=_options
        self.highlighted_option = None
        self.tool_bar =None
        self.screen = screen
        
        #self.text_settings = MenuSettings(color='white', attributes=[]) if text_settings is None else text_settings
        

        self.create_links()

        self.update_inherited_settings()
        self.screen.clear()
        self.screen.refresh()

    def run_menu(self):
        '''
            Runs the current menu
        '''

        self.screen.addstr(0, 0, '{}'.format(self.title))
        help_options =  'Use the up and down arrow keys to move the highlight to your choice.\n'
        help_options += 'Press enter to execute an option.\n'
        help_options += 'Press backspace to go back to a previous menu.\n'
        help_options += 'Press spacebar to reset the output and the filters of a menu.\n'
        help_options += 'Press tab to reset the filters of a menu.\n'
        help_options += 'Press esc inside the Main Menu to quit the tool.\n'
        self.screen.addstr(1, 0, help_options)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        height, width = self.screen.getmaxyx()

        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        corpus_size = len(settings.corpus)
        annotators_in_corpus = len(set([a for t, ans in settings.corpus.items() for a, b in ans.items()]))
        annotations = len([a for f, a_c in settings.corpus.items() 
                        for a_name, d_c in a_c.items() 
                        for s, ans in d_c['annotation_sets'].items()
                        for a in ans if a['mention'] in settings.schema.get_entity_names()])
        if self.has_parent():
            statusbarstr = "Press 'backspace' to return to {} | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(self.parent_menu,corpus_size, annotators_in_corpus, annotations)
        else:
            statusbarstr = "Press 'esc' to exit | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(corpus_size, annotators_in_corpus, annotations)
        if width <= len(statusbarstr):
            self.screen.attron(curses.color_pair(2))
            self.screen.addstr(height-1, 0, statusbarstr[:width-len(statusbarstr)-1])
            #self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            self.screen.attroff(curses.color_pair(2))
        else:
            self.screen.attron(curses.color_pair(2))
            self.screen.addstr(height-1, 0, statusbarstr)
            self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            self.screen.attroff(curses.color_pair(2))
        self.screen.refresh()

        self.read_input()

class CorpusViewerMenu(Menu):
    def __init__(self, title=None, options=None, screen = None, selection_settings=None, text_settings=None, inherit_settings=False, tool_bar=None):
        self.title = title
        self.options = {x.title:x for x in options}
        self.parent_menu = None
        self.child_menus = {}
        self.previous_execution = MenuAction()
        self.inherit_settings = inherit_settings
        #self.selection_settings = MenuSettings(color='white', attributes=['reverse', 'bold']) if selection_settings is None else selection_settings
        #self.text_settings = MenuSettings(color='white', attributes=[]) if text_settings is None else text_settings
        
        
        self.tool_bar = tool_bar
        self.highlighted_option = MenuAction()
        
        self.line = 0
        self.lines = ''
        self.annotation_lines = ''
        
        self.create_links()
        self.screen = screen

        self.input_history_counter = []
        self.update_inherited_settings()
        
        
        
        self.rows, self.columns = self.screen.getmaxyx()
        self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1), self.columns)
        self.out = self.screen.subwin(self.rows - 2, self.columns - 2, 1, 1)
        self.out_rows, self.out_columns = self.out.getmaxyx()
        
        self.screen.clear()
        self.screen.refresh()
        
        
        #self.tool_bar.update_toolbar(1, self.screen, curses.color_pair(1))

    def read_input(self):
        '''
            Reads user input
        '''
        while(True):
            key = KeyboardReader().read_key(self.screen)
            self.validate_user_input(key)

    def update_movement(self, key):

        try:
            try:
                x = {'up':-1, 'down':1}[key]
            except KeyError as e:
                x = 0
            try:
                y = {'left':-1, 'right':1}[key]
            except KeyError as e:
                y = 0

            options_keys = list(self.options.keys())

            h, w = self.screen.getmaxyx()
            if self.tool_bar:
                if y in [1, -1] and not self.highlighted_option.action:
                    
                    self.tool_bar.update_toolbar(y, self.out, curses.color_pair(1), w) # moves left and
                    self.run_menu(input_=False)

            if key == 'down':
                if len(self.lines) - self.line > self.out_rows:
                    self.line += 1
                self.refresh()
            if key == 'up':
                if self.line > 0:
                    self.line -= 1
                self.refresh()
            if key == '--':
                self.refresh()



            # try:
            #     try:
            #         current_option_index = options_keys.index(self.highlighted_option.title)
            #     except AttributeError as e:
            #         current_option_index = 0
            # except ValueError as e: # if current option is exit
            #     current_option_index = len(options_keys) 

            # if current_option_index  == len(options_keys) - 1: # last item in the options list
            #     if x > 0:
            #         if self.tool_bar:
                        
            #             self.highlighted_option = MenuAction()
            #             self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
            #             self.refresh()
                    
            #         current_option_index = 0
            #         self.highlighted_option = self.options[options_keys[current_option_index]]
            #         if not self.has_parent():
            #             self.highlighted_option = MenuAction('Exit',self.exit)
            #         self.refresh()

            #     elif x < 0:
            #         current_option_index += x
            #         if self.tool_bar:
            #             if current_option_index < 0:
                            
            #                 current_option_index = 0
            #                 self.highlighted_option = MenuAction()
            #                 self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
            #                 self.refresh()


            #             # self.tool_bar.update_toolbar(0)
            #             # #self.refresh()
            #             # current_option_index = 0

            #         self.highlighted_option = self.options[options_keys[current_option_index]]
            #         self.refresh()

            # if current_option_index == 0: # first item in the options list
            #     if x < 0:
            #         if self.tool_bar:
            #             self.highlighted_option = MenuAction()
            #             self.tool_bar.update_toolbar(0, self.screen, curses.color_pair(1))
            #             self.refresh()
                        
            #         current_option_index = len(options_keys) - 1
            #         current_menu_action = self.options[options_keys[current_option_index]]
            #         self.highlighted_option = self.options[options_keys[current_option_index]]
            #         if not self.has_parent():
            #             self.highlighted_option = MenuAction('Exit', self.exit)
            #         self.refresh()

            # if current_option_index == len(options_keys): # if in exit go back to top or bottom
            #     if x > 0:
            #         current_option_index = 0
            #         self.highlighted_option = self.options[options_keys[current_option_index]]
            #         self.refresh()

            #     if x < 0:
            #         current_option_index = len(options_keys) - 1
            #         self.highlighted_option = self.options[options_keys[current_option_index]]
            #         self.refresh()

            # if current_option_index + x in range(0, len(options_keys)):
            #     current_option_index += x
            #     self.highlighted_option = self.options[options_keys[current_option_index]]
            #     self.refresh()
        except IndexError as e:
            pass
    def validate_user_input(self, key):
        '''
            Validates the key pressed by the user

        '''
        #self.rows, self.columns = self.screen.getmaxyx()
        if set(self.input_history_counter) == 1 and len(self.input_history_counter):
            key = 'space'
        if key in ['up', 'down', 'left', 'right']:
            if not key in self.input_history_counter:
                self.input_history_counter = []
            
            self.input_history_counter.append(key)
            self.update_movement(key)
            
        elif key == 'space': 
            self.previous_execution = MenuAction()
            if self.tool_bar:
                self.tool_bar.reset_toolbar()
            self.refresh()
        # elif key == 'r':
        #     height, width = self.screen.getmaxyx()
        #     msg = 'restarting tool'
        #     self.screen.addstr(0, width - len(msg), '{}'.format(msg), curses.A_BLINK)
        #     os.execv(sys.executable, ['python3'] + [sys.argv[0]])
        elif key == '--':
            
            self.refresh()

        elif key == 'tab': 
            self.previous_execution = MenuAction()
                
            self.refresh()
        elif key == 'esc' and not self.has_parent(): 
            self.exit()
        elif key == 'backspace':
            self.previous_execution = MenuAction() # clears the output every time one goes back and forth menus
            self.back()
        elif key == 'enter':
            
            if self.tool_bar:
                if self.tool_bar.highlighted_option.action: 
                    current_option = self.tool_bar.highlighted_option

                    current_option_stack = current_option.execute_action()

                    while(True):
                        key = KeyboardReader().read_key(self.screen)
                        if key == 'enter':
                            self.refresh()
                        if key in ['left', 'right']:
                            x = {'left':-1, 'right':1}[key]
                            # get index number
                            current_option_index = current_option_stack.index(current_option.title)
                            
                            if current_option_index == 0:
                                if x < 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[-1]
                                    self.line = 0
                                    self.run_menu(input_ = False)
                                if x > 0:
                                    try:
                                        self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]
                                    except IndexError as e:
                                        self.tool_bar.highlighted_option.title = current_option_stack[-1]
                                    self.line = 0
                                    self.run_menu(input_ = False)
 
                            elif current_option_index  == len(current_option_stack) - 1:
                                if x > 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[0]
                                    self.line = 0
                                    self.run_menu(input_ = False)
                                if x < 0:
                                    self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]
                                    self.line = 0
                                    self.run_menu(input_ = False)
                            elif x + current_option_index in range(0, len(current_option_stack)):
                                self.tool_bar.highlighted_option.title = current_option_stack[current_option_index + x]
                                self.line = 0
                                self.run_menu(input_ = False)

            # self.previous_execution = self.highlighted_option

            # self.refresh()
        else:
            pass # if other keys are found, do nothing
                   

    def run_menu(self, input_=True):
        '''
            Runs the current menu
        '''
        self.screen.clear()
        self.rows, self.columns = self.screen.getmaxyx()
        self.out = self.screen.subwin(self.rows - 2, self.columns - 2, 1, 1)
        self.out_rows, self.out_columns = self.out.getmaxyx()
        try:
            curses.start_color()
            #curses.start_color()
            
            self.screen.addstr(0, 0, '{}'.format(self.title))
            try:
                height, width = self.out.getmaxyx()
                if self.tool_bar:
                    self.tool_bar.generate_toolbar(self.out, curses.color_pair(1), width)
            except RecursionError as e:
                self.refresh()

            filters = self.tool_bar.options

            file = filters[0].title
            annotator_name = filters[1].title
            annotation_set = filters[2].title
            annotation_type = filters[3].title

            document = settings.corpus[file][annotator_name]['text']

            filecontent = document

            encoding = 'utf-8'
            filename = file 
            stdscr = self.screen

            
            corpus_size = len(settings.corpus)
            annotators_in_corpus = len(set([a for t, ans in settings.corpus.items() for a, b in ans.items()]))
            annotations = len([a for f, a_c in settings.corpus.items() 
                            for a_name, d_c in a_c.items() 
                            for s, ans in d_c['annotation_sets'].items()
                            for a in ans if a['mention'] in settings.schema.get_entity_names()])

            doc_annotations = [a for f, a_c in settings.corpus.items() 
                                 for a_name, d_c in a_c.items() 
                                 for s, ans in d_c['annotation_sets'].items()
                                 for a in ans if f == file
                                              if annotator_name == a_name
                                              if s == annotation_set
                                              if a['mention'] == annotation_type]

            self.out_rows, self.out_columns = self.out.getmaxyx()
            self.out_rows -= 1
            self.rows, self.columns = stdscr.getmaxyx()
            self.out_rows -= 5
            offsets = [[i for i in range(x['start'], x['end'])] for x in doc_annotations]

            offsets = [y for x in offsets for y in x]
            #offsets.append(len(doc_annotations))
            
            self.out = stdscr.subwin(self.rows - 2, self.columns - 2, 1, 1)
            file_annotations = []

            for i in range(0, len(filecontent)):
                if i in offsets:
                    file_annotations.append(filecontent[i])
                elif filecontent[i] in ['\n', '\t', '\r', '\a']:
                    file_annotations.append(filecontent[i])
                else:
                    file_annotations.append(' ')
            
            file_annotations = ''.join(file_annotations)

            self.annotation_lines = [x + " " * (self.out_columns - len(x)) for x in reduce(lambda x, y: x + y, [[x[i:i+self.out_columns] for i in range(0, len(x), self.out_columns)] for x in file_annotations.expandtabs(4).splitlines()])]


            self.lines = [x + " " * (self.out_columns - len(x)) for x in reduce(lambda x, y: x + y, [[x[i:i+self.out_columns] for i in range(0, len(x), self.out_columns)] for x in filecontent.expandtabs(4).splitlines()])]
            



            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            #curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            colors = [curses.COLOR_RED, curses.COLOR_GREEN,
                      curses.COLOR_YELLOW, curses.COLOR_BLUE, curses.COLOR_MAGENTA,
                      curses.COLOR_CYAN]

            for i in range(4, len(settings.schema.entities)+4):
                curses.init_pair(i , colors[(i-4) % len(colors)], curses.COLOR_BLACK)
            self.height, self.width = self.screen.getmaxyx()


            instructions = '(↓) Next line | (↑) Previous line'
            top_menu = 'Lines {} to {} of {} of {} {}'.format(self.line + 1, 
                                                         min(len(self.lines), 
                                                         self.line + self.out_rows), 
                                                         len(self.lines), 
                                                         filename,
                                                         instructions)
            if self.width <= len(top_menu):
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(3, 0, top_menu[:self.width-len(top_menu)-1])
                #self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))
            else:
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(3, 0, top_menu)
                self.screen.addstr(3, len(top_menu), " " * (self.width - len(top_menu) - 1))
                self.screen.attroff(curses.color_pair(2))
            # self.screen.attron(curses.color_pair(2))
            # self.screen.addstr(3, 0, top_menu)
            # self.screen.addstr(3, len(top_menu), " " * (self.width - len(top_menu) - 1))
            # self.screen.attroff(curses.color_pair(2))

            # if annotator_name == 'anno2':
            #     self.out.addstr(4,0, '{}'.format(offsets))
                
            # else:
                

            for l in range(0, len(self.lines[self.line:self.line+self.out_rows])):
                for c in range(0, len(self.lines[self.line:self.line+self.out_rows][l])):
                    txt_char = self.lines[self.line:self.line+self.out_rows][l][c]
                    annotated_char = self.annotation_lines[self.line:self.line+self.out_rows][l][c]
                    #annotated_char = '0'
                    #self.out.addstr(4,0, '{}'.format(out))
                    i = list(settings.schema.entities.keys()).index(annotation_type) + 4
                    if annotated_char == ' ' :
                        self.out.addstr(l+4, c, ''.join(txt_char))
                    else:
                        self.out.addstr(l+4, c, ''.join(txt_char), curses.color_pair(i))
       
            

            #self.out.addstr(4, 0, ''.join(self.lines[self.line:self.line+self.out_rows]))
            #self.out.addstr(4, 0, ''.join(self.annotation_lines[self.line:self.line+self.out_rows]))
            # for y in range(4, self.out_rows):
            #     for x in range(0, self.out_columns):
            #         self.out.addstr(y, x, ''.join(self.lines[x][y]))
            #         #if self.annotation_lines[x][y] == ' ':
            #         self.out.addstr(x, y, ''.join(self.annotation_lines[x][y]), curses.color_pair(3))
            
            
            #self.out.addstr(3, 0, '{}'.format(self.lines[self.line:self.line+self.out_rows]))
            if self.has_parent():
                statusbarstr = "Press 'backspace' to return to {} |{} {} annotations".format(self.parent_menu,len(doc_annotations), annotation_type)
            else:
                statusbarstr = "Press 'esc' to exit | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(corpus_size, annotators_in_corpus, annotations)
            if self.width <= len(statusbarstr):
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(self.height-1, 0, statusbarstr[:self.width-len(statusbarstr)-1])
                #self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))
            else:
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(self.height-1, 0, statusbarstr)
                self.screen.addstr(self.height-1, len(statusbarstr), " " * (self.width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))

            # self.screen.refresh()
            # self.out.refresh()
            if input_:
                self.read_input()
        except curses.error as e:
            pass


class SchemaMenu(Menu):
    def __init__(self, title=None, options=None, screen = None, selection_settings=None, text_settings=None, inherit_settings=False, tool_bar=None):
        self.title = title
        self.options = {x.title:x for x in options}
        self.parent_menu = None
        self.child_menus = {}
        self.previous_execution = MenuAction()
        self.inherit_settings = inherit_settings
        #self.selection_settings = MenuSettings(color='white', attributes=['reverse', 'bold']) if selection_settings is None else selection_settings
        #self.text_settings = MenuSettings(color='white', attributes=[]) if text_settings is None else text_settings
        
        self.tool_bar = tool_bar
        self.highlighted_option = MenuAction()

        self.screen = screen
        self.create_links()

        self.update_inherited_settings()
        self.screen.clear()
        self.screen.refresh()



    def run_menu(self, input_=True):


        self.screen.clear()

        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            self.screen.addstr(0, 0, '{}'.format(self.title))


            self.screen.addstr(2, 0, '{}'.format(settings.schema.to_string()))

            height, width = self.screen.getmaxyx()

            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            
            corpus_size = len(settings.corpus)
            annotators_in_corpus = len(set([a for t, ans in settings.corpus.items() for a, b in ans.items()]))
            annotations = len([a for f, a_c in settings.corpus.items() 
                            for a_name, d_c in a_c.items() 
                            for s, ans in d_c['annotation_sets'].items()
                            for a in ans if a['mention'] in settings.schema.get_entity_names()])
            if self.has_parent():
                statusbarstr = "Press 'backspace' to return to {} | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(self.parent_menu,corpus_size, annotators_in_corpus, annotations)
            else:
                statusbarstr = "Press 'esc' to exit | corpus size: {} | annotators in corpus: {} | annotations in corpus: {}".format(corpus_size, annotators_in_corpus, annotations)
            if width <= len(statusbarstr):
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(height-1, 0, statusbarstr[:width-len(statusbarstr)-1])
                #self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))
            else:
                self.screen.attron(curses.color_pair(2))
                self.screen.addstr(height-1, 0, statusbarstr)
                self.screen.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
                self.screen.attroff(curses.color_pair(2))
            self.screen.refresh()

            if input_:
                self.read_input()
        except curses.error as e:
            print(e)
