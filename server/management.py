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

def findElementById(id, list):
  value = None
  for element in list:
    if element.id == id:
      value = element
  
  return value

def findGroup(user):
  current_group = None
  for group in groups:
    if group.id == user.group.id:
      current_group = group
  
  return current_group

def removeUser(user):
  if user:
    for u in users:
      if u.id == user.id:
          users.remove(u)

def handleCommands(conn, addr):
  while True:
    data = conn.recv(64*1024)
    if data:
      data_variable = pickle.loads(data) 
      print('Recebeu', data_variable[0])

      # Server Commands
      if (data_variable[0] == general.SERVER_COMMANDS[2]): 
        # GET_USER_INFORMATION
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[0], None)
      
      # Client Commands
      if (data_variable[0] == general.CLIENT_COMMANDS[3]):
        # ENTRAR_NA_APP
        user = findElementById(data_variable[1], users)

        if user:
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[2], user)
        else: 
          users.append(data_variable[1])
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[1], data_variable[1])
      elif (data_variable[0] == general.CLIENT_COMMANDS[4]):
        # SAIR_DA_APP
        removeUser(data_variable[1])
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[3], None)
      
      # CLient Premium Commands
      if (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[0]):
        # CRIAR_GRUPO
        groups.append(data_variable[1]) 
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[4], [data_variable[1].owner, 'Grupo criado com sucesso!'])
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[1]):
        # ADD_USUARIO_GRUPO
        user = data_variable[1][0]
        new_user = findElementById(data_variable[1][1], users)
        current_group = findGroup(user)
        
        if new_user:
          if current_group:
            message = current_group.addUser(new_user)
            general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[5], [current_group, message])
          else:
            general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[5], [current_group, 'Grupo não encontrado.'])  
        else:
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[5], [current_group, 'Usuário não encontrado.'])
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[2]):
        # REMOVER_USUARIO_GRUPO
        user = data_variable[1][0]
        remove_user = findElementById(data_variable[1][1], users)
        current_group = findGroup(user)
        
        if remove_user:
          if current_group:
            message = current_group.removeUser(remove_user)
            general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[6], [current_group, message])
          else:
            general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[6], [current_group, 'Grupo não encontrado.'])
        else:
          general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[6], [current_group, 'Usuário não encontrado.'])
      elif (data_variable[0] == general.CLIENT_PREMIUM_COMMANDS[3]):
        # VER_GRUPO
        user = data_variable[1]
        current_group = findGroup(user)
        general.formatTcpSendTo(conn, general.MANAGEMENT_COMMANDS[7], current_group)

def createConnection():
  managementSocket.listen()
  while True:
    conn, addr = managementSocket.accept() 
    
    try:
      thread = threading.Thread(target=handleCommands, args=(conn, addr))
      threads.append(thread)
      thread.start()
    
    except Exception as e: 
      print("Houve um problema no servidor!", e) 
      conn.close()
      break

if __name__ == "__main__":
    print('O gerenciador está online...')
    createConnection()
    
    for thread in threads:
      thread.join()