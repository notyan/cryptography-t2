import math
import random

import sympy

from .types import PublicKey, PrivateKey


def get_rand_prime():
    primes = list(sympy.primerange(100, 300))
    return random.choice(primes)


def multiplicative_inverse(e, phi):
    for i in range(phi):
        if (e * i) % phi == 1:
            return i


class AppRSA:

    @classmethod
    def generate_keys(cls) -> (PublicKey, PrivateKey):
        p, q = AppRSA.get_p_and_q()
        n = p * q
        phi = (p - 1) * (q - 1)

        e, d = AppRSA.get_e_and_d(phi)

        pb_key_str = f"{e} {n}"
        pv_key_str = f"{d} {n}"

        return (pb_key_str, pv_key_str)

    @classmethod
    def encrypt(cls, plaintext: str, pb: PublicKey) -> str:
        key = int(pb.split()[0])
        n = int(pb.split()[1])
        enc_res = [(ord(char) ** key) % n for char in plaintext]

        return "".join(map(lambda c: str(c), enc_res))

    @classmethod
    def get_p_and_q(cls) -> (int, int):
        p = get_rand_prime()
        q = get_rand_prime()
        while p == q:
            q = get_rand_prime()

        return (p, q)

    @classmethod
    def get_e_and_d(cls, phi: int) -> (int, int):
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = math.gcd(e, phi)
        d = multiplicative_inverse(e, phi)

        return (e, d)
