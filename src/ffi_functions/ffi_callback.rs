use std::slice;

type Callback1 = extern "C" fn(leaf: *const u8, buffer: *mut u8);

/// Processes the leaves with a provided callback function.
///
/// # Arguments
///
/// * `callback` - A callback function to be applied to each leaf.
/// * `leaves_ptr` - A pointer to the array of byte arrays.
/// * `len_leaves` - The number of leaves.
///
/// # Safety
///
/// Assumes that the pointer and callback are valid.
#[no_mangle]
pub unsafe extern "C" fn process_leaves_with_callback(
    callback: Callback1,
    leaves_ptr: *mut *mut u8,
    len_leaves: usize,
) {
    let leaves: Vec<Vec<u8>> = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect();

    for leaf in &leaves {
        println!("RUST WITHOUT HASH: {leaf:?}");
    }
    for leaf in leaves {
        let mut result: [u8; 32] = [0; 32];
        callback(leaf.as_ptr(), result.as_mut_ptr());
        println!("RUST WITH HASH: {result:?}");
    }
}
