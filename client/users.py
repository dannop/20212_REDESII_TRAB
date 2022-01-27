from groups import Group

class User:
  def __init__(self, id, kind):
    self.id = id
    self.kind = kind
    self.group = Group(0)