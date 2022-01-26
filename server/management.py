import pickle
import general 
from socket import *
import threading

from users import User

serverName = '192.168.1.155'

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)
managementSocket.bind((serverName, managementPort))

users = []

def handle_client(conn, addr):
  while True:
    msg_length = conn.recv(64).decode("utf-8") # I got the error when I put server.recv
    if msg_length:
      msg = conn.recv(int(msg_length)).decode('utf-8') # Here too
      print(msg)

def createConnection():
  managementSocket.listen()
  print('O gerenciador está online...')
  
  while True:
    conn, addr = managementSocket.accept() 
    
    try:
      # thread = threading.Thread(target=handle_client, args=(conn, addr))
      # thread.start()

      data = conn.recv(64*1024)
      data_variable = pickle.loads(data)
      print('Recebeu', data_variable[0])  

      if (data_variable[0] == general.SERVER_COMMANDS[2]): 
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[0], None)
      elif (data_variable[0] == general.CLIENT_COMMANDS[3]):
        if data_variable[1] in users:
          general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[2], None)
        else: 
          general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[1], None)
      elif (data_variable[0] == general.CLIENT_COMMANDS[4]):
        users.remove(data_variable[0])
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[3], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[0]):
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[4], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[1]):
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[5], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[2]):
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[6], None)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[3]):
        general.formatTcpSendTo(managementSocket, general.MANAGEMENT_COMMANDS[7], None)
    
    except Exception as e: 
      print("Houve um problema no servidor!", e) 
      managementSocket.close()
      break

if __name__ == "__main__":
    
    createConnection()