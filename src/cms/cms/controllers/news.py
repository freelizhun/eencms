import logging
import datetime

from pylons import request, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from cms.lib.base import BaseController, render, model
import cms.lib.pagination as pagination

log = logging.getLogger(__name__)


class NewsController(BaseController):
    def __before__(self):
        BaseController.__before__(self)
        c.page = c.tree.find_matching_shortcut('news', 'list')

    def index(self):
        return self.list()

    def list(self):
        c.numnews, newsquery = model.list_news(**request.params)
        c.news = newsquery.all()
        c.pagination = pagination.require_pagination(c.numnews)

        c.cmsmenuOptions['title'] = {1: self._getTitleCmsmenu()}
        c.cmsmenuOptions['news'] = {}
        for news in c.news:
            c.cmsmenuOptions['news'][news.id] = self._getItemCmsmenu(news)

        return render('/pages/news/list.html')

    def view(self, id, title=None):
        c.news = model.findNews(int(id))
        if not c.news:
            abort(404)
        c.cmsmenuOptions['news'] = {c.news.id: self._getItemCmsmenu(c.news)}
        return render('/pages/news/view.html')

    def _getItemCmsmenu(self, news):
        opt = []
        opt.append(dict(label='Item toevoegen',
                        url=url(controller='news', action='edit', id='new')))
        opt.append(dict(label='Item bewerken',
                        url=url(controller='news', action='edit', id=news.id)))
        opt.append(dict(label='Item verstoppen',
                        url=url(controller='news', action='hide', id=news.id),
                        valid='valid_display({0})'.format(int(news.active))))
        opt.append(dict(label='Item tonen',
                        url=url(controller='news',
                                action='unhide',
                                id=news.id),
                        valid='valid_display(%d)' % (int(not news.active))))
        opt.append(dict(label='Item verwijderen',
                        url=url(controller='news',
                        action='delete',
                        id=news.id),
                   separate=True,
                   confirm="confirm('weet je het zeker?');"))
        return opt

    def _getTitleCmsmenu(self):
        opt = []
        opt.append(dict(label='Item toevoegen',
                        url=url(controller='news', action='edit', id='new')))
        return opt

    def edit(self, id=None):
        c.page = c.tree.findMatchingShortcut('news', 'list')
        if id == 'new':
            c.item = model.News()
            c.item.id = 'new'
        else:
            c.item = model.findNews(id)

        if session.get('errors'):
            c.errors = session.get('errors')
            del session['errors']
        if session.get('fields'):
            c.fields = session.get('fields')
            del session['fields']
        session.save()

        return render('/pages/news/edit.html')

    def submit(self, id=None):
        if id == 'new':
            news = model.News()
            news.title = 'Nieuw nieuws'
            news.created = datetime.datetime.now()
            news.active = True
        else:
            news = model.findNews(id)

        rp = request.params
        title = rp.get('title')
        teaser = rp.get('teaser')
        content = rp.get('content')

        errors = []
        if not title:
            errors.append(dict(title='title', message='notempty'))
        if not teaser:
            errors.append(dict(title='teaser', message='notempty'))
        if not content:
            errors.append(dict(title='content', message='notempty'))

        if errors:
            session['errors'] = errors
            session['fields'] = dict(title=title,
                                     teaser=teaser,
                                     content=content)
            session.save()
            redirect(url(controller='news', action='edit', id=id))

        news.title = title
        news.teaser = teaser
        news.content = content
        if id == 'new':
            model.save(news)
        model.commit()

        log.info("Saving new item id=%r;title=%s;created=%s",
                 id,
                 news.title,
                 str(news.created))
        return redirect(url(controller='news', action='list'))

    def hide(self, id=None):
        news = model.findNews(id)
        news.active = False
        model.commit()
        return redirect(url(controller='news', action='list'))

    def unhide(self, id=None):
        news = model.findNews(id)
        news.active = True
        model.commit()
        return redirect(url(controller='news', action='list'))

    def delete(self, id=None):
        news = model.findNews(id)
        log.info("Deleting news item %d %s", news.id, news.title)
        model.delete(news)
        model.commit()
        return redirect(url(controller='news', action='list'))
