# -*- coding: utf-8 -*-

import re
import pickle
import os
import html


SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))


from django import template

register = template.Library()


settings = None  # will be loaded once in ServerRootNode.render()


class SectionNode(template.Node):
    def __init__(self, nodelist, section_name):
        self.nodelist = nodelist
        self.section_name = section_name[1:-1]

    def render(self, context):
        return '''<h2>{0}</h2>'''.format(self.section_name) + self.nodelist.render(context)


@register.tag('section')
def tag_func(parser, token):
    section_name = token.split_contents()[1]
    nodelist = parser.parse(('endsection',))
    parser.delete_first_token()
    return SectionNode(nodelist, section_name)


class SubsectionNode(template.Node):
    def __init__(self, nodelist, subsection_name):
        self.nodelist = nodelist
        self.subsection_name = subsection_name[1:-1]

    def render(self, context):
        counter = context.get('subsection_counter', 0)
        counter += 1
        context['subsection_counter'] = counter
        BACKSLASHMAGIC = 'BACKSLASHMAGIC'
        # TODO: count number of backslashes
        mangle_code_sections = lambda x: (re.sub(r'\n\n+', BACKSLASHMAGIC, x.group(0)))
        unmangle_code_sections = lambda x: (re.sub(BACKSLASHMAGIC, r'\n\n', x))
        inner_raw = re.sub(r'\<code.+?</code>', mangle_code_sections, 
                           self.nodelist.render(context), flags=re.DOTALL)
        inner = unmangle_code_sections('\n\n'.join(['<p>{0}</p>'.format(par) for par in re.split('\n\n+', inner_raw)]))
        return ('<hr>' if counter > 1 else '') + '''<a name="{0}"><h3>{1}</h3></a>'''.format(counter, self.subsection_name) + inner


@register.tag('subsection')
def tag_func(parser, token):
    subsection_name = token.split_contents()[1]
    nodelist = parser.parse(('endsubsection',))
    parser.delete_first_token()
    return SubsectionNode(nodelist, subsection_name)


class ServerRootNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        global settings

        if not settings:
            with open(os.path.join(SCRIPT_ROOT, 'tags_settings.pickle'), 'rb') as f:
                settings = pickle.load(f)
            if not settings['server_root'].endswith('/'):
                settings['server_root'] += '/'
        return settings['server_root']


@register.tag('server_root')
def tag_func(parser, token):
    return ServerRootNode()   


class ProgramCodeNode(template.Node):
    def __init__(self, program_text, language, filename):
        self.program_text = program_text
        self.language = language[1:-1]
        self.filename = filename[1:-1] if filename else ''

    def render(self, context):
        return (('<div class="filename">{0}</div>'.format(self.filename) if self.filename else '') + 
                '''<div><pre><code class="{0}">'''.format(self.language) + 
                self.program_text + 
                '''</code></pre></div>''')


@register.tag('program')
def tag_func(parser, token):
    language, *params = token.split_contents()[1:]
    filename = None
    if params:
        if len(params) > 1:
            raise ValueError('''Error in some file at line {lineno}:
Too many parameters to "program" tag: need LANGUAGE [PROGRAM], got "{0}"'''.format(
                str(params), lineno=token.lineno))
        else:
            filename = params[0]

    text = []
    while True:
        token = parser.tokens.pop(0)
        if token.contents == 'endprogram':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{ ')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{% ')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append(' }}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append(' %}')
    return ProgramCodeNode(html.escape(''.join(text).strip()), language, filename)