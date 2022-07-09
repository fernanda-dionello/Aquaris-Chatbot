import socket
from _thread import *

class Bot():

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.__clientsActive = []
		self.__clientsInTheChat = []
		self.__numberOfConnectionsAllowed = 100
	

	############### AUXILIAR FUNCTIONS ##################

	def addClientsOnlineInChat(self, connection):
		self.__clientsInTheChat.append(connection)
	
	def removeClientsOnlineInChat(self, connection):
		self.__clientsInTheChat.remove(connection)
	
	def removeClientsConnected(self, connection):
		self.__clientsActive.remove(connection)

	def quantityClientsOnlineInChat(self):
		return len(self.__clientsInTheChat)

	def validateMessage(self, clientMessage, connection):
		try:
			if clientMessage == 'exit':
				self.stopConnection(connection)
			choice = int(clientMessage)
			if 0 <= choice <= 4: # <= 5 if without GUI
				match choice:
					case 0: return self.aboutAquaris(connection)
					case 1: return self.showTeachers(connection)
					case 2: return self.classSchedules(connection)
					case 3: return self.contactInfo(connection)
					case 4: return self.talkOnline(connection)
					# case 5: return self.stopConnection(connection)
			else:
				self.invalidMessage(connection)
		except:
			self.invalidMessage(connection)

	############### START AND CLOSE CONNECTIONS ##################

	def startBot(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.host, self.port))
		server.listen(self.__numberOfConnectionsAllowed) #it allows 100 active connections

		while True:
			connection, id = server.accept()
			self.__clientsActive.append(connection)

			# show the user connected
			print(id, "connected")
			print("Clients connected: ", len(self.__clientsActive))

			# For each user is create a thread
			start_new_thread(self.clientConnection,(connection,id))

	def clientConnection(self, connection, id):
		connection.send(self.firstMessage().encode())
		while True:
				try:
					connection.send(self.menu().encode())
					clientMessage = connection.recv(1024).decode()

					if clientMessage:
						self.validateMessage(clientMessage.rstrip(), connection)
						# if clientMessage.rstrip() == '5':
						# 	break
					else:
						print('fimm')
						self.stopConnection(connection)
				except:
					continue
	
	def broadcast(self, message, connection):
		for client in self.__clientsInTheChat:
			if client != connection:
				try:
					client.send(message.encode())
				except:
					self.stopConnection(client)
	
	def stopConnection(self, connection):
		if connection in self.__clientsActive:
			connection.close()
			self.removeClientsConnected(connection)


	############### MESSAGES ##################

	def firstMessage(self):
		return '''
		Welcome to AQUIRIS SWIMMING CLUB!
		'''
	
	def menu(self):
		return '''
		=======================================
		SWIMMING CLUB - AQUARIS
		=======================================
		0-	About Aquaris
		1-	Meet the Teachers
		2-	Class Schedules
		3-	Contact Info
		4-	Talk with students [ONLINE]
		
		Close Session, pressing X button
		========================================

		Place the number of your choice: ''' # 5-	Close Session
	
	def invalidMessage(self, connection):
		message = '''
		Invalid choice, try again a number between 0 and 4.
		'''
		connection.send(message.encode()) #or 5, without GUI
	
	def aboutAquaris(self, connection):
		message = '''
		The Aquaris swimming school was founded in 2000
		and offers swimming lessons for children, youth,
		adults and seniors. The structure has 5 swimming
		pools, 1 of which is Olympic. Aquaris is federated,
		and participates in state and national championships!
		'''
		connection.send(message.encode())
	
	def showTeachers(self, connection):
		message = '''
		=====================================
		TEACHERS
		=====================================
		1-	Fabiane Silva
			* Adults and Seniors
		2-	Marcos Andrade
			* Children
		3-	Cassiane Pereira
			* Children and Youth
		4-	Juliano Rocha
			* Adults and Youth
		5-	Bruna Ferreira
			* Seniors
		6-	Carlos Trindade
			* Adults and Youth
		=====================================
		'''
		connection.send(message.encode())
	
	def classSchedules(self, connection):
		message = '''
		===============================================
		CLASS SCHEDULES
		===============================================
		MONDAY
		-----------------------------------------------
		9AM / 10AM - Fabiane Silva (Adults - Pool 1)
		10AM / 11AM - Fabiane Silva (Seniors - Pool 2)
		2PM / 3PM - Marcos Andrade (Children - Pool 3)
		4PM / 5PM - Cassiane Pereira (Youth - Pool 4)
		6PM / 7PM - Carlos Trindade (Youth - Olimpic)
		7PM / 8PM - Juliano Rocha (Adults - Pool 1)

		TUESDAY
		-----------------------------------------------
		9AM / 10AM - Bruna Ferreira (Seniors - Pool 2)
		10AM / 11AM - Juliano Rocha (Youth - Pool 4)
		2PM / 3PM - Cassiane Pereira (Children - Pool 3)
		4PM / 5PM - Carlos Trindade (Youth - Olimpic)
		6PM / 7PM - Carlos Trindade (Adults - Olimpic)
		7PM / 8PM - Fabiane Silva (Adults - Pool 1)

		WEDNESDAY
		-----------------------------------------------
		9AM / 10AM - Fabiane Silva (Adults - Pool 1)
		10AM / 11AM - Fabiane Silva (Seniors - Pool 2)
		2PM / 3PM - Marcos Andrade (Children - Pool 3)
		4PM / 5PM - Cassiane Pereira (Youth - Pool 4)
		6PM / 7PM - Carlos Trindade (Youth - Olimpic)
		7PM / 8PM - Juliano Rocha (Adults - Pool 1)

		THURSDAY
		-----------------------------------------------
		9AM / 10AM - Bruna Ferreira (Seniors - Pool 2)
		10AM / 11AM - Juliano Rocha (Youth - Pool 4)
		2PM / 3PM - Cassiane Pereira (Children - Pool 3)
		4PM / 5PM - Carlos Trindade (Youth - Olimpic)
		6PM / 7PM - Carlos Trindade (Adults - Olimpic)
		7PM / 8PM - Fabiane Silva (Adults - Pool 1)   

		===============================================
		'''
		connection.send(message.encode())
	
	def contactInfo(self, connection):
		message = '''
		Telephone: +16175551212
		Whatsapp: +16175551214
		Email: aquaris@gmail.com
		'''
		connection.send(message.encode())
	
	def joinedTheChat(self, connection, username, quantityOnlineinChat):
		message = f'''
		Hey {username} you are in the chat now,{quantityOnlineinChat}!
		If you want leave the room write EXIT.
		'''
		connection.send(message.encode())
	
	def adviseUserJoinedChat(self, username):
		return f'''
		{username} joined the chat!
		'''
	
	def messageReceivedInChat(self, username, clientMessageForAll):
		return f'''
		<{username}> {clientMessageForAll}
		'''
	
	def messageLeftTheRoom(self, username):
		return f'''
		{username} left the room.
		'''

	def talkOnline(self, connection):
		self.addClientsOnlineInChat(connection)
		connection.send('SendMeTheName#'.encode())
	
		while True:
			try:
				clientMessage = connection.recv(1024).decode()
				if clientMessage:
					username = clientMessage.rstrip()

					if self.quantityClientsOnlineInChat() == 1:
						quantityOnlineinChat =' but it is just you online'
					else:
						quantityOnlineinChat = f' with more {self.quantityClientsOnlineInChat() - 1} people'

					self.joinedTheChat(connection, username, quantityOnlineinChat)					
					self.broadcast(self.adviseUserJoinedChat(username), connection)

					while True:
						try:
							clientMessageForAll = connection.recv(1024).decode()
							if clientMessageForAll:
								if clientMessageForAll.lower().rstrip() == 'exit':
									self.broadcast(self.messageLeftTheRoom(username), connection)
									self.removeClientsOnlineInChat(connection)
									break
								self.broadcast(self.messageReceivedInChat(username, clientMessageForAll), connection)
						except:
							self.removeClientsConnected(connection)
							self.removeClientsOnlineInChat(connection)
							break
					break
			except:
				self.removeClientsConnected(connection)
				break
	
	#server.close()
serverHost = "localhost"
serverPort = 50007

bot = Bot(serverHost, serverPort)
bot.startBot()