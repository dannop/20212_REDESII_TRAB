import sys
import general
import pickle
import threading
import zlib
from socket import *
from interface import Interface
from video_player import VideoPlayer

serverName = '192.168.1.103'
serverPort = 6000
clientSocket = socket(AF_INET, SOCK_DGRAM)
threads = list()

userInterface = Interface(clientSocket, (serverName, serverPort))

def createConnection():
    print('O cliente está online...') 
    while True:
        try:     
            data, addr = clientSocket.recvfrom(64*1024)
            data_decompressed = zlib.decompress(data)
            data_variable = pickle.loads(data_decompressed)
            print('Recebeu', data_variable[0])

            if (data_variable[0] == general.SERVER_COMMANDS[0]):
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.SERVER_COMMANDS[1]):
                VideoPlayer.runStream(clientSocket, data_variable[1], addr)

        except Exception as e: 
            print("Houve um problema!", e) 
            clientSocket.close()
            userInterface.stop()
        
            

def createUI():
    userInterface = Interface(clientSocket, (serverName, serverPort))
    userInterface.run()

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