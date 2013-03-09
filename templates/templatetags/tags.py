# -*- coding: utf-8 -*-

import re


from django import template

register = template.Library()


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
        inner = '\n\n'.join(['<p>{0}</p>'.format(par) for par in re.split('\n\n+', self.nodelist.render(context))])
        return '''<h3>{0}</h3>'''.format(self.subsection_name) + inner


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
        return '/html/out/'


@register.tag('server_root')
def tag_func(parser, token):
    return ServerRootNode()   


class ProgramCodeNode(template.Node):
    def __init__(self, nodelist, language):
        self.nodelist = nodelist
        self.language = language[1:-1]

    def render(self, context):
        return '''<pre><code class="{0}">'''.format(self.language) + self.nodelist.render(context).lstrip() + '''</code></pre>'''


@register.tag('program')
def tag_func(parser, token):
    language = token.split_contents()[1]
    nodelist = parser.parse(('endprogram',))
    parser.delete_first_token()
    return ProgramCodeNode(nodelist, language)   