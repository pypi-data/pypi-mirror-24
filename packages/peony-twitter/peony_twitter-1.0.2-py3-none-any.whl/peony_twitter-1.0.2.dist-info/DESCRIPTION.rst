Asynchronous Twitter API client for Python 3.5+
===============================================


.. image:: https://travis-ci.org/odrling/peony-twitter.svg?branch=master
  :target: https://travis-ci.org/odrling/peony-twitter

.. image:: https://codecov.io/gh/odrling/peony-twitter/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/odrling/peony-twitter



Installation
------------

To install this module simply run::

    pip install peony-twitter[all]

This will install all the modules required to make peony run out of the box.
You might feel like some of them are not fit for your needs.
Check `Advanced installation`_ for more information about how to install only
the modules you will need.

.. _Advanced installation: https://peony-twitter.readthedocs.io/en/latest/adv_usage/install.html#adv-install

Authorize your client
---------------------

You can use ``peony.oauth_dance`` to authorize your client:

.. code-block:: python

    >>> from peony.oauth_dance import oauth_dance
    >>> tokens = oauth_dance(YOUR_CONSUMER_KEY, YOUR_CONSUMER_SECRET)
    >>> from peony import PeonyClient
    >>> client = PeonyClient(**tokens)

This should open a browser to get a pin to authorize your application.


Getting started
---------------

You can easily create a client using the class ``PeonyClient``.
Make sure to get your api keys and access tokens from
`Twitter's application management page`_ and/or to `Authorize your client`_

.. code-block:: python

    import asyncio

    # NOTE: the package name is peony and not peony-twitter
    from peony import PeonyClient

    loop = asyncio.get_event_loop()

    # create the client using your api keys
    client = PeonyClient(consumer_key=YOUR_CONSUMER_KEY,
                         consumer_secret=YOUR_CONSUMER_SECRET,
                         access_token=YOUR_ACCESS_TOKEN,
                         access_token_secret=YOUR_ACCESS_TOKEN_SECRET)

    # this is a coroutine
    req = client.api.statuses.update.post(status="I'm using Peony!!")

    # run the coroutine
    loop.run_until_complete(req)

.. _Twitter's application management page: https://apps.twitter.com

.. _Authorize your client: #authorize-your-client

Tests
-----

To run the tests run:

.. code-block:: bash

    make install  # install the required dependencies
    make test

You can also use tox to run the tests, a configuration file is provided:

.. code-block:: bash

    tox

Documentation
-------------

Read `Peony's documentation`_.

.. _Peony's documentation: https://peony-twitter.readthedocs.io

Contributing
------------

Every kind of contribution is appreciated.

If you find a bug please start an issue and if you're very motivated you can
create a pull request.

If you have a suggestion you can also start an issue and create a pull
request if you managed to make it work.


