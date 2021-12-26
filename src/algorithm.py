from .ecc import AppECC
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
        "ecc": lambda: AppECC.generate_keys(),
        "ntru": lambda: ("", ""),
    }

    return keys_generator[alg]()


def encrypt(alg: str, message: str, pb: PublicKey) -> str:
    encryptor = {
        "rsa": lambda: AppRSA.encrypt,
        "ecc": lambda: ("", ""),
        "ntru": lambda: ("", ""),
    }

    return encryptor[alg]()(message, pb)


def decrypt(alg: str, message: str, pv: PrivateKey) -> str:
    decryptor = {
        "rsa": lambda: AppRSA.decrypt,
        "ecc": lambda: ("", ""),
        "ntru": lambda: ("", ""),
    }

    return decryptor[alg]()(message, pv)
