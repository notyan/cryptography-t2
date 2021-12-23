from fastapi.testclient import TestClient

from src import app


client = TestClient(app.app)


def test_rsa():

    ####################################################
    #               Keys Generation
    ####################################################

    keys_res = client.post("/rsa/generate-key")

    assert keys_res.status_code == 200

    keys = keys_res.json()
    assert "keys" in keys
    assert "public" in keys["keys"] and "public" in keys["keys"]

    ####################################################
    #             Encryption & Decryption
    ####################################################

    public_key = keys["keys"]["public"]
    private_key = keys["keys"]["private"]
    plaintext = "Some secret message that will be encrypted 0123456789"

    # Encrypt

    encryption_res = client.post("/rsa/encrypt", json={
        "message": plaintext,
        "public_key": public_key
    })

    assert encryption_res.status_code == 200

    # Decrypt

    ciphertext = encryption_res.json()["ciphertext"]

    decryption_res = client.post("/rsa/decrypt", json={
        "message": ciphertext,
        "private_key": private_key
    })

    assert decryption_res.status_code == 200

    assert decryption_res.json()["plaintext"] == plaintext
