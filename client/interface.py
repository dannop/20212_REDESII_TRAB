import sys
import general
from tkinter import * 
from functools import partial

class Interface:
  def __init__(self, server_socket, server_address, management_socket, management_address):
    self.server_socket = server_socket
    self.server_address = server_address
    self.management_socket = management_socket
    self.management_address = management_address

    self.root = Tk() 
    self.root.title("Trabalho - Redes II")
    self.root.geometry("500x500")

    self.header = self.createContainer(0, 10)
    self.createTitle(self.header, "Olá, Cliente")

    self.body = self.createContainer(20, 0)

    self.videos = []

  def clearBody(self):
    for widgets in self.body.winfo_children():
      widgets.destroy()

  def createContainer(self, padx, pady): 
    container = Frame(self.root)
    container["padx"] = padx
    container["pady"] = pady
    container.pack()
    return container

  def createTitle(self, container, text):
    title = Label(container, text=text)
    title["font"] = ("Arial", "40", "bold")
    title.pack()

  def createBtn(self, container, text, action, args=None): 
    action_with_arg = action
    if (args):
      action_with_arg = partial(action, args)

    btn = Button(container)
    btn["text"] = text
    btn["font"] = ("Calibri", "40")
    btn["width"] = 12
    btn["command"] = action_with_arg
    btn.pack()

  def accessApp(self):
    self.management_socket.connect(self.management_address)
    general.formatTcpSendTo(self.management_socket, general.CLIENT_COMMANDS[3], None)

  def getVideos(self):
    general.formatSendTo(self.server_socket, general.CLIENT_COMMANDS[0], None, self.server_address)
    
  def runVideo(self, video):
    general.formatSendTo(self.server_socket, general.CLIENT_COMMANDS[1], video, self.server_address)

  def showBegin(self):
    self.clearBody()
    self.createBtn(self.body, "Entrar", self.showLogin)
    self.createBtn(self.body, "Sair", self.stop)
  
  def showLogin(self):
    self.clearBody()
    self.createTitle(self.body, "LOGIN")
    self.createTitle(self.body, "ID")
    id = Entry(self.body).grid(row = 2,column = 0)
    var1 = IntVar()
    Checkbutton(self.body, text="Convidado", variable=var1).grid(row=2, sticky=W)
    var2 = IntVar()
    Checkbutton(self.body, text="Premium", variable=var2).grid(row=3, sticky=W)
    self.createBtn(self.body, "Entrar", self.showOptions)
    self.createBtn(self.body, "Sair", self.stop)
  
  def showOptions(self):
    self.clearBody()
    self.createBtn(self.body, "Exibir Vídeos", self.getVideos)
    self.createBtn(self.body, "Status do Usuário", self.showStatus)
    self.createBtn(self.body, "Grupo", self.showGroupOptions)
    self.createBtn(self.body, "Sair", self.stop)

  def showVideos(self, videos): 
    self.videos = videos
    self.clearBody()
    self.createBtn(self.body, "Voltar", self.showOptions)
    for video in videos: 
      self.createBtn(self.body, video.name, self.showSelectQuality, video)

  def showSelectQuality(self, video): 
    self.clearBody()
    self.createBtn(self.body, "Voltar", self.showVideos, self.videos)
    self.createBtn(self.body, '240p', self.runVideo, [video, '240p'])
    self.createBtn(self.body, '480p', self.runVideo, [video, '480p'])
    self.createBtn(self.body, '720p', self.runVideo, [video, '720p'])  
  
  def showStatus(self):
    self.clearBody()
    self.createTitle(self.body, "ID:")
    self.createTitle(self.body, "CATEGORIA")
    self.createTitle(self.body, "GRUPO")
    self.createBtn(self.body, "Voltar", self.showOptions)

  def showGroupOptions(self):
    self.clearBody()
    self.createBtn(self.body, "Criar Grupo", self.showNewGroup)
    self.createBtn(self.body, "Ver Grupo", self.showGroup)
    self.createBtn(self.body, "Adicionar Usuário", self.showAddUser)
    self.createBtn(self.body, "Remover Usuário", self.showRemoveUser)
    self.createBtn(self.body, "Voltar", self.showOptions)
  
  def showNewGroup(self):
    self.clearBody()
    self.createTitle(self.body, "NOVO GRUPO")
    self.createTitle(self.body, "NOME DO GRUPO")
    newGroup = Entry(self.body).grid(row = 2,column = 0)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def showGroup(self):
    self.clearBody()
    self.createTitle(self.body, "NOME DO GRUPO:")
    self.createTitle(self.body, "MEMBROS DO GRUPO:")
    self.createBtn(self.body, "Voltar", self.showGroupOptions)
  
  def showAddUser(self):
    self.clearBody()
    self.createTitle(self.body, "ID DO USUÁRIO PARA ADICIONAR:")
    addUser = Entry(self.body).grid(row = 1,column = 0)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def showRemoveUser(self):
    self.clearBody()
    self.createTitle(self.body, "ID DO USUÁRIO PARA REMOVER:")
    removeUser = Entry(self.body).grid(row = 1,column = 0)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def run(self):
    self.root.mainloop()
  
  def stop(self):
    print("Ate a proxima!")
    self.server_socket.close()
    self.root.destroy()
    sys.exit()