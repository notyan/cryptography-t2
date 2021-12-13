SUPPORTED_ALGORITHMS = [
    "rsa",
    "ecc",
    "ntru",
]

def is_valid_algorithm(alg: str) -> bool:
    return alg in SUPPORTED_ALGORITHMS
