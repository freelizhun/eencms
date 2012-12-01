# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353850679.887754
_template_filename = u'/Users/john/Projects/eencms/src/cms/cms/templates/components/tree/node.html'
_template_uri = u'/components/tree/node.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        node = pageargs['node'] 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['node'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<li>\n    ')
        # SOURCE LINE 3
        __M_writer(escape(node.title))
        __M_writer(u' - ')
        __M_writer(escape(node.menutitle))
        __M_writer(u'\n    <span class="meta">[id=')
        # SOURCE LINE 4
        __M_writer(escape(node.id))
        __M_writer(u';iname=')
        __M_writer(escape(node.iname))
        __M_writer(u';created=')
        __M_writer(escape(node.created.strftime("%Y%m%d%H%M%S")))
        __M_writer(u';changed=')
        __M_writer(escape(node.created.strftime("%Y%m%d%H%M%S")))
        __M_writer(u']</span>\n')
        # SOURCE LINE 5
        if len(c.tree.get_children(node)):
            # SOURCE LINE 6
            __M_writer(u'    <ul>\n')
            # SOURCE LINE 7
            for sub in c.tree.get_children(node):
                # SOURCE LINE 8
                __M_writer(u'        ')
                runtime._include_file(context, u'node.html', _template_uri, node=sub)
                __M_writer(u'\n')
                pass
            # SOURCE LINE 10
            __M_writer(u'    </ul>\n')
            pass
        # SOURCE LINE 12
        __M_writer(u'</li>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


