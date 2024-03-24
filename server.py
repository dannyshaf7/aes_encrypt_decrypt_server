# Server program
# Listens at port 7777
# Receives the client's message and replies to it and closes the connection
# Continues listening
# Use Python 3 to run

import socket

# create a socket object that will listen
serverSocket = socket.socket(
   socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
# the socket will isten at port 7777
port = 7777

# bind the socket to the port
serverSocket.bind((host, port))

# start listening for requests
serverSocket.listen()

listenFlag = True
while listenFlag:
   print("Waiting for connection.....")
   # serverSocket accepts if there is a connection request
   # (note that serverSocket is listening).
   # Communictaion will be via the clientSocket
   clientSocket, addr_port = serverSocket.accept()
   # Print the address and port of the client
   # addr_port is a tuple that contains both the address and the port number
   print("Got a connection from " + str(addr_port))
   while True:
      # Receive the message from the client (receive no more than 1024 bytes)
      receivedBytes = clientSocket.recv(1024)
      # if there is no value for received bytes, no longer connected to client so break the while loop
      if not receivedBytes:
         break
      else:
         # Decode the bytes into a string (Do this only for strings, not keys)
         receivedMessage = bytes.decode(receivedBytes)
         # Print the message
         print("From client: ", receivedMessage.upper())

         # This message will be sent to the client
         message = "Hello Client from the server"
         # Encode the message into bytes
         messageBytes = message.encode()
         # Send the bytes through the client socket
         clientSocket.send(messageBytes)

