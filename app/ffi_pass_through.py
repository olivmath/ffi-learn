from ctypes import CDLL, POINTER, c_size_t, c_ubyte
from typing import List


class FFIModifyAndPassThroughLeaves:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.modify_and_pass_through_leaves.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.modify_and_pass_through_leaves.restype = POINTER(POINTER(c_ubyte))

    def modify_and_pass_through_leaves(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        result_ptrs = self.lib.modify_and_pass_through_leaves(
            leaves_pointers, len_leaves
        )

        for i in range(len_leaves):
            result = list(bytes(result_ptrs[i][:33]))
            flag = result[32]
            result = result[:32]
            print(f"flag: {flag}, result: {result}")
