CAPPY |PyPI|
============

CAchingProxyinPython is a file based python proxy based on Sharebear's
`simple python caching
proxy <http://sharebear.co.uk/blog/2009/09/17/very-simple-python-caching-proxy/>`__.

Install
-------

``pip install cappy``

Usage
-----

``cappy run``

Options
~~~~~~~

-  ``--port`` - optional (default: 3030)
-  ``--cache_dir`` - optional (default: Temporary platform specific
   folder)
-  ``--cache_timeout`` - optional (default: 864000 seconds, use 0 for
   caching indefinitely)
-  ``--cache_compress`` - optional (default: False) Compress and store
   the cache

.. |PyPI| image:: https://img.shields.io/pypi/v/cappy.svg?maxAge=2592000?style=plastic
   :target: https://pypi.python.org/pypi/cappy/
