import sys

class StdoutFilter(object):
    def __init__(self):
        self.out = sys.stdout
        self.filters = ['Expected boundary']

    def write(self, message):
        for f in self.filters:
            if f not in message:
                self.out.write(message)

    def flush(self):
        self.out.flush()


class StderrFilter(object):
    def __init__(self):
        self.out = sys.stderr
        self.filters = ['Expected boundary']

    def write(self, message):
        for f in self.filters:
            if f not in message:
                self.out.write(message)

    def flush(self):
        self.out.flush()