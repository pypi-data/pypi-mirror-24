import logging
import math
from complexity_estimator.my_exceptions import UndefinedComplexityException


def estimate_complexity(size1, size2, t1, t2, t, s, resolution=0.05):
    if size2 < size1:
        print('Not correct data. Size2 cant be lower than size1')
        logging.warning('Not correct data')
        return
    if t1 > t2:
        if size2 < 2 * size1:
            print('Change difference between input data to get more precision')
            logging.warning('difference between data is to small')
        else:
            print('Estimating O(1)')
            print('In ', t, 's, estimating size: ',
                  estimate_size(size1, t1, t, 0))
        return

    n = size2 / size1

    estimator_list = [(t1, 'O(1)'), (t1 * math.log2(size2) / math.log2(size1),
                                     'O(logn)'), (t1 * n, 'O(n)'),
                      (t1 * n * math.log2(size2) / math.log2(size1),
                       'O(nlogn)'),
                      (t1 * n * n, 'O(n^2)'),
                      (t1 * n * n * n, 'O(n^3)')]
    logging.info('Estimating complexity')
    for i, (k, v) in enumerate(estimator_list):

        if t2 < (1 + resolution) * k:
            if t2 > (1 - resolution) * k or i == 0:
                print('Estimating ', v)

                tm = estimator(size2, s, t2, i)
                print('For size ', s, ' estimating time: ',
                      format(tm, '.6f'), 's')
                print('In ', t, 's, estimating size: ',
                      estimate_size(size1, t1, t, i - 1))

            else:  # if cant estimate for sure
                print('Estimating between ', estimator_list[(i - 1)][1] +
                      ' and ', v)

                estimate_time(size1, size2, s, t1, t2, i - 1)

                s_min = estimate_size(size1, t1, t, i)

                print('In ', t, 's, estimating size between: ',
                      s_min, ' and ',
                      estimate_size(size1, t1, t, i - 1, s_min))

            return

    raise UndefinedComplexityException('Estimating complexity worse than n^3 ')


def estimate_time(size1, size2, size, t1, t2, index):

    t_min1 = estimator(size1, size, t1, index)

    t_min2 = estimator(size2, size, t2, index)
    t_max1 = estimator(size1, size, t1, index + 1)
    t_max2 = estimator(size2, size, t2, index + 1)

    min_avg = int(t_min1 + t_min2) / 2
    max_avg = int(t_max1 + t_max2) / 2

    if size >= size1:
        min_avg = max(min_avg, t1)

    if size >= size2:
        min_avg = max(min_avg, t2)

    if size <= size1:
        max_avg = max(max_avg, t1)

    if size <= size2:
        max_avg = max(max_avg, t2)

    if abs(min_avg - max_avg) < 0.0001:
        print('For size: ', size, ' estimating time: ',
              format(min_avg, '.6f'), 's')
    else:
        print('For size: ', size, ' estimating time between: ',
              format(min_avg, '.6f'), ' and ', format(max_avg, '.6f'), 's')


def estimator(size1, size2, t1, index):
    n = size2 / size1

    estimator_list = [(t1, 'O(1)'), (t1 * math.log2(size2) / math.log2(size1),
                                     'O(logn)'), (t1 * n, 'O(n)'),
                      (t1 * n * math.log2(size2) / math.log2(size1),
                       'O(nlogn)'), (t1 * n * n, 'O(n^2)'),
                      (t1 * n * n * n, 'O(n^3)')]

    return estimator_list[index][0]  # returns estimated time based on 1 size


def estimate_size(size2, t2, t, index, previous=0):
    size_x = 2 * size2

    while estimator(size2, size_x, t2, index) < t:
        size_x *= 2
        if index == 1 and previous:
            size_x = 2 * previous
            break

    while True:
        temp = (size_x + size2) / 2
        time2 = estimator(size2, temp, t2, index)
        if abs(size2 - size_x) < 1:
            break
        elif time2 > t:
            size_x = temp
        else:
            size2 = temp
            t2 = time2

    return int(size_x)  # size_x was typeof float
