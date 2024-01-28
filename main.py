from ctypes import CDLL, CFUNCTYPE, POINTER, c_size_t, c_ubyte, memmove
from keccaky import hash_it_bytes
from hashlib import sha256
from typing import Callable, List


class Lib:
    def __init__(self) -> None:
        self.lib = CDLL("./libffi_learn.dylib")

        # RUN 1: Call function that just print something
        self.lib.run1.argtypes = []
        self.lib.run1.restype = None

        # RUN 2: Call function that send a list[bytes] and print it
        self.lib.run2.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.run2.restype = None

        # RUN 3: Call function that send a list[bytes] and hash leaves and print it
        self.lib.run3.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.run3.restype = None

        # RUN 4: Call function that send a list[bytes], callback[[bytes], bytes] function and hash leaves
        self.lib.run4.argtypes = [
            CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte)),
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.run4.restype = None

        # RUN 5: Call function that send a list[bytes] and hash leaves and return it
        self.lib.run5.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.run5.restype = POINTER(c_ubyte)

        self.lib.run5free_32.argtypes = [POINTER(c_ubyte)]
        self.lib.run5free_32.restype = None

        # RUN 6: Call function that send a list[bytes] and return a list[bytes]
        self.lib.run6.argtypes = [POINTER(POINTER(c_ubyte)), c_size_t]
        self.lib.run6.restype = POINTER(POINTER(c_ubyte))

        # RUN 7: Call function that send a list[bytes], modified and return a list[bytes]
        self.lib.run7.argtypes = [POINTER(POINTER(c_ubyte)), c_size_t]
        self.lib.run7.restype = POINTER(POINTER(c_ubyte))

    def run1(self):
        print("PYTHON SIDE: Hello FFI")
        self.lib.run1()

    def run2(self, leaves: List[bytes]):
        for leaf in leaves:
            print(f"PYTHON SIDE: {list(leaf)}")

        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        self.lib.run2(leaves_pointers, len_leaves)

    def run3(self, leaves: List[bytes]):
        for leaf in leaves:
            leaf = hash_it_bytes(leaf)
            print(f"PYTHON SIDE: {list(leaf)}")

        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        self.lib.run3(leaves_pointers, len_leaves)

    def run4(self, leaves: List[bytes], function: Callable):
        for leaf in leaves:
            print(f"PYTHON WITHOUT HASH: {list(leaf)}")
        for leaf in leaves:
            leaf = hash_it_bytes(leaf)
            print(f"PYTHON WITH HASH: {list(leaf)}")

        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        callback_type = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte))
        self.lib.run4(callback_type(function), leaves_pointers, len_leaves)

    def run5(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * len(leaf)
            leaves_pointers[i] = array_type(*leaf)

        hash_ptr = self.lib.run5(leaves_pointers, len_leaves)
        hash_bytes = bytes(hash_ptr[:32])
        print(list(hash_bytes))
        self.lib.run5free_32(hash_ptr)
        print(list(hash_bytes))

        concatenated_bytes = b"".join(leaves)
        r = hash_it_bytes(concatenated_bytes)
        print(list(r))

    def run6(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        result_ptrs = self.lib.run6(leaves_pointers, len_leaves)

        for i in range(len_leaves):
            result = list(bytes(result_ptrs[i][:32]))
            print(result)

    def run7(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        result_ptrs = self.lib.run7(leaves_pointers, len_leaves)

        for i in range(len_leaves):
            result = list(bytes(result_ptrs[i][:33]))
            flag = result[32]
            result = result[:32]
            print(f"flag: {flag}, result: {result}")


def callback1(prt, buffer_ptr):
    data = bytes(prt[:32])

    result = hash_it_bytes(data)
    memmove(buffer_ptr, result, 32)


leaves_input = [sha256(data.encode()).digest() for data in ["a", "b", "c", "d"]]
lib = Lib()
# lib.run1()
# lib.run2(leaves_input)
# lib.run3(leaves_input)
# lib.run4(leaves_input, callback1)
# lib.run5(leaves_input)
# lib.run6(leaves_input)
lib.run7(leaves_input)
