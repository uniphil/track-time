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
from flask.views import MethodView
import data
from config import configure_app


app = Flask(__name__)
configure_app(app)


mime_map = {
    'text/html': 'html',
    'application/json': 'json',
}


def acceptable(**type_render):
    def wrapper(func):
        @wraps(func)
        def responder(*args, **kwargs):
            accepted = (m for m, s in mime_map.items() if s in type_render)
            wants = request.accept_mimetypes.best_match(accepted)
            if wants is None:
                abort(406)  # unacceptable type
            stuff = func(*args, **kwargs)
            return type_render[mime_map[wants]](stuff)
        return responder
    return wrapper


jinja2 = lambda template: lambda stuff: render_template(template, stuff=stuff)


@app.route('/')
@acceptable(html=jinja2('hello.html'))
def hello():
    return {}


class Resource(object):

    def __init__(self, name, url_prefix, model):
        self.model = model

        id_url = '{}<id>'.format(url_prefix)
        ep = lambda part: '{}.{}'.format(name, part)
        app.add_url_rule(url_prefix, ep('index'), self.index, methods=['GET'])
        app.add_url_rule(url_prefix, ep('post'), self.post, methods=['POST'])
        app.add_url_rule(id_url, ep('get'), self.get, methods=['GET'])
        app.add_url_rule(id_url, ep('put'), self.put, methods=['PUT'])
        app.add_url_rule(id_url, ep('patch'), self.patch, methods=['PATCH'])
        app.add_url_rule(id_url, ep('delete'), self.delete, methods=['DELETE'])

        self._full_validator_func = None
        self._patch_validator_func = None
        self._filter_validator_func = None

    def full_validator(self, func):
        self._full_validator_func = func
        return func

    def patch_validator(self, func):
        self._patch_validator_func = func
        return func

    def filter_validator(self, func):
        self._filter_validator_func = func
        return func

    def index(self):
        pass

    def post(self):
        pass

    def get(self, id):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass


tasks_resource = Resource('tasks', '/tasks/', data.tasks)
projects_resource = Resource('projects', '/projects/', data.projects)


@tasks_resource.full_validator
def validate_task(task):
    pass

@tasks_resource.patch_validator
def validate_task_patch(patch):
    pass

@tasks_resource.filter_validator
def validate_task_filter(filter):
    pass


@projects_resource.full_validator
def validate_project(project):
    pass

@projects_resource.patch_validator
def validate_project_patch(patch):
    pass

@projects_resource.filter_validator
def validate_project_filter(filter):
    pass


if __name__ == '__main__':
    app.run()
