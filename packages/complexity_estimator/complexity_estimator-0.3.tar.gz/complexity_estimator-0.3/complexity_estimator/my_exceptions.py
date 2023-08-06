class UndefinedComplexityException(Exception):
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}


class TimeoutException(Exception):
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}
