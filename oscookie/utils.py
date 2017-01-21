#!/usr/bin/env python

'''
utils.py: part of oscookie package

'''

import collections
import os
import re
import requests

import shutil
import simplejson
import oscookie.__init__ as hello
from oscookie.logman import bot
import sys

from subprocess import (
    Popen,
    PIPE,
    STDOUT
)

import subprocess

import tempfile
import zipfile


######################################################################################
# Local commands and requests
######################################################################################


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(hello.__file__))


def check_installed(software):
    '''check_installed will check if a software is installed
    :param software: the name of the software
    '''
    testing_command = ["which", software]
    return run_command(testing_command)


def run_command(command):
    '''run_command will run a command (a list)
    :param command: the command to run
    '''
    if not isinstance(command,list):
        command = [command]
    output = Popen(command,stderr=STDOUT,stdout=PIPE)
    t = output.communicate()[0],output.returncode
    result = {'message':t[0],
              'return_code':t[1]}
    return result



############################################################################
## FILE OPERATIONS #########################################################
############################################################################


def zip_dir(zip_dir, zip_name, output_folder=None):
    '''zip_dir will zip up and entire zip directory
    :param folder_path: the folder to zip up
    :param zip_name: the name of the zip to return
    :output_folder:
    '''
    tmpdir = tempfile.mkdtemp()
    output_zip = "%s/%s" %(tmpdir,zip_name)
    zf = zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, allowZip64=True)
    for root, dirs, files in os.walk(zip_dir):
        for file in files:
            zf.write(os.path.join(root, file))
    zf.close()
    if output_folder != None:
        shutil.copyfile(output_zip,"%s/%s"%(output_folder,zip_name))
        shutil.rmtree(tmpdir)
        output_zip = "%s/%s"%(output_folder,zip_name)
    return output_zip



def write_file(filename,content,mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename,mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj,filename,mode="w",print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file
    :param json_obj: the dict to print to json
    :param filename: the output file to write to
    :param pretty_print: if True, will use nicer formatting   
    '''
    with open(filename,mode) as filey:
        if print_pretty == True:
            filey.writelines(simplejson.dumps(json_obj, indent=4, separators=(',', ': ')))
        else:
            filey.writelines(simplejson.dumps(json_obj))
    return filename


def read_file(filename,mode="r"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename,mode) as filey:
        content = filey.readlines()
    return content

############################################################################
## OTHER MISC. #############################################################
############################################################################


def calculate_folder_size(folder_path,truncate=True):
    '''calculate_folder size recursively walks a directory to calculate
    a total size (in MB)
    :param folder_path: the path to calculate size for
    :param truncate: if True, converts size to an int
    '''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filey in filenames:
            file_path = os.path.join(dirpath, filey)
            if os.path.isfile(file_path) and not os.path.islink(file_path):
                total_size += os.path.getsize(file_path) # this is bytes
    size_mb = total_size / 1000000
    if truncate == True:
        size_mb = int(size_mb)
    return size_mb
