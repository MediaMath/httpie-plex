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

If you've installed HTTPie using Homebrew, but it's pointing to your system Python,
there may be other hoops to jump through. Note that this doesn't apply if you've
also installed Python via Homebrew: essentially, if ``pip list`` lists ``httpie``,
you're good to go with the method above. Otherwise, you'll need to manually
install it into the proper directory. First, clone the repository.
You'll then need to figure out which version of HTTPie you have installed.
Then do something like:

.. code-block:: bash

    $ PYTHONPATH="/usr/local/Cellar/httpie/0.9.8/libexec/lib/python2.7/site-packages:/usr/local/Cellar/httpie/0.9.8/libexec/vendor/lib/python2.7/site-packages" \
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
This defaults to, on \*nix machines, ``~/.httpie/plex``. You can set a different base directory by setting the ``HTTPIE_CONFIG_DIR`` environment variable.

Testing and Contributing
------------------------

Tests are run with

.. code-block:: bash

	$ python setup.py test

Contributions are welcome! For new features, tests are a requirement and should
have good coverage. For bug fixes/improvements, tests must pass. Further, code
must be style-checked with `pycodestyle <https://github.com/PyCQA/pycodestyle>`_.
