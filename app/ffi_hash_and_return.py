from ctypes import CDLL, POINTER, c_size_t, c_ubyte
from keccaky import hash_it_bytes
from typing import List


class FFIHashLeavesAndReturn:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.hash_leaves_and_return.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.hash_leaves_and_return.restype = POINTER(c_ubyte)
        self.lib.free_hashed_leaves.argtypes = [POINTER(c_ubyte)]
        self.lib.free_hashed_leaves.restype = None

    def hash_leaves_and_return(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * len(leaf)
            leaves_pointers[i] = array_type(*leaf)

        hash_ptr = self.lib.hash_leaves_and_return(leaves_pointers, len_leaves)
        hash_bytes = bytes(hash_ptr[:32])
        print(list(hash_bytes))

        self.lib.free_hashed_leaves(hash_ptr)
        print(list(hash_bytes))

        concatenated_bytes = b"".join(leaves)
        r = hash_it_bytes(concatenated_bytes)
        print(list(r))
