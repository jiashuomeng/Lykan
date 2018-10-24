#!/usr/bin/python
#coding:utf-8

import os

base_path = os.path.abspath('.')

catalogue = []

text = []

def init_catalogue():
	for f in os.listdir(base_path):
	    if f.startswith('_'):
	    	catalogue.append(f[1:])

def init_text():
	for p in catalogue:
		text.append('## [' + p + '](../../tree/master/_' +  p + ')')
		pp = base_path + '/_' + p
		for c in os.listdir(pp):
			if not c.endswith('.md'):
				continue
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










