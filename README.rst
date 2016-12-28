paka.funcreg
============
.. image:: https://travis-ci.org/PavloKapyshin/paka.funcreg.svg?branch=master
    :target: https://travis-ci.org/PavloKapyshin/paka.funcreg


Migration from older versions of this library
---------------------------------------------
There are two deprecated versions of this library (funcreg from orico-libs,
and libreg). Though internally they differ from ``paka.funcreg``, migration
is just a matter of changing imports and registry factories:

1. Imports like

   .. code-block:: python

       import libreg

   or

   .. code-block:: python

       import funcreg

   become

   .. code-block:: python

       import paka.funcreg

2. Calls like

   .. code-block:: python

       libreg.make()

   or

   .. code-block:: python

       funcreg.make()

   become

   .. code-block:: python

       paka.funcreg.NameRegistry()

3. Calls like

   .. code-block:: python

       libreg.make_type_dispatcher()

   become

   .. code-block:: python

       paka.funcreg.TypeRegistry()
