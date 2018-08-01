from Tkinter import *
import ttk
import tkSimpleDialog
import socket
import json
import threading

host = "localhost"
port = 8000

message = {}
message_lock = threading.Lock()
users = []
username = ""

running = True

def connection_loop():
    global message
    global host
    global username
    global sock
    global running

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(username)
        users = json.loads(sock.recv(4096))
        for u in users:
            namesbox.insert(END, u)
        while running == True:
            with message_lock:
                if message != {}:
                    sock.sendall(json.dumps(message))
                    message = {}
                else:
                    sock.sendall(json.dumps({"type": "null"}))
            data = json.loads(sock.recv(4096))
            for m in data[1]:
                if m['type'] == "message":
                    output.insert(END, m['from'] + ": " + m['data'] + "\n")
                elif m['type'] == "whisper":
                    output.insert(END, m['from'] + " whispers: " + m['data'] + "\n")
            if data[0] != users:
                if len(data) > len(users):
                    #connected
                    output.insert(END, "The following users are now online: ")
                    for i in data[0]:
                        if i not in users:
                            output.insert(END, i)
                    output.insert(END, "\n")
                else:
                    #disconnected
                    output.insert(END, "The following users are now offline: ")
                    for i in users:
                        if i not in data[0]:
                            output.insert(END, i)
                    output.insert(END, "\n")
                users = data[0]
                namesbox.delete(0,'end')
                for u in users:
                    namesbox.insert(END, u)
    except ValueError:
        print "Server disconnected you" #TODO popup
    except socket.error:
        print "Error connecting to server" #TODO popup
    finally:
        sock.close()

def send_message():
    global message
    global username
    while message != {}: continue
    with message_lock:
        message = {"type": "message", "data": textentry.get(), "from": username}
    textentry.delete(0, END)

def send_whisper():
    global message
    global username
    while message != {}: continue
    with message_lock:
        message = {"type": "whisper", "data": messagew.get(), "from": username, "rcpt": namesbox.get(namesbox.curselection())}
    messagew.delete(0, END)

window = Tk()

window.title("A really cool name")
window.configure(background="white")

Label(window, text="\nChatroom", fg="black", bg="white", font="none 12 bold") .grid(row=0, column=0, sticky=W)
output = Text(window, fg="black", bg="lightgrey", width=130, height=39, wrap=WORD)
output.grid(row=3, column=1, columnspan=1, sticky=N)
Label(window, text="Message", fg="black", bg="white", font="none 12 bold") .grid(row=4, column=1, sticky=N)

textentry = Entry(window, width=100, fg="black", bg="white", bd=5)
textentry.grid(row=5, column=1, sticky=N)
Button(window, text="Send", width=4, command=send_message, fg="black", bg="lightgrey") .grid(row=5, column=1, sticky=E)

namesbox = Listbox(window)
namesbox.config(relief=SUNKEN, width=40)
namesbox.grid(row=3, column=0 ,sticky=N)

Label(window, text="Private message", fg="black", bg="white", font="none 12 bold") .grid(row=4, column=0, sticky=W)
messagew = Entry(window, width=35, fg="black", bg="white", bd=5) 
messagew.grid(row=5, column=0, sticky=W)
Button(window, text="Whisper", width=4, command=send_whisper, fg="black", bg="lightgrey") .grid(row=5, column=0, sticky=E)

host = tkSimpleDialog.askstring("Host", "Enter hostname:", parent=window)
username = tkSimpleDialog.askstring("Username", "Enter username:", parent=window) 

thread = threading.Thread(target=connection_loop)
thread.start()
try:
    window.mainloop()
except TclError:
    print "Select a user to whisper to" #TODO popup
running = False

