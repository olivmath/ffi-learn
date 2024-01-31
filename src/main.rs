mod ffi_functions;
use ffi_functions::ffi_print::print_hello;

fn main() {
    unsafe {
        print_hello();
    }
}
