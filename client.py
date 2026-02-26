import socket
import pickle

def send_point(P):
    s = socket.socket()
    s.connect(("localhost", 9999))
    s.send(pickle.dumps(P))
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)