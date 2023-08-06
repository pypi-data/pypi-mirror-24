import argparse


class MyParser:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('module',
                            help='module must contain 3 functions: '
                                 'setup, measure and teardown')

        parser.add_argument('size1', help='size 1 of the problem', type=int)

        parser.add_argument('size2', help='size 2 of the problem', type=int)

        parser.add_argument('sizeToCheckTime',
                            help='size of the problem to estimate time',
                            type=int)

        parser.add_argument('timeToCheckSize',
                            help='time [s] within problem of size'
                                 ' will be executed', type=float)

        parser.add_argument('-t', '--timeout',
                            help='maximum time [s] of running program',
                            type=int, default=30)

        self.args = parser.parse_args()
