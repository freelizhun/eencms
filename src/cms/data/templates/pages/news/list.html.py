# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353606245.429794
_template_filename = '/Users/john/Projects/eencms/src/cms/cms/templates/pages/news/list.html'
_template_uri = '/pages/news/list.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/components/base/base.html', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n                    <div class="column">\n                    </div>\n\n                    <div class="column columndouble">\n')
        # SOURCE LINE 8
        runtime._include_file(context, u'/components/page/pagetitle.html', _template_uri, page=c.page)
        __M_writer(u'\n')
        # SOURCE LINE 9
        if len(c.news):
            # SOURCE LINE 10
            for item in c.news:
                # SOURCE LINE 11
                runtime._include_file(context, u'/components/news/newsitem.html', _template_uri, item=item)
                __M_writer(u'\n')
                pass
            # SOURCE LINE 13
            __M_writer(u'\n')
            # SOURCE LINE 14
            if c.pagination:
                # SOURCE LINE 15
                runtime._include_file(context, u'/components/base/pagination.html', _template_uri, pages=h.pagination.getPageList(c.numnews))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 17
            __M_writer(u'\n')
            # SOURCE LINE 18
        else:
            # SOURCE LINE 19
            __M_writer(u'                        <h3>Helaas</h3>\n                        <p>Geen nieuws gevonden</p>\n')
            pass
        # SOURCE LINE 22
        __M_writer(u'                    </div>\n                    <div class="column_footer">&nbsp;</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'Nieuws')
        return ''
    finally:
        context.caller_stack._pop_frame()


