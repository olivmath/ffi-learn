/// Prints a hello message from the Rust side.
///
/// # Safety
///
/// This function is safe to call from FFI contexts.
#[no_mangle]
pub unsafe extern "C" fn print_hello() {
    println!("RUST SIDE: Hello FFI");
}
