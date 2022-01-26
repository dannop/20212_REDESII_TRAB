class User:
  def __init__(self, id, name, kind):
    self.id = id
    self.name = name
    self.kind = kind
    self.group_ids = []