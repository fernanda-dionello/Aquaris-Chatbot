
import socket
import threading
from tkinter import *
from tkinter import messagebox
 
PORT =50007
SERVER = "localhost"
ADDRESS = (SERVER, PORT)
 
# Create a new client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDRESS)
 
 

class Mural():

    def __init__(self):
        #Open the Tkinter window
        self.Window = Tk()
        self.Window.withdraw()

        #Login screen override the current Window
        self.login = Toplevel()
        self.login.title("Aquaris")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=420,height=200)

        self.introduction = Label(self.login,
                text="Hello! Insert your name to continue:",
                justify=CENTER,
                font="Roboto 16 bold")
        self.introduction.place(relheight=0.15,
            relx=0.2,
            rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                text="Name: ",
                font="Roboto 12")

        self.labelName.place(relheight=0.2,
                relx=0.1,
                rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                font="Roboto 14",
                )
        self.entryName.place(relwidth=0.4,
                relheight=0.15,
                relx=0.32,
                rely=0.35)
        # set the focus of the cursor
        self.entryName.focus()
        

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                text="CONTINUE",
                font="Helvetica 14 bold",
                command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
            rely=0.55)
        
        # self.rcvLogin = threading.Thread(target=self.receive) 
        # self.rcvLogin.start()

        self.entryName.bind('<Return>', lambda event: self.goAhead(self.entryName.get()))
        self.isConnected = False

        # self.goAhead()
        self.login.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Window.mainloop()
    
    def on_closing_login(self):
      if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client.close()
        self.login.destroy()
        self.Window.destroy()

    def on_closing(self):
      if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if self.isConnected == True:
            client.send('exit'.encode())
        client.close()
        self.Window.destroy()
 
    def goAhead(self, name):
        self.login.destroy()

        client.connect(ADDRESS)
        self.isConnected = True

        self.layout(name)
 
        # the thread to receive messages
        self.rcv = threading.Thread(target=self.receive) 
        self.rcv.start()
 
    def layout(self, name):
        
        self.name = name
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
                               text=f"{self.name}",
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

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        self.snd = threading.Thread(target=self.sendMessage()) 
        self.snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode()
                if message != 'SendMeTheName#':
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, f'''
                                    {message}''')

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
                else:
                    client.send(self.name.encode())
            except:
                self.isConnected = False
                client.close()
                break
 
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        print(f"<{self.name}>", self.msg)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, f'''
                                <{self.name}> {self.msg}''')

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        client.send(self.msg.encode())
 

mural = Mural()