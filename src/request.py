from typing import Optional

from pydantic import BaseModel

from . import algorithm


class EncryptionRequest(BaseModel):
    message: str
    public_key: str

    def get_e(self):
        self.public_key.split()[0]

    def get_n(self):
        self.public_key.split()[1]


def validate_algorithm(alg: str) -> Optional[str]:
    if not algorithm.is_supported(alg):
        supported = ', '.join(algorithm.SUPPORTED_ALGORITHMS)
        return f"Unsupported algorithm: {alg}. Supported algorithms are: {supported}"


def validate_key_format(key: str) -> Optional[str]:
    key = key.split()
    if len(key) != 2 or not key[0].isdigit() or not key[1].isdigit():
        return "invalid key format"
