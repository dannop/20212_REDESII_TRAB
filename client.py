from socket import *
from video_player import VideoPlayer
from interface import Interface

serverName = 'localhost'
serverPort = 6000
clientSocket = socket(AF_INET, SOCK_DGRAM)

aux = 0

COMMANDS = [b"LISTAR_VIDEOS", b"REPRODUZIR_VIDEO"]

while True: 
    user_interface = Interface()
    user_interface.run()
    
    if (aux == 0): 
        clientSocket.sendto(COMMANDS[0], (serverName, serverPort))
        aux += 1
    
    if (aux == 1): 
        clientSocket.sendto(COMMANDS[1], (serverName, serverPort))
        aux += 1

    print('Aguardando uma resposta...')   
    sentence, addr = clientSocket.recvfrom(1024)
    print('Recebeu', sentence)

    if (sentence == b"REPRODUZINDO_O_viDEO"):
        vp = VideoPlayer("videos/sao/open-480p.mp4")
        vp.run()

clientSocket.close()