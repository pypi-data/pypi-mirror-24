Contributing to Beefore
=========================


If you experience problems with Beefore, `log them on GitHub`_. If you want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/beefore/issues
.. _fork the code: https://github.com/pybee/beefore
.. _submit a pull request: https://github.com/pybee/beefore/pulls


Setting up your development environment
---------------------------------------

The recommended way of setting up your development envrionment for Beefore
is to install a virtual environment, install the required dependencies and
start coding. Assuming that you are using ``virtualenvwrapper``, you only have
to run::

    $ git clone git@github.com:pybee/beefore.git
    $ cd beefore
    $ mkvirtualenv beefore

Beefore uses ``unittest`` (or ``unittest2`` for Python < 2.7) for its own test
suite as well as additional helper modules for testing. To install all the
requirements for Beefore, you have to run the following commands within your
virutal envrionment::

    $ pip install -e .

Now you are ready to start hacking! Have fun!
