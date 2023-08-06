=====================
 ``zope.ptresource``
=====================

.. image:: https://img.shields.io/pypi/v/zope.ptresource.svg
        :target: https://pypi.python.org/pypi/zope.ptresource/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.ptresource.svg
        :target: https://pypi.org/project/zope.ptresource/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.ptresource.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.ptresource

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.ptresource/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.ptresource?branch=master


.. note::

   This package is at present not reusable without depending on a large
   chunk of the Zope Toolkit and its assumptions. It is maintained by the
   `Zope Toolkit project <http://docs.zope.org/zopetoolkit/>`_.

This package provides a "page template" `resource class
<https://pypi.python.org/pypi/zope.browserresource>`_, a resource
whose content is processed with the `Zope Page Templates
<https://pypi.python.org/pypi/zope.pagetemplate>`_ engine before
being returned to client.

The resource factory class is registered for "pt", "zpt" and "html" file
extensions in the package's ``configure.zcml`` file.
