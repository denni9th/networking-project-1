# server.py - chatroom server

import socket
import threading
import SocketServer
import json

host = "localhost"
port = 8000
messages = []
messages_lock = threading.Lock()
users = []
users_lock = threading.Lock()

# The handler for a connecting client
class ClientTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        global messages
        global messages_lock
        global users
        global users_lock
        hist = []

        username = self.request.recv(1024)
        print "Connection from " + username

        try:
            # initate connection
            with users_lock:
                if username in users: 
                    self.request.sendall(json.dumps({"err": "username taken"}))
                    return
                users.append(username)
            self.request.sendall(json.dumps({"usrs": users}))
            # main loop
            while True:
                data = json.loads(self.request.recv(1024))
                with messages_lock:
                    # process recieved data
                    if data['type'] == "message" or data['type'] == "whisper":
                        messages.append(data)
                    # broadcast new messages
                    msgs = [i for i in messages if i not in hist and not (i['type'] == "whisper" and i['rcpt'] != username)]
                    self.request.sendall(json.dumps({"usrs": users, "msgs": msgs}))
                    hist = hist + [i for i in messages if i not in hist]

                    # cleanup lists to ensure memory usage stays low
                    if len(messages) > 50:
                        messages = [(len(messages) - 50):]
                    hist = [i for i in hist if i in messages]
        
        except ValueError:
            print "User " + username + " disconnected"
        finally:
            with users_lock:
                users.remove(username)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    server = ThreadedTCPServer((host, port), ClientTCPRequestHandler)
    print "Starting server on " + host + ", port " + str(port)
    server.serve_forever()

