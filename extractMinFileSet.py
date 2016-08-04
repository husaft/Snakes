#!/usr/bin/python
import json
import sys
import os

from os import walk
from os.path import join
from sys import argv

# Options
prjdir = argv[1]
found = list()

# Find all project files
for root, dirs, files in walk(prjdir):
    for name in files:
        fullpath = join(root, name)
        simple = fullpath.replace(prjdir, '')[1:]
        found.append(simple)

# Sort them!
sortedFounds = sorted(found, key=str.lower)

# Build index file
with open('filelist.txt', 'w') as idxfile:
    for item in sortedFounds:
        idxfile.write("%s\n" % item)

# Set up text container
texts = set()

# Handle different data types
def processDict(val):
    for k,v in val.iteritems():
        processData(v)

def processList(val):
    for it in val:
        processData(it)

def processText(val):
    txt = val.strip()
    if txt:
        texts.add(txt)

def processNumber(val):
    pass

def processNone(val):
    pass

def processData(data):
    dt = type(data)
    if dt == dict:
        processDict(data)
    elif dt == list:
        processList(data)
    elif dt == unicode:
        processText(data)
    elif dt == int or dt == float or dt == bool:
        processNumber(data)
    elif data is None:
        processNone(data)
    else:
        raise ValueError(dt)

# Read JSON files
for item in sortedFounds:
    if item.endswith('.json'):
        path = join(prjdir, item)
        with open(path, 'r') as jsfile:
            data = json.load(jsfile)
            processData(data)

# Find referenced files
for item in sortedFounds:
    refs = list()
    for text in texts:
        if len(text) >= 2 and text in item:
            refs.append(text)
    if refs:
        print item, refs

