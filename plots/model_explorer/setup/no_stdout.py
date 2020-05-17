import contextlib
import sys


class DummyFile:
    def write(self, x):
        pass


@contextlib.contextmanager
def no_stdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
