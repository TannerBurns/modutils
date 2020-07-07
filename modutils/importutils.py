from typing import Union

def globpath(filepath: str) -> str:
    """convert a filepath to a glob path, ['/'|'\'] to '.'

    filepath {str} -- filepath to glob

    return {str} -- new globpath
    """
    glob = filepath.replace('/', '.').replace('\\', '.')
    while glob[0] == '.':
        glob = glob[1:]
    return glob

def import_from(globpath: str, name: str) -> Union[object, None]:
    """Import module and return instance of given function name

    globpath {str} -- the filepath in glob format
    name {str} -- the method name to import

    return {Union[object, None]} -- method attribute of import
    """
    module = __import__(globpath, fromlist=[name])
    return getattr(module, name) if hasattr(module, name) else None