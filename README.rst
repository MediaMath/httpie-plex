======================
httpie-plex
======================

Bid Opportuinty Firehose OAuth2 Plugin for
`HTTPie <https://github.com/jkbr/httpie>`_.

Installation
------------

.. code-block:: bash

    $ pip install httpie-plex

You should now see ``plex`` under ``--auth-type`` in ``$ http --help`` output.

Homebrew
~~~~~~~~

If you've installed HTTPie using Homebrew, there are some other hoops to jump through.
You'll first need to figure out which version of HTTPie you have installed.
Then do something like:

.. code-block:: bash

    $ PYTHONPATH="/usr/local/Cellar/httpie/0.9.8/libexec/lib/python2.7/site-packages:/usr/local/Cellar/httpie/0.9.3/libexec/vendor/lib/python2.7/site-packages" \
        python setup.py install \
            --prefix=/usr/local/Cellar/httpie/0.9.8/libexec/vendor

Usage
-----

.. code-block:: bash

    $ http --auth-type=plex \
        --auth='client_id:client_secret' \
        https://apibase.com/consumers

Token Storage
-------------

To cache the OAuth2 token, this package uses a folder ``plex`` inside the `HTTPie config directory <https://httpie.org/doc#config>`_.
This defaults to, on \*NIX machines, ``~/.httpie/plex``. You can set a different base directory by setting the ``HTTPIE_CONFIG_DIR`` environment variable.
