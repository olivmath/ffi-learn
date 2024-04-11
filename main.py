from keccaky import hash_it_bytes
from ctypes import memmove
from app.lib import Lib


def callback1(prt, buffer_ptr):
    data = bytes(prt[:32])

    result = hash_it_bytes(data)
    memmove(buffer_ptr, result, 32)


leaves_input = [hash_it_bytes(data.encode()) for data in ["a", "b", "c", "d"]]
lib = Lib()
# lib.print_hello()
# lib.display_leaves(leaves_input)
# lib.hash_and_display_leaves(leaves_input)
# lib.process_leaves_with_callback(leaves_input, callback1)
# lib.hash_leaves_and_return(leaves_input)
# lib.pass_through_leaves(leaves_input)
# lib.modify_and_pass_through_leaves(leaves_input)
lib.make_merkle_root(leaves_input)
# lib.make_array()
