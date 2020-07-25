import asyncio
import sys

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List, NewType
from functools import partial
from colored import fg, style
from tqdm import tqdm

Eventloop = NewType('Eventloop', asyncio.windows_events._WindowsSelectorEventLoop) \
        if sys.platform == 'win32' else NewType('Eventloop', asyncio.unix_events._UnixSelectorEventLoop)


def aioexecute(fn: Callable, args: list = None) -> Any:
    """aioexecute will fn with the mapped args and kwargs from the executor

    :param args: list of required arguments
    :param kwargs: dict of keyword arguments

    :return: Any: return from fn
    """
    fnargs = []
    fnkwargs = {}
    for var in args:
        if isinstance(var, dict):
            fnkwargs.update(var)
        else:
            fnargs.append(var)
    return fn(*fnargs, **fnkwargs)

def aioloop(fn: Callable, args_list: List[List], loop: Eventloop = None,
                max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False,
                progress_bar_color: str = 'green_3a', progress_bar_format: str= None) -> list:
    """create new aioloop, run, and return results

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
    """
    async def aioexecutor() -> list:
        """aioexecutor will create futures from args and collect results as they are finished in the async loop

        :return: list -- list of results from aio loop
        """


        results = []
        with ThreadPoolExecutor(max_workers=max_async_pool) as executor:
            for index in range(0, len(args_list), max_futures):
                futures = [
                    loop.run_in_executor(executor, partial(aioexecute, fn, args))
                    for args in args_list[index:index + max_futures]
                ]
                results.extend([
                    await result for result in tqdm(asyncio.as_completed(futures), total=len(futures),
                                                    disable=disable_progress_bar, bar_format=progress_bar_format)
                ])
        return results

    if progress_bar_format is None:
        progress_bar_format = '{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} [{elapsed}<{remaining},' \
                 ' {rate_fmt}{postfix}]' % (fg(progress_bar_color), style.RESET)
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(aioexecutor())
