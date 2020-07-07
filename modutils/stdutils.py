import json
from sys import stdout
from typing import Any
from requests import Response
from colored import fg, style

from mdv.markdownviewer import main as mdv


class echo(object):
    """
    echo - a modern print statement that resolves objects to printable types
    """
    message: Any
    expand: bool = False
    list_delimiter: str = '\n'
    indent: int = 4
    color: str = None
    newline: bool = True
    markdown: bool = False

    def __init__(self, message: Any, expand:bool=False,
                 list_delimiter:str='\n', indent:int=4, color:str=None, newline:bool=True, markdown:bool=False):
        self.expand = expand
        self.list_delimiter = list_delimiter
        self.indent = indent
        self.color = color
        self.newline = newline
        self.markdown = markdown
        self._resolve(message)


    def _resolve_response_object(self, response: Response) -> str:
        """resolve requests.Response objects to an always printable form based on their status_code from response

        response {requests.Response} -- response object to resolve

        return {str} -- a printable form of the response
        """
        if response.status_code in [200, 201]:
            try:
                return json.dumps(response.json(), indent=4)
            except json.decoder.JSONDecodeError:
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

    def _resolve_class_object(self, cls: object):
        """resolve a class object to an always printable form based on the type of attributes.
        recursively resolves attributes

        cls {object} -- class object to print

        return {None} - does not return anything due to needing to call resolve
        """
        for attr in dir(cls):
            val = getattr(cls, attr)
            if not attr.startswith('__') and not attr.endswith('__'):
                self.newline = False
                self._resolve(attr + ' ')
                self.newline = True
                self._resolve(val)

    def _resolve(self, message:Any) -> None:
        """resolve and print a message based on Any given type

        message {Any} -- an object to print

        return {None} -- does not return anything, this function will write to stdout
        """
        if isinstance(message, str):
            msg = message
            if msg.startswith('#') and self.markdown:
                msg = mdv(md=msg)
        elif isinstance(message, (tuple, list)):
            msg = self.list_delimiter.join(message)
        elif isinstance(message, dict):
            msg = json.dumps(message, indent=self.indent)
        elif isinstance(message, Response):
            msg = self._resolve_response_object(message)
        elif str(type(message)).startswith('<class') and self.expand:
            return self._resolve_class_object(message)
        else:
            msg = str(message)

        if self.newline:
            msg += '\n'

        if self.color:
            msg = f'{fg(self.color)}{msg}{style.RESET}'

        stdout.write(msg)

    def __call__(self, message:Any=None):
        """__call__ can be used to overwrite the current message if you want to reuse an echo object

            x = echo('123')
            x()
            x('345')


        message {Any} -- object to print

        """
        if message:
            self._resolve(message)
        else:
            self._resolve('')
