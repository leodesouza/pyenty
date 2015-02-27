.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorial
====================================

MongoDB connection
---------------------

To open connection to MongoDB is pretty simple.::

    from pyenty import EntityConnection
    EntityConnection.open(db="pyenty_db")

Below a example of tornado's server script::

    from tornado.gen import coroutine
    import tornado.httpserver
    import tornado.ioloop
    import tornado.web

    from pyenty import EntityConnection, EntityManager
    from pyenty.types import Entity, Str, List

Writing your classes
---------------------::

    class Profile(Entity):
        name = Str()

        def __init__(self, name):
            self.name = name


    class User(Entity):
        name = Str()
        last_name = Str()
        profile = List(Profile)

        def __init__(self, name='', last_name=''):
            self.name = name
            self.last_name = last_name

        def add_profile(self, profile):
            self.profile.append(profile)


    class UserHandler(tornado.web.RequestHandler):
        def data_received(self, chunk):
            pass

        @coroutine
        def post(self):
            emanager = EntityManager(entity=User)
            name = self.get_argument('name')
            last_name = self.get_argument('last_name')

            # add user
            user = User(name, last_name)
            user.add_profile(Profile('guest'))
            yield emanager.save(user)

        @coroutine
        def get(self):
            emanager = EntityManager(User)
            yield emanager.find()

    EntityConnection.open(db="pyenty_db")

    if __name__ == "__main__":

        app = tornado.web.Application(
            [(r'/user', UserHandler), ],
            autoreload=True
        )

        app.listen(8884)
        tornado.ioloop.IOLoop.instance().start()



25/Fev - 2015
~~~~~~~~~~~~~


tutorial

.. toctree::
   :maxdepth: 3

   installation
   tutorial
   releasenotes
