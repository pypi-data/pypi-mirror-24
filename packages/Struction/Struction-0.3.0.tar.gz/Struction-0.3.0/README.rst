struction
---------
Pythonic, yet C-Style structs/unions.

Structs are similar to namedtuples, but they allow type assertion and are defined the same way as any class. Creating
a struct is easy.

``$ pip install struction``

.. code-block:: python

    from struction import Struct, default, between, clamp

    class MyStruct(Struct):
        # any types specified *must* be a class/type
        field_0 = int
        field_1 = str

        # you can also allow multiple types
        multi_type = int, str

        # and default values!
        with_default = int, default(10)

        with_multi_and_default = int, str, default(10)

        # it's also possible to set a specific range for fields
        with_range = int, float, between(1, 10)  # setting this to a value < 1 or > 10 will raise ValueError

        # or, values can be clamped to a range
        with_clamp = int, float, clamp(-5, 5)  # setting this to any value outside of range will clamp it


Once a struct is created, it's fields can be changed, but they must match the given type or
a TypeError will be raised. Using ``del`` on a field resets it to its default value.

It's also possible to nest structs.
Any structs that are nested will automatically be initialized.


.. code-block:: python

    class NestMe(Struct):
        field_0 = int
        field_1 = int


    class Nester(Struct):
        abc = str
        nest = OnlyInt  # nested struct


.. code-block:: python

    >>> print(Nester())
    # Nester {
    #     abc = None
    #     nest = OnlyInt {
    #         field_0 = None
    #         field_1 = None
    #     }
    # }

    >>> print(Nester(nest=None))
    # Nester {
    #     abc = None
    #     nest = None
    # }

If you don't want strict types, you can also use a ``TypecastingStruct``. This will attempt to typecast the given value
to the field's type. If it can't be typecasted, it will then raise a TypeError.

.. code-block:: python

    from struction import TypecastingStruct

    class Test(TypecastingStruct):
        i = int
        f = float
        s = str
        all = float, int, str

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

**Note:** Typecasting only works at runtime. The values still need to match their types at class definition.

Reference
---------
These can be applied to any Struct class.

- ``Struct.dict()`` : dict with struct's fields. {name: value, ...}
- ``Struct.fields()`` : list of fields struct has.
- ``str(Struct)`` : Multi-line representation of struct.
- ``repr(Struct)`` : Single line representation of struct.
