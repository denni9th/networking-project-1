import socket
import json

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 8000

if __name__ == "__main__":
    socket.connect((host, port))
    socket.sendall("hanSolo")
    print json.loads(socket.recv(4096))
    socket.sendall(json.dumps({"type": "message", "data": "hello"}))
    print json.loads(socket.recv(4096))
    socket.sendall(json.dumps({"type": "whisper", "data": "hey ;)", "rcpt": "james"}))
    print json.loads(socket.recv(4096))
    socket.sendall(json.dumps({"type": "whisper", "data": "buy milk", "rcpt": "hanSolo"}))
    socket.close()

