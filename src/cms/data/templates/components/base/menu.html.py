# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353535134.221395
_template_filename = u'/Users/john/Projects/eencms/src/cms/cms/templates/components/base/menu.html'
_template_uri = u'/components/base/menu.html'
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
        __M_writer(u'                <ul class="menu">\n')
        # SOURCE LINE 2
        for node in c.tree.get_children(c.menubase):
            # SOURCE LINE 3
            __M_writer(u'                    <li class="head ')
            __M_writer(escape(node.menutitle.lower()))
            __M_writer(u'"><a href="')
            __M_writer(escape(node.get_url()))
            __M_writer(u'" class="head ')
            __M_writer(escape(node.menutitle.lower()))
            __M_writer(u'">')
            __M_writer(escape(node.menutitle))
            __M_writer(u'</a>\n                        <div class="submenu-container">\n                            <div class="margin">\n                                <ul>\n')
            # SOURCE LINE 7
            for sub in c.tree.get_children(node):
                # SOURCE LINE 8
                if sub.order_id == 1:
                    # SOURCE LINE 9
                    __M_writer(u'                                    <li class="first">\n')
                    # SOURCE LINE 10
                else:
                    # SOURCE LINE 11
                    __M_writer(u'                                    <li>\n')
                    pass
                # SOURCE LINE 13
                __M_writer(u'                                        <a href="')
                __M_writer(escape(sub.get_url()))
                __M_writer(u'">')
                __M_writer(escape(sub.menutitle))
                __M_writer(u'</a>\n                                    </li>\n')
                pass
            # SOURCE LINE 16
            __M_writer(u'                                </ul>\n                            </div>\n                        </div>\n                    </li>\n')
            pass
        # SOURCE LINE 21
        __M_writer(u'                </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


