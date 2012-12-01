# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353606245.442797
_template_filename = u'/Users/john/Projects/eencms/src/cms/cms/templates/components/page/pagetitle.html'
_template_uri = u'/components/page/pagetitle.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        page = pageargs['page'] 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['page'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n')
        # SOURCE LINE 2
        if session.get('cmsuser') and session['cmsuser']:
            # SOURCE LINE 3
            __M_writer(u'                        <h2>\n                            ')
            # SOURCE LINE 4
            __M_writer(escape(page.title))
            __M_writer(u'\n                            <a href="#" onclick="return cmsmenu(\'page\', ')
            # SOURCE LINE 5
            __M_writer(escape(page.id))
            __M_writer(u', this);">\n                                <img src="/img/icons/edit.png" />\n                            </a>\n                        </h2>\n')
            # SOURCE LINE 9
        else:
            # SOURCE LINE 10
            __M_writer(u'                        <h2>')
            __M_writer(escape(page.title))
            __M_writer(u'</h2>\n')
            pass
        return ''
    finally:
        context.caller_stack._pop_frame()


