class Iterator:

    def __init__(self, values, n=None):
        if len(values) == 0:
            raise IndexError
        self.values = values
        self.counter = 0
        self.limit = n

    def __next__(self):
        if not self.limit or self.counter < self.limit:
            self.counter += 1
            return self.values[(self.counter - 1) % len(self.values)]
        else:
            raise StopIteration

    def reset(self):
        self.counter = 0


class Animation:

    def __init__(self, name, iterator):
        self.name = name
        self.iterator = iterator

    def __next__(self):
        return next(self.iterator)

    def reset(self):
        self.iterator.reset()
