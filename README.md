# Estudo

- [x] Chamar uma funcao rust do tipo () -> (): apenas print
- [x] Chamar uma funcao rust do tipo (list[bytes], int) -> (): apenas print
- [x] Chamar uma funcao rust do tipo (list[bytes], int) -> (): que processa esses dados com um crate de terceiros
- [x] Chamar uma funcao rust do tipo (list[bytes], int, callback) -> (): que processa esses dados com uma funcao python em rust
- [x] Chamar uma funcao rust do tipo (list[bytes], int, callback) -> bytes: que processa esses dados e devolve um hash bytes 32
- [x] Chamar uma funcao rust do tipo (list[bytes], int, callback) -> list[bytes]: que processa esses dados e devolve um array de 33 bytes sendo 32 o hash e 1 a flag

# Como isso funciona?

## Python

- Cada função está encapsulada dentro de uma classe
- Todas classe estão encapsuladas na classe Lib

## Rust

- Cada módulo tem um única função
