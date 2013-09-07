# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    centralized tracker config, for both the data module and the web ui.

    this module must provide two methods:
    `configure_app`, which takes a flask app as its parameter, and
    `configure_data`, which the data module is expected to call to get its
    configuration.

    author: uniphil
    copyright: whatever 2013
"""

__all__ = ('hello')

hello = lambda: 0

def configure_app(app):
    app.debug = True
