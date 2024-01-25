import ctypes


class Lib:
    def __init__(self) -> None:
        self.lib = ctypes.CDLL("./lib.dylib")

        self.lib.run.argtypes = []
        self.lib.run.restype = None

    def run(self):
        print("PYTHON SIDE: Hello FFI")
        self.lib.run()


lib = Lib()
lib.run()
