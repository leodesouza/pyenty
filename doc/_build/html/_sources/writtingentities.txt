.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Writting your entities
======================
The task of defining entities is pretty simple as well and you won't find trouble to accomplish.
PyEnty accepts anything which inherits from its base class - Entity

Example::

    class Profile(Entity):
        name = Str()

        def __init__(self, name):
            self.name = name



.. toctree::
   :maxdepth: 3


   supportedtypes
   tutorial
   releasenotes

