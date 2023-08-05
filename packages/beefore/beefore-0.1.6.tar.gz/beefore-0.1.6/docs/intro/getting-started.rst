Getting Started
===============

In this guide we will walk you through setting up your Beefore environment
for development and testing. We will assume that you have a working Python
install, and an existing project.

Install Beefore
-----------------

The first step is to install Beefore. If you're using a virtual environment
for your project, don't forget to activate it.

.. code-block:: bash

    $ mkdir tutorial
    $ cd tutorial
    $ virtualenv -p $(which python3) env
    $ . env/bin/activate
    $ pip install beefore

Next Steps
----------

You now have a working Beefore environment, so you can :doc:`start the first
tutorial </tutorials/tutorial-0>`.
