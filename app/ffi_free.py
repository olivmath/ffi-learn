from ctypes import CDLL, POINTER, c_ubyte, c_void_p, cast


class FFIArrayFree:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.make_array.argtypes = []
        self.lib.make_array.restype = POINTER(c_ubyte)

        self.lib.free_32.argtypes = [POINTER(c_ubyte)]
        self.lib.free_32.restype = None

    def make_array(self):
        array_ptr = self.lib.make_array()
        array = bytes(array_ptr[:32])
        print(f"PYTHON SIDE: {list(array)}")

        self.lib.free_32(array_ptr)
        print(f"PYTHON SIDE: {list(bytes(array_ptr[:32]))}")
        array_ptr = cast(array_ptr, c_void_p)
        array_ptr.value = None

        print(f"PYTHON SIDE: {list(array)}")
