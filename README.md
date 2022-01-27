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
export DISPLAY=:0
```

## INSTRUÇÕES DE USO:
Verifique se o serverName confere com o IP compartilhado na sua rede local

Após isso, rode os seguintes comandos no terminal:
```console
cd server
python3 management.py
```

Em outro terminal rode o Server Streaming:
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

Iniciamos o SERVIDOR de GERENCIAMENTO (management.py);
Servidor inicializa um socket TCP na porta 5000;
Imprime no terminal “O gerenciador está online. . .”;
Isso significa que está à espera de mensagens TCP dos CLIENTES e do SERVIDOR de STREAMING;.

Iniciamos o SERVIDOR de STREAMING (streaming.py);
Servidor inicializa um socket UDP na porta 6000;
Imprime no terminal “O servidor está online. . .”;
Isso significa que está à espera de mensagens UDP dos CLIENTES.

Iniciamos o CLIENTE (main.py);
Imprime no terminal “O cliente está online. . .”;
É criada a conexão com o servidor streaming na porta 6000;
É criada a conexão com o servidor de gerenciamento na porta 5000;
Inicia a Interface do Usuário.

Nela, aparecerá a tela de LOGIN;
Entre com um ID e uma CATEGORIA;
O botão “Entrar” enviará uma mensagem “ENTRAR_NA_APP” para o GERENCIADOR;
Caso não esteja já adicionado na lista de usuários, adiciona o novo cliente à lista, e o GERENCIADOR responde com a mensagem “ENTRAR_NA_APP_ACK”.
Caso já esteja na lista de usuários, o GERENCIADOR responde com a mensagem “STATUS_DO_USUÁRIO” e abre a tela de STATUS.

Seguindo, aparecerá a tela OPÇÕES;
Nela terá um botão de “Exibir Vídeos” que irá enviar uma mensagem “LISTAR_VIDEOS” do CLIENTE para o SERVIDOR;
O SERVIDOR irá retornar como mensagem “LISTA_DE_VIDEOS” junto com a lista de vídeos disponíveis para reprodução, que possui Nome e Caminho do Vídeo no servidor;
O CLIENTE clica no botão de um vídeo específico na interface gráfica e abre as opções de qualidade; 

Ao selecionar a qualidade o CLIENTE envia uma mensagem “REPRODUZIR_VIDEO”, junto com qualidade e vídeo que deseja;
O servidor de streaming manda uma mensagem de “GET_USER_INFORMATION” para o gerenciador que responde com uma mensagem de “USER_INFORMATION” com as permissões do usuário atual;

・Se o usuário é PREMIUM:
O servidor de streaming irá enviar uma resposta “REPRODUZINDO O VÍDEO <<NOME DO VÍDEO>> COM RESOLUÇÃO <<RESOLUÇÃO DO VIDEO>>” e a partir desse momento irá executar o Stream do Vídeo selecionado, retornando a mensagem “REPRODUZINDO_VIDEO” com o Frame do vídeo que está sendo executado;
A qualquer momento o CLIENTE poderá fechar o vídeo, assim retornando uma mensagem “PARA_STREAMING”;
・Se o usuário é CONVIDADO: 
Recebe uma resposta do servidor de streaming "NÃO TEM PERMISSÃO PARA REPRODUZIR VÍDEOS, POR FAVOR MUDE SUA CLASSIFICAÇÃO";

Apenas para usuários PREMIUM: Aparecerá um botão “GRUPO” e temos as opções “CRIAR GRUPO”, “VER GRUPO”, “ADICIONAR USUARIO”, “REMOVER USUARIO” e “VOLTAR”.
・No botão de “CRIAR GRUPO” é possível adicionar um novo grupo salvando um ID para facilitar, é enviado para o gerenciador uma mensagem “CRIAR_GRUPO” e o gerenciador responde com o grupo criado e uma mensagem “CRIAR_GRUPO_ACK”;
・No botão de “VER GRUPO”, ele irá mandar pro gerenciador a mensagem “VER_GRUPO” e o gerenciador irá carregar as informações do grupo do usuário atual enviando junto de uma mensagem “GRUPO_DE_STREAMING”;
・No botão “ADICIONAR USUÁRIO” será enviado uma mensagem de “ADD_USUARIO_GRUPO” para o gerenciador;
O gerenciador irá verificar no grupo do usuário atual o id de usuário existente no grupo e irá enviar de volta a resposta “ADD_USUARIO_GRUPO_ACK”, adicionado no grupo do usuário atual um usuário existente no servidor de gerenciamento;
・No botão “REMOVER USUÁRIO" será enviado uma mensagem de “REMOVER_USUARIO_GRUPO” para o gerenciador;
O gerenciador irá verificar  no grupo do usuário atual o id de usuário existente no grupo e irá enviar de volta a resposta “REMOVER_USUARIO_GRUPO_ACK” com uma mensagem descrevendo a ação realizada;
・O botão de “VOLTAR” irá retornar ao menu de opção que mostra “EXIBIR VIDEOS” e “GRUPO”.
