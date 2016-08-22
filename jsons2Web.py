#!/usr/bin/python
import json
import sys
import os

from os import walk
from os.path import join, splitext, basename
from sys import argv
from yattag import Doc

# Options
datadir = argv[1]

# Generation
doc, tag, text = Doc().tagtext()
lines = list()

# Find all JSON files and write them into one JS
with open('bigdata.js', 'w') as bigfile:
    for root, dirs, files in walk(datadir):
        for name in files:
            fullpath = join(root, name)
            name, ext = splitext(fullpath)
            raw = basename(name)
            name = raw.lower()
            ext = ext.lower()
            if ext != '.json':
                continue
            with open(fullpath, 'r') as onefile:
                content = onefile.read()
                bigfile.write('var %s = %s;\n' % (name, content))
                lines.append((raw, name))

# Parser definitions
with open('parser.js', 'w') as prfile:
    prfile.write('')

# Parse references
with open('refs.js', 'w') as prfile:
    for one, two in lines:
        prfile.write('parse%s(%s);\n' % (one, two))

# Generate HTML file
with tag('html'):
    with tag('head'):
        with tag('title'):
            text('JS debug')
        with tag('script', src='bigdata.js'):
            text('')
        with tag('script', src='parser.js'):
            text('')
        with tag('script', src='refs.js'):
            text('')
    with tag('body'):
        with tag('p'):
            text('Just debug that...')

with open('index.html', 'w') as idxfile:
    idxfile.write('%s\n' % doc.getvalue())

# Log exit
print 'Done.'
