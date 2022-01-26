import sys
import general
import pickle
import threading
import zlib
from socket import *
from interface import Interface
from video_player import VideoPlayer

serverName = '192.168.1.155'

streamingPort = 6000
streamingSocket = socket(AF_INET, SOCK_DGRAM)

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)

threads = list()

userInterface = Interface(streamingSocket, (serverName, streamingPort), managementSocket, (serverName, managementPort))

def createConnection():
    print('O cliente está online...') 
    while True:
        try:     
            data, addr = streamingSocket.recvfrom(64*1024)
            data_decompressed = zlib.decompress(data)
            data_variable = pickle.loads(data_decompressed)
            print('Recebeu', data_variable[0])

            if (data_variable[0] == general.SERVER_COMMANDS[0]):
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.SERVER_COMMANDS[1]):
                VideoPlayer.runStream(streamingSocket, data_variable[1], addr)
            
            if (data_variable[0] == general.MANAGEMENT_COMMANDS[1]):
                # mostra na tela a correspondendo notificacao do usuario
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[2]):
                # mostra na tela a informacao do usuario recebida na mensagem
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[3]):
                # fecha a conexão TCP com o servidor gerenciador de serviço e; 
                # caso esteja em um streaming envia notificação “PARAR_STREAMING” para o servidor de streaming.
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[4]):
                # mostra na tela a correspondente notificação para o usuário para CRIAR_GRUPO_ACK
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[5]):
                # mostra na tela a correspondente notificação para o usuário para ADD_USUARIO_GRUPO_ACK
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[6]):
                # mostra na tela a correspondente notificação para o usuário para REMOVER_USUARIO_GRUPO_ACK
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.MANAGEMENT_COMMANDS[6]):
                # mostra na tela a correspondente notificação para o usuário para GRUPO_DE_STREAMING
                userInterface.showVideos(data_variable[1])

        except Exception as e: 
            print("Houve um problema!", e) 
            streamingSocket.close()
            userInterface.stop()

def createThread(threads, target):
    thr = threading.Thread(target=target, args=())
    threads.append(thr)
    thr.start()

if __name__ == "__main__":
    
    createThread(threads, createConnection)

    userInterface.showBegin()
    userInterface.run()

    for thread in threads:
        thread.join()
    
    sys.exit()