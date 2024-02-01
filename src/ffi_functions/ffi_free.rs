use std::slice;

/// Return a simple array of 32 bytes
///
/// # Safety
///
/// This function is safe to call from FFI contexts.
#[no_mangle]
pub unsafe extern "C" fn make_array() -> *mut u8 {
    let mut array = [1u8; 32];
    array[0] = 77;
    array[31] = 77;

    // let boxed_array = array.into_boxed_slice();
    let boxed_array = Box::new(array);
    Box::into_raw(boxed_array) as *mut u8
}

/// Free array of 32 bytes
///
/// # Safety
///
/// This function is safe to call from FFI contexts.
#[no_mangle]
pub unsafe extern "C" fn free_32(ptr: *mut u8) {
    let array = unsafe { Box::from_raw(slice::from_raw_parts_mut(ptr, 32)) };

    drop(array);
}
