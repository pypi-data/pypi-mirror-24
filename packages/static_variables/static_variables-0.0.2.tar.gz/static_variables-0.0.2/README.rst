static\_variables
=================

Static variables for Python

    NOTE:

    This is still very much a work in progress, and will segfault if you
    give it anything that is mildly complex. It will probably not work
    on any implementation except CPython.

Usage
-----

``static``
~~~~~~~~~~

.. code:: python

    from static_variables import static, resolve_static
     
    # You don't really need to import `static`, it just stops
    # IDEs from complaining.
     
    @resolve_static
    def f(to_add=None):
         ls = static([])
         if to_add is not None:
             ls.append(to_add)
         return ls
     
    ls = f()
    f(3)
    assert ls == [3]  # True
    assert ls is f()

Since Python variables are more like name tags, ``static`` will only
really work well for mutable objects, like ``list``\ s or
``io.StringIO``\ s.

For example, the following does not work:

.. code:: python

    @resolve_static
    def f():
        counter = static(0)
        counter += 1
        return counter
     
    assert f() == 1  # True
    assert f() == 2  # False

The only way to do that would be to reimplement a CPython byte-code
interpreter in Python, and modify it to work.

The static variable will always have the same ``id``. It will refer to
the same object, and is stored at the end of a function's
``function.__code__.co_consts``

Empty set literals
~~~~~~~~~~~~~~~~~~

Since sets came after dictionaries, the ``{}`` literal is an empty
dictionary. This changes that.

.. code:: python

    @resolve_static(empty_set_literal=True)
    def f():
        return {}
     
    assert f() == set()  # True
    assert f() != {}  # True; {} is dict() in the outer scope.

You can also use ``EMPTY_SET`` to avoid turning all ``{}`` into empty
sets.

.. code:: python

    from static_variables import resolve_static, EMPTY_SET
     
    # Again, you don't need to import EMPTY_SET.
    # It just stops IDEs from complaining.
     
    @resolve_static(empty_set_literal=False)
    def f():
        my_dict = {}
        my_set = EMPTY_SET  # Equivalent to `set()` but faster.
        return type(my_dict), type(my_set)

    assert f() == (dict, set)  # True

Speed?
------

It would actually be faster to use ``static``, as it delegates some
processing to declaration time, instead of run time.

Take these two snippets:

.. code:: python

    def product_4(it):
        return itertools.product(it, repeat=4)
     
    @resolve_static
    def static_product_4(it):
        return static(itertools.product)(it, repeat=4)

And their disassembly:

::

    product_4(it)
                  0 LOAD_GLOBAL              0 (itertools)
                  2 LOAD_ATTR                1 (product)
                  4 LOAD_FAST                0 (it)
                  6 LOAD_CONST               1 (4)
                  8 LOAD_CONST               2 (('repeat',))
                 10 CALL_FUNCTION_KW         2
                 12 RETURN_VALUE

::

    static_product_4(it)
                  0 LOAD_CONST               3 (<class 'itertools.product'>)
                  2 LOAD_FAST                0 (it)
                  4 LOAD_CONST               1 (4)
                  6 LOAD_CONST               2 (('repeat',))
                  8 CALL_FUNCTION_KW         2
                 10 RETURN_VALUE

The static version just loads the ``itertools.product`` constant, whilst
the normal version looks up a global variable and an attribute on one.

Empty set literals and ``EMPTY_SET`` are equivalent and both faster than
``set()``.

They are not equivalent to ``static(set())`` which would be faster, but
it would be the same static set.

Installation
------------

From `PyPI <https://pypi.org/project/static_variables/>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ pip install static_variables

From source
~~~~~~~~~~~

.. code:: bash

    $ git clone 'https://github.com/MitalAshok/static_variables.git'
    $ python ./static_variables/setup.py install
