static\_variables
=================

Static variables for Python

    NOTE:

    This is still very much a work in progress, and will segfault if you
    give it anything that is mildly complex. It will probably not work
    on any implementation except CPython.

Usage
-----

``static_variables``
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from static_variables import resolve_static
     
    @resolve_static(static_variables={'counter': 0})
    def f():
        counter += 1
        return counter
     
    print(f())  # 1
    print(f())  # 2
    print(f())  # 3

The signature for ``static_variables`` is ``Mapping[str, Any]``, where
the value is the initial value.

Also note that static variables will override global, nonlocal and local
variables with the same name.

Set the value to ``static_variables.NO_VALUE`` to have no value in the
beginning:

.. code:: python

    from static_variables import resolve_static, NO_VALUE
     
    @resolve_static(staic_variables={'value': NO_VALUE})
    def get_value():
        try:
            return value
        except NameError:
            value = could_be_anything()
            # Value could also be `None`, so `None`
            # is not a sensible default.
            return value
     
    get_value()  # Runs `could_be_anything`
    get_value()  # Returns static value

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
really work well for mutable objects, like ``list``\ s or ``set``\ s.

For example, the following does not work:

.. code:: python

    @resolve_static
    def f():
        counter = static(0)
        counter += 1
        return counter
     
    assert f() == 1  # True
    assert f() == 2  # False

You would have to use the ``static_variables`` argument to achieve this.

The static variable will always have the same ``id``. They will refer to
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

How does it work?
-----------------

``static_variables``
~~~~~~~~~~~~~~~~~~~~

This creates a new variable in the closure of a function. The closure
remains between function calls.

It replaces ``(LOAD|STORE|DELETE)_GLOBAL`` and
``(LOAD|STORE|DELETE)_FAST`` (local variables) opcodes in the bytecode
with ``(LOAD|STORE|DELETE)_DEREF`` (load from the closure) ones.

``static``
~~~~~~~~~~

The bytecode in Python is stack-based. ``resolve_static`` looks for a
``LOAD_GLOBAL 'static'`` opcode and then starts tracking what the size
of the stack will be. When the stack size reaches ``0`` and a
``CALL_FUNCTION 1`` (call the top of the stack with 1 item from below it
on the stack) opcode is reached, it extracts the bytecode, creates a new
function, and calls it to evaluate the bytecode. The whole
``static(...)`` is replaced with ``LOAD_CONST``, to load a constant
value which is appended to the code's ``co_consts``.

``empty_set_literal``
~~~~~~~~~~~~~~~~~~~~~

While iterating over the bytecode, if ``BUILD_MAP 0`` is encountered
(Create a new dictionary from the previous 0 items. i.e., an empty
dictionary), it is replaced with ``BUILD_SET 0``, which creates an empty
set instead. This opcode still exists even though it doesn't naturally
occur so that it's argument still correlates with the number of items to
pop off of the stack to build the set with.

If a ``LOAD_GLOBAL 'EMPTY_SET'`` is encountered, it is always replaced
with a ``BUILD_SET 0`` (i.e., a new empty set.)
