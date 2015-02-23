import os
from distutils.core import setup

version = '0.1.1'

setup(
    name="pyenty",
    packages=['pyenty'],
    version=version,
    keywords=["mongo", "mongodb", "entity", "motor", "tornado"],
    description="An simple object-document mapping for mongodb-motor and tornado applications.",
    author="Leonardo Souza",
    author_email="leo.desouza@gmail.com",
    url="https://github.com/leodesouza/entity",
    download_url="https://github.com/leodesouza/pyenty/tree/v0.1.1",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
)
