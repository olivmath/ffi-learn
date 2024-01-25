import ctypes


class Lib:
    def __init__(self) -> None:
        self.lib = ctypes.CDLL("./lib.dylib")

        self.lib.run1.argtypes = []
        self.lib.run1.restype = None

    def run1(self):
        print("PYTHON SIDE: Hello FFI")
        self.lib.run1()


lib = Lib()
lib.run1()
