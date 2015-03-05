from distutils.core import setup

version = '0.1.4'

setup(
    name="pyenty",
    packages=['pyenty'],
    version=version,
    keywords=["mongo", "mongodb", "entity", "motor", "tornado"],
    description="An simple object-document mapping for mongodb-motor and tornado applications.",
    author="Leonardo Souza",
    author_email="leo.desouza@gmail.com",
    url="https://github.com/leodesouza/pyenty",
    download_url="https://github.com/leodesouza/pyenty/tree/v0.1.4-beta",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
)
