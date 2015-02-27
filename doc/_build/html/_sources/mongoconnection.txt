.. pyenty documentation master file, created by
   sphinx-quickstart on Wed Feb 18 13:54:34 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MongoDB connection
====================================

Open connection to MongoDB is pretty simple and can be done using one of the below options.

With default localhost and port::

     EntitySession.open(db="db_name")

Setting up the localhost and port to EntityConnection::

     EntityConnection.open(host, port_number, db="db_name")




