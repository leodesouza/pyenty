#!/usr/bin/env python
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""A simple object-document mapping for mongodb-motor and tornado applications."""

import motor
from tornado.concurrent import TracebackFuture
from tornado.gen import coroutine
from pyenty.types import Entity


class EntityManager(object):
    """Class responsible for object-document mapping.

    Wraps motor functions and provide mapping of instance of Entity
    Entity is a pyenty's base class needed to use with EntityManager

    Example::

        class Product(Entity):
            name = Str()
            description = Str()
            price = Float()

            def __init__(self, name="", description="", price=0.0)
                self.name = name
                self.description = description
                self.price = price

        # using with tornado.gen.coroutine
        @coroutine
        def create_product():
            emanager = EntityManager(Product)
            product = Product(name="p", description="cell phone", price=150.38)
            object_id = yield emanager.save(product)
            saved_product = yield emanager.find_one(_id=object_id)
    """
    def __init__(self, entity, pluralize=False):
        assert isinstance(pluralize, bool), "Error: pluralize parameter must be bool"
        self.__pluralize = pluralize
        self.__session = EntityConnection.get_session()
        self.__entity = entity
        self.__collection_name = None
        self.__collection = None

        self.set_collection(self.__entity)

    def set_pluralize(self, pluralize):
        """enabled/disable pluralization"""
        self.__pluralize = pluralize

    def save(self, entity):
        """Maps entity to dict and returns future"""
        assert isinstance(entity, Entity), " entity must have an instance of Entity"
        return self.__collection.save(entity.as_dict())

    def remove(self, **kwargs):
        """Returns future.

        Executes collection's remove method based on keyword args

        Example::

            manager = EntityManager(Product)
            yield manager.remove(_id=object_id})

        """
        return self.__collection.remove(kwargs)

    def find_one(self, **kwargs):
        """Returns future.

        Executes collection's find_one method based on keyword args
        maps result ( dict to instance ) and return future

        Example::

           manager = EntityManager(Product)
           product_saved = yield manager.find_one(_id=object_id)

         """
        future = TracebackFuture()

        def handle_response(result, error):
            if error:
                future.set_exception(error)
            else:
                instance = self.__entity()
                instance.map_dict(result)
                future.set_result(instance)

        self.__collection.find_one(kwargs, callback=handle_response)

        return future

    @coroutine
    def find(self, **kwargs):
        """Returns List(typeof=).

        Executes collection's find method based on keyword args
        maps results ( dict to list of entity instances).

        Set max_limit parameter to limit the amount of data send back through network

        Example::

            manager = EntityManager(Product)
            products = yield manager.find(age={'$gt': 17}, max_limit=100)

         """
        max_limit = None
        if 'max_limit' in kwargs:
            max_limit = kwargs.pop('max_limit')
        cursor = self.__collection.find(kwargs)
        instances = []
        for doc in (yield cursor.to_list(max_limit)):
            instance = self.__entity()
            instance.map_dict(doc)
            instances.append(instance)
        return instances

    def update(self, entity):
        """ Executes collection's update method based on keyword args.

        Example::

            manager = EntityManager(Product)
            p = Product()
            p.name = 'new name'
            p.description = 'new description'
            p.price = 300.0

            yield manager.update(p)

         """
        assert isinstance(entity, Entity), "Error: entity must have an instance of Entity"
        return self.__collection.update({'_id': entity._id}, {'$set': entity.as_dict()})

    def remove_all(self):
        """ Erase all documents from collection """
        return self.__collection.remove({})

    def set_collection(self, class_):
        assert isinstance(class_, type), "Error: class_ must be an type"
        self.__set_collection(class_.__name__.lower())

    def __set_collection(self, collection_name):
        assert collection_name is not None, "Error: collection_name must be set"
        self.__collection_name = collection_name
        if self.__pluralize:
            self.__collection_name += "s"
        self.__collection = self.__session[self.__collection_name]


class EntityConnection(object):
    """Create a session to be used in all mongodb requests

    Examples::
         - EntitySession.open(db="db_name", io_loop=self.io_loop)
         - EntitySession.open(db="db_name")
         - EntityConnection.open('localhost', port_number, db="db_name")
         - EntityConnection.open('localhost', port_number, db="db_name", io_loop=self.io_loop)
    """

    @classmethod
    def open(cls, *args, **kwargs):
        if 'io_loop' in kwargs:
            motor_client = motor.MotorClient(*args, io_loop=kwargs.pop('io_loop'))
        else:
            motor_client = motor.MotorClient(*args)

        if 'db' in kwargs:
            db_name = kwargs.pop('db')
            setattr(cls, 'session', motor_client[db_name])
        else:
            raise KeyError('db is a Required Argument')

    @classmethod
    def close(cls):
        """Close session"""
        cls.motor_client.close()
        delattr(cls, 'session')

    @classmethod
    def get_session(cls):
        """Get current session"""
        assert hasattr(cls, 'session'), "Error: Session does not exist. First, call EntitySesion.create"
        return cls.session
