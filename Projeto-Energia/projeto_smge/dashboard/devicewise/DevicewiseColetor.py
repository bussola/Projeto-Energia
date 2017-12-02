# -*- coding: utf-8 -*-
from dashboard.devicewise.DevicewiseHttp import DevicewiseHttp
from dashboard.models import Transdutor, Coleta, User
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum

class DevicewiseColetor(object):
    api = None

    def __init__(self):
        self.api = DevicewiseHttp()

    def coletar_por_usuario(self, usuario):
        transdutores = Transdutor.objects.filter(id_cliente=usuario.id)
        if transdutores is None or len(transdutores) < 1:
            print('Devicewise: Nenhum transdutor encontrado para o usuário %s' % usuario.email)
            return False

        for t in transdutores:
            print('Transdutor: %s' % t.chave_api)
            dados = self.api.coletar(t.chave_api)
            if dados and len(dados) > 0:
                data_ultima_leitura = dados['lastCommunication']
                if Coleta.objects.filter(id_transdutor=t.id, data_leitura=data_ultima_leitura):
                    print('Última leitura já está armazenada no banco de dados.')
                else:
                    coleta = Coleta()
                    coleta.data_leitura = dados['lastCommunication']
                    coleta.io6 = dados['io_6']['value']

                    last_5_min = datetime.now() - timedelta(seconds=5*60)
                    soma_5_min = (Coleta.objects
                    .filter(data_leitura__gt=last_5_min)
                    .extra(select={'day': 'date(data_leitura)'})
                    .values('day')
                    .annotate(sum=Sum('io6')))
                    for f in soma_5_min:
                        filtro = f['sum'] #pega o dicionario sum
                    coleta.media_io6 = filtro

                    coleta.io7 = dados['io_7']['value']
                    coleta.io8 = dados['io_8']['value']
                    coleta.io9 = dados['io_9']['value']
                    coleta.io10 = dados['io_10']['value']
                    coleta.io11 = dados['io_11']['value']
                    coleta.io12 = dados['io_12']['value']
                    coleta.id_transdutor = t
                    coleta.save()
                    print('Leitura armazenada no banco de dados.')
            else:
                print('Devicewise: Nenhum dado retornado da API.')
        return True
