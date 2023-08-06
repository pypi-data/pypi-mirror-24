Restcord
========

|PyPI| |PyPI2| |Discord|

Restcord is a rest API wrapper for the Discord API, but this one does not
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
    import asyncio

    loop = asyncio.get_event_loop()
    client = restcord.Restcord(token="Your token here")

    async def test():
        guild = await client.get_guild("Some guild id of a guild that ur bot/user account is in")
        print(guild.__dict__)

    loop.run_until_complete(test())

For user accounts:
~~~~~~~~~~~~~~~~~~

.. code:: py

    import restcord
    import asyncio

    loop = asyncio.get_event_loop()
    client = restcord.Restcord(token="Your token here", selfbot=True)

    async def test():
        guild = await client.get_guild("Some guild id of a guild that ur bot/user account is in")
        print(guild.__dict__)

    loop.run_until_complete(test())

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
.. |PyPI2| image:: https://img.shields.io/pypi/pyversions/restcord.svg
   :target: https://pypi.python.org/pypi/restcord/
.. |Discord| image:: https://img.shields.io/discord/351376159302483968.svg
   :target: https://discord.gg/mV5j7su