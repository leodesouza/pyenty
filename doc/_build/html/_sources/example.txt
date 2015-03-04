.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


A Tornado App Example Using PyEnty
==================================

Here's a simple example of how to create a tornado application with pyenty ::

    from tornado.gen import coroutine
    import tornado.httpserver
    import tornado.ioloop
    import tornado.web

    from pyenty import EntityConnection, EntityManager
    from pyenty.types import Entity, Str, List


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
        emanager = None

        @coroutine
        def post(self):
            self.emanager = EntityManager(entity=User)
            name = self.get_argument('name')
            last_name = self.get_argument('last_name')

            # add user
            user = User(name, last_name)
            user.add_profile(Profile('guest'))
            object_id = yield self.emanager.save(user)


        @coroutine
        def get(self):
            emanager = EntityManager(User)
            user = yield emanager.find()


    EntityConnection.open(db="ym_db_test")
    if __name__ == "__main__":

        app = tornado.web.Application(
            [(r'/user', UserHandler), ],
            autoreload=True
        )

        app.listen(8889)
        tornado.ioloop.IOLoop.instance().start()
