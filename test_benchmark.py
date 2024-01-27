# BENCHMARK
### run with keccak into Rust
### run with keccak outside Python

from ctypes import CDLL, CFUNCTYPE, POINTER, c_size_t, c_ubyte, memmove
from keccaky import hash_it_bytes
from typing import Callable, List
from hashlib import sha256
import pytest
import time


class Lib:
    def __init__(self) -> None:
        self.lib = CDLL("./libbenchmark.dylib")

        # HASH WITHIN RUST
        self.lib.hash_within_rust.argtypes = [
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.hash_within_rust.restype = None

        # # HASH WITHOUT RUST
        self.lib.hash_without_rust.argtypes = [
            CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte)),
            POINTER(POINTER(c_ubyte)),
            c_size_t,
        ]
        self.lib.hash_without_rust.restype = None

    def hash_within_rust(self, leaves: List[bytes]):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        self.lib.run3(leaves_pointers, len_leaves)

    def hash_without_rust(self, leaves: List[bytes], function: Callable):
        len_leaves = len(leaves)
        leaves_pointers = (POINTER(c_ubyte) * len_leaves)()

        for i, leaf in enumerate(leaves):
            array_type = c_ubyte * 32
            leaves_pointers[i] = array_type(*leaf)

        callback_type = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(c_ubyte))
        self.lib.run4(callback_type(function), leaves_pointers, len_leaves)


def callback1(prt, buffer_ptr):
    data = bytes(prt[:32])

    result = hash_it_bytes(data)
    memmove(buffer_ptr, result, 32)


def hash_1000_leaveas_within_rust():
    lib = Lib()
    leaves = [sha256(str(i).encode()).digest() for i in range(1000)]
    lib.hash_within_rust(leaves)


def hash_1000_leaveas_without_rust():
    lib = Lib()
    leaves = [sha256(str(i).encode()).digest() for i in range(1000)]
    lib.hash_without_rust(leaves, callback1)


@pytest.mark.benchmark(group="HashWithinRust", timer=time.time)
def test_hash_1000_leaveas_within_rust(benchmark):
    benchmark(hash_1000_leaveas_within_rust)


@pytest.mark.benchmark(group="HashWithoutRust", timer=time.time)
def test_hash_1000_leaveas_without_rust(benchmark):
    benchmark(hash_1000_leaveas_without_rust)
