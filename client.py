import socket
import json

b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

b_port = 8000
m_port = 8001
host = "146.232.50.232"

b_socket.connect((host, b_port))
m_socket.connect((host, m_port))

try:
    b_socket.send("hanSolo")
    users = json.loads(b_socket.recv(4096))
    print users
finally:
    b_socket.close()
    m_socket.close()

