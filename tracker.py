#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    tracker
    ~~~~~~~

    this module provides the web ui

    author: uniphil
    copyright: whatever 2013
"""

from functools import wraps
from flask import Flask, request, render_template, abort, jsonify
import data
from config import configure_app


app = Flask(__name__)
configure_app(app)


mime_map = {
    'text/html': 'html',
    'application/json': 'json',
}


def acceptable(**type_render):
    print("setting up acceptable with", ", ".join(type_render))
    def wrapper(func):
        print("wrapping", func)
        @wraps(func)
        def responder(*args, **kwargs):
            print("responding...")
            data = func(*args, **kwargs)
            accepted = (m for m, s in mime_map.items() if s in type_render)
            wants = request.accept_mimetypes.best_match(accepted)
            if wants is None:
                abort(406)  # unacceptable type
            data = func(*args, **kwargs)
            return type_render[mime_map[wants]](data)
        return responder
    return wrapper


jinja2 = lambda template: lambda data: render_template(template, data=data)


@app.route('/')
@acceptable(html=jinja2('hello.html'))
def hello():
    return {}


@app.route('/tasks/', methods=['GET', 'POST'])
@acceptable(html=jinja2('task_index.html'), json=jsonify)
def tasks_index():
    if request.method == 'POST':



@app.route('/tasks/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@acceptable(html=jinja2('task.html'), json=jsonify)
def task(id):
    return {}


@app.route('/projects/', methods=['GET', 'POST'])
@acceptable(html=jinja2('project_index.html'), json=jsonify)
def projects():
    return 'projects'


@app.route('/projects/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@acceptable(html=jinja2('project.html'), json=jsonify)
def project(id):
    return {}


if __name__ == '__main__':
    app.run()
