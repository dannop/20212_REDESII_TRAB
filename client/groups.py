class Group:
  def __init__(self, id, user):
    self.id = id
    self.owner = user
    self.users = []