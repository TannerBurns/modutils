# Modutils

    A library with modern utilities to assist development efficiency 
    
# Documentation
- [ modutils.aioutils ](#modutils.aioutils_3117516967911913793)
	- [ aiobulk ](#aiobulk_3900877271683308502)
	- [ aioloop ](#aioloop_5183290130458578128)
- [ modutils.hashutils ](#modutils.hashutils_9099713)
	- [ calc_sha256_from_dir ](#calc_sha256_from_dir_1893375329)
	- [ calc_sha256_from_dir_map ](#calc_sha256_from_dir_map_1000019374)
	- [ sha256_from_dir ](#sha256_from_dir_1523514038)
	- [ sha256_from_dir_map ](#sha256_from_dir_map_1310874601)
	- [ sha256_from_file ](#sha256_from_file_136289233)
- [ modutils.importutils ](#modutils.importutils_1652321527)
	- [ globpath ](#globpath_346197787)
	- [ import_from ](#import_from_679080163)
- [ modutils.packageutils ](#modutils.packageutils_2091287763)
	- [ has_package ](#has_package_1270361615)
	- [ install_package ](#install_package_1298376952)
	- [ list_packages ](#list_packages_1777836065)
	- [ update_package ](#update_package_1100192072)
- [ modutils.sessionutils ](#modutils.sessionutils_5867312898996405855)
	- [ modutils.sessionutils.BaseSession ](#modutils.sessionutils.BaseSession_2677308962921948920)
		- [ BaseSession.__init__ ](#BaseSession.__init___4074244197413366741)
		- [ BaseSession._log_response ](#BaseSession._log_response_1975778443043522547)
		- [ BaseSession._resolver ](#BaseSession._resolver_8386464650303821733)
		- [ BaseSession.delete ](#BaseSession.delete_6360896686043141700)
		- [ BaseSession.get ](#BaseSession.get_4801989696975619918)
		- [ BaseSession.head ](#BaseSession.head_232502297474810491)
		- [ BaseSession.patch ](#BaseSession.patch_999451590068817040)
		- [ BaseSession.post ](#BaseSession.post_794375458216340934)
		- [ BaseSession.put ](#BaseSession.put_7202945418070415894)
	- [ modutils.sessionutils.EmailSession ](#modutils.sessionutils.EmailSession_3898108880321399818)
		- [ EmailSession.__enter__ ](#EmailSession.__enter___4680498672731444297)
		- [ EmailSession.__exit__ ](#EmailSession.__exit___8091060023295603066)
		- [ EmailSession.__init__ ](#EmailSession.__init___7015344739597253847)
		- [ EmailSession.send ](#EmailSession.send_1351989794129380348)
- [ modutils.stdutils ](#modutils.stdutils_1737493875)
	- [ modutils.stdutils.echo ](#modutils.stdutils.echo_362805693)
		- [ echo.__call__ ](#echo.__call___318159007)
		- [ echo.__init__ ](#echo.__init___1476576396)
		- [ echo._resolve ](#echo._resolve_1902868456)
		- [ echo._resolve_class_object ](#echo._resolve_class_object_1121738252)
		- [ echo._resolve_response_object ](#echo._resolve_response_object_1840220819)
- [ modutils.typeutils ](#modutils.typeutils_135504944)
	- [ nget ](#nget_42222092)
	- [ modutils.typeutils.sha256 ](#modutils.typeutils.sha256_1273030348)

<a name="modutils.aioutils_3117516967911913793"></a>
## modutils.aioutils

<a name="aiobulk_3900877271683308502"></a>
#### `aiobulk(function, loop: Eventloop = None, max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False, progress_bar_color: str = 'green_3a', progress_bar_format: str = None)`

add a method called 'bulk' to given function

        :param function {Callable}: function to map to arguments
        :param loop {Eventloop}: a pre-defined asyncio loop
        :param max_async_pool {int}: max async pool, this will define the number of processes to run at once
        :param max_futures {int}: max futures, this will define the number of processes to setup and execute at once.
            If there is a lot of arguments and futures is very large, can cause memory issues.
        :param disable_progress_bar {bool}: disable progress bar from printing
        :param progress_bar_color {str}: color of progress bar; default: green
        :param progress_bar_format {str}: format for progress bar output; default: None

        Examples:
            @aiobulk
            def add(x:int,y:int)->int:return x+y


            # call the original function
            add.add(1,2)

            # call the newly added bulk function
            args = [[x,y] for x in range(0,5) for y in range(5,10)]
            list_of_returns = add.bulk(args)


            @aiobulk
            def get_url(url, params:dict=None):
                return requests.get(url, params=params)

            args = [
                ['https://www.google.com', {'params':{'q':'Why is the sky blue?'}}]
            ]
            responses = get_url.bulk(args)


        :return list of results
    

<a name="aioloop_5183290130458578128"></a>
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

<a name="modutils.hashutils_9099713"></a>
## modutils.hashutils

<a name="calc_sha256_from_dir_1893375329"></a>
#### `calc_sha256_from_dir(directory: str) -> list`

calculate sha256 values from files found in a directory

    directory {str} -- path to directory to search

    return {list} -- list of sha256 values found
    

<a name="calc_sha256_from_dir_map_1000019374"></a>
#### `calc_sha256_from_dir_map(directory: str) -> dict`

calculate sha256 values from files found in a directory and map them to their filepath

    directory {str} -- path to directory to search

    return {dict} -- dictionary with filepath as key and sha256 as value
    

<a name="sha256_from_dir_1523514038"></a>
#### `sha256_from_dir(directory: str) -> list`

extract all sha256 values from all files inside of a directory using regex

    directory {str} -- path to directory to search

    return {list} -- list of sha256 values found
    

<a name="sha256_from_dir_map_1310874601"></a>
#### `sha256_from_dir_map(directory: str) -> dict`

extract all sha256 values from all files inside of a directory using regex and map them to their filepath

    directory {str} -- path to directory to search

    return {dict} -- dictionary of filepath as key and found sha256 list as value
    

<a name="sha256_from_file_136289233"></a>
#### `sha256_from_file(filepath: str) -> list`

extract all sha256 values from a file using regex

    filepath {str} -- path to file to search

    return {list} -- list of sha256 values found
    

<a name="modutils.importutils_1652321527"></a>
## modutils.importutils

<a name="globpath_346197787"></a>
#### `globpath(filepath: str) -> str`

convert a filepath to a glob path, ['/'|''] to '.'

    filepath {str} -- filepath to glob

    return {str} -- new globpath
    

<a name="import_from_679080163"></a>
#### `import_from(globpath: str, name: str) -> Union[object, NoneType]`

Import module and return instance of given function name

    globpath {str} -- the filepath in glob format
    name {str} -- the method name to import

    return {Union[object, None]} -- method attribute of import
    

<a name="modutils.packageutils_2091287763"></a>
## modutils.packageutils

<a name="has_package_1270361615"></a>
#### `has_package(name: str, version: Union[str, int, float] = None) -> bool`

check if current environment has a package

    name {str} -- name of package to check
    version {Union[str, int, float]} -- OPTIONAL, will append version for a specific version check of package

    return {bool} -- True if package was found and False if not
    

<a name="install_package_1298376952"></a>
#### `install_package(name: str, force: bool = False, extra_index: str = None, trusted_host: str = None) -> Tuple[str, str]`

install a pip3 package using a subprocess in current environment
    
    name {str} -- name of package to install
    force {bool} -- force newest edition
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    

<a name="list_packages_1777836065"></a>
#### `list_packages() -> list`

list current pip3 packages in environment

    return {list} -- a list of available packages
    

<a name="update_package_1100192072"></a>
#### `update_package(name: str, extra_index: str = None, trusted_host: str = None) -> Tuple[str, str]`

update a pip3 package by name, leverages install_package with force = True

    name {str} -- name of package to install
    extra_index {str} -- extra url to index in package manager
    trusted_host {str} -- extra url where package is hosted

    return {tuple} -- return the output, and error of subprocess run
    
<a name="modutils.sessionutils_5867312898996405855"></a>
## modutils.sessionutils

<a name="modutils.sessionutils.BaseSession_2677308962921948920"></a>
### modutils.sessionutils.BaseSession(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16, resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None)

A base session to build persistent sessions to handle resolving specific status codes

<a name="BaseSession.__init___4074244197413366741"></a>
#### `BaseSession.__init__(self, max_retries: int = 3, pool_connections: int = 16, pool_maxsize: int = 16, resolve_status_codes: list = None, verbose: bool = False, auth: tuple = None)`

Initialize a new session

<a name="BaseSession._log_response_1975778443043522547"></a>
#### `BaseSession._log_response(self, response: requests.models.Response) -> None`

log each requests from resolver

<a name="BaseSession._resolver_8386464650303821733"></a>
#### `BaseSession._resolver(self, request: functools.partial) -> requests.models.Response`

attempt to resolve a requests with an invalid status code

        if the status code of the requests is not one to resolve:
            Default:  [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
        the requests will be sent up to max_retries or until receiving an accepted status_code

        :param request: partial requests function to be used to attempt and resolve a valid response

        :return: response from the requests
        

<a name="BaseSession.delete_6360896686043141700"></a>
#### `BaseSession.delete(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session delete
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="BaseSession.get_4801989696975619918"></a>
#### `BaseSession.get(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session get
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="BaseSession.head_232502297474810491"></a>
#### `BaseSession.head(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session head
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="BaseSession.patch_999451590068817040"></a>
#### `BaseSession.patch(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session patch
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="BaseSession.post_794375458216340934"></a>
#### `BaseSession.post(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session post
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="BaseSession.put_7202945418070415894"></a>
#### `BaseSession.put(self, url: Union[str, bytes], **kwargs) -> requests.models.Response`

 override of requests.Session put
            calls Session.get with resolver

        :param url: url for requests
        :param kwargs: named arguments for requests

        :return: response from requests
        

<a name="modutils.sessionutils.EmailSession_3898108880321399818"></a>
### modutils.sessionutils.EmailSession(self, smtp_server, smtp_port, from_address: str = None, authentication_required: bool = False, auth_username: str = None, auth_password: str = None)

New email session

<a name="EmailSession.send_1351989794129380348"></a>
#### `EmailSession.send(self, subject: str, body: str, to_address_list: list, cc_address_list: list = None, from_address: str = None, encoding: str = 'html', logo_images: list = None, file_attachments: list = None) -> dict`


    :param subject: Subject string for email, required
    :param body: Message content for email, required
    :param to_address_list: addresses to send email to, required
    :param cc_address_list: addresses to cc on email, default: None
    :param from_address: address to send email from, default: None, will use self.from_address if one was given
    :param encoding: encoding for body, default: html
    :param logo_images: list of paths to images to use for logos, default: None
    :param file_attachments: list of paths to attachments for email, default: None

    :return: dict
    
    send email    


<a name="modutils.stdutils_1737493875"></a>
## modutils.stdutils

<a name="fg_1840553876"></a>
#### `fg(color)`

alias for colored().foreground()

<a name="main_890288721"></a>
#### `main(md=None, filename=None, cols=None, theme=None, c_theme=None, bg=None, c_no_guess=None, display_links=None, link_style=None, from_txt=None, do_html=None, code_hilite=None, c_def_lexer=None, theme_info=None, no_colors=None, tab_length=4, no_change_defenc=False, header_nrs=False, **kw)`

 md is markdown string. alternatively we use filename and read 

<a name="modutils.stdutils.echo_362805693"></a>
### modutils.stdutils.echo(self, message: Any, expand: bool = False, list_delimiter: str = '\n', indent: int = 4, color: str = None, newline: bool = True, markdown: bool = False)


    echo - a modern print statement that resolves objects to printable types
    

<a name="echo.__call___318159007"></a>
#### `echo.__call__(self, message: Any = None)`

__call__ can be used to overwrite the current message if you want to reuse an echo object

            x = echo('123')
            x()
            x('345')


        message {Any} -- object to print

        

<a name="echo.__init___1476576396"></a>
#### `echo.__init__(self, message: Any, expand: bool = False, list_delimiter: str = '\n', indent: int = 4, color: str = None, newline: bool = True, markdown: bool = False)`

None

<a name="echo._resolve_1902868456"></a>
#### `echo._resolve(self, message: Any) -> None`

resolve and print a message based on Any given type

        message {Any} -- an object to print

        return {None} -- does not return anything, this function will write to stdout
        

<a name="echo._resolve_class_object_1121738252"></a>
#### `echo._resolve_class_object(self, cls: object)`

resolve a class object to an always printable form based on the type of attributes.
        recursively resolves attributes

        cls {object} -- class object to print

        return {None} - does not return anything due to needing to call resolve
        

<a name="echo._resolve_response_object_1840220819"></a>
#### `echo._resolve_response_object(self, response: requests.models.Response) -> str`

resolve requests.Response objects to an always printable form based on their status_code from response

        response {requests.Response} -- response object to resolve

        return {str} -- a printable form of the response
        

<a name="modutils.typeutils_135504944"></a>
## modutils.typeutils

<a name="nget_42222092"></a>
#### `nget(d: dict, *args: Union[str, list]) -> Any`

nget - nested get call to easily retrieve nested information with a single call and set a default
    Ex.
        nget(dict, ['key1', 'key2', ..], default)
        nget(dict, key1, key2, .., default)

        nget use an iterable of keys to retrieve nested information and can set a default if a key is not found
    

<a name="modutils.typeutils.sha256_1273030348"></a>
### modutils.typeutils.sha256(self, value)

An implementation of a sha256 type based off the str type



 