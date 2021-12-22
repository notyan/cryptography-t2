from fastapi import FastAPI

from . import algorithm
#from .request import *


app = FastAPI()

@app.post("/{alg}/generate-key")
def generate_key(alg: str):
    if not algorithm.is_supported(alg):
        supported = ', '.join(algorithm.SUPPORTED_ALGORITHMS)
        return {"error": f"Unsupported algorithm: {alg}. Supported algorithms are: {supported}"}

    return {"res": f"Key for {alg.upper()} is successfully generated"}
