import pickle

CLIENT_COMMANDS = [
    "LISTAR_VIDEOS", 
    "REPRODUZIR_VIDEO", 
    "PARA_STREAMING", 
    "ENTRAR_NA_APP", 
    "SAIR_DA_APP",
    "REPRODUZIR_VIDEO_GRUPO"
]
CLIENT_PREMIUM_COMMANDS = [
    "CRIAR_GRUPO", 
    "ADD_USUARIO_GRUPO", 
    "REMOVER_USUARIO_GRUPO", 
    "VER_GRUPO"
]
SERVER_COMMANDS = [
    "LISTA_DE_VIDEOS", 
    "REPRODUZINDO_O_VIDEO", 
    "GET_USER_INFORMATION"
]
MANAGEMENT_COMMANDS = [
    "USER_INFORMATION", 
    "ENTRAR_NA_APP_ACK", 
    "STATUS_DO_USUARIO", 
    "SAIR_DA_APP_ACK", 
    "CRIAR_GRUPO_ACK", 
    "ADD_USUARIO_GRUPO_ACK", 
    "REMOVER_USUARIO_GRUPO_ACK", 
    "GRUPO_DE_STREAMING",
    "PLAY_VIDEO_TO_GROUP"
]

def formatSendTo(socket, message, data, addr):
    data = [message, data]
    data_string = pickle.dumps(data)
    socket.sendto(data_string, addr)

def formatTcpSendTo(socket, message, data):
    data = [message, data]
    data_string = pickle.dumps(data)
    socket.send(data_string)