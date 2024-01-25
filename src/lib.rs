#[no_mangle]
pub unsafe extern "C" fn run() {
    println!("RUST SIDE: Hello FFI");
}
