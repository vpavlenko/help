#!/usr/bin/env python3

import sys
import os
import shutil
import collections
import re

SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))


with open('settings.py', 'w') as output_file:
	output_file.write('''
SECRET_KEY = '42'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)

TEMPLATE_DIRS = (
	'{0}',
)		
'''.format(os.path.join(SCRIPT_ROOT, 'templates')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from django import template
from django.template import loader


def print_usage():
	print('''Usage:
{0} INPUT_DIR OUTPUT_DIR

Script directory should contain the folder 'libraries/'.

Possible layout in INPUT_DIR:
INPUT_DIR
|--01_python
|  |--help_config.py
|  |--index_content.html
|  |--01_intro.txt
|  |--02_datatypes.py  (file extension doesn't matter)
|--02_html
   |--help_config.py
   |--index_content.html   
   |--01_intro.html
   |--02_tables.html'''.format(sys.argv[0]))


def render_index(index_content, courses, output_dir):
	index_template = template.Template(open(os.path.join(SCRIPT_ROOT, 'templates/site-index.html')).read())
	index_context = template.Context({})
	with open(os.path.join(output_dir, 'index.html'), 'w') as output_file:
		output_file.write(index_template.render(index_context))


def render_course(course, output_dir):
	os.mkdir(os.path.join(output_dir, course.urlname))


def main():
	if len(sys.argv) != 3:
		print_usage()
		sys.exit(1)
	else:
		input_dir, output_dir = sys.argv[1:]
		libraries_dir = os.path.join(SCRIPT_ROOT, 'libraries')

		print('Remove "{0}"'.format(output_dir))
		shutil.rmtree(output_dir, ignore_errors=True)
		print('Create "{0}"'.format(output_dir))
		os.mkdir(output_dir)
		print('Copy libraries from "{0}" to "{1}"'.format(libraries_dir, output_dir))
		shutil.copytree(libraries_dir, os.path.join(output_dir, 'libraries'))

		Course = collections.namedtuple('Course', ['directory', 'urlname', 'name'])

		courses = []

		for course_dir in sorted([filename for filename in os.listdir(input_dir) 
				if re.match(r'^[0-9]+_', filename)], 
				key=lambda x: int(x.split('_')[0])):
			urlname = course_dir.split('_', maxsplit=1)[1]
			course_complete_dir = os.path.join(input_dir, course_dir)
			config = eval(open(os.path.join(course_complete_dir, 'help_config.py')).read())
			courses.append(Course(directory=course_complete_dir, urlname=urlname, name=config['name']))

		print('Render index')
		index_content = open(os.path.join(input_dir, 'index_content.html')).read()
		render_index(index_content, courses, output_dir)

		for course in courses:
			print('Render course "{0}" ({1})'.format(course.directory, course.name))
			render_course(course, output_dir)
		

if __name__ == '__main__':
	main()