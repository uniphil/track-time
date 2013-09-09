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


# @app.route('/tasks/', methods=['GET', 'POST'])
# @acceptable(html=jinja2('task_index.html'), json=jsonify)
# def tasks_index():
#     if request.method == 'POST':
#         raise NotImplementedError('lalala')
#         # validate input
#         stuff = {}
#         new_task = data.tasks.save_new(stuff)
#         # return 303 see other
#     return data.get_tasks()


# @app.route('/tasks/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
# @acceptable(html=jinja2('task.html'), json=jsonify)
# def task(id):
#     this_task = (id)
#     if request.method == 'GET':
#         return this_task
#     elif request.method == 'PUT':
#         raise NotImplementedError('lalala')
#         # validate task
#         updated = {}
#         this_task.update(updated)
#         this_task.save()
#         return this_task
#     elif request.method == 'PATCH':
#         raise NotImplementedError('lalala')
#         # validate update
#         update = {}
#         this_task.update(update)
#         this_task.save()
#         return this_task
#     elif request.method == 'DELETE':
#         raise NotImplementedError('lalala')
#         this_task.remove()
#         # return 204 no content


# @app.route('/projects/', methods=['GET', 'POST'])
# @acceptable(html=jinja2('project_index.html'), json=jsonify)
# def projects():
#     if request.method == 'POST':
#         raise NotImplementedError('lalala')
#         # validate input
#         stuff = {}
#         new_project = data.projects.save_new(**stuff)
#         # Return 303 see other
#     return data.get_some_project_stuff()


# @app.route('/projects/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
# @acceptable(html=jinja2('project.html'), json=jsonify)
# def project(id):
#     this_project = data.get_project(id)
#     if request.method == 'GET':
#         return this_project
#     elif request.method == 'PUT':
#         raise NotImplementedError('lalala')
#         # validate task
#         updated = {}
#         this_project.update(updated)
#         this_project.save()
#         return this_project
#     elif request.method == 'PATCH':
#         raise NotImplementedError('lalala')
#         # validate update
#         update = {}
#         this_project.update(update)
#         this_project.save()
#         return this_project
#     elif request.method == 'DELETE':
#         raise NotImplementedError('lalala')
#         this_task.remove()
#         # return 204 no content


if __name__ == '__main__':
    app.run()
