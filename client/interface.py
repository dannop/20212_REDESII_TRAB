import sys
import general
from tkinter import * 
from functools import partial
from users import User

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
    self.createTitle(self.header, "")

    self.body = self.createContainer(20, 0)

    self.videos = []

    self.current_user = None
    
    self.user_id = StringVar()
    self.user_kind = IntVar()

    self.group_id = StringVar()

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

  def createParagraph(self, container, text):
    title = Label(container, text=text)
    title["font"] = ("Arial", "20")
    title.pack()

  def createBtn(self, container, text, action, args=None): 
    action_with_arg = action
    if (args):
      action_with_arg = partial(action, args)

    btn = Button(container)
    btn["text"] = text
    btn["font"] = ("Calibri", "40")
    btn["width"] = 20
    btn["command"] = action_with_arg
    btn.pack()

  def createInput(self, container, label_text, value): 
    label = Label(container, text=label_text, width=20)
    label["font"] = ("Arial", "40", "bold")
    label.pack()
    
    entry = Entry(container, textvariable=value)
    entry.pack()
  
  def createRadioOptions(self, container, variable, values): 
    for (text, value) in values.items():
      Radiobutton(container, text = text, variable = variable,
                value = value).pack(fill = X, ipady = 5)

  def accessApp(self):
    user_id = self.user_id.get()
    user_kind = self.user_kind.get()
    
    if user_id != '':
      user = User(user_id, user_kind)
      general.formatTcpSendTo(self.management_socket, general.CLIENT_COMMANDS[3], user)
  
  def logout(self):
    general.formatTcpSendTo(self.management_socket, general.CLIENT_COMMANDS[4], self.current_user)
  
  def newGroup(self):
    general.formatTcpSendTo(self.management_socket, general.CLIENT_PREMIUM_COMMANDS[0], self.current_user)

  def showGroup(self):
    general.formatTcpSendTo(self.management_socket, general.CLIENT_PREMIUM_COMMANDS[3], self.current_user)

  def addUser(self):
    general.formatTcpSendTo(self.management_socket, general.CLIENT_PREMIUM_COMMANDS[1], self.current_user)

  def removeUser(self):
    general.formatTcpSendTo(self.management_socket, general.CLIENT_PREMIUM_COMMANDS[2], self.current_user)

  def getVideos(self):
    general.formatSendTo(self.server_socket, general.CLIENT_COMMANDS[0], None, self.server_address)
    
  def runVideo(self, video):
    general.formatSendTo(self.server_socket, general.CLIENT_COMMANDS[1], video, self.server_address)
  
  def showLogin(self):
    self.clearBody()
    self.createTitle(self.body, "Trabalho de Redes II")
    self.createInput(self.body, "ID", self.user_id)
    self.createRadioOptions(self.body, self.user_kind, {"Convidado" : 0, "Premium" : 1})
    self.createBtn(self.body, "Entrar", self.accessApp)
    self.createBtn(self.body, "Sair", self.stop)
  
  def showOptions(self):
    self.clearBody()
    self.createBtn(self.body, "Exibir Vídeos", self.getVideos)
    self.createBtn(self.body, "Grupo", self.showGroupOptions)
    self.createBtn(self.body, "Sair", self.logout)

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
  
  def showStatus(self, user):
    self.clearBody()
    self.createTitle(self.body, "ID: "+user.id)
    
    if user.kind == 0:
      self.createTitle(self.body, "Tipo: Convidado")
    else:
      self.createTitle(self.body, "Tipo: Premium")
    
    self.createTitle(self.body, "Grupo:")
    
    for id in user.group.user_ids:
      self.createParagraph(self.body, id)
    
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
    self.createTitle(self.body, "Novo Grupo")
    self.createInput(self.body, "ID", self.group_id)
    self.createBtn(self.body, "Confirmar", self.newGroup)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def showGroup(self, group):
    self.clearBody()
    self.createTitle(self.body, "ID do Grupo: "+group.id)
    self.createTitle(self.body, "Membros:")
    
    for id in group.user_ids:
      self.createParagraph(self.body, id)
    
    self.createBtn(self.body, "Voltar", self.showGroupOptions)
  
  def showAddUser(self):
    self.clearBody()
    self.createTitle(self.body, "Adicionar Usuário:")
    self.createInput(self.body, "ID", self.user_id)
    self.createBtn(self.body, "Confirmar", self.addUser)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def showRemoveUser(self):
    self.clearBody()
    self.createTitle(self.body, "Remover Usuário:")
    self.createInput(self.body, "ID", self.user_id)
    self.createBtn(self.body, "Confirmar", self.removeUser)
    self.createBtn(self.body, "Voltar", self.showGroupOptions)

  def run(self):
    self.root.mainloop()
  
  def stop(self):
    print("Ate a proxima!")
    self.server_socket.close()
    self.management_socket.close()
    self.root.destroy()
    sys.exit()