use std::slice;

use super::utils::hash_it;

fn hash_function(left: &[u8], right: &[u8], buffer: &mut [u8; 32]) {
    let concat = [left, right].concat();
    hash_it(&concat, buffer)
}

/// Constructs a Merkle root from the given leaves and returns it.
///
/// # Arguments
///
/// * `leaves_ptr` - A pointer to the array of byte arrays representing the leaves.
/// * `len_leaves` - The number of leaves.
///
/// # Returns
///
/// A pointer to the Merkle root.
///
/// # Safety
///
/// Assumes that the pointer is valid and that `len_leaves` correctly represents the number of elements.
#[no_mangle]
pub unsafe extern "C" fn make_merkle_root(
    leaves_ptr: *const *const u8,
    len_leaves: usize,
) -> *mut u8 {
    let mut leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect::<Vec<Vec<u8>>>();

    while leaves.len() > 1 {
        let mut next_level = Vec::new();

        for leaf_pair in leaves.chunks(2) {
            let mut node = [0u8; 32];
            match leaf_pair {
                [left, right] => hash_function(left, right, &mut node),
                [left] => node.copy_from_slice(left),
                _ => unreachable!(),
            };
            next_level.push(node.to_vec());
        }

        leaves = next_level;
    }

    let root = leaves.first().unwrap().to_vec();
    print!("ROOT: {root:?}");
    let boxed_root = root.into_boxed_slice();
    Box::into_raw(boxed_root) as *mut u8
}

/// Frees the memory allocated for the Merkle root.
///
/// # Arguments
///
/// * `ptr` - A pointer to the Merkle root to be freed.
///
/// # Safety
///
/// Assumes that the pointer is valid and was allocated by `make_merkle_root`.
#[no_mangle]
pub unsafe extern "C" fn free_merkle_root(ptr: *mut u8) {
    unsafe {
        let _ = Box::from_raw(ptr);
    }
}
