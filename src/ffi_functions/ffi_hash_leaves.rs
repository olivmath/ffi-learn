use super::utils::hash_it;
use std::slice;

/// Hashes the leaves and displays the hashed values.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays to be hashed.
/// * `len_leaves` - The number of leaves.
///
/// # Safety
///
/// Assumes that the pointer is valid and that `len_leaves` correctly represents the number of elements.
#[no_mangle]
pub unsafe extern "C" fn hash_and_display_leaves(leaves_ptr: *mut *mut u8, len_leaves: usize) {
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
