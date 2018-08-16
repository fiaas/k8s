Gotchas
=======

Strings as alternate type
-------------------------

In order to stay compatible with Python 2 and 3, we use `six` in a few places, most notably when setting types of string fields. We use `six.text_type` in these cases. Fields can have a primary type, and an alternate type.

This gotcha is usually encountered when you have a Python 2 code base, and have a field with string as the secondary type, such as this::

    class RollingUpdateDeployment(Model):
        maxUnavailable = Field(int, alt_type=six.text_type)
        maxSurge = Field(int, alt_type=six.text_type)

Under the hood, `six.text_type` resolves to `unicode` in Python 2, which means you need to be careful about which type of string you are using in your code. If you try the following code in Python 2, it will crash with a `ValueError`. In Python 3 it will work as expected::

    RollingUpdateDeployment(maxSurge="25%")

The reason for this is that the code checks if the value is of either the primary type or the alternate type, and if that is not the case, it is converted into the primary type using the type constructor.

If your string is of type `str`, it will not be `int` and not be `unicode`, so it will be coerced to `int` using `int(value)`. If your string contains anything other than numbers, this won't work.

The solution is to always be aware of which kind of strings you have. You should use `unicode` when setting fields on k8s models, as that is the type used internally.

In Python 3 this problem goes away, because unless you are doing strange things, all your strings are going to be of the type `str`, which is what `six.text_type` resolves to in Python 3.
