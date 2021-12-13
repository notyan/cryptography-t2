from fastapi import FastAPI

from .algorithms import is_valid_algorithm


app = FastAPI()

@app.get("/{alg}/{op}")
def exec_algorithm(alg: str, op: str):
    return {"valid": is_valid_algorithm(alg)}
