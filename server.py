# server.py - chatroom server

import socket
import threading
import SocketServer

host = "146.232.50.232"
sport = 8000
rport = 8001
lock = threading.Lock()
messages = []
users = []

# The handler for a connecting client
# Broadcasts any user changes and messages in the message queue
class MessageSendTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        username = self.request.recv(1024)
        print "Connection from " + username
        self.request.sendall(json.dumps(users))

# Receives messages from clients and adds them to message send queue
class MessageRecvTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    sserver = ThreadedTCPServer((host, sport), MessageSendTCPRequestHandler)
    rserver = ThreadedTCPServer((host, rport), MessageRecvTCPRequestHandler)
    print "Starting server on " + host + ", ports " + str(sport) + " and " + str(rport)
    sserver_thread = threading.Thread(target=sserver.serve_forever)
    rserver_thread = threading.Thread(target=rserver.serve_forever)
    sserver_thread.start()
    rserver_thread.start()

