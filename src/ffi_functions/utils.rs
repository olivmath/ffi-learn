use tiny_keccak::{Hasher, Keccak};

/// Hashes the input data using Keccak algorithm.
///
/// # Arguments
///
/// * `data` - A slice of bytes to be hashed.
/// * `result` - A mutable array of 32 bytes where the hash result will be stored.
pub fn hash_it(data: &[u8], result: &mut [u8; 32]) {
    let mut k256 = Keccak::v256();
    k256.update(data);
    k256.finalize(result);
}
