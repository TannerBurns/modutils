from typing import Any, Union, Tuple
from re import compile, Pattern
from hashlib import sha256
from time import sleep
from json import dumps
from json.decoder import JSONDecodeError
from requests import Response
from colored import fg, style
from subprocess import Popen, PIPE

from modutils.aio import aioloop
from modutils.http import BaseSession

'''
##################################################################
Type Helpers
Utils to help with new types
##################################################################
'''


sha256_pattern: Pattern = compile('[A-Fa-f0-9]{64}')  # non case sensitive matching, can return non unique

class sha256:
    name = 'sha256'

    def __init__(self, value):
        """convert a valid sha256 string to object

        :param value: value to convert to sha256 object
        """
        value_str = str(value)
        self.__value__ = value_str if sha256_pattern.match(value_str) else None
        if not self.__value__:
            raise TypeError(f'{value!r} is not a valid sha256 type')

    def __str__(self):
        """print sha256 object as lowercase"""
        return self.__value__.lower()

    def __eq__(self, value):
        """compare sha256 objects, convert to lower so that upper case is equal to lower case"""
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

'''
##################################################################
Print Helpers
Utils to help with printing objects
##################################################################
'''


def response_to_str(response: Response) -> str:
    """
    response_to_str - convert Response object to string and interpret status codes
    :param response: Response object to convert to string
    :return: string of Response object
    """
    if response.status_code in [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]:
        try:
            return dumps(response.json(), indent=4)
        except JSONDecodeError:
            return response.text
    elif response.status_code in [401, 403]:
        return f'({response.status_code}) Invalid permissions for requests: {response.url}'
    elif response.status_code == 404:
        return f'({response.status_code}) Unable to find requested resource for: {response.url}'
    elif response.status_code == 400:
        return f'({response.status_code}) Bad request to: {response.url}'
    elif response.status_code >= 500:
        return f'({response.status_code}) Server error - {response.url} - {response.status_code} - {response.text}'
    elif response.status_code == None:
        return f'({response.status_code}) Server error - {response.url} - {response.text}'
    return f'({response.status_code}) {response.text}'


def echo(content: Any, list_delimiter: str = '\n', indent: int = 4, color: str = None, flush: bool = False) -> None:
    """echo - automatically pretty print or resolve to a printable object

    :param content: the object to print
    :param list_delimiter: delimiter to join list; default: \n
    :param indent: indent space count; default: 4
    :param color: change color of text; default: None
    :param flush: flush will make the current line be overwritten; default: False
    :return: None
    """
    if isinstance(content, (tuple, list)):
        content = list_delimiter.join(map(str, content))
    elif isinstance(content, dict):
        content = dumps(content, indent=indent)
    elif isinstance(content, Response):
        content = response_to_str(content)

    if not isinstance(content, str):
        content = str(content)

    if color:
        content = f'{fg(color)}{content}{style.RESET}'

    if flush:
        print(f'{content}', end='\r', flush=flush)
    else:
        print(content)

def scroll(content: list, sleep_timer=1, list_delimiter: str = '\n', indent: int = 4, color: str = None) -> None:
    """ use echo and a delay to scroll text over same line

    :param content: the object to print
    :param list_delimiter: delimiter to join list; default: \n
    :param indent: indent space count; default: 4
    :param color: change color of text; default: None
    :return: None
    """
    for item in content:
        echo(item, flush=True, list_delimiter=list_delimiter, indent=indent, color=color)
        sleep(sleep_timer)


'''
##################################################################
Package Helpers
Utils to help with installing, listing, and checking packages
inside a python script
##################################################################
'''


def install_package(name: str, force: bool = False, extra_index: str = None,
                    trusted_host: str = None) -> Tuple[str, str]:
    """install a pip3 package using a subprocess in current environment

    name {str} -- name of package to install
    force {bool} -- force newest edition
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    """
    cmd = ['pip3', 'install', name]
    if extra_index:
        cmd.extend(['--extra-index-url', extra_index])
    if trusted_host:
        cmd.extend(['--trusted-host', trusted_host])
    if force:
        cmd.append('--upgrade')

    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    return out.decode('utf-8'), err.decode('utf-8')


def update_package(name: str, extra_index: str = None, trusted_host: str = None) -> Tuple[str, str]:
    """update a pip3 package by name, leverages install_package with force = True

    name {str} -- name of package to install
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    """
    return install_package(name, force=True, extra_index=extra_index, trusted_host=trusted_host)


def list_packages() -> list:
    """list current pip3 packages in environment

    return {list} -- a list of available packages
    """
    cmd = ['pip3', 'freeze']
    out, _ = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
    return [pkg for pkg in out.decode('utf-8').replace('\r', '').split('\n') if pkg]


def has_package(name: str, version: Union[str, int, float] = None) -> bool:
    """check if current environment has a package

    name {str} -- name of package to check
    version {Union[str, int, float]} -- OPTIONAL, will append version for a specific version check of package

    return {bool} -- True if package was found and False if not
    """
    pkg = f'{name}=={version}' if version else name
    return any(pkg in pp for pp in list_packages())

'''
##################################################################
Import Helpers
Utils to help with importing packages inside a python script
##################################################################
'''


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
