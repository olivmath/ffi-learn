from ctypes import CDLL
from app.ffi_callback import FFIProcessLeavesWithCallback
from app.ffi_display_leaves import FFIDisplayLeaves
from app.ffi_free import FFIArrayFree
from app.ffi_hash_and_return import FFIHashLeavesAndReturn
from app.ffi_hash_leaves import FFIHashAndDisplayLeaves
from app.ffi_merkle_tree import FFIMerkleTreeRoot
from app.ffi_modify_and_pass_through_leaves import FFIPassThrough
from app.ffi_pass_through import FFIModifyAndPassThroughLeaves

from app.ffi_print import FFIPrint


class Lib(
    FFIModifyAndPassThroughLeaves,
    FFIProcessLeavesWithCallback,
    FFIHashAndDisplayLeaves,
    FFIHashLeavesAndReturn,
    FFIMerkleTreeRoot,
    FFIDisplayLeaves,
    FFIPassThrough,
    FFIArrayFree,
    FFIPrint,
):
    def __init__(self) -> None:
        self.lib = CDLL("./libffi_learn.dylib")

        FFIModifyAndPassThroughLeaves.__init__(self, self.lib)
        FFIProcessLeavesWithCallback.__init__(self, self.lib)
        FFIHashAndDisplayLeaves.__init__(self, self.lib)
        FFIHashLeavesAndReturn.__init__(self, self.lib)
        FFIMerkleTreeRoot.__init__(self, self.lib)
        FFIDisplayLeaves.__init__(self, self.lib)
        FFIPassThrough.__init__(self, self.lib)
        FFIArrayFree.__init__(self, self.lib)
        FFIPrint.__init__(self, self.lib)
