SoonTM

Restcord
========

|PyPI| |PyPI|

Restcord is a rest API wrapper for the Discord API, but this one doesn’t
include WebSockets, this is for people who dont want websockets but only
make requests to the api.

Breaking Changes
~~~~~~~~~~~~~~~~

The discord API is constantly changing and the wrapper API is as well.

Installing
----------

To install the library, you can just run the following command:

::

    pip install -U restcord

Please note that on Linux installing voice you must install the
following packages via your favourite package manager (e.g. ``apt``,
``yum``, etc) before running the above command:

-  python-dev (e.g. ``python3.5-dev`` for Python 3.5)

Quick Example
-------------

.. code:: py

    import restcord

Requirements
------------

-  Python 3.4.2+ (There will be no effort to add support for lower
   versions)
-  ``aiohttp`` library

Usually ``pip`` will handle these for you.

Related Projects
----------------

-  `discord.py`_

.. _discord.py: https://github.com/rapptz/discord.py

.. |PyPI| image:: https://img.shields.io/pypi/v/restcord.svg
   :target: https://pypi.python.org/pypi/restcord/
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/restcord.svg
   :target: https://pypi.python.org/pypi/restcord/