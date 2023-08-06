"""Quokka CMS!"""

__version__ = '0.3.0'

from quokka.app import QuokkaApp
from quokka.core import configure_extensions, configure_extension
from quokka.core.flask_dynaconf import configure_dynaconf
# from quokka.core.db import configure_db


def create_app_base(test=False, ext_list=None, **settings):
    """Creates basic app only with extensions provided in ext_list
    useful for testing."""

    app = QuokkaApp('quokka')
    configure_dynaconf(app)
    # configure_db(app)
    if settings:
        app.config.update(settings)

    if test or app.config.get('TESTING'):
        app.testing = True

    if ext_list:
        for ext in ext_list:
            configure_extension(ext, app=app)

    return app


def create_app(test=False, **settings):
    """Creates full app with all extensions loaded"""
    app = create_app_base(test=test, **settings)
    configure_extensions(app)
    return app
