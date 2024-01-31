from ctypes import CDLL


class FFIPrint:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.print_hello.argtypes = []
        self.lib.print_hello.restype = None

    def print_hello(self):
        print("PYTHON SIDE: Hello FFI")
        self.lib.print_hello()
