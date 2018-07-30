from Tkinter import *
import ttk

#key down function
def send():	
	entered_text=textentry.get()	
	output.insert(END, entered_text)
	textentry.delete(0, END)

def send_name():	
	entered_name=name.get()	
	output.insert(END, entered_name)
	name.delete(0, END)
	
def whisper():	
	entered_msg = message.get()	
	output.insert(END, entered_msg)
	message.delete(0, END)

	

window = Tk()
window.title("A really cool name")
window.configure(background="white")

Label(window, text="\nChatroom", fg="black", bg="white", font="none 12 bold") .grid(row=0, column=0, sticky=W)
output = Text(window, fg="black", bg="lightgrey", width=150, height=39, wrap=WORD)
output.grid(row=3, column=1, columnspan=1, sticky=N)
Label(window, text="Message", fg="black", bg="white", font="none 12 bold") .grid(row=4, column=1, sticky=N)

textentry = Entry(window, width=135, fg="black", bg="white", bd=5)
textentry.grid(row=5, column=1, sticky=W)
Button(window, text="Send", width=4, command=send, fg="black", bg="lightgrey") .grid(row=5, column=1, sticky=E)

names = Text(window, fg="black", bg="lightgrey", width=60, height=39, wrap=WORD)
names.grid(row=3, column=0, columnspan=2, sticky=W)
Label(window, text="Whisper to", fg="black", bg="white", font="none 12 bold") .grid(row=4, column=0, sticky=W)
name = Entry(window, width=20, fg="black", bg="white", bd=5) 
name.grid(row=5, column=0, sticky=W)
Button(window, text="OK", width=4, command=send_name, fg="black", bg="lightgrey") .grid(row=5, column=0, sticky=E)
Label(window, text="Private message", fg="black", bg="white", font="none 12 bold") .grid(row=6, column=0, sticky=W)
message = Entry(window, width=50, fg="black", bg="white", bd=5) 
message.grid(row=7, column=0, sticky=W)
Button(window, text="Whisper", width=4, command=whisper, fg="black", bg="lightgrey") .grid(row=7, column=0, sticky=E)

window.mainloop()
