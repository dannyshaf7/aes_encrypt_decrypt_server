# Server program
# Listens at port 7777
# Receives the client's message and replies to it and closes the connection
# Continues listening
# Use Python 3 to run

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import socket
import sys

serverName="localhost"
serverPort=12000
clientSocket=socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
#message=input("Enter a message: ")
#while (message != "bye"): #Keeps going until the client enters bye

mode=sys.argv[1].lower()
if (mode.equals("ecb")):
    keysize = sys.arv[0]
    aes_key = get_random_bytes(keysize)
    # hmac_key = get_random_bytes(16)
    cipher = AES.new(aes_key, AES.MODE_CBC)
    decryptedBytes = cipher.decrypt(receivedBytes)
    # Decode the bytes into a string (Do this only for strings, not keys)
    receivedMessage = bytes.decode(decryptedBytes)
    # Print the message
    print("From client: ", receivedMessage.upper())
    cipherBytes = cipher.encrypt(messageBytes)
    # hmac = HMAC.new(hmac_key, digestmod=SHA256)
    # tag = hmac.update(cipher.nonce + ciphertext).digest()
    # Send the bytes through the client socket

    clientSocket.send(cipherBytes)
    messageBytes=str.encode(message) #converting message to bytes
    clientSocket.send(messageBytes) #Sends the message in bytes
    messageFromServerBytes=clientSocket.recv(1024)
    print("Received",bytes.decode(messageFromServerBytes),"from",(serverName,serverPort))
    message=input("Enter a message: ") #Updates the while loop
elif (mode.equals("cbc")):

else:
    print("")

print("Client is disconnecting")
clientSocket.close()



