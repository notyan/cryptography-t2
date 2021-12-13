from fastapi import FastAPI

from .algorithms import *
from .request import *


app = FastAPI()

@app.post("/{alg}/generate-key")
def generate_key(alg: str, req: KeyGenerationRequest):
    if not is_valid_algorithm(alg):
        msg = ( f"Unsupported algorithm: {alg}."
                f" Supported algorithms are: {', '.join(SUPPORTED_ALGORITHMS)}" )
        return {"error": msg}

    return {"req": req}
