========================
~~ Better Contextvars ~~
========================

.. image:: https://img.shields.io/badge/Python-3.5%20|%203.6%20|%203.7-blue.svg
    :target: https://www.python.org

.. image:: https://travis-ci.com/itsVale/better-contextvars.svg?branch=master
    :target: https://travis-ci.com/itsVale/better-contextvars

.. image:: https://api.codacy.com/project/badge/Grade/0a4eb517bdcd4618947bfa56e73e1282
    :target: https://www.codacy.com/app/itsVale/better-contextvars?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=itsVale/better-contextvars&amp;utm_campaign=Badge_Grade

.. image:: https://api.codacy.com/project/badge/Coverage/0a4eb517bdcd4618947bfa56e73e1282
    :target: https://www.codacy.com/app/itsVale/better-contextvars?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=itsVale/better-contextvars&amp;utm_campaign=Badge_Coverage

.. image:: https://api.codeclimate.com/v1/badges/20552710af9220ac17c2/maintainability
   :target: https://codeclimate.com/github/itsVale/better-contextvars/maintainability

.. image:: https://img.shields.io/github/issues/itsVale/better-contextvars.svg
    :target: https://GitHub.com/itsVale/better-contextvars/issues

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: http://perso.crans.org/besson/LICENSE.html

About this project
##################

This project implements a backport of the `PEP 567 contextvars <https://www.python.org/dev/peps/pep-0567>`_ module from Python 3.7 for Python 3.5+.
It is a full implementation of the original contextvars module with the same features.

Installation
############

Installation is very easy. Either install it from PyPI or directly from GitHub:

.. code-block::

    $ pip3 install -U better-contextvars
    $ pip3 install -U git+https://github.com/itsVale/better-contextvars#better-contextvars

    $ git clone https://github.com/itsVale/better-contextvars
    $ python3 setup.py install

Documentation
#############

As stated above, this is an exact representation of the original contextvars module.
Because of that, it is totally fine to use the `official documentation for contextvars <https://docs.python.org/3/library/contextvars.html>`_.

`PEP 567 <https://www.python.org/dev/peps/pep-0567>`_ provides a comprehensive overview of the API.

Usage
#####

You use it the same way as the original module.

.. code-block:: python

    import better_contextvars as contextvars

    var = contextvars.ContextVar('test')
    ...

For more usage examples, have a look at tests_.

.. _tests: https://github.com/itsVale/better-contextvars/tree/master/tests

Contributing
############

If you decide to contribute, please always lint your code. The preferred linter is `pylama <https://github.com/klen/pylama>`_.