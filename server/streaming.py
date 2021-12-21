import pickle
from socket import *
from video import Video

serverName = 'localhost'
serverPort = 6000
serversocket = socket(AF_INET, SOCK_DGRAM)

CLIENT_COMMANDS = ["LISTAR_VIDEOS", "REPRODUZIR_VIDEO"]
SERVER_COMMANDS = ["LISTA_DE_VIDEOS", "REPRODUZINDO_O_VIDEO"]

serversocket.bind((serverName, serverPort))

videos = []
videos.append(Video('Batman', 143, 'videos/batman'))
videos.append(Video('Matrix', 172, 'videos/matrix'))

print('O servidor está online...')

def formatSendTo(message, data, addr):
    data = [message, data]
    data_string = pickle.dumps(data)
    serversocket.sendto(data_string, addr)

while True:
    try:  
        data, addr = serversocket.recvfrom(1024)
        data_variable = pickle.loads(data)
        print('Recebeu', data_variable)

        if (data_variable[0] == CLIENT_COMMANDS[0]): 
            formatSendTo(SERVER_COMMANDS[0], videos, addr)
        elif (data_variable[0] == CLIENT_COMMANDS[1]): 
            formatSendTo(SERVER_COMMANDS[0], videos[0], addr)

    except Exception as e: 
        print("Houve um problema no servidor!", e) 
        serversocket.close()
        break