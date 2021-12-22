from typing import Optional

from pydantic import BaseModel

from . import algorithm


class KeyGenerationRequest(BaseModel):
    with_private_key: Optional[bool] = False


def validate_algorithm(alg: str) -> (str):
    err = None
    if not algorithm.is_supported(alg):
        supported = ', '.join(algorithm.SUPPORTED_ALGORITHMS)
        err = {"err": f"Unsupported algorithm: {alg}. Supported algorithms are: {supported}"}
    return err
