pagure-dist-git
===============

.. split here

Since 3.0 pagure offers a way to customize the creation and compilation the of
the gitolite configuration file.

This project hosts the logic to generate gitolite's configuration file for
dist-git which has a different access model than regular projects on pagure (for
example, forced pushed is forbidden).

Tests
=====

The tests here require the *test suite* of pagure itself to work.  You have to
modify your PYTHONPATH to find them. Run with::

    $ PYTHONPATH=.:/path/to/pagure/checkout nosetests dist_git_auth_tests.py
