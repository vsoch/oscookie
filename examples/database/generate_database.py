#!/usr/bin/env python

from oscookie.database import generate_os_packages
import os

outdir = "%s/lists/base" %os.getcwd()
if not os.path.exists(outdir):
    os.mkdir(outdir)

generate_os_packages(outdir)
