from socket import *

serverName = ''
serverPort = 6000
serversocket = socket(AF_INET, SOCK_DGRAM)

COMMANDS = [b"LISTAR_VIDEOS", b"REPRODUZIR_VIDEO"]

serversocket.bind((serverName, serverPort))

print('O servidor está online...')

while True:
    sentence, addr = serversocket.recvfrom(1024)
    if (sentence == COMMANDS[0]): 
        serversocket.sendto(b"LISTA_DE_VIDEOS", addr)
    if (sentence == COMMANDS[1]): 
        serversocket.sendto(b"REPRODUZINDO_O_viDEO", addr)

serversocket.close()