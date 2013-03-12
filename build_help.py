#!/usr/bin/env python3

import sys
import os
import shutil
import collections
import re
import pickle


SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))


with open('settings.py', 'w') as output_file:
	output_file.write('''
SECRET_KEY = '42'

TEMPLATE_DEBUG = True

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
from django.template.loader import add_to_builtins

add_to_builtins('templates.templatetags.tags')


def print_usage():
	print('''Usage:
{0} INPUT_DIR OUTPUT_DIR SERVER_ROOT

Script directory should contain the folder 'libraries/'.

Possible layout in INPUT_DIR:
INPUT_DIR
|--01_python
|  |--help_config.py
|  |--01_intro.txt
|  |--02_datatypes.py  (file extension doesn't matter)
|--02_html
   |--help_config.py
   |--01_intro.html
   |--02_tables.html'''.format(sys.argv[0]))


def is_section_file(filename):
	return re.match(r'^[0-9]+_', filename)


class Section:
	def __init__(self, section_src_file):
		self.section_src_file = section_src_file
		self.number, self.filename = os.path.split(section_src_file)[1].split('_', maxsplit=1)
		self.number = int(self.number)
		self.filename = os.path.splitext(self.filename)[0] + '.html'
		with open(section_src_file) as f:
			self.raw = f.read()
		try:
			self.name = re.match(r'''\{%\s+section\s+['"]([^'"]+)['"]\s+%\}''', self.raw).group(1)
		except AttributeError as e:
			print('Possibly file "{0}" has no "section" tag'.format(self.section_src_file))
			self.name = 'Unnamed'
		self.subsections = re.findall(r'''\{%\s+subsection\s+['"]([^'"]+)['"]\s+%\}''', self.raw)


class Course:
	def __init__(self, input_dir, course_dir, courses):
		self.courses = courses
		self.urlname = course_dir.split('_', maxsplit=1)[1]
		self.src_path = os.path.join(input_dir, course_dir)
		config = eval(open(os.path.join(self.src_path, 'help_config.py')).read())
		self.name = config.get('name', '')

		self.sections = []
		self.files = []

		for filename in set(os.listdir(self.src_path)) - {'help_config.py'}:
			if is_section_file(filename):
				self.sections.append(Section(os.path.join(self.src_path, filename)))
			else:
				self.files.append(os.path.join(self.src_path, filename))

		self.sections.sort(key=lambda section: section.number)


	def render_course(self, output_dir):	
		os.mkdir(os.path.join(output_dir, self.urlname))

		index_template = template.Template(open(os.path.join(SCRIPT_ROOT, 'templates/course-index.html')).read())
		index_context = template.Context({'courses': self.courses, 'course': self})
		with open(os.path.join(output_dir, self.urlname, 'index.html'), 'w') as output_file:
			output_file.write(index_template.render(index_context))

		for file in self.files:
			try:
				shutil.copytree(file, os.path.join(output_dir, self.urlname, os.path.split(file)[1]))
			except NotADirectoryError:
				shutil.copy2(file, os.path.join(output_dir, self.urlname, os.path.split(file)[1]))

		for section in self.sections:
			print('  Render section "{0}"'.format(section.name))
			section_template = template.Template(open(os.path.join(SCRIPT_ROOT, 'templates/course-section.html'))
					.read().replace('SECTION_CONTENT', section.raw))
			section_context = template.Context({'courses': self.courses, 'course': self, 'section': section})
			with open(os.path.join(output_dir, self.urlname, section.filename), 'w') as f:
				f.write(section_template.render(section_context))


def render_index(index_content, courses, output_dir):
	index_template = template.Template(open(os.path.join(SCRIPT_ROOT, 'templates/site-index.html')).read())
	index_context = template.Context({'courses': courses})
	with open(os.path.join(output_dir, 'index.html'), 'w') as output_file:
		output_file.write(index_template.render(index_context))


def main():
	if len(sys.argv) != 4:
		print_usage()
		sys.exit(1)
	else:
		input_dir, output_dir, server_root = sys.argv[1:]

		with open(os.path.join(SCRIPT_ROOT, 'templates/templatetags/tags_settings.pickle'), 'wb') as f:
			pickle.dump({'server_root': server_root}, f)

		libraries_dir = os.path.join(SCRIPT_ROOT, 'libraries')

		print('Remove "{0}"'.format(output_dir))
		shutil.rmtree(output_dir, ignore_errors=True)
		print('Create "{0}"'.format(output_dir))
		os.mkdir(output_dir)
		print('Copy libraries from "{0}" to "{1}"'.format(libraries_dir, output_dir))
		shutil.copytree(libraries_dir, os.path.join(output_dir, 'libraries'))

		courses = []

		for course_dir in sorted([filename for filename in os.listdir(input_dir) 
				if is_section_file(filename)], 
				key=lambda x: int(x.split('_')[0])):
			courses.append(Course(input_dir, course_dir, courses))

		print('Render index')
		index_content = open(os.path.join(input_dir, 'index_content.html')).read()
		render_index(index_content, courses, output_dir)

		for course in courses:
			print('Render course "{0}" ({1})'.format(course.src_path, course.name))
			course.render_course(output_dir)
		

if __name__ == '__main__':
	main()