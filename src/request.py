from typing import Any, Callable, Optional

from pydantic import BaseModel

from . import algorithm


class EncryptionRequest(BaseModel):
    message: str
    public_key: str


class DecryptionRequest(BaseModel):
    message: str
    private_key: str


def run_validators(validations: list[(Callable, Any)]) -> Optional[str]:
    for v, arg in validations:
        err = v(arg)
        if err is not None:
            return err


def validate_algorithm(alg: str) -> Optional[str]:
    if not algorithm.is_supported(alg):
        supported = ', '.join(algorithm.SUPPORTED_ALGORITHMS)
        return f"Unsupported algorithm: {alg}. Supported algorithms are: {supported}"


def validate_key_format(key: str) -> Optional[str]:
    for k in key.split():
        if not k.isdigit():
            return "invalid key format"
