import pickle
import cv2
import base64
import zlib

CLIENT_COMMANDS = ["LISTAR_VIDEOS", "REPRODUZIR_VIDEO", "PARA_STREAMING"]
SERVER_COMMANDS = ["LISTA_DE_VIDEOS", "REPRODUZINDO_O_VIDEO"]

def formatSendTo(socket, message, data, addr):
    data = [message, data]
    data_string = pickle.dumps(data)
    data_compressed = zlib.compress(data_string)
    socket.sendto(data_compressed, addr)

def formatSendFrameTo(socket, message, frame, addr):
    encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])
    frame_formated = base64.b64encode(buffer)
    formatSendTo(socket, message, frame_formated, addr)