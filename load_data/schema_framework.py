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
import configparser
import os, sys
from pathlib import Path


class Schema():
    def __init__(self, name = None, entities = None):
        self.name = name
        self.entities = {} if entities is None else entities

    def __repr__(self):
        
        out = '{}\n{}\n'.format(self.name, '-'*len(self.name))

        for k, v in self.entities.items():
            if not v.has_parent_entity():
                out += '{}\n'.format(v)

                for i, j in v.sub_entities.items():
                    out += '{} {}\n'.format('-'*2 ,j.name)

        return out

    def to_string(self):
        
        out = ''

        for k, v in self.entities.items():
            if not v.has_parent_entity():
                out += '{}\n'.format(v)

                for i, j in v.sub_entities.items():
                    out += '{} {}\n'.format('-'*2 ,j)

        return out

    def len(self):
        return len(self.entities)

    def get_type(self, t):
        return self.entities[t]

    def get_overlaps(self):
        temp = {}
                    
        for s, obj in self.entities.items():
            
            if obj.is_sub_entity():
                
                main_entity_overlaps = self.entities[obj.get_parent_entity_name()].overlaps

                x = [o for n, o in main_entity_overlaps.items()]
                x.append(obj.get_parent_entity_name())
                temp[s] = [o for n, o in obj.overlaps.items()] + x

            else:
                if obj.has_sub_entities():

                    temp[s] = [o for n, o in obj.overlaps.items()] + obj.get_sub_entity_names()
                else:
                    x = []
                    for n, ent in obj.overlaps.items():
                        if self.entities[n].has_sub_entities():
                            x += self.entities[n].get_sub_entity_names()

                    temp[s] = [o for n, o in obj.overlaps.items()] + x


        return temp

    def add_entry(self, entry):
        # entry is class entity
        if not entry.name in self.entities.keys():
            self.entities[entry.name] = entry
            if entry.has_sub_entities():
                for x, y in entry.sub_entities.items(): # is list
                    if x in self.entities.keys():
                        entry.sub_entities[x] = self.entities[x]
                        entry.sub_entities[x].parent_entity = entry
                    else:
                        self.entities[x] = entry.sub_entities[x]
                        entry.sub_entities[x].parent_entity = entry
            if entry.has_overlaps():
                for x, y in entry.overlaps.items(): # is list
                    if x in self.entities.keys():
                        entry.overlaps[x] = self.entities[x]

                    # else:
                    #     self.entities[x] = entry.overlaps[x]
        else:
            self.entities[entry.name].features = entry.features
            self.entities[entry.name].overlaps = entry.overlaps
            if self.entities[entry.name].has_parent_entity():
                entry.parent_entity = self.entities[entry.name].parent_entity
            if self.entities[entry.name].has_sub_entities():
                entry.parent_entity = self.entities[entry.name].sub_entities

    def get_simple_schema(self):
        simple_schema = {}
        for n, e in self.entities.items():
            simple_schema[n] = e.features

        return simple_schema
        
    def get_entity_names(self):
        return list(self.entities.keys())


class Entity():
    def __init__(self, name = None, features = None, overlaps = None, sub_entities = None, parent_entity = None):
        self.name = name
        self.features = {} if features is None else features
        self.parent_entity = parent_entity
        self.sub_entities = {} if sub_entities is None else sub_entities
        self.overlaps = {} if overlaps is None else overlaps

    def __repr__(self):

        if self.features:
        
            return '{} : ({})'.format(self.name, ', '.join(['{} | {}'.format(a,b) for a, b in self.features.items()]))

        return '{}'.format(self.name)

    def has_overlaps(self):
        return True if len(self.overlaps) else False

    def has_parent_entity(self):
        return True if self.parent_entity else False

    def has_sub_entities(self):
        return True if self.sub_entities else False

    def is_parent_entity(self):
        return self.has_sub_entities()

    def is_sub_entity(self):
        return self.has_parent_entity()

    def get_parent_entity_name(self):

        return self.parent_entity.name if self.has_parent_entity() else None

    def get_parent_entity(self):
        return self.parent_entity if self.has_parent_entity else None

    def get_sub_entity_names(self):
        return list(self.sub_entities.keys())

    def get_sub_entity(self, n):
        return self.sub_entities[n] if self.has_sub_entities() and n in self.get_sub_entity_names() else None

    def is_concurrent(self):
        return True if len(self.parent_entity) > 1 else False



