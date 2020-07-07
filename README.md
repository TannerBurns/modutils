# Modutils

    A library with modern utilities to assist development efficiency 
    
# Documentation

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



 