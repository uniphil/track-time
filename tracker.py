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
import dateutil.parser

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
        self.name = name
        self.model = model
        self._clean_incoming_func = None
        self._clean_outgoing_func = None
        self._clean_filters_func = None
        self._autometa_func = None
        id_url = '{}<id>'.format(url_prefix)
        ep = lambda part: '{}.{}'.format(name, part)
        app.add_url_rule(url_prefix, ep('index'), self.index, methods=['GET'])
        app.add_url_rule(url_prefix, ep('post'), self.post, methods=['POST'])
        app.add_url_rule(id_url, ep('get'), self.get, methods=['GET'])
        app.add_url_rule(id_url, ep('put'), self.put, methods=['PUT'])
        app.add_url_rule(id_url, ep('patch'), self.patch, methods=['PATCH'])
        app.add_url_rule(id_url, ep('delete'), self.delete, methods=['DELETE'])

    def clean_incoming(self, func):
        self._clean_incoming_func = func
        return func

    def clean_outgoing(self, func):
        self._clean_outgoing_func = func
        return func

    def clean_filters(self, func):
        self._clean_filters_func = func
        return func

    def autometa(self, func):
        self._autometa_func = func
        return func

    def index(self):
        filter = {}
        models = self.model.filter(**filter)
        polished = [self._clean_outgoing_func(t) for t in models]
        return jsonify({self.name: polished})

    def post(self):
        stuff = self._clean_incoming_func(request.form)
        saved = self.model.save_new(stuff)
        polished = self._clean_outgoing_func(saved)
        return jsonify(polished)

    def get(self, id):
        task = self.model.get(id)
        polished = self._clean_outgoing_func(task)
        return jsonify(polished)

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass


tasks_resource = Resource('tasks', '/tasks/', data.tasks)

@tasks_resource.clean_incoming
def task_rest_to_data(incoming, should_have_ref=False):
    invalid = lambda message: 'Invalid task: {}'.format(message)

    # 1. validate
    missing = lambda thing: invalid('missing {}'.format(thing))
    assert 'description' in incoming, missing('description')
    assert 'duration' in incoming, missing('duration')
    assert 'date' in incoming, missing('date')
    if should_have_ref:
        assert 'ref' in incoming, missing('ref')

    # 2. clean
    cleaned = {}
    cleaned['description'] = incoming['description']
    assert incoming['duration'].isdigit(), invalid('duration must be an int')
    cleaned['duration'] = int(incoming['duration'])
    try:
        cleaned['date'] = dateutil.parser.parse(incoming['date'])
    except ValueError as ve:
        raise AssertionError(invalid('date: {}'.format(ve.message)))
    if 'project' in incoming:
        project_matches = data.projects.filter(name=incoming['project'])
        if project_matches:
            project = project_matches[0]
        else:
            # WARNING: possible race condition
            new_project = {'name': incoming['project']}
            project = data.projects.save_new(new_project)
    else:
        project = None
    cleaned['project'] = project
    if should_have_ref:
        assert '/' in incoming['ref'], invalid('ref: should have "/"')
        cleaned['id'] = incoming['ref'].rsplit('/', 1)[-1]

    # 3. hooray
    return cleaned

@tasks_resource.clean_outgoing
def task_data_to_rest(outgoing):
    cleaned = outgoing.copy()
    id = cleaned.pop('id')
    cleaned['ref'] = url_for('tasks.get', id=id)
    if not cleaned['project']:
        project = {'name': None, 'ref': None}
    else:
        oid = cleaned['project']['_oid']
        ref = url_for('projects.get', id=str(oid))
        project = {'name': proj['name'], 'ref': ref}
    cleaned['project'] = project
    return cleaned

@tasks_resource.autometa
def task_autometa(task):
    if 'recorded' not in task:
        task['recorded'] = datetime.now()
    return task


projects_resource = Resource('projects', '/projects/', data.projects)


if __name__ == '__main__':
    app.run()
