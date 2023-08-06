proxy-manager
=============

This module loads and returns proxies for easy use with ``requests``.

Installation
------------

This module is available via pip:

::

    $ pip install proxymngr

Basic Usage
-----------

``proxies.txt``:

::

    00.11.222.33:4444
    55.66.777.88:9999:username:password

``test.py``:

.. code:: py

    from proxymngr import ProxyManager

    proxy_manager = ProxyManager('proxies.txt')

    random_proxy = proxy_manager.random_proxy()
    print(random_proxy) # { 'http':'http://...', 'https':'https://...' }

    first_proxy = proxy_manager.next_proxy()
    print(first_proxy) # { 'http':'http://00.11.222.33:4444', 'https':'https://00.11.222.33:4444' }
    second_proxy = proxy_manager.next_proxy()
    print(second_proxy) # { 'http':'http://username:password@55.66.777.88:9999', 'https':'https://username:password@55.66.777.88:9999' }
    third_proxy = proxy_manager.next_proxy()
    print(third_proxy) # { 'http':'http://00.11.222.33:4444', 'https':'https://00.11.222.33:4444' }

Documentation
-------------

Proxy File Format
~~~~~~~~~~~~~~~~~

Proxies in proxy files must have one of the following formats:

``ip:port``

or

``ip:port:username:password``

These can be combined and alternated.

``ProxyManager``
~~~~~~~~~~~~~~~~

``ProxyManager(proxy_file_path)``

Returns a new ``ProxyManager`` instance given the path to a proxy file.

Parameters
^^^^^^^^^^

1. ``string`` - File path to the proxy

Returns
^^^^^^^

``ProxyManager`` - ProxyManager with proxies loaded

Example
^^^^^^^

.. code:: py

    from proxymngr import ProxyManager

    proxy_manager = ProxyManager('proxies.txt')

``ProxyManager.random_proxy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ProxyManager.random_proxy()``

Returns a random proxy of those loaded into the proxy manager

Parameters
^^^^^^^^^^

none

Returns
^^^^^^^

``dict`` - Proxy as a dict in the form
``{ 'http':'http://...', 'https':'https://...' }``

Example
^^^^^^^

.. code:: py

    random_proxy = proxy_manager.random_proxy()
    print(random_proxy) # { 'http':'http://...', 'https':'https://...' }

``ProxyManager.next_proxy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ProxyManager.next_proxy()``

Returns proxies consecutively. Thread-safe. Loops continuously through
available proxies, with wrapping.

Parameters
^^^^^^^^^^

none

Returns
^^^^^^^

``dict`` - Proxy as a dict in the form
``{ 'http':'http://...', 'https':'https://...' }``

Example
^^^^^^^

.. code:: py

    first_proxy = proxy_manager.next_proxy()
    print(first_proxy) # { 'http':'http://00.11.222.33:4444', 'https':'https://00.11.222.33:4444' }
