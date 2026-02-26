from ecc_core import generate_invalid_point, scalar_mult
from client import send_point

PRIVATE_KEY = 37

def detect_leak(P):
    seen = set()
    for i in range(1, 20):
        Q = scalar_mult(i, P)
        if Q in seen:
            return True
        seen.add(Q)
    return False

def run_tests(n=25):
    leaked = 0
    for _ in range(n):
        P = generate_invalid_point()
        if detect_leak(P):
            leaked += 1
    return leaked, n

if __name__ == "__main__":
    l, t = run_tests()
    print(f"Leakage before fix: {(l/t)*100:.2f}%")