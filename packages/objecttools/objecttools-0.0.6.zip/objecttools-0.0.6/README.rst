objecttools
===========

Various tools for working with objects and classes in Python

Cached properties
-----------------

Works just like a normal property, but returned values are cached:

.. code:: python

    from objecttools import CachedProperty

    class ExpensiveOperations(object):
        @CachedProperty
        def expensive_attribute(self):
            return self.calculate()
        
        # To make it settable
        
        @expensive_attribute.setter
        def expensive_attribute(self, value):
            pass
        
        # To make it deletable
        
        @expensive_attribute.deleter
        def expensive_attribute(self):
            pass

    e = ExpensiveOperations()
    e.other_attribute = 1
    print(e.expensive_attribute)  # Takes a long time.
    print(e.expensive_attribute)  # Very quick; just retrieve from cache
    v = e.expensive_attribute

    e.other_attribute = 2  # expensive_attribute should be different now!
    print(e.expensive_attribute)  # Old value that is wrong.
    del e.expensive_attribute
    print(e.expensive_attribute)  # Takes a long time, but returns new value.
    e.other_attribute = 1
    # Reset to known value
    e.expensive_attribute = v
    print(e.expensive_attribute)  # Correct value!

Singletons
----------

.. code:: python

    from objecttools import Singleton

    Sentinel = Singleton.create('Sentinel')

    Sentinel() is Sentinel()  # True

    d.get('missing_value', Sentinel()) is Sentinel()  # True

    class GlobalState(dict, metaclass=Singleton):
        attr = 0


    gs = GlobalState()
    gs['value'] = 7
    gs.attr = 1

    print(GlobalState()['value'] + GlobalState().attr)  # 8

For Python 2 and 3 compatibility, use it as a decorator:

.. code:: python

    @Singleton.as_decorator
    class Class(object):
        pass

Installing
----------

From `PyPI <https://pypi.org/project/objecttools/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install objecttools

From source
~~~~~~~~~~~

.. code:: bash

    $ git clone 'https://github.com/MitalAshok/objecttools.git'
    $ python ./objecttools/setup.py install
