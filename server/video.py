class Video:
  def __init__(self, name, time, path):
    self.name = name
    self.time = time
    self.path = path

  def getLowQuality(self):
    return self.path + '240p.mp4'

  def getMediumQuality(self):
    return self.path + '480p.mp4'

  def getHighQuality(self):
    return self.path + '720p.mp4'