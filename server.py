# Server program
# Listens at port 7777
# Receives the client's message and replies to it and closes the connection
# Continues listening
# Use Python 3 to run

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket

# create a socket object that will listen
server_socket = socket.socket(
   socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
# the socket will listen at port 7777
port = 7777

# bind the socket to the port
server_socket.bind((host, port))

# start listening for requests ok
server_socket.listen()

listenFlag = True
while listenFlag:
   print("Waiting for connection.....")
   # serverSocket accepts if there is a connection request
   # (note that serverSocket is listening).
   # Communictaion will be via the clientSocket
   client_socket, addr_port = server_socket.accept()
   # Print the address and port of the client
   # addr_port is a tuple that contains both the address and the port number
   print("Got a connection from " + str(addr_port))
   key_received = client_socket.recv(1024)
   print("key received: ", key_received, "\n")
   mode_bytes = client_socket.recv(1024)
   mode_received = mode_bytes.decode().lower()
   if mode_received == "ecb":
      print("ecb mode")
      while True:
         # Receive the message from the client (receive no more than 1024 bytes)
         msg_received = client_socket.recv(1024)

         # if there is no value for received bytes, no longer connected to client so break the while loop
         if not msg_received:
            break
         else:
            cipher = AES.new(key_received, AES.MODE_ECB)
            pt_bytes = unpad(cipher.decrypt(msg_received), AES.block_size)
            received_plaintext = pt_bytes.decode()
            print("decrypted message: ", received_plaintext)
         user_input = input("Please enter a message to send to the client: "
                           "(enter 'bye' to exit)")
         message_bytes = user_input.encode(encoding="utf-8")
         cipher = AES.new(key_received, AES.MODE_ECB)
         ct_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))
         ct_string = ct_bytes.decode(encoding="utf-8", errors="ignore")
         print("key: ", key_received, "\nencrypted text: ", ct_string, "\n")
         # Send the bytes through the connection socket
         client_socket.send(ct_bytes)

   elif mode_received == "cbc":
      print("cbc mode")
      while True:
         iv_received = client_socket.recv(1024)
         print("iv received: ", iv_received)
         # Receive the message from the client (receive no more than 1024 bytes)
         msg_received = client_socket.recv(1024)
         # if there is no value for received bytes, no longer connected to client so break the while loop
         if not msg_received:
            break
         else:
            cipher = AES.new(key_received, AES.MODE_CBC, iv_received)
            pt_bytes = unpad(cipher.decrypt(msg_received), AES.block_size)
            received_plaintext = pt_bytes.decode()
            print("decrypted message: ", received_plaintext)
         user_input = input("Please enter a message to send to the client: "
                            "(enter 'bye' to exit)")
         message_bytes = user_input.encode(encoding="utf-8")
         cipher = AES.new(key_received, AES.MODE_CBC, iv_received)
         ct_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))
         ct_string = ct_bytes.decode(encoding="utf-8", errors="ignore")
         print("key: ", key_received, "\nencrypted text: ", ct_string, "\n")
         # Send the bytes through the connection socket
         client_socket.send(ct_bytes)
