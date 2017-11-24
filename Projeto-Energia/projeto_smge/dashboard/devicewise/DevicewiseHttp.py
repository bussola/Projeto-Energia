# -*- coding: utf-8 -*-
from httplib2 import Http
import simplejson as json
from django.views.decorators.csrf import csrf_exempt


class DevicewiseHttp(object):
    # Mantidas as mesmas nomenclaturas que a API usa
    # Endpoint da API (url)
    endpoint = 'http://api.devicewise.com/api'

    # Identificador da aplicacao
    app_id = "hab0001"

    # Token da aplicacao
    app_token = ""

    # Identifica o metodo 'thing' que sera executado
    thing_key = ""

    # Nome do usuario para conectar no servidor.
    username = 'brunodrago@e-saveconsultoria.com.br'

    # Senha para conectar no servidor.
    password = 'Aa@203851'

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

        if (len(self.session_id) == 0) or (self.postar("diag.ping") == False):
            self.session_id = ""
            self.autenticar()

    # Efetua autenticacao na API. Dependendo da configuracao, autentica o aplicativo ou usuario.
    # @return    bool    Sucesso ou falha na autenticacao.
    def autenticar(self):
        """Dependendo da servico, autentica o aplicativo ou usuario."""
        if len(self.app_id) > 0 and len(self.app_token) > 0 and len(self.thing_key) > 0:
            return self.autenticar_aplicativo(self.app_id, self.app_token, self.thing_key)
        elif len(self.username) > 0 and len(self.password) > 0:
            return self.autenticar_usuario(self.username, self.password)
        return False

    # Autentica a aplicacao
    # @param     string    app_id                ID da aplicacao.
    # @param     string    app_token             Token da aplicacao.
    # @param     string    thing_key             Chave (key) da aplicacao (thing).
    # @param     bool      update_session_id     Atualiza ID da sessao.
    # @return    bool      Sucesso ou falha na autenticacao.
    def autenticar_aplicativo(self, app_id, app_token, thing_key, update_session_id=True):
        """Autentica a aplicacao."""
        string_json = {"auth": {"command": "api.authenticate",
                                "params": {"appId": app_id, "appToken": app_token, "thingKey": thing_key}}}
        response = self.postar(string_json)
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
    @csrf_exempt
    def autenticar_usuario(self, username, password, update_session_id=True):
        """Autentica um usuário."""
        string_json = {"auth": {"command": "api.authenticate", "params": {"username": username, "password": password}}}
        if self.postar(string_json):
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

    # Envia a requisição para o servidor e converte a resposta.
    # @param    mixed    string_json     Comendos JSON e argumentos. Este parametro pode ser um dicionario que será convertido para uma string JSON.
    # @return   bool     Sucesso ou falha no POST.
    def postar(self, string_json):
        '''    # Este metodo envia a requisição para o servidor e converte a resposta.'''
        self.error = ""
        self.last_status = True
        self.last_received = ""
        self.response = ""

        string_json = self.informar_auth_json(string_json)
        self.last_sent = string_json

        http_obj = Http(disable_ssl_certificate_validation=True)
        result, self.last_received = http_obj.request(self.endpoint, "POST", string_json)
        if not result["status"] == "200":
            raise Exception("Falha no POST para %s" % self.endpoint)

        self.response = json.loads(self.last_received)

        if "errorMessages" in self.response:
            self.error = self.response["errorMessages"]

        if "success" in self.response:
            self.last_status = self.response["success"]

        return self.last_status

    # Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido.
    # @return    dict    Resposta de dados.
    def obter_resposta(self):
        """Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido."""''
        if self.response['dados']['success'] is False:
            raise Exception(self.response['dados']['errorMessages'])

        if self.last_status and len(self.response['dados']['params']['properties']) > 0:
            self.response['dados']['params']['properties']['lastCommunication'] = self.response['dados']['params'][
                'lastCommunication']
            return self.response['dados']['params']['properties']
        return None

    # Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido.
    # @return    dict    Resposta de dados.
    def obter_canal(self):
        """Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido."""
        if self.last_status and len(self.response['canal']['params']['values']) > 0:
            return self.response['canal']['params']['values']
        return None

    # Retorna uma lista de opções. Util para inicialização e objetos existentes de uma sub-classe.
    # @return    dict    Lista de opções.
    def obter_opcoes(self):
        """Retorna uma lista de opções. Util para inicialização e objetos existentes de uma sub-classe."""
        return {
            "endpoint": self.endpoint,
            "session_id": self.session_id,
            "app_id": self.app_id,
            "app_token": self.app_token,
            "thing_key": self.thing_key,
            "username": self.username,
            "password": self.password
        }

    # Retorna uma lista de informações para debug após execução do último comando.
    # @return    dict    Dados para debug.
    def debugar(self):
        """Retorna uma lista de informações para debug após execução do último comando."""
        return {
            "endpoint": self.endpoint,
            "last_sent": self.last_sent,
            "last_received": self.last_received,
            "error": self.error
        }

    # Formata objeto datetime para formato requerido pela API.
    # @param     datetime    data   Objeto datetime que será reformatado.
    # @return    string      A data formatada no estilo requerido pela API.
    def formatar_datatime(self, data):
        """Converte uma string de dados para formato da API."""
        if type(data) is str:
            return data
        else:
            data_string = data.strftime("%Y-%m-%dT%H:%M:%S%z")
            data_formatada = data_string[:-2] + ':' + data_string[-2:]  # 2004-02-12T15:19:21+00:00
            return data_formatada

    # Executa o metodo 'thing.find'.
    # @param     thing_key   Codigo de identificacao do cliente.
    # @return    string      Json contento coletas encontradas.
    def coletar(self, thing_key):
        json = {'auth': {'sessionId': self.session_id},
                'dados': {'command': 'thing.find', 'params': {'key': thing_key}}}
        if self.postar(json):
            return self.obter_resposta()
        return None

    # Executa o metodo 'property.history' que traz as leituras de um canal especifico.
    # @param    thing_key   Codigo de identificacao do cliente
    # @param    canal       Canal desejado do transdutor
    # @param    data_inicio Data inicial
    # @param    data_fim    Data final
    def coletar_por_canal(self, thing_key, canal, data_inicio, data_fim):
        params = {'thingKey': thing_key, 'key': canal, 'start': data_inicio, 'end': data_fim}
        string_json = {'auth': {'sessionId': self.session_id},
                       'canal': {'command': 'property.history', 'params': params}}
        if self.postar(string_json):
            return self.obter_canal()
        return None
