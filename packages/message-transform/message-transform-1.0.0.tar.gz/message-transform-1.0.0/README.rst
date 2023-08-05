message-transform
=================

Fast, simple message transformations

Usage
=====

Usage::

  from message_transform import mtransform

  mtransform({'a':'b'},{'x':'y'}) => {'a':'b','x':'y'}
  mtransform({'a':'b'},{'x':'y','c':{'d':'e'}}) => {'a':'b','x':'y','c':{'d':'e'}}
  mtransform({'a':'b'},{'x':' specials/$message->{a}'}) => {'a':'b','x':'a'}

Contributing
============

Open up a pull request via https://github.com/dana/python-message-transform, please consider adding tests for any new functionality.  To set up the dev environment (assuming you're using [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper))::

  $ mkvirtualenv message-transform
  $ pip install -r dev-requirements.txt
  $ py.test

Description
===========

This is a very light-weight and fast library that does some basic but reasonably powerful message transformations.

Function
========

Function::
  mtransform(message,transform)

Takes two and only two arguments, both dictionaries, and mutates the message according to the transform.

Bugs
====

None known.

Copyright
=========

Copyright (c) 2012, 2013, 2016, 2017 Dana M. Diederich. All Rights Reserved.

Author
======

Dana M. Diederich diederich@gmail.com dana@realms.org

