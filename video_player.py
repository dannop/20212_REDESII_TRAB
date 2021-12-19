import cv2

class VideoPlayer:
  def __init__(self, path):
    self.path = path

  def run(self):
    cap = cv2.VideoCapture(self.path)
    if (cap.isOpened()== False):
      print("Error opening video stream or file")
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
        cv2.imshow('Streaming', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      else:
        break
    cap.release()
    cv2.destroyAllWindows()