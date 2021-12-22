SUPPORTED_ALGORITHMS = [
    "rsa",
    "ecc",
    "ntru",
]

def is_supported(alg: str) -> bool:
    return alg in SUPPORTED_ALGORITHMS
