# ecc_core.py

import random
import time

# Toy curve parameters
p = 233
a = 1
b = 1

# ---------------- MODULAR INVERSE ----------------
def modinv(a_, p_):
    t, newt = 0, 1
    r, newr = p_, a_ % p_
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        return None
    if t < 0:
        t += p_
    return t

# ---------------- POINT ADDITION ----------------
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        m = ((y2 - y1) * modinv(x2 - x1, p)) % p
    else:
        m = ((3 * x1 * x1 + a) * modinv(2 * y1, p)) % p

    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p

    return (x3, y3)

# ---------------- SCALAR MULTIPLICATION ----------------
def scalar_mult(k, P):
    R = None
    Q = P
    while k > 0:
        if k & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1
    return R

# ---------------- CURVE VALIDATION ----------------
def is_on_curve(P):
    if P is None:
        return True
    x, y = P
    return (y*y - (x*x*x + a*x + b)) % p == 0

# ---------------- INVALID POINT GENERATOR ----------------
def generate_invalid_point():
    while True:
        P = (random.randint(0, p-1), random.randint(0, p-1))
        if not is_on_curve(P):
            return P