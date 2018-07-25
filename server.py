# server.py - chatroom server

import socket
import threading
import SocketServer
import json

host = "146.232.50.232"
b_port = 8000
m_port = 8001
lock = threading.Lock()
messages = []
users = []

# The handler for a connecting client
# Broadcasts any user changes and messages in the message queue
class BroadcastTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        username = self.request.recv(1024)
        print "Connection from " + username
        self.request.sendall(json.dumps(users))

# Receives messages from clients and adds them to message send queue
class MessagesTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    b_server = ThreadedTCPServer((host, b_port), BroadcastTCPRequestHandler)
    m_server = ThreadedTCPServer((host, m_port), MessagesTCPRequestHandler)
    print "Starting server on " + host + ", ports " + str(b_port) + " and " + str(m_port)
    b_server_thread = threading.Thread(target=b_server.serve_forever)
    m_server_thread = threading.Thread(target=m_server.serve_forever)
    b_server_thread.start()
    m_server_thread.start()

