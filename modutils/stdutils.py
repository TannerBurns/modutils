from time import sleep
from json import dumps
from json.decoder import JSONDecodeError
from typing import Any
from requests import Response
from colored import fg, style

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
    for item in content:
        echo(item, flush=True, list_delimiter=list_delimiter, indent=indent, color=color)
        sleep(sleep_timer)
