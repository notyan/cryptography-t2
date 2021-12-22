from fastapi import FastAPI, Response
import fastapi

from . import algorithm, request


app = FastAPI()

@app.post("/{alg}/generate-key", status_code=fastapi.status.HTTP_200_OK)
def generate_key(alg: str, response: Response):
    err = request.validate_algorithm(alg)
    if err is not None:
        response.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

    (pb, pv) = algorithm.get_keys(alg)

    return {
        "keys": {
            "public": pb,
            "private": pv
        }
    }

@app.post("/{alg}/encrypt", status_code=fastapi.status.HTTP_200_OK)
def encrypt(alg: str, req: request.EncryptionRequest, res: Response):
    err = request.validate_algorithm(alg)
    if err is not None:
        res.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

    err = request.validate_key_format(req.public_key)
    if err is not None:
        res.status_code = fastapi.status.HTTP_400_BAD_REQUEST
        return {"err": err}

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
