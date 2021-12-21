import pickle

CLIENT_COMMANDS = ["LISTAR_VIDEOS", "REPRODUZIR_VIDEO", "PARA_STREAMING"]
SERVER_COMMANDS = ["LISTA_DE_VIDEOS", "REPRODUZINDO_O_VIDEO"]

def formatSendTo(socket, message, data, addr):
    data = [message, data]
    data_string = pickle.dumps(data)
    socket.sendto(data_string, addr)