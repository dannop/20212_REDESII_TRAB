import pickle
from tkinter import * 

CLIENT_COMMANDS = ["LISTAR_VIDEOS", "REPRODUZIR_VIDEO"]

class Interface:
  def __init__(self, socket, address):
    self.socket = socket
    self.address = address

    self.root = Tk() 
    
    self.fontePadrao = ("Arial", "10")

    self.primeiroContainer = self.createContainer(10)

    self.segundoContainer = Frame(self.root)
    self.segundoContainer["padx"] = 20
    self.segundoContainer.pack()

    self.terceiroContainer = Frame(self.root)
    self.terceiroContainer["padx"] = 20
    self.terceiroContainer.pack()

    self.quartoContainer = self.createContainer(20)

    self.createTitle(self.primeiroContainer, "Serviço de Streaming")

    self.createBtn(self.segundoContainer, "Listar Vídeos", self.getVideos)
    self.createBtn(self.terceiroContainer, "Exibir Vídeo", self.runVideo)

    self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
    self.mensagem.pack()

  def createContainer(self, pady): 
    container = Frame(self.root)
    container["pady"] = pady
    container.pack()
    return container

  def createTitle(self, container, text):
    title = Label(container, text=text)
    title["font"] = ("Arial", "10", "bold")
    title.pack()

  def createBtn(self, container, text, command): 
    btn = Button(container)
    btn["text"] = text
    btn["font"] = ("Calibri", "8")
    btn["width"] = 12
    btn["command"] = command
    btn.pack()

  def getVideos(self):
    data = [CLIENT_COMMANDS[0], None]
    data_string = pickle.dumps(data)
    self.socket.sendto(data_string, self.address)
    
  def runVideo(self):
    data = [CLIENT_COMMANDS[1], None]
    data_string = pickle.dumps(data)
    self.socket.sendto(data_string, self.address)

  def run(self):
    self.root.mainloop()
  
  def stop(self):
    self.root.quit()
