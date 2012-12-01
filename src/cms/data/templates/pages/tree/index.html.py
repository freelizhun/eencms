# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353851168.670729
_template_filename = '/Users/john/Projects/eencms/src/cms/cms/templates/pages/tree/index.html'
_template_uri = '/pages/tree/index.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n    <head>\n        <title>Website Tree</title>\n        <style type="text/css">\n            body { background-color: rgb(223, 223, 225); color: #000; font-size: 11pt; }\n            * { font-family: verdana, sans-serif; }\n            .meta { font-size: 0.7em; }\n        </style>\n    </head>\n    <body>\n        <h2>Hoe ziet de website-tree er uit?</h2>\n        <ul>\n')
        # SOURCE LINE 13
        for node in c.tree.get_nodes(0):
            # SOURCE LINE 14
            runtime._include_file(context, u'/components/tree/node.html', _template_uri, node=node)
            __M_writer(u'\n')
            pass
        # SOURCE LINE 16
        __M_writer(u'        </ul>\n    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


