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
    keysize = sys.argv[0]
    if (keysize.equals("128") or keysize.equals("192") or keysize.equals("256")):
        aes_key = get_random_bytes(int(keysize))
        # hmac_key = get_random_bytes(16)
        #Generate the AES key
        cipher = AES.new(aes_key, AES.MODE_ECB)
        #Display the key on the client window
        print("The key that was generated was: "+cipher)
        sendCipher=bytes.encode(cipher)
        #Sending the key to the server
        clientSocket.send(sendCipher)


        while (message != "bye"):  # Keeps going until the client enters bye
            # print("The message:", message, "and bye is") helped with decoding
            # print((message != "bye")) decoding message
            messageBytes = str.encode(message)  # converting message to bytes
            clientSocket.send(messageBytes)  # Sends the message in bytes
            messageFromServerBytes = clientSocket.recv(1024)
            print("Received", bytes.decode(messageFromServerBytes), "from", (serverName, serverPort))
            message = input("Enter a message: ")  # Updates the while loop
    else:
        print("There was an error in creating your AES key with the key size given. Please try either 128, 192, or 256.")

elif (mode.equals("cbc")):
    keysize = sys.argv[0]
    if (keysize.equals("128") or keysize.equals("192") or keysize.equals("256")):
        aes_key = get_random_bytes(int(keysize))
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
        messageBytes = str.encode(message)  # converting message to bytes
        clientSocket.send(messageBytes)  # Sends the message in bytes
        messageFromServerBytes = clientSocket.recv(1024)
        print("Received", bytes.decode(messageFromServerBytes), "from", (serverName, serverPort))
        message = input("Enter a message: ")  # Updates the while loop

else:
    print("There was an error in creating your AES key with the mode given. Please try either ecb or cbc.")

print("Client is disconnecting")
clientSocket.close()



