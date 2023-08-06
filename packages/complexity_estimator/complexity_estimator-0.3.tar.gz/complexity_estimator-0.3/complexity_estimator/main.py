import time
import importlib
import logging
from complexity_estimator.timeout import timeout
from complexity_estimator.my_parser import MyParser
from complexity_estimator.complexity import estimate_complexity
from complexity_estimator.my_exceptions import UndefinedComplexityException,\
    TimeoutException


class Main:
    def __init__(self, tested_module_name, size1, size2, size_to_check_time,
                 time_to_check_size, my_timeout, to1, to2):
        self.tested_module_name = tested_module_name
        self.size1 = size1
        self.size2 = size2
        self.time_to_check_size = time_to_check_size
        self.size_to_check_time = size_to_check_time
        self.timeout = my_timeout
        self.tested_object1 = to1
        self.tested_object2 = to2

    def execute(self, a, t, s):
        t1 = a.measure(a.tested_object1)
        t2 = a.measure(a.tested_object2)

        print('Time: ', format(t1, '.6f'), 's for size: ', self.size1)
        print('Time: ', format(t2, '.6f'), 's for size: ', self.size2)
        try:
            estimate_complexity(self.size1, self.size2, t1, t2, t, s)
        except UndefinedComplexityException as ece:
            logging.warning('Undefined complexity')
            print(ece.strerror)
        except Exception as ex:
            logging.error('Error')
            print(str(ex))

    def start(self, my_timeout):
        @timeout(my_timeout)  # setting timeout for executing program
        def started():
            with MyContextManager(self.tested_object1,
                                  self.tested_object2) as A:
                self.execute(A, self.time_to_check_size,
                             self.size_to_check_time)

        return started()


def time_measuring(decfunction):
    def inner(*args, **kwargs):
        start_time = time.time()
        decfunction(*args, **kwargs)
        end_time = time.time()
        logging.debug('%r %2.2f sec' % (decfunction.__name__,
                                        end_time - start_time))
        return end_time - start_time

    return inner


class MyContextManager:
    def __init__(self, tested_object1, tested_object2):
        self.tested_object1 = tested_object1
        self.tested_object2 = tested_object2

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        logging.info('tearing down')
        self.tested_object1.teardown()
        self.tested_object2.teardown()

    @time_measuring
    def measure(self, tested, *args, **kwargs):
        logging.info('measuring')
        tested.measure(*args, **kwargs)


def run(module_name, size1, size2,
        size_to_check_time, time_to_check_size, my_timeout=30):
    logging.basicConfig(level=logging.DEBUG, filename='logs.log',
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    try:
        tested_module = importlib.import_module(module_name)
        tested_class = getattr(tested_module, 'TestedClass')
        logging.info('setting up modules')
        start(module_name, size1, size2,
              size_to_check_time, time_to_check_size, my_timeout, tested_class)
    except ImportError as e:
        print(e)
        exit(1)


def start(module_name, size1, size2,
          size_to_check_time, time_to_check_size, my_timeout, tested_class):
    print('Starting...')
    logging.info('setting up modules')
    m = Main(module_name, size1, size2,
             size_to_check_time, time_to_check_size, my_timeout,
             tested_class(size1), tested_class(size2))
    try:
        m.start(my_timeout)
    except TimeoutException:
        print("Unfortunately the estimating function exceeded the ",
              my_timeout, " timeout. Try to change sizes of your problem"
                          " or increase the timeout")


def run_example():
    """Program will estimate the complexity of a sample module
    sorting a list of numbers. It will show also estimated time
    whithin the 10 million elements can be sorted and size
    of list it can be sorded in one second"""
    logging.basicConfig(level=logging.DEBUG, filename='logs.log',
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    from pythonzad2.testedModule import TestedClass
    module_name = 'testedModule'
    size1 = 100000
    size2 = 1000000
    size_to_check_time = 10000000
    time_to_check_size = 1
    my_timeout = 30
    print(run_example.__doc__)
    start(module_name, size1, size2,
          size_to_check_time, time_to_check_size, my_timeout, TestedClass)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='logs.log',
                        format=' %(asctime)s - %(levelname)s - %(message)s')

    print('''Program estimates complexity of some algorithms given
    in a specially created module containing 3 functions:
          setup, measure and teardown. Additionally it shows estimated
          running time of given size of problem
          and also returns maximum size algorithm
          it can be executed in given time''')
    p = MyParser()
    ars = p.args

    run(ars.module, ars.size1, ars.size2,
        ars.sizeToCheckTime, ars.timeToCheckSize, ars.timeout)
