# server.py - chatroom server

import socket
import threading
import SocketServer
import json

host = "0.0.0.0"
port = 8000
messages = []
messages_lock = threading.Lock()
users = []
users_lock = threading.Lock()
counter = 0
counter_lock = threading.Lock()

# The handler for a connecting client
class ClientTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        global messages
        global messages_lock
        global users
        global users_lock
        global counter
        global counter_lock
        hist = []

        username = self.request.recv(1024)
        print "Connection from " + username
        if username in users:
            self.request.close()
            return

        try:
            # initate connection
            with users_lock:
                users.append(username)
            self.request.sendall(json.dumps(users))
            # main loop
            while True:
                data = json.loads(self.request.recv(1024))
                with messages_lock:
                    # process recieved data
                    if data['type'] == "message" or data['type'] == "whisper":
                        with counter_lock:
                            counter += 1
                            data['id'] = counter
                        messages.append(data)
                    # broadcast new messages
                    msgs = [i for i in messages if 
                            i not in hist and 
                            not (i['type'] == "whisper" and (i['rcpt'] != username and i['from'] != username))]
                    self.request.sendall(json.dumps([users, msgs]))
                    hist = hist + [i for i in messages if i not in hist]

                    # cleanup lists to ensure memory usage stays low
                    if len(messages) > 5:
                        i = len(messages) - 5
                        messages = messages[i:]
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

