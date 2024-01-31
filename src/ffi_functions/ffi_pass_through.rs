use std::slice;

use super::utils::hash_it;


/// Returns a pointer to the original array of leaves.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays.
/// * `len_leaves` - The number of leaves.
///
/// # Returns
///
/// A pointer to the original array of leaves.
///
/// # Safety
///
/// Assumes that the pointer is valid.
#[no_mangle]
pub unsafe extern "C" fn pass_through_leaves(
    leaves_ptr: *const *const u8,
    len_leaves: usize,
) -> *const *const u8 {
    let leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) };
    leaves.as_ptr()
}

// Modifies the leaves by hashing them and returns a pointer to the modified array.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays.
/// * `len_leaves` - The number of leaves.
///
/// # Returns
///
/// A pointer to the modified array of leaves.
///
/// # Safety
///
/// Assumes that the pointer is valid.
#[no_mangle]
pub unsafe extern "C" fn modify_and_pass_through_leaves(
    leaves_ptr: *const *const u8,
    len_leaves: usize,
) -> *mut *mut u8 {
    let leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) };

    let mut hashed_leaves = Vec::new();

    for leaf_ptr in leaves {
        let leaf = unsafe { slice::from_raw_parts(*leaf_ptr, 32) };
        let mut result: [u8; 32] = [0; 32];
        hash_it(leaf, &mut result);
        //
        // put flag in final of array
        let mut array_flag = [0u8; 33];
        array_flag[..32].copy_from_slice(&result);
        array_flag[32] = true as u8;
        //
        hashed_leaves.push(Box::into_raw(Box::new(array_flag)) as *mut u8);
    }

    let boxed_slice = hashed_leaves.into_boxed_slice();
    Box::into_raw(boxed_slice) as *mut *mut u8
}
