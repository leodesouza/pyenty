.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyEnty
======

A simple object-document mapper written in python for motor( a driver for MongoDB) and to be used in tornado applications.
Although, motor accomplish the hard task of provide async methods to access mongodb,
we  still have to get along with classic python dictionary which force us to create and maintain 
mapping of dicts-to-instance or instance-to-dicts.

Simple example using motor::

    #saves a dict with some values
    @gen.coroutine
    def save_product():
        product = {'name':'cell phone', 'description':'black phone', 'price':10.5}
        # motor collection
        objectid = yield collection.insert(product)

    #read from motor's find_one method
    @gen.coroutine
    def find_product():
        product = yield collection.find_one({'_id': objectid})
        name = product['name']
        description = product['description']
        price = product['price']



There's no problem if you prefer to work like this, but you always have to use some kind of mapping
for any new added class and maintain your existing mapping when something changes.
If you really want to release yourself from boring task of accessing key/value
whenever you write code to read/write from/to database, we suggest you to work such as in the example below:

Write your entities::

    class ShippingOptions(Entity):
        name = Str()
        def __init__(self, name=""):
            self.name = name

    class Product(Entity):
        name = Str()
        description = Str()
        price = Float()
        shipping_options = List(ShippingOptions)

        def __init__(self, name="", description="", price=0.0):
            self.name = name
            self.description = description
            self.price = price

        def add_shipping_option(self, shipping_option):
            assert isinstance(shipping_option, Entity), "shipping_option is not an instance of Entity"
            self.shipping_options.append(shipping_option)





Create an instance of entity with some data and call EntityManager to save and find::

    @gen.coroutine
    def save_product():
        emanager = EntityManager(Product)
        product = Product('book', 'book of the year', 35.00)

        # adding shipping options
        product.add_shipping_option(ShippingOptions('option1'))
        product.add_shipping_option(ShippingOptions('option2'))
        product.add_shipping_option(ShippingOptions('option3'))

        object_id = yield self.emanager.save(product)

    @gen.coroutine
    def find_product():
        emanager = EntityManager(Product)
        saved_product = yield self.emanager.find_one(object_id)

        #read product attributes
        name = saved_product.name
        description = saved_product.description
        price = saved_product.price

        #read shipping options
        #it's just an example to show that pyenty maps results to object
        for option in saved.product.shipping_options:
            self.name = option.name




.. toctree::
   :maxdepth: 1

   installation
   requirements
   example
   releasenotes

