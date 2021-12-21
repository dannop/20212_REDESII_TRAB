class Video:
  def __init__(self, name, time, path):
    self.name = name
    self.time = time
    self.path = path

  def getMinimunQuality(self):
    return self.path + '240.mp4'

  def getMediumQuality(self):
    return self.path + '480.mp4'

  def getHighQuality(self):
    return self.path + '720.mp4'