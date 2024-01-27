cargo b -r --out-dir . -Z unstable-options
mv libffi_learn.dylib  libbenchmark.dylib

pytest