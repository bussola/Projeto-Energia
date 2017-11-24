# -*- coding: utf-8 -*-
import sys
from httplib2 import Http
import simplejson as json
from django.views.decorators.csrf import csrf_exempt


class DevicewiseHttp(object):
    # Endpoint da API (url)
    endpoint = 'http://api.devicewise.com/api'

    # Identificador da aplicacao
    app_id = ""

    # Token da aplicacao
    app_token = ""

    # Identifica o metodo 'thing' que sera executado
    thing_key = ""

<<<<<<< HEAD
    # Nome do usuario para conectar no servidor.
=======
    # Nome do usuario para conectar no servidor
>>>>>>> d4d87af116a88152c484395f13bbc860a07da8ac
    username = 'brunodrago@e-saveconsultoria.com.br'

    # Senha para conectar no servidor.
    password = 'Aa@203851'
<<<<<<< HEAD
=======

    # Contem o identificador da sessao atual
    session_id = ""
>>>>>>> d4d87af116a88152c484395f13bbc860a07da8ac

    # String JSON do ultimo recebimento do endpoint. ***Usado para debug.
    last_received = ""

    # Ultima string JSON enviada para o endpoint. ***Usado para debug.
    last_sent = ""

    # Informa se o ultimo 'request' foi bem sucedido ou falhou
    last_status = None

    # Contem os dados da resposta do chamado a API.
    response = []

    # Mantem qualquer erro retornado pela api.
    error = []

    _instancia = None

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(DevicewiseHttp, cls).__new__(cls)
            return cls._instancia
        else:
            return cls._instancia

    def __init__(self):
        if (len(self.session_id) == 0):
            print('Status da conexão: Não autenticado')
            self.autenticar()
        else:
            print('Status da conexão: Autenticado')

    def autenticar(self):
        string_json = {
            "auth": {"command": "api.authenticate", "params": {"username": self.username, "password": self.password}}}
        string_json = json.dumps(string_json)
        self.last_sent = string_json
        try:
            print('Autenticador: Fazendo login na API...')
            http_obj = Http(disable_ssl_certificate_validation=True)
            result, self.last_received = http_obj.request(self.endpoint, 'POST', string_json)

            if not result['status'] == '200':
                raise Exception('Autenticador: Falha no POST para %s' % self.endpoint)

            self.response = json.loads(self.last_received)
            self.session_id = self.response["auth"]["params"]["sessionId"]
            return len(self.session_id) > 0
        except:
            print('Autenticador: Ocorreu uma exceção ao tentar autenticar usuário.')
            print(sys.exc_info())

        return False


    def set_json_auth(self, json_string):
        if not type(json_string) is dict:
            json_string = json.loads(json_string)

        if not "auth" in json_string:
            if len(self.session_id) == 0:
                self.autenticar()
            # if it is still empty, we cannot proceed
            if len(self.session_id) == 0:
                raise Exception(
                    "Autenticação não autorizada pela API. Por favor, verifique as configurações do aplicativo.")
            json_string["auth"] = {"sessionId": self.session_id}

        json_string = json.dumps(json_string)
        return json_string


    def is_online(self):
        if self.session_id is None or len(self.session_id) <= 0:
            return False
        string_json = {"auth": {"sessionId": self.session_id}, "dados": {"command": "diag.ping"}}
        http = Http(disable_ssl_certificate_validation=True)
        resposta = http.request(self.endpoint, 'POST', string_json)
        return resposta and resposta['dados']['success']


    def postar(self, string_json):
        self.error = ''
        self.last_status = False  # TODO: setei para false, porque ele deve setar como True apenas se obtiver exito
        self.last_received = ''
        self.response = ''

        string_json = json.dumps(string_json)
        self.last_sent = string_json

        try:
            print('-------------- AUTENTICAR')
            print('\nString Json do POST: ')
            print(string_json)
            http_obj = Http(disable_ssl_certificate_validation=True)
            result, self.last_received = http_obj.request(self.endpoint, 'POST', string_json)

            if not result['status'] == '200':
                raise Exception('Falha no POST para %s' % self.endpoint)

            print('\nResultado do Post: ')
            print(self.last_received)
            self.response = json.loads(self.last_received)
        except:
            print('\nOcorreu um erro (Exception):')
            print(sys.exc_info())

        if 'errorMessages' in self.response:
            self.error = self.response['errorMessages']

        if 'success' in self.response:
            print('sucesso')
            self.last_status = self.response['success']
        else:
            print('nao sucesso')

        print('\nRESPOSTA: ')
        print(self.response)
        return self.last_status


    def coletar(self, thing_key):
        string_json = {'auth': {'sessionId': self.session_id},
                       'dados': {'command': 'thing.find', 'params': {'key': thing_key}}}

        string_json = json.dumps(string_json)

        try:
            #print('\nString Json do POST: ')
            #print(string_json)
            http_obj = Http(disable_ssl_certificate_validation=True)
            result, self.last_received = http_obj.request(self.endpoint, 'POST', string_json)

            if not result['status'] == '200':
                raise Exception('Falha no POST para %s' % self.endpoint)

            self.response = json.loads(self.last_received)
            #print('\nResultado do Post: ')
            #print(self.response)

            if "success" in self.response['dados']:
                self.last_status = self.response['dados']['success']

            if self.last_status and len(self.response['dados']['params']['properties']) > 0:
                self.response['dados']['params']['properties']['lastCommunication'] = self.response['dados']['params'][
                    'lastCommunication']
                print('Transdutor %s SINCRONIZADO' % thing_key)
                return self.response['dados']['params']['properties']
        except:
            print('\nOcorreu um erro (Exception):')
            print(sys.exc_info())

        return None


    def obter_resposta(self):
        """Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido."""''
        if self.response['dados']['success'] is False:
            raise Exception(self.response['dados']['errorMessages'])

        if self.last_status and len(self.response['dados']['params']['properties']) > 0:
            self.response['dados']['params']['properties']['lastCommunication'] = self.response['dados']['params'][
                'lastCommunication']
            return self.response['dados']['params']['properties']

        return None


    def obter_canal(self):
        """Retorna a resposta de dados para o ultimo comando se o ultimo foi bem sucedido."""
        if self.last_status and len(self.response['canal']['params']['values']) > 0:
            return self.response['canal']['params']['values']
        return None


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


    def debugar(self):
        """Retorna uma lista de informações para debug após execução do último comando."""
        return {
            "endpoint": self.endpoint,
            "last_sent": self.last_sent,
            "last_received": self.last_received,
            "error": self.error
        }


    def formatar_datatime(self, data):
        """Converte uma string de dados para formato da API."""
        if type(data) is str:
            return data
        else:
            data_string = data.strftime("%Y-%m-%dT%H:%M:%S%z")
            data_formatada = data_string[:-2] + ':' + data_string[-2:]  # 2004-02-12T15:19:21+00:00
            return data_formatada


    def coletar_por_canal(self, thing_key, canal, data_inicio, data_fim):
        params = {'thingKey': thing_key, 'key': canal, 'start': data_inicio, 'end': data_fim}
        string_json = {'auth': {'sessionId': self.session_id},
                       'canal': {'command': 'property.history', 'params': params}}
        if self.postar(string_json):
            return self.obter_canal()
        return None
