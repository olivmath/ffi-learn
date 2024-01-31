from ctypes import CDLL, POINTER, c_size_t, c_ubyte
from typing import List


class FFIDisplayLeaves:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.display_leaves.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.display_leaves.restype = None

    def display_leaves(self, leaves: List[bytes]):
        for leaf in leaves:
            print(f"PYTHON SIDE: {list(leaf)}")

        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        self.lib.display_leaves(leaves_pointers, len_leaves)
