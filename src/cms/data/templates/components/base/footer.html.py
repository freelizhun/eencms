# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1353535107.899234
_template_filename = u'/Users/john/Projects/eencms/src/cms/cms/templates/components/base/footer.html'
_template_uri = u'/components/base/footer.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        url = context.get('url', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'        <div class="footer">\n            <div class="footer-inner">\n                <ul id="social">\n                    <li id="linkedin"><a href="#">Bezoek ons op Linkedin.</a></li>\n                    <li id="rss"><a class="popup_iframe" href="')
        # SOURCE LINE 5
        __M_writer(escape(url(controller='rss', action='index')))
        __M_writer(u'">Blijf op de hoogte</a></li>\n                    <li id="payoff">Opdrachtgevert |\n                        <a href="')
        # SOURCE LINE 7
        __M_writer(escape(url.current()))
        __M_writer(u'">Sitemap</a> |\n                        <a href="')
        # SOURCE LINE 8
        __M_writer(escape(url.current()))
        __M_writer(u'">Disclaimer</a> |\n                        <a href="')
        # SOURCE LINE 9
        __M_writer(escape(url.current()))
        __M_writer(u'">Privacybeleid</a>\n                    </li>\n                </ul>\n                <div class="clear"></div>\n            </div>\n            <div class="clear"></div>\n        </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


