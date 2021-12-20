from tkinter import * 
from tkinter import ttk 

class Interface:
  def __init__(self):
    self.root = Tk() 
    self.frm = ttk.Frame(self.root, padding=10) 

  def run(self):
    self.frm.grid() 
    ttk.Label(self.frm, text="Hello World!").grid(column=0, row=0) 
    ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(column=1, row=0) 
    self.root.mainloop()