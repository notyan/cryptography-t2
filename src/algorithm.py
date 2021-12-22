from .rsa import AppRSA
from .types import PublicKey, PrivateKey


SUPPORTED_ALGORITHMS = [
    "rsa",
    "ecc",
    "ntru",
]


def is_supported(alg: str) -> bool:
    return alg in SUPPORTED_ALGORITHMS


def get_keys(alg: str) -> (PublicKey, PrivateKey):
    keys_generator = {
        "rsa": lambda: AppRSA.generate_keys(),
        "ecc": lambda: ("", ""),
        "ntru": lambda: ("", ""),
    }

    return keys_generator[alg]()
