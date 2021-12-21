import sys
import general
import pickle
from socket import *
import cv2
from interface import Interface
import threading

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
            data_variable = pickle.loads(data)
            print('Recebeu', data_variable)

            if (data_variable[0] == general.SERVER_COMMANDS[0]):
                print(userInterface) 
                userInterface.showVideos(data_variable[1])
            elif (data_variable[0] == general.SERVER_COMMANDS[1]):
                cv2.imshow('Streaming', data_variable[1])

                if cv2.waitKey(60) & 0xFF == ord('q'):
                    general.formatSendTo(clientSocket, general.CLIENT_COMMANDS[2], None, addr)
                    cv2.destroyAllWindows()

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