import cv2
import pyaudio
import wave

class VideoPlayer:
  def __init__(self, path):
    self.path = path

  def Audio_play(self):
    CHUNK = 1024

    wf = wave.open(self.path, 'rb')
    pa = pyaudio.PyAudio()
    default_output = pa.get_default_host_api_info().get('defaultOutputDevice')
    stream =pa.open(format   = pa.get_format_from_width(wf.getsampwidth()), 
                    channels = wf.getnchannels(), 
                    rate     = wf.getframerate(), 
                    output   = True,
                    output_device_index = default_output)

    NUM = int(wf.getframerate()/CHUNK * 15)
    while NUM:
      data = wf.readframes(CHUNK)
      if data == " ": break
      stream.write(data)
      NUM -= 1
    stream.stop_stream()
    stream.close()
    del data
    pa.terminate()

  def run(self):
    # self.Audio_play()
    cap = cv2.VideoCapture(self.path)
    
    if (cap.isOpened()== False):
      print("Error opening video stream or file")
    
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
        cv2.imshow('Streaming', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
      else:
        break
    
    cap.release()
    cv2.destroyAllWindows()