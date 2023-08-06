tmpld
=====

Jinja2 templating on steroids for docker containers.

.. image:: https://travis-ci.org/joeblackwaslike/tmpld.svg?branch=master
   :target: https://travis-ci.org/joeblackwaslike/tmpld
   :alt: Build Status

.. image:: https://img.shields.io/docker/pulls/joeblackwaslike/tmpld.svg
   :target: https://hub.docker.com/r/joeblackwaslike/tmpld/
   :alt: Docker Pulls

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/joeblackwaslike/tmpld
   :alt: Github Repo


CLI tool combining jinja2 with parsers and other objects including Kubernetes
API objects and linux capabilities objects.


Usage
-----
    ::

        usage: tmpld (sub-commands ...) [options ...] {arguments ...}

        Base Controller

        positional arguments:
          templates             template files to render

        optional arguments:
          -h, --help            show this help message and exit
          --debug               toggle debug output
          --quiet               suppress all output
          -d DATA, --data DATA  file(s) containing context data
          -s, --strict          Raise an exception if a variable is not defined
