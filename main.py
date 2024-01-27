from keccaky import hash_it_bytes
from hashlib import sha256
from typing import List
import ctypes


class Lib:
    def __init__(self) -> None:
        self.lib = ctypes.CDLL("./libffi_learn.dylib")

        # RUN 1: Call function that just print something
        self.lib.run1.argtypes = []
        self.lib.run1.restype = None

        # RUN 2: Call function that send a list[bytes] and print it
        self.lib.run2.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.c_size_t,
        ]
        self.lib.run2.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))

        # RUN 3: Call function that send a list[bytes] and hash leaves and print it
        self.lib.run3.argtypes = [
            ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.c_size_t,
        ]
        self.lib.run3.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))

    def run1(self):
        print("PYTHON SIDE: Hello FFI")
        self.lib.run1()

    def run2(self, leaves: List[bytes]):
        for leaf in leaves:
            print(f"PYTHON SIDE: {list(leaf)}")

        len_leaves = len(leaves)
        leaf_pointers = (ctypes.POINTER(ctypes.c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = ctypes.c_ubyte * 32
            leaf_pointers[i] = array_type(*leaf)

        self.lib.run2(leaf_pointers, len_leaves)

    def run3(self, leaves: List[bytes]):
        for leaf in leaves:
            leaf = hash_it_bytes(leaf)
            print(f"PYTHON SIDE: {list(leaf)}")

        len_leaves = len(leaves)
        leaf_pointers = (ctypes.POINTER(ctypes.c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = ctypes.c_ubyte * 32
            leaf_pointers[i] = array_type(*leaf)

        self.lib.run3(leaf_pointers, len_leaves)


lib = Lib()
lib.run1()
leaves_input = [sha256(data.encode()).digest() for data in ["a", "b", "c", "d"]]
lib.run2(leaves_input)
lib.run3(leaves_input)
