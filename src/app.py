from fastapi import FastAPI

from . import algorithm, request


app = FastAPI()

@app.post("/{alg}/generate-key")
def generate_key(alg: str):
    err = request.validate_algorithm(alg)
    if err is not None:
        return err

    return {
        "res": f"Key for {alg.upper()} is successfully generated"
    }

@app.post("/{alg}/encrypt")
def encrypt(alg: str):
    err = request.validate_algorithm(alg)
    if err is not None:
        return err

    return {
        "res": f"Successfully encrypting algorithm {alg}",
    }

@app.post("/{alg}/decrypt")
def decrypt(alg: str):
    err = request.validate_algorithm(alg)
    if err is not None:
        return err

    return {
        "res": f"Successfully decrypting algorithm {alg}",
    }
