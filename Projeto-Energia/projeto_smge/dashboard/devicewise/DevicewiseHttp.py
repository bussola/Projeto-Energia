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


   