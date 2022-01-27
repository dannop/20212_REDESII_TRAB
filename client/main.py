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
streamingAddress = (serverName, streamingPort)

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)
managementAddress = (serverName, managementPort)

threads = list()

userInterface = Interface(streamingSocket, streamingAddress, managementSocket, managementAddress)

def createUdpConnection():
    while True:
        try: 
            data, addr = streamingSocket.recvfrom(64*1024)
            if data:
                data_decompressed = zlib.decompress(data)
                data_variable = pickle.loads(data_decompressed)
                print('Recebeu', data_variable[0])

                if (data_variable[0] == general.SERVER_COMMANDS[0]):
                    userInterface.showVideos(data_variable[1])
                elif (data_variable[0] == general.SERVER_COMMANDS[1]):
                    VideoPlayer.runStream(streamingSocket, data_variable[1], addr)   
                
        except Exception as e: 
            print("Houve um problema na conexão UDP!", e) 
            streamingSocket.close()
            userInterface.stop()

def createTcpConnection():
    managementSocket.connect(managementAddress)

    while True:
        try: 
            data = managementSocket.recv(64*1024)
            if data:
                data_variable = pickle.loads(data)
                print('Recebeu', data_variable[0])

                if (data_variable[0] == general.MANAGEMENT_COMMANDS[1]):
                    # mostra na tela as opcoes iniciais
                    userInterface.showOptions()
                elif (data_variable[0] == general.MANAGEMENT_COMMANDS[2]):
                    # mostra na tela a informacao do usuario recebida na mensagem
                    userInterface.showVideos(data_variable[1])
                elif (data_variable[0] == general.MANAGEMENT_COMMANDS[3]):
                    # fecha a conexão TCP com o servidor gerenciador de serviço e; 
                    # caso esteja em um streaming envia notificação “PARAR_STREAMING” para o servidor de streaming.
                    general.formatSendTo(streamingSocket, general.CLIENT_COMMANDS[2], None, streamingAddress)
                    userInterface.stop()
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
            print("Houve um problema na conexão TCP!", e) 
            managementSocket.close()
            userInterface.stop()

def createThread(threads, target):
    thr = threading.Thread(target=target, args=())
    threads.append(thr)
    thr.start()

if __name__ == "__main__":
    
    createThread(threads, createUdpConnection)
    createThread(threads, createTcpConnection)

    print('O cliente está online...') 
    
    userInterface.showLogin()
    userInterface.run()

    for thread in threads:
        thread.join()