from typing import Any, Union
from modutils.hashutils import sha256_pattern

class sha256:
    name = 'sha256'

    def __init__(self, value):
        value_str = str(value)
        self.__value__ = value_str if sha256_pattern.match(value_str) else None
        if not self.__value__:
            raise TypeError(f'{value!r} is not a valid sha256 type')

    def __str__(self):
        return self.__value__.lower()

    def __eq__(self, value):
        if self.__value__.lower() == sha256(value).__value__.lower():
            return True
        return False

def nget(d:dict, *args:Union[str, list]) -> Any:
    """nget - nested get call to easily retrieve nested information with a single call and set a default
    Ex.
        nget(dict, ['key1', 'key2', ..], default)
        nget(dict, key1, key2, .., default)

        nget use an iterable of keys to retrieve nested information and can set a default if a key is not found
    """

    if len(args) == 0:
        raise ValueError(f'At least 1 key is required. None given')

    keys = args[0] if (isinstance(args[0], list) or len(args) == 1) else args[:-1]
    default = args[-1] if len(args) > 1 else None

    if isinstance(d, dict):
        if isinstance(keys, str):
            keys = [keys]
        if isinstance(keys, (tuple, list)):
            for k in keys:
                d = d.get(k, default)
                if d == default:
                    return default
            if d:
                return d
        else:
            raise TypeError(f'Invalid type of iterable for keys: {type(keys)!r}. Must be tuple or list')
    else:
        raise TypeError(f'First argument must be of type dict, given was type: {type(d)!r}')

    return default
