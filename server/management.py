import pickle
import general 
from socket import *
import threading

serverName = '192.168.1.155'

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)
managementSocket.bind((serverName, managementPort))

threads = list()
groups = list()
users = list()

def removeUser(user):
  if user:
    for u in users:
      if u.id == user.id:
          users.remove(u)

def handleClient(conn, addr):
  while True:
    data = conn.recv(64*1024)
    if data:
      data_variable = pickle.loads(data) 
      print('Recebeu', data_variable[0])

      if (data_variable[0] == general.SERVER_COMMANDS[2]): 
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[0], None)
      elif (data_variable[0] == general.CLIENT_COMMANDS[3]):
        if data_variable[1] in users:
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[2], None)
        else: 
          users.append(data_variable[1])
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[1], data_variable[1])
      elif (data_variable[0] == general.CLIENT_COMMANDS[4]):
        removeUser(data_variable[1])
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[3], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[0]):
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[4], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[1]):
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[5], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[2]):
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[6], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[3]):
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[7], None)

def createConnection():
  managementSocket.listen()
  print('O gerenciador está online...')
  
  while True:
    conn, addr = managementSocket.accept() 
    
    try:
      thread = threading.Thread(target=handleClient, args=(conn, addr))
      threads.append(thread)
      thread.start()
    
    except Exception as e: 
      print("Houve um problema no servidor!", e) 
      conn.close()
      break

if __name__ == "__main__":
    
    createConnection()

    for thread in threads:
      thread.join()