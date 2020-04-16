#####################
Starlette-OpenTracing
#####################

|Maintenance yes| |PyPI pyversions| |Build info|

`OpenTracing`_ support for Starlette and FastApi. Inspired by: `Flask-OpenTracing`_
OpenTracing implementations exist for major distributed tracing systems and can be bound or swapped with a one-line
configuration change. This package uses the `OpenTracing API for Python`_ to implement it's functionality.

WORK IN PROGRESS. Not ready for production!

The package will implement: Starlette middleware that can be used to add Opentracing support to all incoming requests.
It also support the usage of a customer root span by looking at extra headers for incoming request.

This work was funded by `SURFnet`_.

.. _OpenTracing: http://opentracing.io/
.. _OpenTracing API for Python: https://github.com/opentracing/opentracing-python
.. _Flask-OpenTracing: https://github.com/opentracing-contrib/python-flask
.. _SURFnet: https://www.surf.nl/en
.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/acidjunk/starlette-opentracing/graphs/commit-activity
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/Starlette-Opentracing.svg
   :target: https://pypi.python.org/pypi/Starlette-Opentracing/
.. |Build info| image:: https://travis-ci.com/acidjunk/starlette-opentracing.svg?branch=master
    :target: https://travis-ci.com/acidjunk/starlette-opentracing


Installation
============

Run the following command:

.. code-block::

    $ pip install Starlette-Opentracing

Usage
=====

See the examples for FastAPI and Starlette in `examples/`

Deploy
======

Increase version in VERSION

.. code-block::

    git commit -a -m "bumped version to 0.0.3"
    git tag -a v0.0.3 -m "version 0.0.3"
    git push --follow-tags

License info
============

Copyright 2020 R. Dohmen <acidjunk@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
