import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

nickname = input("Choose your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket initialization
client.connect(('127.0.0.1', 48763)) #connecting client to server

## get rsa key ##
key = RSA.generate(2048)

## private and public 
privatekey = key.export_key()
publickey = key.public_key().export_key()

## RSA key
rsa_public_key = RSA.import_key(publickey) #public
cipher = PKCS1_OAEP.new(rsa_public_key) #make it more secure!

## DEFINE ##
def receive():
    while True: #making valid connection
        message = client.recv(4096).decode()
        if message == 'NICKNAME':
            client.send(nickname.encode('ascii'))
        else:
            ciphertext = message.encode()
            orinal_message = unpad(cipher.decrypt(ciphertext),AES.block_size) #decrypt message 
            print(orinal_message.decode()) 

def write():
    while True: #message layout
        message = '{}: {}'.format(nickname, input(''))
        ciphertext = cipher.encrypt(message.encode()) #encrypt message
        client.send(ciphertext)


## MAIN ##
receive_thread = threading.Thread(target=receive) #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write) #sending messages 
write_thread.start()