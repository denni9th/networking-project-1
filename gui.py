from Tkinter import *
import ttk

#key down function
def click():
	
	entered_text=textentry.get()	
	output.insert(END, entered_text)
	textentry.delete(0, END)
	

window = Tk()
window.title("A really cool name")
window.configure(background="white")

Label(window, text="\nChatroom", fg="black", bg="white", font="none 12 bold") .grid(row=0, column=0, sticky=W)
output = Text(window, fg="black", bg="lightgrey", width=160, height=39, wrap=WORD)
output.grid(row=3, column=0, columnspan=2, sticky=W)

textentry = Entry(window, width=137, fg="black", bg="white", bd=5)
textentry.grid(row=4, column=0, sticky=W)
Button(window, text="Send", width=4, command=click, fg="black", bg="lightgrey") .grid(row=4, column=0, sticky=E)

window.mainloop()
