from httplib2 import Http
import simplejson as json


class DevicewiseHttp(object):
    # Mantidas as mesmas nomenclaturas que a API usa

    # Endpoint da API (url)
    endpoint = ""

    # Identificador da aplicação
    app_id = ""

    # Token da aplicação
    app_token = ""

    # Identifica o método 'thing' que será executado
    thing_key = ""

    # Nome do usuário para conectar no servidor.
    username = ""

    # Senha para conectar no servidor.
    password = ""

    # String JSON do ultimo recebimento do endpoint. ***Usado para debug.
    last_received = ""

    # Ultima string JSON enviada para o endpoint. ***Usado para debug.
    last_sent = ""

    # Informa se o ultimo 'request' foi bem sucedido ou falhou
    last_status = None

    # Contem os dados da resposta do chamado a API.
    response = []

    # Contem o identificador da sessao atual
    session_id = ""

    # Mantem qualquer erro retornado pela api.
    error = []

    # Inicializa o objeto.
    # @param    dict    opcoes    Opcoes de inicializacao (endpoint, app_id, app_token, thing_key, username, password, session_id).
    def __init__(self, opcoes={}):
        if "endpoint" in opcoes:
            self.endpoint = opcoes["endpoint"]

        if "app_id" in opcoes:
            self.app_id = opcoes["app_id"]
        if "app_token" in opcoes:
            self.app_token = opcoes["app_token"]
        if "thing_key" in opcoes:
            self.thing_key = opcoes["thing_key"]

        if "username" in opcoes:
            self.username = opcoes["username"]
        if "password" in opcoes:
            self.password = opcoes["password"]

        if "session_id" in opcoes:
            self.session_id = opcoes["session_id"]

        if (len(self.session_id) == 0) or (self.executar("diag.ping") == False):
            self.session_id = ""
            self.autenticar()

    # Efetua autenticacao na API. Dependendo da configuração, autentica o aplicativo ou usuário.
    # @return    bool    Sucesso ou falha na autenticacao.
    def autenticar(self):
        """Dependendo da servico, autentica o aplicativo ou usuário."""
        if len(self.app_id) > 0 and len(self.app_token) > 0 and len(self.thing_key) > 0:
            return self.autenticar_aplicativo(self.app_id, self.app_token, self.thing_key)
        elif len(self.username) > 0 and len(self.password) > 0:
            return self.autenticar_usuario(self.username, self.password)
        return False

    # Autentica a aplicação
    # @param     string    app_id                ID da aplicação.
    # @param     string    app_token             Token da aplicação.
    # @param     string    thing_key             Chave (key) da aplicação (thing).
    # @param     bool      update_session_id     Atualiza ID da sessão.
    # @return    bool      Sucesso ou falha na autenticação.
    def autenticar_aplicativo(self, app_id, app_token, thing_key, update_session_id=True):
        """Autentica a aplicação."""
        params = {"appId": app_id, "appToken": app_token, "thingKey": thing_key}
        response = self.executar("api.authenticate", params)
        if response == True:
            if update_session_id:
                self.session_id = self.response["auth"]["params"]["sessionId"]
            return True
        return False

    # Autentica um usuário.
    # @param     string    username             Nome do usuario (username).
    # @param     string    password             Senha de acesso (password).
    # @param     bool      update_session_id    Atualiza ID da sessão.
    # @return    bool      Success or failure to authenticate.
    def autenticar_usuario(self, username, password, update_session_id=True):
        """Autentica um usuário."""
        params = {"username": username, "password": password}
        if self.executar("api.authenticate", params):
            if update_session_id:
                self.session_id = self.response["auth"]["params"]["sessionId"]
            return True
        return False


    # Checa o comando JSON para o parametro auth. Se não informado será adicionado.
    # @param    mixed    string_json    A JSON string or the dict representation of JSON.
    # @return   string   Uma string JSON com o parametro auth.
    def informar_auth_json(self, string_json):
        """Adiciona parametro AUTH caso não informado."""
        if not type(string_json) is dict:
            string_json = json.loads(string_json)

        if not "auth" in string_json:
            if len(self.session_id) == 0:
                self.autenticar()
            # levantar exception caso parametro nao informado
            if len(self.session_id) == 0:
                raise Exception("Autenticação falhou. Por favor confira as configurações da aplicação.")
            string_json["auth"] = {"sessionId": self.session_id}

        string_json = json.dumps(string_json)
        return string_json

