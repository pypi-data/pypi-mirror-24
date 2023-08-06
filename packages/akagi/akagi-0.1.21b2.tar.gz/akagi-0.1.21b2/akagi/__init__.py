from __future__ import absolute_import

# -*- coding: utf-8 -*-
__author__ = """Yuichiro Someya"""
__email__ = 'ayemos.y@gmail.com'
__version__ = '0.1.21b2'


import os

from akagi import data_file
from akagi import data_files

from akagi import data_file_bundle
from akagi import data_file_bundles

from akagi import iterators


def home():
    return os.getenv('AKAGI_HOME', os.path.expanduser('~/.akagi'))
