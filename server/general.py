import pickle
import cv2
import base64
import zlib

CLIENT_COMMANDS = ["LISTAR_VIDEOS", "REPRODUZIR_VIDEO", "PARA_STREAMING", "ENTRAR_NA_APP", "SAIR_DA_APP"]
CLIENT_PREMIUM_COMMANDS = ["CRIAR_GRUPO", "ADD_USUARIO_GRUPO", "REMOVER_USUARIO_GRUPO", "VER_GRUPO"]
SERVER_COMMANDS = ["LISTA_DE_VIDEOS", "REPRODUZINDO_O_VIDEO", "GET_USER_INFORMATION"]
MANAGEMENT_COMMANDS = ["USER_INFORMATION", "ENTRAR_NA_APP_ACK", "STATUS_DO_USUARIO", "SAIR_DA_APP_ACK", "CRIAR_GRUPO_ACK", "ADD_USUARIO_GRUPO_ACK", "REMOVER_USUARIO_GRUPO_ACK", "GRUPO_DE_STREAMING"]

def formatSendTo(socket, message, data, addr):
    data = [message, data]
    data_string = pickle.dumps(data)
    data_compressed = zlib.compress(data_string)
    socket.sendto(data_compressed, addr)

def formatTcpSendTo(socket, message, data):
    print('socket', socket)
    data = [message, data]
    data_string = pickle.dumps(data)
    socket.send(data_string)
    
def formatSendFrameTo(socket, message, frame, addr):
    encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])
    frame_formated = base64.b64encode(buffer)
    formatSendTo(socket, message, frame_formated, addr)