import os
from distutils.core import setup

version = 'v0.1.3'

setup(
    name="entmapper",
    packages=['entmapper'],
    version=version,
    keywords=["mongo", "mongodb", "entity", "motor", "tornado"],
    description="An simple object-document mapping for mongodb-motor and tornado applications.",
    author="Leonardo Souza",
    author_email="leo.desouza@gmail.com",
    url="https://github.com/leodesouza/entity",
    download_url="https://github.com/leodesouza/entity/tree/v0.1.0-beta",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
)
