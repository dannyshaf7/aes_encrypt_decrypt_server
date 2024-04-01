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

if (sys.argv[1].isalpha()):
    mode=sys.argv[1].lower()
    if (mode.equals("ecb")):
        if sys.argv[0].isdigit():
            keysize = sys.argv[0]
            if (keysize.equals("128") or keysize.equals("192") or keysize.equals("256")):
                key_bytes= int(keysize) / 8 #Calculates the number of bytes for the key from the bits given
                aes_key = get_random_bytes(key_bytes)
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
                    message = input("Enter a message: ")  # Updates the while loop
                    encryptedText=cipher.encrypt(message)
                    messageBytes = str.encode(encryptedText)  # converting message to bytes
                    clientSocket.send(messageBytes)  # Sends the message in bytes
                    messageFromServerBytes = clientSocket.recv(1024)
                    decryptedText=cipher.decrypt(messageFromServerBytes)
                    print("Received", decryptedText, "from", (serverName, serverPort))
                print("Client is disconnecting")
                clientSocket.close()
            else:  # Inputted a number but was not one of the 3 key sizes
                print("There was an error in creating your AES key with the key size given. Please try either 128, 192, or 256.")
        else:  # Did not input a number at all
                print("There was an error in creating your AES key with the key size given. Please try inputting a number, either 128, 192, or 256.")

    elif (mode.equals("cbc")):
        if sys.argv[0].isdigit():
            keysize = sys.argv[0]
            if (keysize.equals("128") or keysize.equals("192") or keysize.equals("256")):
                key_bytes = int(keysize) / 8  # Calculates the number of bytes for the key from the bits given
                aes_key = get_random_bytes(key_bytes)
                IV = get_random_bytes(16)
                # hmac_key = get_random_bytes(16)
                cipher = AES.new(aes_key, AES.MODE_CBC, IV)
                # Display the key on the client window
                print("The key that was generated was: " + cipher)
                # Sending the key to the server
                sendCipher = bytes.encode(cipher)
                clientSocket.send(sendCipher)
                sendIV = bytes.encode(IV)
                clientSocket.send(IV)
                while (message != "bye"):  # Keeps going until the client enters bye
                    # print("The message:", message, "and bye is") helped with decoding
                    # print((message != "bye")) decoding message
                    message = input("Enter a message: ")  # Updates the while loop
                    encryptedText = cipher.encrypt(message)
                    messageBytes = str.encode(encryptedText)  # converting message to bytes
                    clientSocket.send(messageBytes)  # Sends the message in bytes
                    messageFromServerBytes = clientSocket.recv(1024)
                    decryptedText = cipher.decrypt(messageFromServerBytes)
                    print("Received", decryptedText, "from", (serverName, serverPort))
                print("Client is disconnecting")
                clientSocket.close()
            else: #Inputted a number but was not one of the 3 key sizes
                print("There was an error in creating your AES key with the key size given. Please try either 128, 192, or 256.")
        else: #Did not input a number at all
            print("There was an error in creating your AES key with the key size given. Please try inputting a number, either 128, 192, or 256.")
    else: #The mode given is not ecb or cbc
            print("There was an error in creating your AES key with the mode given. Please try either ecb or cbc.")
else: #Mode given is not words
    print("There was an error in creating your AES key with the mode given. Please try either ecb or cbc.")

print("Client is disconnecting")
clientSocket.close()



