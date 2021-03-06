from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import fastapi

from . import algorithm, request


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/{alg}/generate-key", status_code=fastapi.status.HTTP_200_OK)
def generate_key(alg: str, res: Response):
    err = request.validate_algorithm(alg)
    if err is not None:
        res.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

    pb, pv = algorithm.get_keys(alg)

    return {
        "keys": {
            "public": pb,
            "private": pv
        }
    }

@app.post("/{alg}/encrypt", status_code=fastapi.status.HTTP_200_OK)
def encrypt(alg: str, req: request.EncryptionRequest, res: Response):
    err = request.run_validators([
        (request.validate_algorithm, alg),
        (request.validate_key_format, req.public_key)
    ])

    if err is not None:
        res.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

    return {
        "algorithm": alg,
        "ciphertext": algorithm.encrypt(alg, req.message, req.public_key),
    }

@app.post("/{alg}/decrypt", status_code=fastapi.status.HTTP_200_OK)
def decrypt(alg: str, req: request.DecryptionRequest, res: Response):
    err = request.run_validators([
        (request.validate_algorithm, alg),
        (request.validate_key_format, req.private_key)
    ])

    if err is not None:
        res.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

    return {
        "algorithm": alg,
        "plaintext": algorithm.decrypt(alg, req.message, req.private_key),
    }
