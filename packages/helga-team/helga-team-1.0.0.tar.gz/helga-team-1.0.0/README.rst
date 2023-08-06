helga-team
==============

.. image:: https://badge.fury.io/py/helga-team.png
    :target: https://badge.fury.io/py/helga-team

.. image:: https://travis-ci.org/narfman0/helga-team.png?branch=master
    :target: https://travis-ci.org/narfman0/helga-team

Team plugin to track candidates and interview process

Installation
------------

Install via pip::

    pip install helga-team

And add to settings!

Usage
-----

    !team help

Team uses argparse for most things. The available arguments are::

    '-i', '--id'
    '-n', '--name'
    '-s', '--status', default='pending'
    '-o', '--owner'
    '-r', '--recruiter'
    '-c', '--code_review'

Here is an example adding a candidate, updating some attributes, and
requesting status::

    !team add -i 1 -n "Calvin Candidaton"
    !team update -i 1 -o "Eric Employerson"
    !team update -i 1 -r "Roger Recruitenbridge"
    !team update -i 1 -s "Phone Screen 1/1"
    !team status -i 1
    helga> "Calvin Candidaton, owner: Eric Employerson, recruiter: Roger
    Recruitenbridge, status: Phone Screen 1/1, id: 1"

Update only updates a single candidate. Status can return many candidates,
using the arguments as filters. e.g.::

    !team add -i 1 -n "Calvin Candidaton" -o "Jon R"
    !team add -i 1 -n "Roger Recruitenbridge" -o "Jon R"
    !team status -o "Jon R"
    helga> Calvin Candidaton...
    helga> Roger Recruitenbridge...

TODO
----

* Add a "notes" table where anyone can write down their thoughts on a candidate
* Add a "review" table where anyone can rate the candidate after different
  stages in the interview process

Development
-----------

Install all the testing requirements::

    pip install -r requirements_test.txt

Run tox to ensure everything works::

    make test

You may also invoke `tox` directly if you wish.

Release
-------

To publish your plugin to pypi, sdist and wheels are (registered,) created and
uploaded with::

    make release

License
-------

Copyright (c) 2017 Jon Robison

See LICENSE for details
