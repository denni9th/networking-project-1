import socket

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s_port = 8000
host = "146.232.50.232"

s_socket.connect((host, s_port))
s_socket.sendall(bytes("This is from Client"))
s_socket.close()

r_port = 8001
r_socket.connect((host, r_port))

while True:
	in_data = r_socket.recv(1024)
	print "From server: ", in_data.decode()
	out_data = input()
	r_socket.sendall(bytes(out_data, "UTF-8"))
	if out_data=="bye":
		break
r_socket.close()
