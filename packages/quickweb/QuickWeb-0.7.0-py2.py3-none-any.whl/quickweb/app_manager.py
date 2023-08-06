#!/usr/bin/python
"""
This module implements the application management commands
"""
from __future__ import print_function

import shutil
import sys
import os
from glob import glob
from os.path import basename, exists, join, isdir

import quickweb
import quickweb.app
from quickweb.colorhelper import info, warning, success, print_error, print_success
from quickweb.template_manager import download_template
from quickweb import controller


def create(app_directory, template_name, force):
    """
    Create an application using a template
    """
    print("** Creating app on directory %s " % (info(app_directory + "/")))

    if exists(app_directory):
        if force:
            shutil.rmtree(app_directory)
        else:
            print_error(app_directory + ' already exists!')
            print('Use %s if you want to overwrite.' % warning('--force'))
            sys.exit(2)

    download_template(template_name, app_directory)
    quickweb_required_dir = join('/', 'usr', 'share', 'quickweb')
    quickweb_required_mask = join(quickweb_required_dir, 'QuickWeb_Application_en_US.md')
    required_files = glob(quickweb_required_mask)
    base_required_files = [basename(x) for x in required_files]
    print("** Adding startup files %s from %s" %
          (info(str(base_required_files)), info(quickweb_required_dir)))
    for filename in required_files:
        shutil.copy(filename, app_directory)
    print_success('Application successfully created.')
    print_success('You can start it with:')
    print('    $ ' + success('quickweb run ' + app_directory))
    print_success('Or read about the app structure with:')
    print('    $ ' + success('more ' + join(app_directory, 'QuickWeb_Application_en_US.md')))
    print("**")


def run(app_directory):
    quickweb.app.run(app_directory)


def describe(app_directory):
    quickweb.app.run(app_directory, running_describe=True)
    for key, values in controller._app_root.__dict__.items():
        print(key, values)


def setup_cf_deployment(app_directory):
    app_directory = app_directory or os.getcwd()
    webroot_dir = join(app_directory, 'webroot')
    if not isdir(webroot_dir):
        print_error("Unable to find webroot directory '%s'" % webroot_dir)
        exit(2)
