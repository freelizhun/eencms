# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353606279.336614
_template_filename = '/Users/john/Projects/eencms/src/cms/cms/templates/pages/cms/login.html'
_template_uri = '/pages/cms/login.html'
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
        url = context.get('url', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n\n                    <div class="column">\n                        <div class="helptext">\n                            &nbsp;\n                        </div>\n                    </div>\n\n                    <div class="column columndouble">\n                        <h2>Inloggen in het CMS</h2>\n')
        # SOURCE LINE 12
        if c.error:
            # SOURCE LINE 13
            __M_writer(u'                        <p class="error">')
            __M_writer(escape(c.error))
            __M_writer(u'</p>\n')
            pass
        # SOURCE LINE 15
        __M_writer(u'                        <div class="hr firsthr">\n                            <hr />\n                        </div>\n                        <form name="cmslogin" method="post" action="')
        # SOURCE LINE 18
        __M_writer(escape(url(controller='cms', action='submit')))
        __M_writer(u'" id="inschrijven">\n                            <dl>\n                                <dt><label for="my_username_id">Gebruikersnaam</label></dt>\n                                <dd><input name="username" id="my_username_id" type="text" class="last" /></dd>\n                                <dt><label for="my_passwd_id">Wachtwoord</label></dt>\n                                <dd><input name="passwd" id="my_passwd_id" type="password" class="last" /></dd>\n                            </dl>\n                            <input name="inloggen" type="submit" class="readmore" id="inschrijven_submit" value="Inloggen"> \n                            <div class="hr"> \n                                <hr /> \n                            </div> \n                        </form>\n                    </div>\n                    <div class="column_footer">&nbsp;</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'CMS Login')
        return ''
    finally:
        context.caller_stack._pop_frame()


