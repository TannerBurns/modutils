from functools import update_wrapper
from typing import Callable, List

from modutils.aio import Eventloop, aioloop

class aiobulk(object):

    def __init__(self, function: Callable):
        """initialize aiobulk
        the function being decorated will receive a new attribute for the bulk call

        :param function: function being decorated
        """
        self.__self__ = None
        self.__bound__ = function
        update_wrapper(self, function)

    def __call__(self, *args: tuple, **kwargs: dict):
        """call base function"""
        if self.__self__ is not None:
            args = (self.__self__,) + args
        return self.__bound__(*args, **kwargs)

    def __get__(self, instance, _):
        """update self if instance is found

        :param instance: cls instance
        :return: return self with instance
        """
        if instance is None:
            return self
        else:
            self.__self__ = instance
            return self

    def bulk(self, args_list: List[list], loop: Eventloop = None, max_async_pool: int = 16, max_futures: int = 100000,
             disable_progress_bar: bool = False, progress_bar_color: str = 'green_3a',
             progress_bar_format: str = None) -> list:
        """add a method called 'bulk' to given function

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
                add(1,2)

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
        """
        if self.__self__ is not None:
            args_list = [[self.__self__] + args for args in args_list]
        return aioloop(self.__bound__, args_list, loop=loop, max_async_pool=max_async_pool, max_futures=max_futures,
                       disable_progress_bar=disable_progress_bar, progress_bar_color=progress_bar_color,
                       progress_bar_format=progress_bar_format)