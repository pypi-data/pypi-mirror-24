message-match
=============

Fast, simple message matching

Usage
=====

Usage::

  from message_match import mmatch

  mmatch({'a':'b'},{'a':'b'}) == True
  mmatch({'a':'b','c':'d'},{'a':'b'}) == True
  mmatch({'a':'b'},{'c':'d'}) == False
  mmatch({'a':'b', 'c':'d'},{'a':'b', 'c':'d'}) == True
  mmatch({'x':{'y':'z'}},{'x':{'y':'z'}}) == True
  mmatch({'a':'b', 'x':{'y':'z'}},{'x':{'y':'z'}}) == True
  mmatch({'a':'b', 'x':{'y':'z'}},{'a':'b', 'x':{'y':'z'}}) == True
  mmatch({'a': [1,2,3]},{'a':2}) == True  #TODO
  mmatch({'a': [1,2,3]},{'a':5}) == True  #TODO
  mmatch({'a': [1,2,3]},{'a': [1,2,3]}) == True   #TODO
  mmatch({'a': [{'a':'b'},2,3]},{'a': [{'a':'b'},2,3]}) == True   #TODO
  mmatch({'a':'forefoot'},{'a':' special/foo/'})== True   #TODO
  mmatch({'a':'forefoot'},{'a':' special/smurf/'}) == False   #TODO
  mmatch({'a':'forefoot'},{'a':' special/FOO/'})== False  #TODO
  mmatch({'a':'forefoot'},{'a':' special/FOO/i'})== True  #TODO
  mmatch({'a':'b'},{}) == True
  mmatch({},{}) == True
  mmatch({'a':{'b':'c'}},{'a':{}}) == True
  mmatch({'a':{'b':'c'}}, {'a':{}, 'x':'y'}) == False
  mmatch({'a':{'b':'c'}},{}) == True
  mmatch({'a':''},{'a':''}) == True
  mmatch({'a':''},{'a':0}) == False
  mmatch({'a':'forefoot'},{'a':' specialhuhFOO/i'}) == False

Contributing
============

Open up a pull request via https://github.com/dana/python-message-match, please consider adding tests for any new functionality.  To set up the dev environment (assuming you're using [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper))::

  $ mkvirtualenv message-match
  $ pip install -r dev-requirements.txt
  $ py.test

Description
===========

This is a very light-weight and fast library that does some basic but reasonably powerful message matching.

Function
========

Function::
  mmatch(message,match)

Takes two and only two arguments, both dictionaries, and returns a boolean.

Bugs
====

None known.

Copyright
=========

Copyright (c) 2012, 2013, 2016, 2017 Dana M. Diederich. All Rights Reserved.

Author
======

Dana M. Diederich diederich@gmail.com dana@realms.org

