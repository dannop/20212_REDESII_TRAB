from socket import *

serverName = 'localhost'
serverPort = 6000
serversocket = socket(AF_INET, SOCK_DGRAM)

CLIENT_COMMANDS = [b"LISTAR_VIDEOS", b"REPRODUZIR_VIDEO"]
SERVER_COMMANDS = [b"LISTA_DE_VIDEOS", b"REPRODUZINDO_O_VIDEO"]

serversocket.bind((serverName, serverPort))

print('O servidor está online...')

while True:
    try:  
        sentence, addr = serversocket.recvfrom(1024)
        print('Recebeu', sentence)

        if (sentence == CLIENT_COMMANDS[0]): 
            serversocket.sendto(SERVER_COMMANDS[0], addr)
        elif (sentence == CLIENT_COMMANDS[1]): 
            serversocket.sendto(SERVER_COMMANDS[1], addr)
    except: 
        print("Houve um problema no servidor!") 
        serversocket.close()
        break