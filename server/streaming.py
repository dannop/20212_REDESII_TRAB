import sys
import pickle
import general 
from socket import *
from video import Video
import cv2
import time
import multiprocessing
import threading

serverName = '192.168.1.155'

streamingPort = 6000
streamingSocket = socket(AF_INET, SOCK_DGRAM)
streamingAddress = (serverName, streamingPort)
streamingSocket.bind(streamingAddress)

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)
managementAddress = (serverName, managementPort)

videos = list()
videos.append(Video('Batman', 14300, "videos/batman/"))
videos.append(Video('Matrix', 17200, "videos/matrix/"))

threads = list()
all_processes = list()

def stream(video, addr, streamingSocket):
    cap = None

    if video[1] == '240p':
        cap = cv2.VideoCapture(video[0].getLowQuality())
    elif video[1] == '480p':
        cap = cv2.VideoCapture(video[0].getMediumQuality())
    else:
        cap = cv2.VideoCapture(video[0].getHighQuality())
    
    if (cap):
        if (not cap.isOpened()):
            print("Error opening video stream or file")
        
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                general.formatSendFrameTo(streamingSocket, general.SERVER_COMMANDS[1], frame, addr)
                time.sleep(0.1)
            else:
                break

        cap.release()

def createConnection():
    while True:
        try:   
            data, addr = streamingSocket.recvfrom(64*1024)
            if data:
                data_variable = pickle.loads(data)
                print('Recebeu', data_variable[0])

                if (data_variable[0] == general.CLIENT_COMMANDS[0]): 
                    general.formatSendTo(streamingSocket, general.SERVER_COMMANDS[0], videos, addr)
                elif (data_variable[0] == general.CLIENT_COMMANDS[1]): 
                    process = multiprocessing.Process(target=stream, args=(data_variable[1], addr, streamingSocket))
                    all_processes.append(process)
                    process.start()
                elif (data_variable[0] == general.CLIENT_COMMANDS[2]): 
                    process = all_processes[len(all_processes)-1]
                    process.terminate()
                    general.formatSendTo(streamingSocket, general.SERVER_COMMANDS[0], videos, addr)   

        except Exception as e: 
            print("Houve um problema no servidor!", e) 
            streamingSocket.close()
            break

def createManagementConnection():
    managementSocket.connect(managementAddress)

    while True:
        try: 
            data = managementSocket.recv(64*1024)
            data_variable = pickle.loads(data)
            print('Recebeu', data_variable[0])
            
        except Exception as e: 
            print("Houve um problema no gerenciador!", e) 
            managementSocket.close()

def createThread(threads, target):
    thr = threading.Thread(target=target, args=())
    threads.append(thr)
    thr.start()

if __name__ == "__main__":
    
    createThread(threads, createConnection)
    createThread(threads, createManagementConnection)

    print('O servidor está online...')

    for thread in threads:
        thread.join()

    sys.exit()