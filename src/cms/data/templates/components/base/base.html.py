# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353534935.368592
_template_filename = u'/Users/john/Projects/eencms/src/cms/cms/templates/components/base/base.html'
_template_uri = u'/components/base/base.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        session = context.get('session', UNDEFINED)
        config = context.get('config', UNDEFINED)
        c = context.get('c', UNDEFINED)
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n    <head>\n')
        # SOURCE LINE 5
        if hasattr(self, 'title'):
            # SOURCE LINE 6
            __M_writer(u'        <title>')
            __M_writer(escape(self.title()))
            __M_writer(u' &mdash; ')
            __M_writer(escape(config.get('website_title', 'website')))
            __M_writer(u'</title>\n')
            # SOURCE LINE 7
        else:
            # SOURCE LINE 8
            __M_writer(u'        <title>')
            __M_writer(escape(config.get('website_title', 'website')))
            __M_writer(u'</title>\n')
            pass
        # SOURCE LINE 10
        __M_writer(u'\n        <link rel="shortcut icon" href="/res/favicon.ico" type="image/x-icon" />\n\n        <link rel="stylesheet" href="/res/style.css" type="text/css" />\n\n')
        # SOURCE LINE 15
        if session.get('cmsuser') and session['cmsuser']:
            # SOURCE LINE 16
            __M_writer(u'        <link rel="stylesheet" href="/res/cms.css" type="text/css" />\n        <script src="/res/cms.js" type="text/javascript"></script>\n')
            pass
        # SOURCE LINE 19
        __M_writer(u'\n        <script src="/res/jquery.js" type="text/javascript"></script>\n        <script src="/res/jquery-ui.js" type="text/javascript"></script>\n        <script src="/res/jquery.hoverintent.js" type="text/javascript"></script>\n        <script src="/res/basic.js" type="text/javascript"></script>\n')
        # SOURCE LINE 24
        if hasattr(self, 'extraJS'):
            # SOURCE LINE 25
            __M_writer(u'        ')
            __M_writer(escape(self.extraJS()))
            __M_writer(u'\n')
            pass
        # SOURCE LINE 27
        __M_writer(u'    </head>\n    <body\n')
        # SOURCE LINE 29
        if c.bodyclass:
            # SOURCE LINE 30
            __M_writer(u'        id="')
            __M_writer(escape(c.bodyclass))
            __M_writer(u'"\n')
            pass
        # SOURCE LINE 32
        if hasattr(self, 'onload'):
            # SOURCE LINE 33
            __M_writer(u'        onload="')
            __M_writer(escape(self.onload()))
            __M_writer(u'"\n')
            pass
        # SOURCE LINE 35
        __M_writer(u'    >\n        <div class="wrapper">\n            <div class="content_holder">\n                <h1><a href="/" class="logo">')
        # SOURCE LINE 38
        __M_writer(escape(config.get('website_title', 'website')))
        __M_writer(u'</a></h1>\n')
        # SOURCE LINE 39
        runtime._include_file(context, u'menu.html', _template_uri)
        __M_writer(u'\n                <div class="contentholder">\n                    ')
        # SOURCE LINE 41
        __M_writer(escape(self.body()))
        __M_writer(u'\n                    <div class="column_footer">&nbsp;</div>\n                </div>\n            </div>\n            <div class="push"></div>\n        </div>\n')
        # SOURCE LINE 47
        runtime._include_file(context, u'footer.html', _template_uri)
        __M_writer(u'\n\n')
        # SOURCE LINE 49
        if session.get('cmsuser'):
            # SOURCE LINE 50
            runtime._include_file(context, u'/components/cms/cmsmenu.html', _template_uri)
            __M_writer(u'\n')
            # SOURCE LINE 51
            runtime._include_file(context, u'/components/cms/overlay.html', _template_uri)
            __M_writer(u'\n')
            # SOURCE LINE 52
            runtime._include_file(context, u'/components/cms/menuoptions.html', _template_uri)
            __M_writer(u'\n')
            pass
        # SOURCE LINE 54
        __M_writer(u'    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


