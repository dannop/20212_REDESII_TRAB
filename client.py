from socket import *
from video_player import VideoPlayer
from interface import Interface
import threading
import logging

serverName = 'localhost'
serverPort = 6000
clientSocket = socket(AF_INET, SOCK_DGRAM)

SERVER_COMMANDS = [b"LISTA_DE_VIDEOS", b"REPRODUZINDO_O_VIDEO"]
    
def menu(option):
    if (option == SERVER_COMMANDS[0]): 
      print('Lista de Videos')
    elif (option == SERVER_COMMANDS[1]):
      vp = VideoPlayer("videos/sao/open-480p.mp4")
      vp.run()

def createConnection(name):
    logging.info("Thread %s: starting", name)
    while True:
        try:     
            print('Aguardando uma resposta...')   
            sentence, addr = clientSocket.recvfrom(1024)
            print('Recebeu', sentence)
            # userInterface.menu(sentence)
        except: 
            print("Houve um problema!") 
            clientSocket.close()
            break

def createUI(name):
    logging.info("Thread %s: starting", name)
    userInterface = Interface(clientSocket, (serverName, serverPort))
    userInterface.run()

def createThread(threads, target, index):
    thr = threading.Thread(target=target, args=(index,))
    threads.append(thr)
    thr.start()

if __name__ == "__main__":

    threads = list()
    createThread(threads, createConnection, 0)
    createThread(threads, createUI, 1)

    for index, thread in enumerate(threads):
        thread.join()