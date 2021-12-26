from fastapi.testclient import TestClient

from src import app


client = TestClient(app.app)


def test_ecc():

    ####################################################
    #               Keys Generation
    ####################################################

    keys_res = client.post("/ecc/generate-key")

    assert keys_res.status_code == 200

    keys = keys_res.json()
    assert "keys" in keys
    assert "public" in keys["keys"] and "public" in keys["keys"]

    ####################################################
    #             Encryption & Decryption
    ####################################################

    public_key = keys["keys"]["public"]
    private_key = keys["keys"]["private"]
    plaintext = "message"

    # Encrypt

    encryption_res = client.post("/ecc/encrypt", json={
        "message": plaintext,
        "public_key": public_key
    })

    assert encryption_res.status_code == 200

    # Decrypt

    ciphertext = encryption_res.json()["ciphertext"]

    decryption_res = client.post("/ecc/decrypt", json={
        "message": ciphertext,
        "private_key": private_key
    })

    assert decryption_res.status_code == 200

    assert decryption_res.json()["plaintext"] == plaintext
