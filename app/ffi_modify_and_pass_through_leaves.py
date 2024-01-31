from ctypes import CDLL, POINTER, c_size_t, c_ubyte
from typing import List


class FFIPassThrough:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.pass_through_leaves.argtypes = [POINTER(POINTER(c_ubyte)), c_size_t]
        self.lib.pass_through_leaves.restype = POINTER(POINTER(c_ubyte))

    def pass_through_leaves(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        result_ptrs = self.lib.pass_through_leaves(leaves_pointers, len_leaves)

        for i in range(len_leaves):
            result = list(bytes(result_ptrs[i][:32]))
            print(result)
