import pickle
import general 
from socket import *

from users import User

serverName = '192.168.1.155'

managementPort = 5000
managementSocket = socket(AF_INET, SOCK_STREAM)
managementSocket.bind((serverName, managementPort))
managementSocket.listen(5)

users = []
users.append(User(1, 'Daniel', 'Convidado'))
users.append(User(1, 'Juliana', 'Premium'))

def createConnection():
  print('O gerenciador está online...')
  while True:
    try:
      conn, addr = managementSocket.accept()   
      data = managementSocket.recv(64*1024)
      data_variable = pickle.loads(data)
      print('Recebeu', data_variable[0])  

      if (data_variable[0] == general.SERVER_COMMANDS[2]): 
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[0], None, addr)
      elif (data_variable[0] == general.CLIENT_COMMANDS[3]):
        if data_variable[1] in users:
          general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[2], None, addr)
        else: 
          general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[1], None, addr)
      elif (data_variable[0] == general.CLIENT_COMMANDS[4]):
        users.remove(data_variable[0])
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[3], None, addr)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[0]):
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[4], None, addr)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[1]):
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[5], None, addr)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[2]):
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[6], None, addr)
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[3]):
        general.formatSendTo(managementSocket, general.MANAGEMENT_COMMANDS[7], None, addr)
    
    except Exception as e: 
      print("Houve um problema no servidor!", e) 
      managementSocket.close()
      break

if __name__ == "__main__":
    
    createConnection()

# import socket
# import threading

# def handle_client(conn, addr):
#   while True:
#     msg_length = conn.recv(64).decode("utf-8") # I got the error when I put server.recv
#     if msg_length:
#       msg = conn.recv(int(msg_length)).decode('utf-8') # Here too
#       print(msg)

# def start():
#   server.listen()
#   while True:
#     conn, addr = server.accept()
#     thread = threading.Thread(target=handle_client, args=(conn, addr))
#     thread.start()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((socket.gethostbyname(socket.gethostname()), 5050))