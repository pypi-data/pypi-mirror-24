import random


class TestedClass:

    def __init__(self, size):
        self.list = self.setup(size)

    @staticmethod
    def setup(size):
        return [random.randrange(1, size) for _ in range(size)]

    def measure(self):
        return sorted(self.list)

    def teardown(self, *args, **kwargs):
        pass
