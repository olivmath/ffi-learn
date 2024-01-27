## Resultados do Benchmark

Os testes de benchmark foram realizados em duas categorias: "HashWithinRust" e "HashWithoutRust". Abaixo estão os resultados detalhados para cada teste.

### Benchmark: Hash Within Rust

| Name                              | Min (ms) | Max (ms) | Mean (ms) | StdDev | Median (ms) | IQR   | Outliers | OPS      | Rounds | Iterations |
|-----------------------------------|----------|----------|-----------|--------|-------------|-------|----------|----------|--------|------------|
| test_hash_1000_leaveas_within_rust | 6.8991   | 11.7571  | 8.7186    | 1.9290 | 8.1213      | 2.6341| 1;0      | 114.6975 | 5      | 1          |

### Benchmark: Hash Without Rust

| Name                                 | Min (ms) | Max (ms) | Mean (ms) | StdDev  | Median (ms) | IQR    | Outliers | OPS    | Rounds | Iterations |
|--------------------------------------|----------|----------|-----------|---------|-------------|--------|----------|--------|--------|------------|
| test_hash_1000_leaveas_without_rust  | 882.2100 | 936.9600 | 896.9821  | 22.5651 | 887.7201    | 16.5730| 1;1      | 1.1148 | 5      | 1          |

#### Legenda:

- **Outliers**: Desvios padrão da média; Intervalo interquartílico (IQR) do 1º quartil e 3º quartil.
- **OPS**: Operações por segundo, calculadas como 1 / Média.
