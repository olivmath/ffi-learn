#[no_mangle]
pub unsafe extern "C" fn run1() {
    println!("RUST SIDE: Hello FFI");
}
