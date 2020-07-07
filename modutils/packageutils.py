from subprocess import Popen, PIPE
from typing import Union, Tuple

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
    return [pkg for pkg in out.decode('utf-8').replace('\r','').split('\n') if pkg]

def has_package(name: str, version: Union[str, int, float] = None) -> bool:
    """check if current environment has a package

    name {str} -- name of package to check
    version {Union[str, int, float]} -- OPTIONAL, will append version for a specific version check of package

    return {bool} -- True if package was found and False if not
    """
    pkg = f'{name}=={version}' if version else name
    return any(pkg in pp for pp in list_packages())

