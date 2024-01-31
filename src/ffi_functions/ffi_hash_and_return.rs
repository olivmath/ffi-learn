use std::slice;
use tiny_keccak::{Hasher, Keccak};
/// Hashes the leaves and returns the hash result.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays to be hashed.
/// * `len_leaves` - The number of leaves.
///
/// # Returns
///
/// A pointer to the resulting hash.
///
/// # Safety
///
/// Assumes that the pointer is valid and that `len_leaves` correctly represents the number of elements.
#[no_mangle]
pub unsafe extern "C" fn hash_leaves_and_return(
    leaves_ptr: *const *const u8,
    len_leaves: usize,
) -> *const u8 {
    let mut hasher = Keccak::v256();
    let mut final_hash = [0u8; 32];

    for i in 0..len_leaves {
        let leaf = slice::from_raw_parts(*leaves_ptr.add(i), 32);
        hasher.update(leaf);
    }

    hasher.finalize(&mut final_hash);

    let boxed_hash = Box::new(final_hash);
    Box::into_raw(boxed_hash) as *const u8
}

/// Frees the memory allocated for the hashed leaves.
///
/// # Arguments
///
/// * `ptr` - A pointer to the memory to be freed.
///
/// # Safety
///
/// Assumes that the pointer is valid and was allocated by `hash_leaves_and_return`.
#[no_mangle]
pub unsafe extern "C" fn free_hashed_leaves(ptr: *mut u8) {
    unsafe {
        let _ = Box::from_raw(ptr);
    }
}
