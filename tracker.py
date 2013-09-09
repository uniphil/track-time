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
from datetime import datetime
import dateutil.parsers

from flask import Flask, request, render_template, url_for, abort, jsonify
from flask.views import MethodView

import data
from config import configure_app


app = Flask(__name__)
configure_app(app)


@app.route('/')
def hello():
    return render_template('hello.html')


class Resource(object):

    def __init__(self, name, url_prefix, model):
        self.model = model
        self.format = None
        self.filters = None
        self._autometa_func = None

        id_url = '{}<id>'.format(url_prefix)
        ep = lambda part: '{}.{}'.format(name, part)
        app.add_url_rule(url_prefix, ep('index'), self.index, methods=['GET'])
        app.add_url_rule(url_prefix, ep('post'), self.post, methods=['POST'])
        app.add_url_rule(id_url, ep('get'), self.get, methods=['GET'])
        app.add_url_rule(id_url, ep('put'), self.put, methods=['PUT'])
        app.add_url_rule(id_url, ep('patch'), self.patch, methods=['PATCH'])
        app.add_url_rule(id_url, ep('delete'), self.delete, methods=['DELETE'])

    def autometa(self, func):
        self._autometa_func = func
        return func

    def _clean(self, params):
        pass

    def _format(self, stuff):
        pass

    def index(self):
        filter = {}
        all_of_them = self.model.filter(**filter)
        return jsonify(all_of_them)

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


required = lambda thing: len(thing) > 0
absent = lambda thing: thing is None


def inflate_project(name):
    matches = data.projects.filter(name=name)
    if matches:
        project = matches[0]
    else:
        new_project = {'name': name}
        project = data.projects.save_new(new_project)
    return project


def project_fix_refs(proj):
    if not proj:
        return {'name': None,
                'ref': None}
    oid = proj['_oid']
    ref = url_for('projects.get', id=str(oid))
    return {'name': proj['name'],
            'ref': ref}


tasks_resource = Resource('tasks', '/tasks/', data.tasks)

tasks_resource.format = {
    'description': dict(validate=[required]),
    'duration': dict(validate=[required], convert_in=('duration', int)),
    'project': dict(validate=[],
                    convert_in=inflate_project,
                    convert_out=project_fix_refs),
    'date': dict(validate=[required],
                 convert_in=('date', lambda s: dateutil.parser.parse(s))),
    'ref': dict(validate=[],
                convert_in=('id', lambda s: s.rsplit('/', 1)[-1])),
}

@tasks_resource.autometa
def task_autometa(task):
    if 'recorded' not in task:
        task['recorded'] = datetime.now()
    return task


projects_resource = Resource('projects', '/projects/', data.projects)

projects_resource.format = {
    'name': dict(validate=[required])
}


if __name__ == '__main__':
    app.run()
