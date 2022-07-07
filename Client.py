import socket
import select
import sys

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def startConnection(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.host, self.port))

        while True:
            sockets_list = [sys.stdin, server]
            message = ''
            read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == server:
                    message = socks.recv(2048).decode()
                    print(message)
                else:
                    message = sys.stdin.readline()
                    server.send(message.encode())
            if message.lower().rstrip() == '5':
                break
        server.close()

client = Client("localhost", 50007)
client.startConnection()