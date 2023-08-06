"""
Things to check:
1. Check whether validation for all the arguments of a function are specified
2. Validate datatype of each of the arguments passed
3. validate data type of the keyword argument if present
"""

import inspect
import six
from functools import wraps


class InvalidInput(Exception):
    message = 'Invalid input'


DATATYPES = {
    'int': lambda x: isinstance(x, six.integer_types),
    'float': lambda x: isinstance(x, float),
    'str': lambda x: isinstance(x, six.string_types),
    'dict': lambda x: isinstance(x, dict),
    'list': lambda x: isinstance(x, list),
    'tuple': lambda x: isinstance(x, tuple)
}


def check_args(**ch_kwargs):
    def decorate(func):
        o = inspect.getargspec(func)
        v_args = o.args

        for ch in ch_kwargs.values():
            if ch not in DATATYPES:
                raise InvalidInput('Incorrect chk args passed %s %s' % (ch, DATATYPES.values()))

        @wraps(func)
        def dec(*arg, **kwargs):
            for i, v_arg in enumerate(v_args):
                if v_arg not in ch_kwargs:
                    raise InvalidInput(
                        "Specifying data types of all the argument is mandatory missing - %s passed - %s", v_arg, ch_kwargs
                    )

                fn = DATATYPES[ch_kwargs[v_arg]]

                if v_arg in kwargs:
                    a = kwargs[v_arg]
                else:
                    a = arg[i]

                if not fn(a):
                    raise InvalidInput('Input data should be valid %s %s' % (v_arg, a))

            return func(*arg, **kwargs)

        return dec

    return decorate
