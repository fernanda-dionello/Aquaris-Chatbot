
import socket
import threading
from tkinter import *
from tkinter import messagebox
from tkmacosx import Button

class Mural():

    def __init__(self):
        
        # Open the Tkinter window
        self.Window = Tk()
        self.Window.withdraw()
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        

        # Login screen override the current Window
        self.login = Toplevel()
        self.login.title("Aquaris")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=420,height=200)
        self.login.protocol("WM_DELETE_WINDOW", self.on_closing)

        ## Login - Place a image in the Login Background 
        bg = PhotoImage(file = "ocean.png")
        label1 = Label( self.login, image = bg)
        label1.place(x = 0, y = 0)

        ## Login - Introduction text title
        self.introduction = Label(self.login,
                text="Hello! Insert your name to continue:",
                justify=CENTER,
                font="Roboto 16 bold",
                bg='#fff',
                fg='black')

        self.introduction.place(relheight=0.15, relx=0.165, rely=0.1)

        ## Login - Input Text
        self.entryName = Entry(self.login, font="Roboto 14", bg='white', highlightbackground='white', fg='black')
        self.entryName.place(relwidth=0.4, relheight=0.15, relx=0.30, rely=0.35)
        self.entryName.focus()
        self.entryName.bind('<Return>', lambda event: self.openChat(self.entryName.get()))

        ## Login - Send Button
        self.go = Button(self.login,
                text="ENTER",
                font="Roboto 14 bold",
                bg='white',
                highlightbackground='white',
                command=lambda: self.openChat(self.entryName.get()))

        self.go.place(relx=0.390, rely=0.55)

        ## Start with server connection off in Login
        self.isConnected = False
        self.PORT = 50007
        self.SERVER = "localhost"
        self.ADDRESS = (self.SERVER, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.Window.mainloop()


    # Close client connection and chat
    def on_closing(self):
      if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if self.isConnected == True:
            self.client.send('exit'.encode())
        self.client.close()
        self.Window.destroy()
 
    # Close Login window and open the chat
    def openChat(self, name):
        self.login.destroy()

        # open cliente connection with server
        self.client.connect(self.ADDRESS)
        self.isConnected = True

        # shows chat interface
        self.chat(name)

        # create a Thread that allows the Client receive messages
        self.rcv = threading.Thread(target=self.receive) 
        self.rcv.start()
 
    # Chat interface
    def chat(self, name):

        # Chat Window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=600, height=620, bg="#17202A")

        # Chat Header
        self.name = name
        self.header = Label(self.Window, bg="#17202A", fg="#EAECEE", text=f"{self.name}", font="Helvetica 13 bold", pady=5)
        self.header.place(relwidth=1)
        
        # Chat Body
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.05)
        self.windowText = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.windowText.place(relheight=0.810, relwidth=1, rely=0.08)
        self.windowText.config(cursor="arrow")
        self.windowText.config(state=DISABLED)

        ## Chat Scrollbar
        scrollbar = Scrollbar(self.windowText)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.windowText.yview)

        # Chat Footer
        self.footer = Label(self.Window, bg="#ABB2B9", height=80)
        self.footer.place(relwidth=1, rely=0.890)

        ## Chat Input Message
        self.entryText = Entry(self.footer, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryText.bind('<Return>', lambda event: self.sendButton(self.entryText.get()))
        self.entryText.place(relwidth=0.74, relheight=0.03, rely=0.008, relx=0.011)
        self.entryText.focus()
 
        ## Chat Send Text Button
        self.sendMessageButton = Button(self.footer, text="Send", font="Roboto 14 bold", width=20, bg="#fff", highlightbackground="#fff", command=lambda: self.sendButton(self.entryText.get()))
        self.sendMessageButton.place(relx=0.77, rely=0.008, relheight=0.03, relwidth=0.22)
  
    # Create the thread that allows to send messages
    def sendButton(self, msg):
        self.windowText.config(state=DISABLED)
        self.msg = msg
        self.entryText.delete(0, END)
        self.snd = threading.Thread(target=self.sendMessage()) 
        self.snd.start()
 
    # Function that is call by Thread that receives message
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message != 'SendMeTheName#':

                    # insert messages in window chat
                    self.windowText.config(state=NORMAL)
                    self.windowText.insert(END, f'''
                                    {message}''')

                    self.windowText.config(state=DISABLED)
                    self.windowText.see(END)
                else:
                    self.client.send(self.name.encode())
            except:
                self.isConnected = False
                self.client.close()
                break
 
    # Function that is call by Thread that sends message
    def sendMessage(self):
        self.windowText.config(state=DISABLED)
        self.windowText.config(state=NORMAL)
        self.windowText.insert(END, f'''
                                <{self.name}> {self.msg}''')
        self.windowText.config(state=DISABLED)
        self.windowText.see(END)

        print(f"<{self.name}>", self.msg)
        self.client.send(self.msg.encode())

# Create Mural/Client instance
mural = Mural()