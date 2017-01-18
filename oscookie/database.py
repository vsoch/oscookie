#!/usr/bin/env python

import os
from glob import glob

from oscookie.utils import (
    get_installdir,
    read_file,
    write_file
)

from oscookie.logman import bot
from oscookie.info import (
    get_baseos, 
    get_managers
)

import requests

try:
     import xmlrpclib
except ImportError:
     import xmlrpc.client as xmlrpclib


def generate_os_packages(outdir=None):
    '''generate os_package will generate files with package
    lists in variable outdir (or install directory/lists) 
    if not defined using Docker.  This function is not intended
    for the user, but is provided so that the original data can be reproduced.
    param outdir: the output directory for the lists, a series of text files
    '''
    if outdir == None:
        outdir = "%s/lists" %get_installdir()

    ## OS IMAGES (provided via official docker library)
    images = get_baseos()

    # We will generate a package list for each distribution based on the base
    managers = get_managers()

    # Commands to generate OS package lists
    for image in images:
        bot.logger.info("Generating list for %s",image)        
        baseos,version = image.split(':')
        if baseos in managers:
            manager_command = managers[baseos]
            outfile = '%s/%s.txt' %(outdir,image)
            if not os.path.exists(outfile):
                os.system('docker run %s %s >> %s' %(image, manager_command, outfile))


def update_python_packages():
    '''update_python_packages is a wrapper for generate_python_packages
    ensuring no argument is provided to update the packages provided
    in the installation
    '''
    return generate_python_packages()


def generate_python_packages(outdir=None):
    '''generate python packages will scrape a list of packages from pypi
    :param outdir: the output directory for the packages. If none defined,
    will use lists
    '''
    if outdir == None:
        outdir = "%s/lists" %get_installdir()
   
    outfile = '%s/pypi.txt' %(outdir)
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    packages = client.list_packages()
    write_file(outfile,'\n'.join(packages))
    return outfile


def get_os_packages(base=None):
    '''get package lists will return lists of files
    specific to different packages.
    :param base: the folder to read in package lists from
    if not defined, uses oscookie folder with lists
    '''
    lists = dict()
    if base == None:
        base = get_installdir()
    package_files = glob("%s/lists/*.txt" %(base))
    for package_file in package_files:
        package_name = os.path.splitext(os.path.basename(package_file))[0].replace('.txt','')
        content = read_file(package_file)
        content = [x.strip('\n').split(' ')[0] for x in content]
        lists[package_name] = content
    return lists

def get_python_packages(outdir=None):
    '''get python packages will return the list of python packages
    '''
    if outdir == None:
        outdir = "%s/lists" %get_installdir()
   

