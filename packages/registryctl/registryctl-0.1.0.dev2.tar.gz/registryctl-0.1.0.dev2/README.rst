Registryctl
###########

Install
=======

.. code-block:: shell

    pip install registryctl


Usage
=====

* Help

    .. code-block:: shell

        registryctl --help



Note: Delete images
====================

`registryctl catalog delete IMG TAG` does not actually remove physically the image/tag,
it removes the reference.

Please see https://docs.docker.com/registry/garbage-collection/
