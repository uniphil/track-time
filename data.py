# -*- coding: utf-8 -*-
"""
    data
    ~~~~

    this module provides a python-level interface to the data store. while
    this version builds on mongodb, you could replace this module with
    another that uses pickle or sqlalchemy or redis or whatever you want.

    author: uniphil
    copyright: whatever 2013
"""


__all__ = ('tasks', 'projects', 'NotFoundError')


from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from config import data_config


class NotFoundError(ValueError): pass


client = MongoClient(data_config['mongo_uri'])
db = client[data_config['dbname']]


class MongoStore(object):

    def __init__(self, collection_name):
        self.collection = db[collection_name]

    def _id_to_oid(self, id):
        try:
            oid = ObjectId(id)
        except InvalidId:
            raise NotFoundError('Invalid id: {}'.format(id))
        return oid

    def _oid_to_id(self, document):
        thing = document.copy()
        if '_id' not in thing:
            return thing
        thing['id'] = str(thing.pop('_id'))
        return thing

    def get(self, id=None, **filters):
        if id:
            oid = self._id_to_oid(id)
            query = {'_id': oid}
        else:
            query = filters
        document = self.collection.find_one(query)
        if document is None:
            raise NotFoundError('Could not find for id: {}'.format(id))
        id_document = self._oid_to_id(document)
        return id_document

    def filter(self, **filters):
        search_filters = filters.copy()
        if 'id' in search_filters:
            oid = self._id_to_oid(search_filters.pop('id'))
            search_filters['_id'] = oid
        documents = self.collection.find(search_filters)
        id_documents = map(self._oid_to_id, documents)
        return id_documents

    def save_new(self, thing):
        self.collection.insert(thing)
        converted = self._oid_to_id(thing)
        return converted

    def save(self, thing):
        to_save = thing.copy()
        try:
            to_save['_id'] = self._id_to_oid(to_save.pop('id'))
        except KeyError:
            raise NotFoundError('this looks like an unsaved document (missing'
                                ' id)')
        self.collection.save(to_save)

    def remove(self, id):
        oid = self._id_to_oid(id)
        result = self.collection.remove(oid)
        if result.get('n') == 0:
            raise NotFoundError('could not find the document {}'.format(id))


tasks = MongoStore(data_config.get('tasks_collection', 'tasks'))
projects = MongoStore(data_config.get('projects_collection', 'projects'))
