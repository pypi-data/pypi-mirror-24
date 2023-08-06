struction
---------
Pythonic, C-Style structs.

Structs are similar to namedtuples, but they allow type assertion and are defined the same way as any class. Creating
a struct is easy.

``$ pip install struction``

.. code-block:: python

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

- ``Struct.dict()`` : dict with struct's fields. {name: value, ...}
- ``Struct.fields`` : list of fields struct has.
