import sys
import general
import pickle
from socket import *
from video_player import VideoPlayer
import cv2
from interface import Interface
import threading

serverName = '192.168.56.1'
serverPort = 6000
clientSocket = socket(AF_INET, SOCK_DGRAM)
threads = list()
    
def createConnection(name):
    print('Iniciando cliente...') 
    while True:
        try:     
            data, addr = clientSocket.recvfrom(64*1024)
            data_variable = pickle.loads(data)
            print('Recebeu', data_variable)

            if (data_variable[0] == general.SERVER_COMMANDS[0]): 
                print('Lista de Videos')
            elif (data_variable[0] == general.SERVER_COMMANDS[1]):
                cv2.imshow('Streaming', data_variable[1])

                if cv2.waitKey(60) & 0xFF == ord('q'):
                    general.formatSendTo(clientSocket, general.CLIENT_COMMANDS[2], None, (serverName, serverPort))
                    cv2.destroyAllWindows()

        except Exception as e: 
            print("Houve um problema!", e) 
            clientSocket.close()
            sys.exit()

def createUI(name):
    userInterface = Interface(clientSocket, (serverName, serverPort))
    userInterface.run()

def createThread(threads, target, index):
    thr = threading.Thread(target=target, args=(index,))
    threads.append(thr)
    thr.start()

if __name__ == "__main__":
    
    createThread(threads, createConnection, 0)
    createThread(threads, createUI, 1)

    for index, thread in enumerate(threads):
        thread.join()