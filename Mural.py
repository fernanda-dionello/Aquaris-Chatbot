# import all the required  modules
import socket
import threading
from tkinter import *
from tkinter import messagebox
 
# import all functions /
#  everything from chat.py file
# from Bot import *
 
PORT =50007
SERVER = "localhost"
ADDRESS = (SERVER, PORT)
 
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
 
 
# GUI class for the chat
class GUI():
    # constructor method
    def __init__(self):
        
        # chat window which is currently hidden
        self.Window = Tk()
        # self.Window.withdraw()
        self.goAhead()
 
        # self.go.place(relx=0.4,
        #               rely=0.55)

        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Window.mainloop()
    
    def on_closing(self):
      # self.rcv.stop()
      if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client.send('exit'.encode())
        client.close()
        self.Window.destroy()
 
    def goAhead(self):
        self.layout()
 
        # the thread to receive messages
        self.rcv = threading.Thread(target=self.receive) 
        self.rcv.start()
 
    # The main layout of the chat
    def layout(self):
 
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=True)
        self.Window.configure(width=600,
                              height=620,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text="AQUARIUS",
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        self.entryMsg.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        self.snd = threading.Thread(target=self.sendMessage) 
        self.snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode()
                # insert messages to text box
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END,
                                      message+"\n\n")

                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
            except:
                client.close()
                break
 
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        message = (self.msg)
        client.send(message.encode())
 
 
# create a GUI class object
g = GUI()