#  based on http://stackoverflow.com/a/21861599
from threading import Thread
import functools
from complexity_estimator.my_exceptions import TimeoutException


def timeout(time):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!'
                             % (func.__name__, timeout))]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(time)
            except Exception as je:
                print('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise TimeoutException('Time')
            return ret
        return wrapper
    return deco
