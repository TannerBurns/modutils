# Modutils

    Modern python3 utilities
    A collection of classes and functions
<br>
    
[ Skip to docs ](#docs)

    
# Most common utilities

### aioloop
    
This function provides an easy way to use another defined function to provide async functionality. 
Named arguments should be provided in a single dictionary inside the list of arguments.
    
```python
import requests
from modutils import aioloop

# example w/o named arguments
def add(x:int,y:int)->int:return x+y

args = [[x,y] for x in range(0,5) for y in range(5,10)]
list_of_returns = aioloop(add, args)


# example w/ named arguments
def get_url(url, params:dict=None):
    return requests.get(url, params=params)

args = [
        ['https://www.google.com', {'params':{'q':'Why is the sky blue?'}}],
        ['https://www.github.com']
    ]
list_of_returns = aioloop(get_url, args)
```
<br> 

### aiobulk

aiobulk is a decorator used to add a bulk attribute to the existing function. This decorator leverages aioloop for async functionality.
    
```python
import requests
from modutils.decorators import aiobulk

# example w/o named arguments
@aiobulk
def add(x:int,y:int)->int:return x+y

args = [[x,y] for x in range(0,5) for y in range(5,10)]
list_of_returns = add.bulk(args)


# example w/ named arguments
@aiobulk
def get_url(url, params:dict=None):
    return requests.get(url, params=params)

args = [
        ['https://www.google.com', {'params':{'q':'Why is the sky blue?'}}],
        ['https://www.github.com']
    ]
list_of_returns = get_url.bulk(args)
```
<br>

### BaseSession

This class is a modified requests session class that enables logging per request and will persistently attempt to resolve requests with incorrect status codes.

```python
from modutils.http import BaseSession
```
<br>
    
### BaseAsyncSession

This class is built with BaseSession and aiobulk to provide a bulk attribute for each request functions: get, put, post, patch, head, and delete

```python
from modutils.http import BaseAsyncSession
session = BaseAsyncSession()
args = [
        ['https://www.google.com', {'params':{'q':'Why is the sky blue?'}}],
        ['https://www.github.com']
    ]
list_of_returns = session.get.bulk(args)
```
<br>

### Email

The Email class allows a simple way to send emails via an non-authenticated or authenticated session

```python
from modutils.http import Email
```
<br>

### Urlscraper

The urlscraper method is an easy way to search web pages for matching content of a given pattern

```python
from modutils.http import urlscraper
# this example will use a regex pattern to find all the sha256 hashes in a given blog
# note: the blog is fake and will need to be replaced for example
sha256hashes = urlscraper('https://fakeblogsite.com', '[A-Fa-f0-9]{64}', regex=True)
```


### echo

echo is a fancy print that allows you to easily print objects in their prettiest form, add color, and flush the current line.

```python
from modutils import echo
echo({'hello': 'world'}, color='red')
```
 <br>
 
<a name="docs"></a>
# Documentation 

- [ modutils.aio ](#modutils.aio_5229308776497159722)
	- [ aioloop ](#aioloop_8885906970529181510)
- [ modutils.decorators ](#modutils.decorators_980589605870121525)
	- [ aiobulk.\_\_init\_\_ ](#aiobulk.__init___1815237342438632813)
	- [ aiobulk.bulk ](#aiobulk.bulk_2652515655308176417)
- [ modutils.http ](#modutils.http_6860961663441781746)
    - [ urlscraper ](#urlscraper_5869860748378830970)
	- [ modutils.http.BaseAsyncSession ](#modutils.http.BaseAsyncSession_7048839415358285160)
		- [ BaseAsyncSession.\_\_init\_\_ ](#BaseAsyncSession.__init___2624241592854672828)
	- [ modutils.http.BaseSession ](#modutils.http.BaseSession_7129533737347880003)
		- [ BaseSession.\_\_init\_\_ ](#BaseSession.__init___284116210118425907)
	- [ modutils.http.Email ](#modutils.http.Email_6219263455091284767)
		- [ Email.\_\_init\_\_ ](#Email.__init___5909366176742243457)
		- [ Email.send ](#Email.send_1264049943792425762)
- [ modutils ](#modutils_8302506306604331608)
	- [ echo ](#echo_6254100437156621322)
	- [ globpath ](#globpath_8277747260912108967)
	- [ has_package ](#has_package_799630035152214553)
	- [ import_from ](#import_from_7798535269709248701)
	- [ install_package ](#install_package_7206308496330428784)
	- [ list_packages ](#list_packages_1639171450864803932)
	- [ nget ](#nget_5476107451956719196)
	- [ response_to_str ](#response_to_str_3575013933436391480)
	- [ scroll ](#scroll_1683689735572407726)
	- [ update_package ](#update_package_8893359438089742518)
	- [ modutils.sha256 ](#modutils.sha256_6761098578614895022)


<a name="modutils.aio_5229308776497159722"></a>
## modutils.aio

modutils.aio defines a new type called Eventloop. This type is created at runtime to specify the type by operating system.

<a name="aioloop_8885906970529181510"></a>
#### `aioloop(function: Callable, args_list: List[List], loop: Eventloop = None, max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False, progress_bar_color: str = 'green_3a', progress_bar_format: str = None) -> list`

create new aioloop, run, and return results

    :param fn {Callable}: function to map to arguments
    :param args_list {List[List]}: list of arguments to send to function
    :param loop {Eventloop}: a pre-defined asyncio loop
    :param max_async_pool {int}: max async pool, this will define the number of processes to run at once
    :param max_futures {int}: max futures, this will define the number of processes to setup and execute at once.
        If there is a lot of arguments and futures is very large, can cause memory issues.
    :param disable_progress_bar {bool}: disable progress bar from printing
    :param progress_bar_color {str}: color of progress bar; default: green
    :param progress_bar_format {str}: format for progress bar output; default: None


    :return list of results
    
<a name="modutils.decorators_980589605870121525"></a>
## modutils.decorators
    
<a name="aiobulk.__init___1815237342438632813"></a>
#### `aiobulk.__init__(self, function: Callable)`


initialize aiobulk
        the function being decorated will receive a new attribute for the bulk call

        :param function: function being decorated
        

<a name="aiobulk.bulk_2652515655308176417"></a>
#### `aiobulk.bulk(self, args_list: List[list], loop: <function NewType.<locals>.new_type at 0x0000021B97E921F0> = None, max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False, progress_bar_color: str = 'green_3a', progress_bar_format: str = None) -> list`

add a method called 'bulk' to given function

            :param function {Callable}: function to map to arguments
            :param loop {Eventloop}: a pre-defined asyncio loop
            :param max_async_pool {int}: max async pool, this will define the number of processes to run at once
            :param max_futures {int}: max futures, this will define the number of processes to setup and execute at once.
                If there is a lot of arguments and futures is very large, can cause memory issues.
            :param disable_progress_bar {bool}: disable progress bar from printing
            :param progress_bar_color {str}: color of progress bar; default: green
            :param progress_bar_format {str}: format for progress bar output; default: None

            :return list of results
        

<a name="modutils.http_6860961663441781746"></a>
## modutils.http

<a name="urlscraper_5869860748378830970"></a>
#### `urlscraper(url: str, pattern: str, regex: bool = False) -> list`

urlscraper is a simple method to scrape information from a url based on a given string pattern

    :param url: the url to run pattern against
    :param pattern: the string representation of the pattern
    :param regex: flag for using a pattern as regex or string compare

    :return: list of strings that matched or contained pattern

<a name="modutils.http.BaseAsyncSession_7048839415358285160"></a>
### modutils.http.BaseAsyncSession(self, *args, **kwargs)

BaseAsyncSession to be used for sessions that need to be able to make asynchronous requests

<a name="BaseAsyncSession.__init___2624241592854672828"></a>
#### `BaseAsyncSession.__init__(self, *args, **kwargs)`

initialize BaseAsyncSession

        :param args: list of args
        :param kwargs: dict of named args
        

<a name="modutils.http.BaseSession_7129533737347880003"></a>
### modutils.http.BaseSession(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16, resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None)

BaseSession that will log requests and persist requests to attempt to resolve desired status codes

<a name="BaseSession.__init___284116210118425907"></a>
#### `BaseSession.__init__(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16, resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None)`

initialize BaseSession

        :param max_retries: maximum amount of retries if non resolved status code found
        :param pool_connections: number of pool connection; default 16
        :param pool_maxsize: max number of connections in pool; default 16
        :param resolve_status_codes: extra status codes to resolve; default None
        :param verbose: more verbose logging output if response fails; default False
        :param auth: basic auth username and password tuple; default None        
        

<a name="modutils.http.Email_6219263455091284767"></a>
### modutils.http.Email(self, smtp_server, smtp_port, from_address: str = None, authentication_required: bool = False, auth_username: str = None, auth_password: str = None)

Class to easily send emails

<a name="Email.__init___5909366176742243457"></a>
#### `Email.__init__(self, smtp_server, smtp_port, from_address: str = None, authentication_required: bool = False, auth_username: str = None, auth_password: str = None)`

Create a new email session

<a name="Email.send_1264049943792425762"></a>
#### `Email.send(self, subject: str, body: str, to_address_list: list, cc_address_list: list = None, from_address: str = None, encoding: str = 'html', logo_images: list = None, file_attachments: list = None) -> dict`


        :param subject: Subject string for email, required
        :param body: Message content for email, required
        :param to_address_list: addresses to send email to, required
        :param cc_address_list: addresses to cc on email, default: None
        :param from_address: address to send email from, default: None, will use self.from_address if one was given
        :param encoding: encoding for body, default: html
        :param logo_images: list of paths to images to use for logos, default: None
        :param file_attachments: list of paths to attachments for email, default: None

        :return: dict

<a name="modutils_8302506306604331608"></a>
## modutils

<a name="echo_6254100437156621322"></a>
#### `echo(content: Any, list_delimiter: str = '\n', indent: int = 4, color: str = None, flush: bool = False) -> None`

echo - automatically pretty print or resolve to a printable object

    :param content: the object to print
    :param list_delimiter: delimiter to join list; default: 

    :param indent: indent space count; default: 4
    :param color: change color of text; default: None
    :param flush: flush will make the current line be overwritten; default: False
    :return: None
    

<a name="globpath_8277747260912108967"></a>
#### `globpath(filepath: str) -> str`

convert a filepath to a glob path, ['/'|''] to '.'

    filepath {str} -- filepath to glob

    return {str} -- new globpath
    

<a name="has_package_799630035152214553"></a>
#### `has_package(name: str, version: Union[str, int, float] = None) -> bool`

check if current environment has a package

    name {str} -- name of package to check
    version {Union[str, int, float]} -- OPTIONAL, will append version for a specific version check of package

    return {bool} -- True if package was found and False if not
    

<a name="import_from_7798535269709248701"></a>
#### `import_from(globpath: str, name: str) -> Union[object, NoneType]`

Import module and return instance of given function name

    globpath {str} -- the filepath in glob format
    name {str} -- the method name to import

    return {Union[object, None]} -- method attribute of import
    

<a name="install_package_7206308496330428784"></a>
#### `install_package(name: str, force: bool = False, extra_index: str = None, trusted_host: str = None) -> Tuple[str, str]`

install a pip3 package using a subprocess in current environment

    name {str} -- name of package to install
    force {bool} -- force newest edition
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    

<a name="list_packages_1639171450864803932"></a>
#### `list_packages() -> list`

list current pip3 packages in environment

    return {list} -- a list of available packages
    

<a name="nget_5476107451956719196"></a>
#### `nget(d: dict, *args: Union[str, list]) -> Any`

nget - nested get call to easily retrieve nested information with a single call and set a default
    Ex.
        nget(dict, ['key1', 'key2', ..], default)
        nget(dict, key1, key2, .., default)

        nget use an iterable of keys to retrieve nested information and can set a default if a key is not found
    


<a name="modutils.stdutils_1737493875"></a>
## modutils.stdutils

<a name="scroll_1683689735572407726"></a>
#### `scroll(content: list, sleep_timer=1, list_delimiter: str = '\n', indent: int = 4, color: str = None) -> None`

use echo and a delay to scroll text over same line

    :param content: the object to print
    :param list_delimiter: delimiter to join list; default: 

    :param indent: indent space count; default: 4
    :param color: change color of text; default: None
    :return: None
    

<a name="update_package_8893359438089742518"></a>
#### `update_package(name: str, extra_index: str = None, trusted_host: str = None) -> Tuple[str, str]`

update a pip3 package by name, leverages install_package with force = True

    name {str} -- name of package to install
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    

<a name="modutils.sha256_6761098578614895022"></a>
### modutils.sha256(self, value)

sha256 type