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
import config_reader_test
from config_reader_test import read_config_file_information
from read_schema import *
from os.path import *
import json
import os
from os import access, R_OK
import schema_framework


configuration = {}
config_path = r'config.config'
configuration = read_config_file_information(config_path)
schema = schema_framework
#Check if configuration is readable
print("Performing Config Checks")
print("________________________________________________________\n")
def config_check():
    flag = 0
    print("Checking if configuration is valid\n")
    if not configuration:
        flag = 1
        print("Configuration not read correctly")
    else:
        print("--Configuration read correctly\n")
    #check if task is correct
    tasks=["sequence labelling","classification"]
    print("Checking if task is valid\n")
    if configuration['task'] not in tasks:
        flag = 1
        print(configuration['task'])
        print("The task listed is not valid, please only enter sequence_labelling or classification")
    else:
        print("--Task is valid\n")
    print("Checking if annotation directory is valid\n")
    if not exists(configuration['annotation_dir']):
        flag = 1
        print("The annotation_file_location is not a valid file location")
    if not isdir(configuration['annotation_dir']):
        flag = 1
        print("The annotation_file_location is not a valid directory")
    else:
        print("--annotation file location is a valid directory\n")
    print("Checking if annotation files are available and readable")
    print("If all files are listed they are available and readable\n")
    def scan_folder(parent):
    # iterate over all the files in directory 'parent'
        #print("These are all annotation files:")
        flag = 0
        for file_name in os.listdir(parent):
            if not exists(file_name):
                print("\t"+file_name)
                file_name=str(parent)+"/"+file_name
                for file in os.listdir(file_name):
                    if file.endswith(".xml"):
                        full_file= file_name + str(file)
                        access(full_file, R_OK)
                        print("\t\t"+file)
    scan_folder(configuration['annotation_dir'])
    return(flag)
    #check if all schema file is valid through checking overlaps and sub_entities    
if not(config_check()):
    print("\nNo errors found in the configuration file")
else:
    print("There is an error in the configuration file")
    exit()
