.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Relationships Between Entities
==============================

Whenever you want or need to work with lists, you have to use the PyEnty List(typeof=) class.
List(typeof=) only accepts items of the same type and release you from dealing with a MongoDB model
that doesn't reflects your entities model defined in your project.

Remeber that, whenever you use lists, your class will be mapped to a document with an array
embedded in it.

Example::

    class Seller(Entity):
        name = Str()
        last_name = Str()
        sold_products = List(Products)

        def __init__(self, name='', last_name=''):
            self.name = name
            self.last_name = last_name
            self.sold_products = List(Products)

    user = Seller('jonh', 'ted')
    user.sold_products.append(Product('p1'))
    user.sold_products.append(Product('p2'))
    user.sold_products.append(Product('p3'))

The way the class will be saved in mongodb::

    {
         "_id" : ObjectId("54f083faaa89ba219873a3fa"),
         "name" : "jonh",
         "last_name" : "ted"
         "products"  : [{'name':'p1'}, {'name':'p2'}, {'name':'p3'}]
    }

In this example, products lists tends to grow a lot and can impact your project in future with some MongoDB limitations.
For more information about this limitations, take a look at `MongoDB Limits and Thresholds <http://docs.mongodb.org/manual/reference/limits/>`_


`Rules MongoDB Schema Design <http://blog.mongodb.org/post/87200945828/6-rules-of-thumb-for-mongodb-schema-design-part-1>`_::



