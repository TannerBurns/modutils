import asyncio
import sys

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, List, NewType
from functools import partial
from colored import fg, style
from tqdm import tqdm


class aioloop():


    Eventloop = NewType('Eventloop', asyncio.windows_events._WindowsSelectorEventLoop) \
        if sys.platform == 'win32' else NewType('Eventloop', asyncio.unix_events._UnixSelectorEventLoop)


    def __new__(cls, fn: Callable, args_list: List[List], loop: Eventloop = None,
                max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False,
                progress_bar_color: str = 'green_3a') -> list:
        """create new aioloop, run, and return results

        :param fn {Callable}: function to map to arguments
        :param args_list {List[List]}: list of arguments to send to function
        :param loop {Eventloop}: a pre-defined asyncio loop
        :param max_async_pool {int}: max async pool, this will define the number of processes to run at once
        :param max_futures {int}: max futures, this will define the number of processes to setup and execute at once.
            If there is a lot of arguments and futures is very large, can cause memory issues.
        :param disable_progress_bar {bool}: disable progress bar from printing
        :param progress_bar_color {str}: color of progress bar; default: green

        :return list of results
        """
        instance = super(aioloop, cls).__new__(aioloop)
        instance.__init__(fn, args_list, loop=loop, max_async_pool=max_async_pool, max_futures=max_futures,
                            disable_progress_bar=disable_progress_bar, progress_bar_color=progress_bar_color)
        return instance.run()


    def __init__(self, fn: Callable, args_list: List[List], loop: Eventloop = None,
                max_async_pool: int = 16, max_futures: int = 100000, disable_progress_bar: bool = False,
                progress_bar_color: str = 'green_3a'):
        """initalize aioloop

        :param fn {Callable}: function to map to arguments
        :param args_list {List[List]}: list of arguments to send to function
        :param loop {Eventloop}: a pre-defined asyncio loop
        :param max_async_pool {int}: max async pool, this will define the number of processes to run at once
        :param max_futures {int}: max futures, this will define the number of processes to setup and execute at once.
            If there is a lot of arguments and futures is very large, can cause memory issues.
        :param disable_progress_bar {bool}: disable progress bar from printing
        :param progress_bar_color {str}: color of progress bar; default: green
        """
        self.__aiocall__ = fn
        self.args_list = args_list
        self.loop = loop or asyncio.new_event_loop()
        self.max_async_pool = max_async_pool
        self.max_futures = max_futures
        self.disable_progress_bar = disable_progress_bar
        self.progress_bar_color = progress_bar_color
        self.bar_format = '{l_bar}%s{bar}%s| {n_fmt}/{total_fmt} [{elapsed}<{remaining},' \
                         ' {rate_fmt}{postfix}]' % (fg(progress_bar_color), style.RESET)


    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.loop = None


    def aioexecute(self, args: list = None, kwargs: dict = None) -> Any:
        """aioexecute will self.__aiocall__ with the mapped args and kwargs from the executor

        :param args: list of required arguments
        :param kwargs: dict of keyword arguments

        :return: Any: return from self.__aiocall__
        """
        args = args or []
        kwargs = kwargs or {}
        return self.__aiocall__(*args, **kwargs)


    async def aioexecutor(self) -> list:
        """aioexecutor will create futures from args and collect results as they are finished in the async loop

        :return: list -- list of results from aio loop
        """
        results = []
        with ThreadPoolExecutor(max_workers=self.max_async_pool) as executor:
            for index in range(0, len(self.args_list), self.max_futures):
                futures = [
                    self.loop.run_in_executor(executor, partial(self.aioexecute, *args))
                    for args in self.args_list[index:index + self.max_futures]
                ]
                results.extend([
                    await result for result in tqdm(asyncio.as_completed(futures), total=len(futures),
                                                    disable=self.disable_progress_bar, bar_format=self.bar_format)
                ])
        return results


    def run(self) -> list:
        """run will be called by aioloop __new__ to start async operations with callable function

        :return: list of results
        """
        return self.loop.run_until_complete(self.aioexecutor())

