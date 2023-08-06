# Programowanie w jezyku Python 2016/2017 zadanie 2

This program is estimating complexity of algorithm comparing executing times for vary sizes of problem.
It is assumed that the greater size is, the more time it takes.
Additionally program estimates execution time for given size of problem and in reverse - whats the estimating size of problem, it can be solved in a specified time.

## How to use
1. Open your console and type:
    $ pip install git+https://github.com/AGHPythonCourse2017/zad2-detori.git
or install from PyPI:
    $ pip install complexity_estimator

2. Run python and then type:
 - from complexity_estimator import main

### Run example:
 - main.run_example()
to get estimating of prepared module

### Estimate complexity your own module
3. Type:
 - main.run([module], [size1], [size2], [sizeToCheckTime],[timeToCheckSize], [timeout=30])


* module - name of module you want to test out. It needs to have a special structure containing 3 functions:
  * setup - a function initializing and preparing structures, connections etc. Time of setup is not taken under account.
  * measure - a general function of which the time is measured
  * teardown - a function tearing down like ie. closing connections with databases, deleting some files etc.

* size1 - the size of smaller problem you want to check out.
* size2 - the size of bigger problem, should be greater than size1 (ie. 10 times)
* sizeToCheckTime - the size of problem you want to estimate time
* timeToCheckSize - the time within the specified problem can be resolved
* timeout - optional function when you can set the maximum time of calculating. Default it is set to 30 seconds. It is not recommended to setting up a lower timeout.
The best complexity estimating result is when it takes at least a few seconds to calculate.
For the small sizes,the difference can be unnoticeable that results inaccurate complexity measurements. If so try to increase the size of problems

