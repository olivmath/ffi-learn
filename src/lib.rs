use std::slice;
use tiny_keccak::{Hasher, Keccak};

pub fn hash_it(data: &[u8], result: &mut [u8; 32]) {
    let mut k256 = Keccak::v256();

    k256.update(data);
    k256.finalize(result);
}

/// # Safety
///
/// FFI to Python.
#[no_mangle]
pub unsafe extern "C" fn run1() {
    println!("RUST SIDE: Hello FFI");
}

/// # Safety
///
/// FFI to Python.
#[no_mangle]
pub unsafe extern "C" fn run2(leaves_ptr: *const *const u8, len_leaves: usize) {
    let leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect::<Vec<Vec<u8>>>();

    for leaf in leaves {
        println!("RUST SIDE: {leaf:?}");
    }
}

/// # Safety
///
/// FFI to Python.
#[no_mangle]
pub unsafe extern "C" fn run3(leaves_ptr: *mut *mut u8, len_leaves: usize) {
    let leaves: Vec<Vec<u8>> = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect();

    for leaf in leaves {
        let mut result: [u8; 32] = [0; 32];
        hash_it(&leaf, &mut result);
        println!("RUST SIDE: {result:?}");
    }
}
