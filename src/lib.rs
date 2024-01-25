use std::slice;

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
pub unsafe extern "C" fn run2(leaves_ptr: *mut *mut u8, len_leaves: usize) {
    let leaves = unsafe { slice::from_raw_parts(leaves_ptr, len_leaves) }
        .iter()
        .map(|leaf_ptr| unsafe { slice::from_raw_parts(*leaf_ptr, 32).to_vec() })
        .collect::<Vec<Vec<u8>>>();

    for leaf in leaves {

        println!("RUST SIDE: {leaf:?}");
    }

    
}
