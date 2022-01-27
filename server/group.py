class Group:
  def __init__(self, id, user):
    self.id = id
    self.owner = user
    self.users = []

  def addUser(self, user):
    if self.owner.id == user.id:
      message = 'Usuário é o dono do grupo.' 
    else:
      finded = False
      for u in self.users:
        if u.id == user.id:
          finded = True
      
      if finded:
        message = 'Usuário já adicionado!'
      else:
        self.users.append(user)
        message = 'Usuário adicionado com sucesso!'

    return message

  def removeUser(self, user):
    finded = False
    for u in self.users:
      if u.id == user.id:
        finded = True
        self.users.remove(u)
    
    if finded:
      message = 'Usuário removido com sucesso!'
    else:
      message = 'Usuário não encontrado.'

    return message