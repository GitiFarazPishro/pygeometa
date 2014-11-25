# -*- coding: iso-8859-15 -*-
# =================================================================
#
# Copyright (c) 2014 Her Majesty the Queen in Right of Canada
#
# Author: Tom Kralidis <tom.kralidis@ec.gc.ca>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from ConfigParser import ConfigParser
import os
import sys
from xml.dom import minidom

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

__version__ = '0.1.0'

TEMPLATES = '%s%stemplates' % (os.path.dirname(os.path.realpath(__file__)),
                               os.sep)


def read_mcf(mcf):
    """returns dict of ConfigParser object"""

    c = ConfigParser()
    c.read(mcf)
    return c.__dict__['_sections']


def pretty_print(xml):
    """clean up indentation and spacing"""

    val = minidom.parseString(xml)
    return '\n'.join([l for l in
                      val.toprettyxml(indent=' '*2).split('\n') if l.strip()])


def render_template(record, record_format, path=None):
    """convenience function to render Jinja2 template"""

    if path is None:  # default templates dir
        abspath = '{}{}{}'.format(TEMPLATES, os.sep, record_format)
    else:  # user-defined
        pass

    env = Environment(loader=FileSystemLoader(abspath))
    env.globals.update(zip=zip)

    try:
        template = env.get_template('main.j2')
    except TemplateNotFound:
        raise RuntimeError('Missing metadata template')

    xml = template.render(record=read_mcf(record),
                          software_version=__version__)
    return pretty_print(xml)


def get_supported_formats():
    """returns a list of supported formats"""

    return os.listdir(TEMPLATES)
