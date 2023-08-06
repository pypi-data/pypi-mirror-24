===============================
yunpian
===============================

.. image:: https://img.shields.io/pypi/v/yunpian.svg
        :target: https://pypi.python.org/pypi/yunpian

.. image:: https://img.shields.io/travis/mozillazg/yunpian.svg
        :target: https://travis-ci.org/mozillazg/yunpian

.. image:: https://img.shields.io/coveralls/mozillazg/yunpian/master.svg
        :target: https://coveralls.io/r/mozillazg/yunpian

.. image:: https://readthedocs.org/projects/yunpian/badge/?version=latest
        :target: https://readthedocs.org/projects/yunpian/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/dm/yunpian.svg
        :target: https://pypi.python.org/pypi/yunpian

.. image:: https://badges.gitter.im/mozillazg/yunpian.svg
        :alt: Join the chat at https://gitter.im/mozillazg/yunpian
        :target: https://gitter.im/mozillazg/yunpian



An async yunpian API library for Python

* Free software: MIT license
* Documentation: https://yunpian.readthedocs.org
* GitHub: https://github.com/mozillazg/yunpian
* PyPI: https://pypi.python.org/pypi/yunpian
* Python version: 3.5, 3.6

Features
--------

* TODO

Installation
--------------

At the command line::

    $ pip install yunpian

Usage
--------

::

    import aiohttp
    from yunpian import SMSClient
    from yunpian.contrib.aiohttp import Aiohttp

    async with aiohttp.ClientSession() as session:
        c = SMSClient(Aiohttp(session), 'api_key')
        response = await c.single_send('134xxx', '【测试网】您的验证码是 12432')

    print(response)
    print(response.json())

Credits
---------

This package was created with Cookiecutter_ and the `mozillazg/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`mozillazg/cookiecutter-pypackage`: https://github.com/mozillazg/cookiecutter-pypackage
