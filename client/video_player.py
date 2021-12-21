import general
import cv2
import pyaudio
import wave
import base64
import numpy as np

class VideoPlayer:
  def Audio_play():
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

  def runStream(socket, frame_formated, addr):
    frame_decoded = base64.b64decode(frame_formated)
    np_data = np.fromstring(frame_decoded, dtype = np.uint8)
    frame = cv2.imdecode(np_data, 1)
    cv2.imshow('Streaming', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        general.formatSendTo(socket, general.CLIENT_COMMANDS[2], None, addr)
        cv2.destroyAllWindows()