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

"""A module required to model your classes."""

from collections import OrderedDict


class Typed:
    """ Base class for descriptors """
    _expected_type = type(None)

    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError('Type Received:' + str(type(value)) +  'Type Expected: ' + str(self._expected_type))
        instance.__dict__[self._name] = value


class Int(Typed):
    _expected_type = int


class Str(Typed):
    _expected_type = str


class Float(Typed):
    _expected_type = float


class Type(Typed):
    _expected_type = None

    def __init__(self, typeof):
        self._expected_type = typeof

    @property
    def expected_type(self):
        return self. _expected_type


class List(Typed, list):
    """ List inherit from both Typed and list in order to use only one type
        entity requires
    """
    _expected_type = None

    def __init__(self, typeof, *args):
        self._typeof = typeof
        self._expected_type = List
        list.__init__(self, *args)

    def list_not_accepted(self, lst):
        for item in lst:
            if not isinstance(item, self._typeof):
                return True

    def __set__(self, instance, lst):
        if not isinstance(lst, List):
            raise TypeError("type must be a typed List(typeof=) of entity")

        if lst.typed_of != self._typeof:
            raise TypeError('typeof expected: ' + str(self.typed_of))

        if not isinstance(lst, self._expected_type) or self.list_not_accepted(lst):
            raise TypeError('Type Expected: ' + str(self._expected_type))
        instance.__dict__[self._name] = lst

    def __setitem__(self, key, item):
        if not type(item) is self._typeof:
            raise TypeError("Invalid Type %s" % type(item).__name__)
        super(List, self).__setitem__(key)

    def __getitem__(self, key):
        return super(List, self).__getitem__(key)

    def append(self, obj):
        if not type(obj) is self._typeof:
            raise TypeError("Invalid Type %s" % type(obj).__name__)
        super(List, self).append(obj)

    @property
    def typed_of(self):
        return self._typeof

    @property
    def expected_type(self):
        return self._expected_type


class OrderedMeta(type):
    """ Metaclass which provides an OrderedDict instead of default dict to map Entity instances"""
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        order = []
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                order.append(name)
        d['_order'] = order
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return OrderedDict()


class Entity(metaclass=OrderedMeta):
    """A entity base class required throughout entity
    All of your classes you want to persist in mongo must inherit from Entity
    Usage::

        Product(Entity):
            name = Str()
            description = Str()
            price =  Float()

            def __init__(self, name, description, price):
                self.name = name
                self.description = description
                self.price = price
    """
    dict_entity = None

    def map_dict(self, dict_entity):
        """ map dict_entity to current instance(self) """
        self.dict_entity = dict_entity
        Entity.map(self, self.dict_entity)

    def as_dict(self):
        """ create a dict based on class attributes """
        odict = OrderedDict()
        for name in self._order:
            attr_value = getattr(self, name)
            if isinstance(attr_value, List):
                _list = []
                for item in attr_value:
                    _list.append((item.as_dict() if isinstance(item, Entity) else item))
                    odict[name] = _list
            elif isinstance(attr_value, Entity):
                odict[name] = attr_value.as_dict()
            else:
                odict[name] = getattr(self, name)
        return odict

    @staticmethod
    def map(cls, dict_entity):
        """ staticmethod which will be used in recursive mode in order to map dict to instance """
        for key, value in dict_entity.items():
            if hasattr(cls, key):
                if isinstance(value, list):
                    _list = getattr(cls, key)
                    if isinstance(_list.expected_type, list):
                        for _dict in value:
                            _list.append(cls.map(_list.typeof(), _dict))
                elif isinstance(value, dict):
                    attr = getattr(cls, key)
                    instance = attr.expected_type()
                    Entity.map(instance, value)
                    setattr(cls, key, instance)
                else:
                    setattr(cls, key, value)
            else:
                setattr(cls, key, value)