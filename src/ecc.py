from dataclasses import dataclass
import binascii
import json
import math
import os
import random

from .types import PrivateKey, PublicKey


## utils

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modsqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def bytes_count_of(n: int) -> int:
    if n == 0:
        return 0
    return int(math.log(n, 256)) + 1

## Endutils


@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def is_at_infinity(self) -> bool:
        return self.x is None and self.y is None

    def dict(self):
        return {"x": self.x, "y": self.y}

    def __add__(self, other):
        return self.curve.add_point(self, other)

    def __neg__(self):
        return self.curve.neg_point(self)

    def __mul__(self, scalar: int):
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)

    def __str__(self):
        return f"{self.x} {self.y}"

    def __repr__(self):
        return self.__str__()


class Curve:
    def __init__(self, a, b, p, n, G_x, G_y):
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.G_x = G_x
        self.G_y = G_y

    def G(self) -> Point:
        return Point(self.G_x, self.G_y, self)

    def INF(self) -> Point:
        return Point(None, None, self)

    def is_on_curve(self, point: Point) -> bool:
        if point.curve != self:
            return False
        return point.is_at_infinity() or self._is_on_curve(point)

    def _is_on_curve(self, point: Point) -> bool:
        left = point.y * point.y
        right = (point.x * point.x * point.x) + (self.a * point.x) + self.b
        return (left - right) % self.p == 0

    def add_point(self, point1: Point, point2: Point) -> Point:
        if (not self.is_on_curve(point1)) or (not self.is_on_curve(point2)):
            raise ValueError("The points are not on the curve.")

        if point1.is_at_infinity():
            return point2
        elif point2.is_at_infinity():
            return point1

        if point1 == point2:
            return self._double_point(point1)
        if point1 == -point2:
            return self.INF()

        return self._add_point(point1, point2)

    def _add_point(self, point1: Point, point2: Point) -> Point:
        delta_x = point1.x - point2.x
        delta_y = point1.y - point2.y
        s = delta_y * modinv(delta_x, self.p)
        res_x = (s * s - point1.x - point2.x) % self.p
        res_y = (point1.y + s * (res_x - point1.x)) % self.p
        return - Point(res_x, res_y, self)

    def double_point(self, point: Point) -> Point:
        if not self.is_on_curve(point):
            raise ValueError("The point is not on the curve.")

        if point.is_at_infinity():
            return self.INF()

        return self._double_point(point)

    def _double_point(self, point: Point) -> Point:
        s = (3 * point.x * point.x + self.a) * modinv(2 * point.y, self.p)
        res_x = (s * s - 2 * point.x) % self.p
        res_y = (point.y + s * (res_x - point.x)) % self.p
        return -Point(res_x, res_y, self)

    def mul_point(self, d: int, point: Point) -> Point:
        if not self.is_on_curve(point):
            raise ValueError("The point is not on the curve.")

        if point.is_at_infinity() or d == 0:
            return self.INF()

        res = None
        d = abs(d)
        tmp = point

        while d:
            if d & 0x1 == 1:
                res = self.add_point(res, tmp) if res else tmp
            tmp = self.double_point(tmp)
            d >>= 1

        return -res if d < 0 else res

    def neg_point(self, point: Point) -> Point:
        if not self.is_on_curve(point):
            raise ValueError("The point is not on the curve.")
        if point.is_at_infinity():
            return self.INF()

        return self._neg_point(point)

    def _neg_point(self, point: Point) -> Point:
        return Point(point.x, -point.y % self.p, self)

    def compute_y(self, x: int) -> int:
        right = (x * x * x + self.a * x + self.b) % self.p
        y = modsqrt(right, self.p)
        return y

    def encode_point(self, plaintext: bytes) -> Point:
        plaintext = len(plaintext).to_bytes(1, byteorder="big") + plaintext
        while True:
            x = int.from_bytes(plaintext, "big")
            y = self.compute_y(x)
            if y:
                return Point(x, y, self)
            plaintext += os.urandom(1)

    def decode_point(self, point: Point) -> bytes:
        byte_len = bytes_count_of(point.x)
        plaintext_len = (point.x >> ((byte_len - 1) * 8)) & 0xff
        plaintext = ((point.x >> ((byte_len - plaintext_len - 1) * 8))
                     & (int.from_bytes(b"\xff" * plaintext_len, "big")))
        return plaintext.to_bytes(plaintext_len, byteorder="big")


curve = Curve(
    a=-3,
    b=41058363725152142129326129780047268409114441015993725554835256314039467401291,
    p=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
    n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
    G_x=0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    G_y=0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
)


class AppECC:

    @classmethod
    def generate_keys(cls) -> (PublicKey, PrivateKey):
        private_key = cls.get_private_key()
        public_key = cls.get_public_key(private_key)

        return (str(public_key), str(private_key))

    @classmethod
    def encrypt(cls, plaintext: str, pb: PublicKey) -> str:
        p1, p2 = cls.encrypt_bytes(plaintext.encode(), pb)

        return f"{p1} {p2}"

    @classmethod
    def decrypt(cls, ciphertext: str, pv: PrivateKey) -> str:
        global curve

        ct = ciphertext.split()
        assert len(ct) == 4

        p1 = Point(int(ct[0]), int(ct[1]), curve)
        p2 = Point(int(ct[2]), int(ct[3]), curve)

        return cls.decrypt_bytes(int(pv), p1, p2)

    @classmethod
    def get_private_key(cls) -> int:
        global curve

        order_bits = 0
        order = curve.n

        while order > 0:
            order >>= 1
            order_bits += 1

        order_bytes = (order_bits + 7) // 8
        extra_bits = order_bytes * 8 - order_bits

        rand = int(binascii.hexlify(os.urandom(order_bytes)), 16)
        rand >>= extra_bits
        while rand >= curve.n:
            rand = int(binascii.hexlify(os.urandom(order_bytes)), 16)
            rand >>= extra_bits

        return rand

    @classmethod
    def get_public_key(cls, d: int) -> Point:
        global curve
        return d * curve.G()

    @classmethod
    def encrypt_bytes(cls, plaintext: bytes, pb: Point) -> (Point, Point):
        global curve

        points = pb.split()
        x = int(points[0])
        y = int(points[1])
        pb = Point(x, y, curve)

        M = curve.encode_point(plaintext)

        return cls.encrypt_point(M, pb)

    @classmethod
    def encrypt_point(cls, plaintext: Point, pb: Point) -> (Point, Point):
        global curve

        G = curve.G()
        M = plaintext

        random.seed(os.urandom(1024))
        k = random.randint(1, curve.n)

        C1 = k * G
        C2 = M + k * pb

        return C1, C2

    @classmethod
    def decrypt_bytes(cls, pv: int, p1: Point, p2: Point) -> bytes:
        global curve

        M = cls.decrypt_point(pv, p1, p2)

        return curve.decode_point(M)

    @classmethod
    def decrypt_point(cls, pv: int, p1: Point, p2: Point) -> Point:
        global curve

        M = p2 + (curve.n - pv) * p1

        return M
