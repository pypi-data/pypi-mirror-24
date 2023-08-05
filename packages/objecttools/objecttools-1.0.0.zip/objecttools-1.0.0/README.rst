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

ObjectProxy
-----------

Create a weak-referenceable proxy to an object that supports the same
operations:

.. code:: python

    from objecttools import ObjectProxy
     
    ls = [1, 2, 3]
    proxy = ObjectProxy(ls)
     
    proxy.append(4)
    proxy += [5, 6]
    proxy[2:4] = [7, 8, 9]
    print(ls)  # [1, 2, 7, 8, 9, 5, 6]

serializable
------------

Create serializable forms of objects (For pickling)

.. code:: python

    from objecttools import SerializableFunction, SerializableConstant
    import pickle
     
    file = open('file.txt', 'w')
     
    f = lambda file, a: file.write(a)
     
    try:
        # Cannot pickle files, even though it is a global constant
        gile = pickle.loads(pickle.dumps(file))
    except TypeError:
        gile = pickle.loads(pickle.dumps(SerializableConstant('file', __name__)))
     
    try:
        # Cannot pickle functions if they are lambdas
        # Or are inner functions
        # Or are deleted after creation
        # Or are methods
        g = pickle.loads(pickle.dumps(f))
    except pickle.PicklingError:
        g = pickle.loads(pickle.dumps(SerializableFunction(f)))
     
    g(gile, 'data')  # Works

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
