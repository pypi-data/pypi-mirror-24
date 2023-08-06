struction
---------
Pythonic, C-Style structs.

Structs are similar to namedtuples, but they allow type assertion and are defined the same way as any class. Creating
a struct is easy.

``$ pip install struction``

.. code-block:: python

    from struction import Struct

    class MyStruct(Struct):
        # fieldName = type
        field_0 = int
        field_1 = str

        # you can also allow multiple types
        multi_type = [int, str]  # fieldName = [type0, type1, ...]

        # and default values!
        with_default = int, 10  # fieldName = type, default

        with_multi_and_default = [int, str], "hi"  # fieldName = [type0, type1, ...], default


Once a struct is created, it's fields can be changed, but they must match the given type or
a TypeError will be raised.

``del struct.field`` resets the field to ``None``.

It's also possible to nest structs.
Any structs that are nested will automatically be initialized.


.. code-block:: python

    class OnlyInt(Struct):
        field_0 = int
        field_1 = int


    class Nested(Struct):
        abc = str
        nest = OnlyInt  # nested struct


.. code-block:: python

    >>> print(Nested())
    # Nested {
    #     abc = None
    #     nest = OnlyInt {
    #         field_0 = None
    #         field_1 = None
    #     }
    # }

    >>> print(Nested(nest=None))
    # Nested {
    #     abc = None
    #     nest = None
    # }

If you don't want strict types, you can also use a ``TypecastingStruct``. This will attempt to typecast the given value
to the field's type. If it can't be typecasted, it will then raise a TypeError.

.. code-block:: python

    from struction import Struct

    class Test(TypecastingStruct):
        i = int
        f = float
        s = str
        all = [float, int, str]

.. code-block:: python

    >>> test = Test()
    >>> test.i = 5.3
    >>> test.f = 100
    >>> test.s = {"a": 1, "b":2}
    >>> print(test)
    # Struct Test {
    #     all = None
    #     f = 100.0
    #     i = 5
    #     s = "{'a': 1, 'b': 2}"
    # }
    >>> # If multiple types are allowed for a field, the value will be
    >>> # casted to the first type that doesn't throw an Exception
    >>> test.all = ("a", 1, "b", 2, "c", 3)
    >>> test.all
    # '("a", 1, "b", 2, "c", 3)'

**Note:** Typecasting only works at runtime. The values still need to match there types at class definition.

Reference
---------
These can be applied to any Struct class.

- ``Struct.dict()`` : dict with struct's fields. {name: value, ...}
- ``Struct.fields()`` : list of fields struct has.
