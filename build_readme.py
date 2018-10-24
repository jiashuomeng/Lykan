#!/usr/bin/python
#coding:utf-8

import os


PREFIX = '_'

base_path = os.path.abspath('.')

catalogue = []

text = []

def init_catalogue():
	for f in os.listdir(base_path):
	    if f.startswith(PREFIX):
	    	catalogue.append(f[1:])

def init_text():
	for p in catalogue:

		text.append('## [' + p + '](../../tree/master/_' +  p + ')')

		pp = base_path + '/' + PREFIX + p
		for c in os.listdir(pp):
			text.append('- [' + c[:-3] + '](_' + p + '/' + c + ')  ')

def write_file():
	with open('./README.md', 'w') as f:
		for t in text:
			f.write(t)
			f.write('\n')


init_catalogue()

init_text()

write_file()

print 'refresh success!'










