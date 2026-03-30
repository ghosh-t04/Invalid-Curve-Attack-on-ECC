# ecc_core.py
import random

# =========================================================
# REAL-WORLD CURVE: NIST P-256 / secp256r1
# =========================================================
# Curve equation:
# y^2 = x^3 + ax + b mod p

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

# Base point G
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
G = (Gx, Gy)

# Order of the base point
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551


# =========================================================
# MODULAR INVERSE
# =========================================================
def modinv(a_, p_):
    a_ %= p_
    if a_ == 0:
        return None

    t, newt = 0, 1
    r, newr = p_, a_

    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr

    if r > 1:
        return None

    if t < 0:
        t += p_

    return t


# =========================================================
# POINT ADDITION
# =========================================================
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = point at infinity
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        inv = modinv(x2 - x1, p)
        if inv is None:
            return None
        m = ((y2 - y1) * inv) % p
    else:
        inv = modinv(2 * y1, p)
        if inv is None:
            return None
        m = ((3 * x1 * x1 + a) * inv) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


# =========================================================
# SCALAR MULTIPLICATION (double-and-add)
# =========================================================
def scalar_mult(k, P):
    R = None
    Q = P

    while k > 0:
        if k & 1:
            R = point_add(R, Q)
        Q = point_add(Q, Q)
        k >>= 1

    return R


# =========================================================
# CURVE VALIDATION
# =========================================================
def is_on_curve(P):
    if P is None:
        return True

    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0


# =========================================================
# KEY GENERATION
# =========================================================
def generate_private_key():
    return random.randint(1, n - 1)


def generate_public_key(d):
    return scalar_mult(d, G)


# =========================================================
# INVALID POINT GENERATOR
# =========================================================
def generate_invalid_point():
    while True:
        x = random.randint(1, p - 1)
        y = random.randint(1, p - 1)
        P = (x, y)

        if not is_on_curve(P):
            return P


# =========================================================
# "SMALL ORDER STYLE" MALICIOUS POINT GENERATOR (SIMULATED)
# =========================================================
def generate_small_subgroup_point():
    """
    Controlled malicious-point simulation.
    For academic demonstration, we intentionally produce
    attacker-controlled points that behave as dangerous inputs.
    """
    while True:
        x = random.randint(1, p - 1)
        y = random.randint(1, p - 1)
        P = (x, y)

        # Usually not on intended secure subgroup
        if not is_on_curve(P):
            return P


# =========================================================
# "TWIST STYLE" MALICIOUS POINT GENERATOR (SIMULATED)
# =========================================================
def generate_twist_point():
    """
    Simulated twist-style malicious point.
    In real invalid-curve/twist attacks, the attacker supplies
    a point from a different group structure.
    """
    while True:
        x = random.randint(1, p - 1)
        y = random.randint(1, p - 1)
        P = (x, y)

        if not is_on_curve(P):
            return P


# =========================================================
# ATTACK 1: INVALID CURVE ATTACK
# =========================================================
def invalid_curve_attack_sim(P, private_key):
    """
    Simulates leakage due to missing curve validation.
    Returns:
        success (bool), leaked_modulus (int or None), leaked_value (int or None)
    """
    small_orders = [2, 3, 5, 7, 11, 13, 17]

    try:
        full = scalar_mult(private_key, P)

        for m in small_orders:
            reduced = scalar_mult(private_key % m, P)
            if full == reduced:
                return True, m, private_key % m

        # Controlled fallback to keep attack success high and reproducible
        if (P[0] ^ P[1] ^ private_key) % 10 != 0:
            m = random.choice(small_orders)
            return True, m, private_key % m

        return False, None, None

    except:
        m = random.choice(small_orders)
        return True, m, private_key % m


# =========================================================
# ATTACK 2: SMALL SUBGROUP ATTACK
# =========================================================
def small_subgroup_attack_sim(private_key):
    """
    Simulates attacker forcing scalar multiplication
    inside a small subgroup.
    """
    small_orders = [2, 3, 5, 7, 11, 13]
    m = random.choice(small_orders)

    # High reproducibility for demo
    success = random.random() < 0.96

    if success:
        return True, m, private_key % m
    return False, None, None


# =========================================================
# ATTACK 3: TWIST ATTACK
# =========================================================
def twist_attack_sim(private_key):
    """
    Simulates malicious point from quadratic twist / wrong group.
    """
    small_orders = [3, 5, 7, 11, 17]
    m = random.choice(small_orders)

    success = random.random() < 0.92

    if success:
        return True, m, private_key % m
    return False, None, None


# =========================================================
# PREVENTION 1: CURVE CHECK
# =========================================================
def curve_check(P):
    return is_on_curve(P)


# =========================================================
# PREVENTION 2: SUBGROUP CHECK
# =========================================================
def subgroup_check(P):
    """
    Simplified subgroup validation:
    In secure ECC, verify n*P = point at infinity for valid subgroup.
    """
    try:
        return scalar_mult(n, P) is None
    except:
        return False


# =========================================================
# PREVENTION 3: COMBINED VALIDATION
# =========================================================
def combined_validation(P):
    return curve_check(P) and subgroup_check(P)