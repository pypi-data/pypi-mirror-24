Registryctl
###########

.. note:: WORK IN PROGRESS

Install
=======

Get `registryctl` from pip::

    pip install registryctl


Usage
=====

* Help::

    registryctl --help


* Catalog::

    registryctl catalog list
    registryctl catalog show REPOSITORY [TAG]
    registryctl catalog delete REPOSITORY TAG



Note: Delete images
====================

`registryctl catalog delete IMG TAG` does not actually remove physically the image/tag,
it removes the reference.

Please see https://docs.docker.com/registry/garbage-collection/


TODO
====

* Return error json responses
* Add unit tests
