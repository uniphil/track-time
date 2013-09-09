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


@app.route('/tasks/', methods=['GET', 'POST'])
@acceptable(html=jinja2('task_index.html'), json=jsonify)
def tasks_index():
    if request.method == 'POST':
        raise NotImplementedError('lalala')
        # validate input
        stuff = {}
        new_task = data.Task(**stuff)
        new_task.save()
        # return 303 see other
    return data.get_tasks()


@app.route('/tasks/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@acceptable(html=jinja2('task.html'), json=jsonify)
def task(id):
    this_task = data.get_task(id)
    if request.method == 'GET':
        return this_task
    elif request.method == 'PUT':
        raise NotImplementedError('lalala')
        # validate task
        updated = {}
        this_task.update(updated)
        this_task.save()
        return this_task
    elif request.method == 'PATCH':
        raise NotImplementedError('lalala')
        # validate update
        update = {}
        this_task.update(update)
        this_task.save()
        return this_task
    elif request.method == 'DELETE':
        raise NotImplementedError('lalala')
        this_task.remove()
        # return 204 no content


@app.route('/projects/', methods=['GET', 'POST'])
@acceptable(html=jinja2('project_index.html'), json=jsonify)
def projects():
    if request.method == 'POST':
        raise NotImplementedError('lalala')
        # validate input
        stuff = {}
        new_project = data.Project(**stuff)
        new_project.save()
        # Return 303 see other
    return data.get_some_project_stuff()


@app.route('/projects/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@acceptable(html=jinja2('project.html'), json=jsonify)
def project(id):
    this_project = data.get_project(id)
    if request.method == 'GET':
        return this_project
    elif request.method == 'PUT':
        raise NotImplementedError('lalala')
        # validate task
        updated = {}
        this_project.update(updated)
        this_project.save()
        return this_project
    elif request.method == 'PATCH':
        raise NotImplementedError('lalala')
        # validate update
        update = {}
        this_project.update(update)
        this_project.save()
        return this_project
    elif request.method == 'DELETE':
        raise NotImplementedError('lalala')
        this_task.remove()
        # return 204 no content


if __name__ == '__main__':
    app.run()
