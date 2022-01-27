import sys
import general
from tkinter import * 
from functools import partial

from group import Group
from user import User
from video import Video

class Interface:
  def __init__(self):
    self.root = Tk() 
    self.root.title("Trabalho - Redes II")
    self.root.geometry("500x500")

    self.header = self.createContainer(0, 10)
    self.createTitle(self.header, "Admin")

    self.body = self.createContainer(20, 0)

    self.videos = []
    self.videos.append(Video('Batman', 14300, "videos/batman/"))
    self.videos.append(Video('Matrix', 17200, "videos/matrix/"))

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

  def showVideos(self): 
    self.clearBody()
    
    for video in self.videos: 
      self.createBtn(self.body, video.name, self.showSelectQuality, video)

    self.createBtn(self.body, "Adicionar", self.showVideos)

  def showSelectQuality(self, video): 
    self.clearBody()
    self.createBtn(self.body, "Remover", self.showVideos)
    self.createBtn(self.body, "Voltar", self.showVideos)
  
  def run(self):
    self.root.mainloop()
  
  def stop(self):
    self.root.destroy()
    sys.exit()