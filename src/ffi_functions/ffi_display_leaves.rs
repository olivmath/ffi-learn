use std::slice;

/// Displays the leaves (byte arrays) passed from Python.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays.
/// * `len_leaves` - The number of leaves.
///
/// # Safety
///
/// Assumes that the pointer is valid and that `len_leaves` correctly represents the number of elements.
#[no_mangle]
pub unsafe extern "C" fn display_leaves(leaves_ptr: *const *const u8, len_leaves: usize) {
    let leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect::<Vec<Vec<u8>>>();

    for leaf in leaves {
        println!("RUST SIDE: {leaf:?}");
    }
}
