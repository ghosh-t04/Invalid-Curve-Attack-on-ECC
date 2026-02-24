# server.py

import socket
import pickle
from ecc_core import scalar_mult, is_on_curve

PRIVATE_KEY = 37     # Secret key
VALIDATION = False  # Toggle protection

def handle_point(P):
    if VALIDATION and not is_on_curve(P):
        return "INVALID POINT BLOCKED"
    return scalar_mult(PRIVATE_KEY, P)

s = socket.socket()
s.bind(("localhost", 9999))
s.listen(1)
print("ECC Server running...")

while True:
    conn, _ = s.accept()
    P = pickle.loads(conn.recv(1024))
    Q = handle_point(P)
    conn.send(pickle.dumps(Q))
    conn.close()