pygnusocial
===========

|Build Status| |PyPI| |Docs|

Installation
------------

``pip install gnusocial``

or

``python3 setup.py install``

You can also install ``python-gnusocial`` package from `AUR <https://aur.archlinux.org/>`_.

Documentation
-------------

Documentation is hosted at https://pygnusocial.readthedocs.io/en/latest/


Basic usage
-----------


::

>>> from gnusocial import statuses
>>> r = statuses.update('https://gnusocial.server.com', data={'status':"I've just installed #pygnusocial!", 'source':'python3'}, auth=('username', 'password'))


If you want to help with the development of pygnusocial, check out the `contribution guide <https://source.heropunch.io/dtluna/pygnusocial/blob/master/CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://source.heropunch.io/dtluna/pygnusocial/badges/develop/build.svg
   :target: https://source.heropunch.io/dtluna/pygnusocial/commits/develop
   :alt: Build Status

.. |PyPI| image:: https://img.shields.io/pypi/v/gnusocial.svg
   :target: https://pypi.python.org/pypi/gnusocial/
   :alt: Latest Version

.. |Docs| image:: https://readthedocs.org/projects/pygnusocial/badge/?version=latest
   :target: https://pygnusocial.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
