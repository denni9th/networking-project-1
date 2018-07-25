# networking-project-1

The Chat Protocol:
Broadcast port 8000
 - client connects to server
 - client sends username
 - server sends user list (or error if user already exists)
 - server broadcasts messages as they are sent by clients
Message port 8001
 - client connects to server
 - client sends messages to be broadcast
 - server broadcasts messages on 8000

