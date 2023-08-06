Advanced serialization library for Python 2.7+
##############################################

Tickle is a library that allows one to serialize more advanced types, such as lambdas,
modules and builtins. It mirrors the ``pickle`` module with more advanced features.

It is coded entirely in Python, and as such, is completely portable and does not require
external C compilation.

.. contents::

.. section-numbering::

Features
========

- Backwards compatible with ``pickle``
- Serialize lambdas
- Serialize module objects
- Serialize builtins

Installation
============

Simply install using ``pip``:

.. code-block:: bash

    $ pip install --upgrade tickle


(If ``pip`` installation fails for some reason, you can try
``easy_install tickle`` as a fallback.)

Python version
--------------

An up-to-date Python 2.x distribution is recommended. Development has been done
and tested on Python 2.7, specifically 2.7.13.

Requirements
------------

No other packages are required for this project to run.

Unstable version
----------------

You can also instead of the latest the latest unreleased development version
directly from the ``develop`` branch on Bitbucket.

It is a work-in-progress of a future stable release so the experience
might be not as smooth.

With ``pip``:

.. code-block:: bash

    $ pip install --upgrade 'https://bitbucket.org/overridelogic/tickle/get/develop.tar.gz'


Reference
=========

Usage
-----

Usage is pretty similar to the ``pickle`` module:

.. code-block:: python

    import tickle

    value = 42
    func = lambda x: value + x

    serialized = tickle.dumps(func)
    deserialized = tickle.loads(serialized)

    assert deserialized(10) == 52

Limitations
-----------

Due to the nature of how Python handles closures, there are some limitations to the library.
First and foremost, deserialized objects are copies of the original objects, which means that:


.. code-block:: python

    import tickle
    
    class MyObject(object):
        def __eq__(self):
            return self.__class__.__name__ == other.__class__.__name__ and \
                self.__dict__ == other.__dict__
        
    inst = MyObject()
    func = lambda: inst
     
    serialized = tickle.dumps(func)
    deserialized = tickle.loads(serialized)
    
    assert func() is inst                        # works
    assert isinstance(deserialized(), MyObject)  # works
    assert deserialized() is inst                # fails

...the ``inst`` object is serialized into the scope of the serialized object with its
state saved at the time of serialization. The deserializer creates a copy of the original
object. They are equal, but they are not the same object.

Extending
---------

With support from both ``pickle`` and ``tickle``, there will rarely be a need to extend
this library.

However, if it is required, one can extend the ``Ticklable`` class and register a custom
type for dispatch:

.. code-block:: python

    import tickle

    class MyClass(object):
        pass

    class MyClassTicklable(tickle.Ticklable):
        def __getstate__(self):
            """returns the number of time the object has been serialized"""
            try:
                return self.data.count
            except AttributeError:
                return 0

        def __setstate__(self, data):
            """increase the counter by one at each deserialization"""
            self.data = MyClass()
            self.data.count = data + 1

    # register the handler for this type
    tickle.dispatch[MyClass] = MyClassTicklable

    inst = MyClass()

    serialized = tickle.dumps(inst)
    inst = tickle.loads(serialized)
    assert inst.count == 1

    serialized = tickle.dumps(inst)
    inst = tickle.loads(serialized)
    assert inst.count == 2

How it works:

- the ``__getstate__`` method has access to the ``self.data`` attribute, which contains
  the object to be serialized. It produces data relevant to deserialization.
- the ``_setstate__`` method accepts the ``data`` argument, which is the output the of
  ``__getstate__`` call. It sets the ``self.data`` attribute to the resulting object.

Contributing
============

Contributions are always welcome. If you want to contribute:

- Fork the project
- Test your code (see below)
- Push your code
- Submit a pull request

Testing
-------

Contributions must pass both the tests and styling guidelines. Before submitting a patch,
make sure you run:

.. code-block:: bash

    $ ./setup.py flake8
    $ ./setup.py test

About the project
=================

Change log
----------

See `CHANGELOG <https://bitbucket.org/overridelogic/tickle/raw/master/CHANGELOG.rst>`_.

Licence
-------

MIT License: see `LICENSE <https://bitbucket.org/overridelogic/tickle/raw/master/LICENSE>`_.

Authors
-------

**Francis Lacroix** `@francislacroix` created ``tickle`` while at **OverrideLogic**.
