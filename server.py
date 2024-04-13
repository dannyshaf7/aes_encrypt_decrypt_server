# Server program
# Listens at port 7777
# Receives the client's message and replies to it and closes the connection
# Continues listening
# Use Python 3 to run

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import math
import socket
import time


def fragment_message(message):
   frag_count = math.ceil(len(message) / 1020)
   # print("Number of fragments: ", frag_count)
   msg_length = frag_count.to_bytes(2, 'big', signed=False)
   client_socket.send(msg_length)
   time.sleep(0.01)
   byte_start = 0
   byte_end = 1020
   count = 0
   for i in range(frag_count, 0, -1):
      count_bytes = count.to_bytes(4, byteorder="big")
      frag_msg = count_bytes + message[byte_start:byte_end]
      # print(frag_msg, ";")
      count += 1
      byte_start += 1020
      byte_end += 1020
      client_socket.send(frag_msg)
      time.sleep(0.01)


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
   print("Got a connection from " + str(addr_port))

   print("Generating RSA key")
   #server generates RSA key 

   keys=RSA.generate(3072) #3072 is the suggested size according to NIST 
   #display public key
   print(keys.public_key().exportKey()) #returns the key encoded into bytes 
   #send public key 
   print("Sending RSA key")
   client_socket.send(keys.public_key().exportKey())
   time.sleep(1)

   # Print the address and port of the client
   # addr_port is a tuple that contains both the address and the port number
   
   encrypted_key_received = client_socket.recv(1024)
   print("Encrypted key received ", encrypted_key_received)
   private_key=RSA.importKey(keys.exportKey()) #Have to create RSA key
   #print("The private key is ", private_key)
   RSA_decrypt=PKCS1_OAEP.new(private_key)

   key_received= RSA_decrypt.decrypt(encrypted_key_received)

   print("decrypted key received: ", key_received, "\n")
   mode_bytes = client_socket.recv(1024)
   mode_received = mode_bytes.decode().lower()
   if mode_received == "ecb":
      while True:
         # Receive the message from the client (receive no more than 1024 bytes)
         # msg_received = client_socket.recv(1024)
         frag_num = client_socket.recv(1024)
         # print(frag_num)
         # if there is no value for received bytes, no longer connected to client so break the while loop
         # if not msg_received:
         if not frag_num:
            break
         else:
            msg_received = b''
            frag_list = []
            frag_num = int.from_bytes(frag_num, 'big', signed=False)
            # print("Number of fragments: ", frag_num)
            if frag_num > 1:
               for i in range(0, frag_num):
                  msg_received = client_socket.recv(1024)
                  # print(msg_received)
                  seq_bytes = msg_received[:4]
                  seq_num = int.from_bytes(seq_bytes, byteorder='big')
                  # print("sequence number: ", seq_num)
                  frag_list.insert(seq_num, msg_received[4:])
                  msg_received = b''
                  # print(frag_list)
               # print(frag_list)
               for j in range(0, len(frag_list)):
                  # print(j, ": ", frag_list[j])
                  msg_received += frag_list[j]
                  # print(msg_received)
               # print(msg_received)
               time.sleep(0.01)
            else:
               msg_received = client_socket.recv(1024)
            # print(msg_received)
            cipher = AES.new(key_received, AES.MODE_ECB)
            pt_bytes = unpad(cipher.decrypt(msg_received), AES.block_size)
            received_plaintext = pt_bytes.decode()
            print("decrypted message: ", received_plaintext)
         user_input = input("Please enter a message to send to the client: "
                           "(enter 'bye' to exit)")
         message_bytes = user_input.encode(encoding="utf-8")
         cipher = AES.new(key_received, AES.MODE_ECB)
         ct_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))
         # ct_string = ct_bytes.decode(encoding="utf-8", errors="ignore")
         # print("key: ", key_received, "\nencrypted text: ", ct_string, "\n")
         # Send the bytes through the connection socket
         if len(ct_bytes) > 1024:
            fragment_message(ct_bytes)
         else:
            frag_count = 1
            # print("Number of fragments: ", frag_count)
            msg_length = frag_count.to_bytes(2, 'big', signed=False)
            # print(msg_length)
            client_socket.send(msg_length)
            time.sleep(0.01)
            client_socket.send(ct_bytes)
         # client_socket.send(ct_bytes)

   elif mode_received == "cbc":
      while True:
         iv_received = client_socket.recv(1024)
         # print("iv received: ", iv_received)
         # Receive the message from the client (receive no more than 1024 bytes)
         frag_num = client_socket.recv(1024)
         # print(frag_num)
         # if there is no value for received bytes, no longer connected to client so break the while loop
         # if not msg_received:
         if not frag_num:
            break
         else:
            msg_received = b''
            frag_list = []
            frag_num = int.from_bytes(frag_num, 'big', signed=False)
            # print("Number of fragments: ", frag_num)
            if frag_num > 1:
               for i in range(0, frag_num):
                  msg_received = client_socket.recv(1024)
                  # print(msg_received)
                  seq_bytes = msg_received[:4]
                  seq_num = int.from_bytes(seq_bytes, byteorder='big')
                  # print("sequence number: ", seq_num)
                  frag_list.insert(seq_num, msg_received[4:])
                  msg_received = b''
                  # print(frag_list)
               # print(frag_list)
               for j in range(0, len(frag_list)):
                  # print(j, ": ", frag_list[j])
                  msg_received += frag_list[j]
                  # print(msg_received)
               # print(msg_received)
               time.sleep(0.01)
            else:
               msg_received = client_socket.recv(1024)
            cipher = AES.new(key_received, AES.MODE_CBC, iv_received)
            pt_bytes = unpad(cipher.decrypt(msg_received), AES.block_size)
            received_plaintext = pt_bytes.decode()
            print("decrypted message: ", received_plaintext)
         user_input = input("Please enter a message to send to the client: "
                            "(enter 'bye' to exit)")
         message_bytes = user_input.encode(encoding="utf-8")
         cipher = AES.new(key_received, AES.MODE_CBC, iv_received)
         ct_bytes = cipher.encrypt(pad(message_bytes, AES.block_size))
         # ct_string = ct_bytes.decode(encoding="utf-8", errors="ignore")
         # print("key: ", key_received, "\nencrypted text: ", ct_string, "\n")
         # Send the bytes through the connection socket
         if len(ct_bytes) > 1024:
            fragment_message(ct_bytes)
         else:
            frag_count = 1
            # print("Number of fragments: ", frag_count)
            msg_length = frag_count.to_bytes(2, 'big', signed=False)
            # print(msg_length)
            client_socket.send(msg_length)
            time.sleep(0.01)
            client_socket.send(ct_bytes)
         # client_socket.send(ct_bytes)