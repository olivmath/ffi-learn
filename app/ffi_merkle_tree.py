from ctypes import CDLL, POINTER, c_size_t, c_ubyte
from typing import List


class FFIMerkleTreeRoot:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.make_merkle_root.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.make_merkle_root.restype = POINTER(c_ubyte)

        self.lib.free_merkle_root.argtypes = [POINTER(c_ubyte)]
        self.lib.free_merkle_root.restype = None

    def make_merkle_root(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * len(leaf)
            leaves_pointers[i] = array_type(*leaf)

        hash_ptr = self.lib.make_merkle_root(leaves_pointers, len_leaves)
        hash_bytes = bytes(hash_ptr[:32])
        print(list(hash_bytes))

        self.lib.free_merkle_root(hash_ptr)
        print(list(bytes(hash_ptr[:32])))
