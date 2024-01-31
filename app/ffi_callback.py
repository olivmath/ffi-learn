from ctypes import CDLL, CFUNCTYPE, POINTER, c_size_t, c_ubyte
from keccaky import hash_it_bytes
from typing import Callable, List


class FFIProcessLeavesWithCallback:
    def __init__(self, lib: CDLL) -> None:
        self.lib = lib
        self.lib.process_leaves_with_callback.argtypes = [
            CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte)),
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.process_leaves_with_callback.restype = None

    def process_leaves_with_callback(self, leaves: List[bytes], function: Callable):
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
        self.lib.process_leaves_with_callback(
            callback_type(function), leaves_pointers, len_leaves
        )
