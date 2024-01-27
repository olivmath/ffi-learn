# rustc --crate-type cdylib src/lib.rs -o lib.dylib
cargo b -r --out-dir . -Z unstable-options

python main.py