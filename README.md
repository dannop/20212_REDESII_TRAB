# Trabalho de Redes II - Streaming de Vídeos

## Dependências e soluções de problemas
### No MacOS 
```console
xcode-select --install
brew install portaudio
brew install python-tk
```

### Linux
```console
sudo apt install portaudio19-dev python-all-dev
```

### Geral
```console
pip install opencv-python
pip install pyaudio
pip install tk
```

Em caso de problema com interface gráfica com Subsistema linux, instale o Xming no WIndows e rode no terminal:
```console
export DISPLAY =:0
```

## INSTRUÇÕES DE USO:
Verifique se o serverName confere com o IP compartilhado na sua rede local

Após isso, rode os seguintes comandos no terminal:
```console
cd server 
python3 streaming.py
```

Em outro terminal rode o Cliente:
```console
cd client
python3 main.py
```

## LOGS DE APLICAÇÃO:

Iniciamos o SERVIDOR de STREAMING (streaming.py);

Servidor inicializa um socket UDP na porta 6000;

Imprime no terminal “O servidor está online. . .”;

Significa que está à espera de mensagens UDP dos CLIENTES;

Iniciamos o CLIENTE (main.py);

É criada a conexão com o SERVIDOR na porta 6000;

Imprime no terminal “O cliente está online. . .”;

Iniciada a Interface do Usuário;

Nela terá um botão de "Exibir Vídeos” que irá enviar uma mensagem “LISTAR_VIDEOS” do CLIENTE para o SERVIDOR;

O SERVIDOR irá retornar como mensagem “LISTA_DE_VIDEOS” junto com a lista de vídeos disponíveis para reprodução, que possui Nome e Caminho do Vídeo no servidor;

O CLIENTE clica no botão de um vídeo específico na interface gráfica e abre as opções de qualidade; 

Ao selecionar a qualidade o CLIENTE envia uma mensagem “REPRODUZIR_VIDEO”, junto com qualidade e vídeo que deseja;

O SERVIDOR a partir desse momento irá executar o Stream do Vídeo selecionado, retornando a mensagem “REPRODUZINDO_VIDEO” com o Frame do vídeo que está sendo executado;

A qualquer momento o CLIENTE poderá fechar o vídeo, assim retornando uma mensagem “PARA_STREAMING”;
