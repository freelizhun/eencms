"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper


def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    mc = map.connect

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    mc('/error/{action}', controller='error')
    mc('/error/{action}/{id}', controller='error')

    # Home
    mc('/', controller='home', action='index')

    # very custom
    mc('/{id}-{title}', controller='page', action='view')

    mc('/cms', controller='mgmt', action='index')
    mc('/cms/{action}', controller='mgmt')
    mc('/cms/{action}/{id}', controller='mgmt')

    mc('/nieuws', controller='news', action='list')
    mc('/nieuws/{id}/{title}', controller='news', action='view')

    mc('/resource/{action}/{id}/{name}', controller='fetch')

    # Default fallbacks (cms, other pages)
    mc('/{controller}', action='index')
    mc('/{controller}/{action}')
    mc('/{controller}/{action}/{id}')

    return map
